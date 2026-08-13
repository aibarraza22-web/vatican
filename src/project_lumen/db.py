from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY,
    institution TEXT NOT NULL,
    collection_name TEXT,
    shelfmark TEXT NOT NULL,
    source_url TEXT NOT NULL,
    iiif_manifest TEXT,
    rights_status TEXT NOT NULL DEFAULT 'unknown',
    rights_checked_on TEXT,
    UNIQUE(institution, shelfmark)
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES sources(id),
    title TEXT,
    date_not_before INTEGER,
    date_not_after INTEGER,
    languages_json TEXT NOT NULL DEFAULT '[]',
    scripts_json TEXT NOT NULL DEFAULT '[]',
    catalog_description TEXT,
    status TEXT NOT NULL DEFAULT 'intake',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id),
    folio TEXT NOT NULL,
    region_json TEXT,
    page_url TEXT,
    UNIQUE(document_id, folio, region_json)
);

CREATE TABLE IF NOT EXISTS texts (
    id INTEGER PRIMARY KEY,
    page_id INTEGER NOT NULL REFERENCES pages(id),
    kind TEXT NOT NULL CHECK(kind IN (
        'diplomatic', 'expanded', 'normalized',
        'translation_literal', 'translation_readable'
    )),
    language TEXT,
    text_content TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN (
        'model', 'candidate', 'human_corrected', 'expert_reviewed'
    )),
    created_by TEXT NOT NULL,
    parent_text_id INTEGER REFERENCES texts(id),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS claims (
    id INTEGER PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id),
    statement TEXT NOT NULL,
    level TEXT NOT NULL CHECK(level IN ('L0','L1','L2','L3','L4','L5')),
    confidence TEXT NOT NULL CHECK(confidence IN (
        'unknown', 'weak', 'plausible', 'substantial', 'strong'
    )),
    status TEXT NOT NULL CHECK(status IN (
        'open', 'corroborated', 'rejected', 'published', 'retracted'
    )),
    falsification_test TEXT,
    novelty_search TEXT,
    created_by TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY,
    claim_id INTEGER NOT NULL REFERENCES claims(id),
    evidence_type TEXT NOT NULL,
    locator TEXT NOT NULL,
    description TEXT NOT NULL,
    supports INTEGER NOT NULL CHECK(supports IN (0,1))
);

