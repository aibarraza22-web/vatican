from __future__ import annotations

import argparse
from pathlib import Path

from .db import (
    add_claim,
    add_source_and_document,
    audit_database,
    connect,
    init_db,
)
from .scoring import rank_corpora
from .survey import profile_ranked_candidates, run_signal_survey


def command_init_db(args: argparse.Namespace) -> None:
    init_db(args.database)
    print(f"Initialized {args.database}")


def command_rank_corpora(args: argparse.Namespace) -> None:
    for index, corpus in enumerate(rank_corpora(args.csv), start=1):
        print(f"{index:>2}. {corpus.corpus_id:<18} {corpus.score:>5.2f}  {corpus.name}")


def command_demo(args: argparse.Namespace) -> None:
    init_db(args.database)
    with connect(args.database) as connection:
        document_id = add_source_and_document(
            connection,
            institution="Biblioteca Apostolica Vaticana",
            collection="Borgiani messicani",
            shelfmark="Borg.mess.1",
            source_url="https://digi.vatlib.it/view/MSS_Borg.mess.1",
            title="Calendarial, astronomical, divinatory, and ritual texts",
            languages=[],
        )
        claim_id = add_claim(
            connection,
            document_id=document_id,
            statement=(
                "The manuscript is useful as a control case for evaluating "
                "Project Lumen's handling of visual and non-alphabetic evidence."
            ),
            level="L2",
            confidence="substantial",
            created_by="Project Lumen demo",
            evidence=[
                {
                    "type": "catalog",
                    "locator": "Borg.mess.1 catalog description",
                    "description": (
                        "The official record describes late-fifteenth-century "
                        "calendarial, astronomical, divinatory, and ritual texts."
                    ),
                    "supports": True,
                }
            ],
            alternatives=[
                "Use a Latin alphabetic manuscript as the initial control.",
                "Treat Borg.mess.1 only as contextual material, not a pipeline control.",
            ],
            falsification_test=(
                "A pilot may show that its visual writing system is too unlike "
                "the target corpora to provide a useful control."
            ),
        )
        print(f"Created demo document {document_id} and claim {claim_id}")


def command_audit(args: argparse.Namespace) -> None:
    with connect(args.database) as connection:
        problems = audit_database(connection)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        raise SystemExit(1)
    print("Audit passed.")


def command_survey_search(args: argparse.Namespace) -> None:
    hits = run_signal_survey(
        output_directory=args.output,
        rows=args.rows,
        max_pages_per_term=args.pages,
        delay_seconds=args.delay,
    )
    print(
        f"Collected {len(hits)} signal hits across "
        f"{len({hit.shelfmark for hit in hits})} manuscripts."
    )


def command_profile_candidates(args: argparse.Namespace) -> None:
    profiles = profile_ranked_candidates(
        ranked_csv=args.ranked_csv,
        output_csv=args.output_csv,
        cache_directory=args.cache,
        limit=args.limit,
        delay_seconds=args.delay,
    )
    print(f"Profiled {len(profiles)} candidates.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lumen")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-db")
    init_parser.add_argument("database", type=Path)
    init_parser.set_defaults(func=command_init_db)

    rank_parser = subparsers.add_parser("rank-corpora")
    rank_parser.add_argument("csv", type=Path)
    rank_parser.set_defaults(func=command_rank_corpora)

    demo_parser = subparsers.add_parser("demo")
    demo_parser.add_argument("database", type=Path)
    demo_parser.set_defaults(func=command_demo)

    audit_parser = subparsers.add_parser("audit")
    audit_parser.add_argument("database", type=Path)
    audit_parser.set_defaults(func=command_audit)

    survey_parser = subparsers.add_parser("survey-search")
    survey_parser.add_argument("output", type=Path)
    survey_parser.add_argument("--rows", type=int, default=100)
    survey_parser.add_argument("--pages", type=int, default=1)
    survey_parser.add_argument("--delay", type=float, default=1.5)
    survey_parser.set_defaults(func=command_survey_search)

    profile_parser = subparsers.add_parser("profile-candidates")
    profile_parser.add_argument("ranked_csv", type=Path)
    profile_parser.add_argument("output_csv", type=Path)
    profile_parser.add_argument("--cache", type=Path, required=True)
    profile_parser.add_argument("--limit", type=int, default=25)
    profile_parser.add_argument("--delay", type=float, default=1.5)
    profile_parser.set_defaults(func=command_profile_candidates)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