CREATE TABLE IF NOT EXISTS alternatives (
    id INTEGER PRIMARY KEY,
    claim_id INTEGER NOT NULL REFERENCES claims(id),
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY,
    claim_id INTEGER NOT NULL REFERENCES claims(id),
    reviewer TEXT NOT NULL,
    expertise TEXT NOT NULL,
    decision TEXT NOT NULL CHECK(decision IN (
        'approve', 'revise', 'reject'
    )),
    notes TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    object_type TEXT NOT NULL,
    object_id INTEGER,
    details_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def connect(path: str | Path) -> sqlite3.Connection:
    connection = sqlite3.connect(Path(path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db(path: str | Path) -> None:
    with connect(path) as connection:
        connection.executescript(SCHEMA)
        connection.execute(
            """
            INSERT INTO audit_events(actor, action, object_type, details_json)
            VALUES (?, ?, ?, ?)
            """,
            ("system", "database_initialized", "database", "{}"),
        )


def add_source_and_document(
    connection: sqlite3.Connection,
    *,
    institution: str,
    collection: str,
    shelfmark: str,
    source_url: str,
    title: str | None = None,
    languages: list[str] | None = None,
) -> int:
    cursor = connection.execute(
        """
        INSERT INTO sources(
            institution, collection_name, shelfmark, source_url
        ) VALUES (?, ?, ?, ?)
        """,
        (institution, collection, shelfmark, source_url),
    )
    source_id = int(cursor.lastrowid)
    cursor = connection.execute(
        """
        INSERT INTO documents(
            source_id, title, languages_json
        ) VALUES (?, ?, ?)
        """,
        (source_id, title, json.dumps(languages or [])),
    )
    document_id = int(cursor.lastrowid)
    connection.execute(
        """
        INSERT INTO audit_events(
            actor, action, object_type, object_id, details_json
        ) VALUES (?, ?, ?, ?, ?)
        """,
        (
            "system",
            "document_created",
            "document",
            document_id,
            json.dumps({"shelfmark": shelfmark}),
        ),
    )
    return document_id


def add_claim(
    connection: sqlite3.Connection,
    *,
    document_id: int,
    statement: str,
    level: str,
    confidence: str,
    created_by: str,
    evidence: list[dict[str, Any]],
    alternatives: list[str],
    falsification_test: str | None = None,
) -> int:
    if not evidence:
        raise ValueError("A claim must include at least one evidence item.")
    if level in {"L2", "L3", "L4", "L5"} and not alternatives:
        raise ValueError(f"{level} claims must include at least one alternative.")

    cursor = connection.execute(
        """
        INSERT INTO claims(
            document_id, statement, level, confidence, status,
            falsification_test, created_by
        ) VALUES (?, ?, ?, ?, 'open', ?, ?)
        """,
        (
            document_id,
            statement,
            level,
            confidence,
            falsification_test,
            created_by,
        ),
    )
    claim_id = int(cursor.lastrowid)

    for item in evidence:
        connection.execute(
            """
            INSERT INTO evidence(
                claim_id, evidence_type, locator, description, supports
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                claim_id,
                item["type"],
                item["locator"],
                item["description"],
                int(bool(item.get("supports", True))),
            ),
        )
    for alternative in alternatives:
        connection.execute(
            "INSERT INTO alternatives(claim_id, description) VALUES (?, ?)",
            (claim_id, alternative),
        )
    connection.execute(
        """
        INSERT INTO audit_events(
            actor, action, object_type, object_id, details_json
        ) VALUES (?, ?, ?, ?, ?)
        """,
        (
            created_by,
            "claim_created",
            "claim",
            claim_id,
            json.dumps({"level": level, "confidence": confidence}),
        ),
    )
    return claim_id


def audit_database(connection: sqlite3.Connection) -> list[str]:
    problems: list[str] = []

    rows = connection.execute(
        """
        SELECT c.id, c.level
        FROM claims c
        LEFT JOIN evidence e ON e.claim_id = c.id
        GROUP BY c.id
        HAVING COUNT(e.id) = 0
        """
    ).fetchall()
    for row in rows:
        problems.append(f"Claim {row['id']} ({row['level']}) has no evidence.")

    rows = connection.execute(
        """
        SELECT c.id, c.level
        FROM claims c
        LEFT JOIN alternatives a ON a.claim_id = c.id
        WHERE c.level IN ('L2','L3','L4','L5')
        GROUP BY c.id
        HAVING COUNT(a.id) = 0
        """
    ).fetchall()
    for row in rows:
        problems.append(
            f"Claim {row['id']} ({row['level']}) has no alternative hypothesis."
        )

    rows = connection.execute(
        """
        SELECT c.id, c.level
        FROM claims c
        LEFT JOIN reviews r ON r.claim_id = c.id AND r.decision = 'approve'
        WHERE c.level IN ('L4','L5')
        GROUP BY c.id
        HAVING COUNT(r.id) = 0
        """
    ).fetchall()
    for row in rows:
        problems.append(
            f"Claim {row['id']} ({row['level']}) lacks approving expert review."
        )

    rows = connection.execute(
        """
        SELECT c.id
        FROM claims c
        JOIN documents d ON d.id = c.document_id
        JOIN sources s ON s.id = d.source_id
        WHERE c.level = 'L5'
          AND (s.rights_status = 'unknown' OR s.rights_checked_on IS NULL)
        """
    ).fetchall()
    for row in rows:
        problems.append(
            f"Claim {row['id']} is L5 but source rights are not resolved."
        )

    return problems

