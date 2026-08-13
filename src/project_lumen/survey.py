from __future__ import annotations

import csv
import html
import json
import re
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from http.cookiejar import CookieJar
from pathlib import Path


BASE_URL = "https://digi.vatlib.it"
SEARCH_PATH = "/mss/search"
USER_AGENT = (
    "ProjectLumen/0.1 metadata-only scholarly audit "
    "(compatible with Mozilla/5.0)"
)


DEFAULT_SIGNALS = {
    "palinsesto": 10.0,
    "palimpsestus": 10.0,
    "rescriptus": 9.0,
    "sottoscrittura": 8.0,
    "frammento": 7.0,
    "fragmentum": 7.0,
    "inedito": 7.0,
    "inedita": 7.0,
    "anonimo": 6.0,
    "anonymus": 6.0,
    "attribuzione": 6.0,
    "autografo": 6.0,
    "minuta": 6.0,
    "bozza": 6.0,
    "cancellato": 6.0,
    "rasura": 7.0,
    "postille": 5.0,
    "marginalia": 5.0,
    "ignoto": 5.0,
    "non identificato": 8.0,
}


@dataclass(frozen=True)
class SearchHit:
    shelfmark: str
    term: str
    signal_weight: float
    section: str
    snippet: str
    detail_url: str
    viewer_url: str
    score: float


def _strip_markup(value: str) -> str:
    value = re.sub(r"<script\b.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def parse_search_results(
    page: str, *, term: str, signal_weight: float
) -> list[SearchHit]:
    pattern = re.compile(
        r'<div class="row-search-result-record\b.*?'
        r'(?=<div class="row-search-result-record\b|'
        r'<hr class="search-result-control-separator")',
        flags=re.S,
    )
    results: list[SearchHit] = []
    for block in pattern.findall(page):
        match = re.search(
            r'<a\s+href="/mss/detail/([^"/]+)"\s+'
            r'class="link-search-result-record-view">([^<]+)</a>',
            block,
        )
        if not match:
            continue
        path_shelfmark = html.unescape(match.group(1))
        shelfmark = _strip_markup(match.group(2))
        section_match = re.search(
            r'<span class="search-result-detail-label">(.*?)</span>',
            block,
            flags=re.S,
        )
        section = (
            _strip_markup(section_match.group(1)) if section_match else "General Data"
        )
        snippet = _strip_markup(block)
        snippet = re.sub(
            rf"^Manuscript:\s*{re.escape(shelfmark)}\s*", "", snippet, flags=re.I
        )
        if len(snippet) > 1000:
            snippet = snippet[:997] + "..."

        section_factor = 0.55 if "Bibliographic" in section else 1.0
        sparse_bonus = 1.5 if len(snippet) < 180 else 0.0
        score = round(signal_weight * section_factor + sparse_bonus, 2)
        results.append(
            SearchHit(
                shelfmark=shelfmark,
                term=term,
                signal_weight=signal_weight,
                section=section,
                snippet=snippet,
                detail_url=f"{BASE_URL}/mss/detail/{path_shelfmark}",
                viewer_url=f"{BASE_URL}/view/MSS_{path_shelfmark}",
                score=score,
            )
        )
    return results


class VaticanCatalogClient:
    def __init__(self, *, delay_seconds: float = 1.5, timeout_seconds: int = 45):
        self.delay_seconds = delay_seconds
        self.timeout_seconds = timeout_seconds
        self._last_request = 0.0
        cookie_jar = CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cookie_jar)
        )
        self._prime()

    def _request(self, url: str, *, referer: str) -> str:
        wait = self.delay_seconds - (time.monotonic() - self._last_request)
        if wait > 0:
            time.sleep(wait)
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Referer": referer,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Encoding": "identity",
            },
        )
        try:
            with self.opener.open(request, timeout=self.timeout_seconds) as response:
                return response.read().decode("utf-8", "replace")
        finally:
            self._last_request = time.monotonic()

    def _prime(self) -> None:
        self._request(f"{BASE_URL}/mss/", referer=f"{BASE_URL}/")

    def search(self, term: str, *, rows: int = 100, page: int = 1) -> str:
        params = urllib.parse.urlencode(
            {"k_f": 0, "k_v": term, "r": rows, "p": page}
        )
        return self._request(
            f"{BASE_URL}{SEARCH_PATH}?{params}",
            referer=f"{BASE_URL}/mss/",
        )

    def detail(self, shelfmark: str) -> str:
        safe_shelfmark = urllib.parse.quote(shelfmark, safe=".")
        return self._request(
            f"{BASE_URL}/mss/detail/{safe_shelfmark}",
            referer=f"{BASE_URL}/mss/",
        )


def run_signal_survey(
    *,
    output_directory: str | Path,
    signals: dict[str, float] | None = None,
    rows: int = 100,
    max_pages_per_term: int = 1,
    delay_seconds: float = 1.5,
) -> list[SearchHit]:
    output = Path(output_directory)
    cache = output / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    client = VaticanCatalogClient(delay_seconds=delay_seconds)
    hits: list[SearchHit] = []

    for term, weight in (signals or DEFAULT_SIGNALS).items():
        for page_number in range(1, max_pages_per_term + 1):
            cache_path = cache / f"{urllib.parse.quote(term, safe='')}-{page_number}.html"
            if cache_path.exists():
                page = cache_path.read_text(encoding="utf-8")
            else:
                page = client.search(term, rows=rows, page=page_number)
                cache_path.write_text(page, encoding="utf-8")
            page_hits = parse_search_results(
                page, term=term, signal_weight=float(weight)
            )
            hits.extend(page_hits)
            if len(page_hits) < rows:
                break

    write_survey_outputs(hits, output)
    return hits


def aggregate_hits(hits: list[SearchHit]) -> list[dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for hit in hits:
        record = records.setdefault(
            hit.shelfmark,
            {
                "shelfmark": hit.shelfmark,
                "aggregate_score": 0.0,
                "signal_count": 0,
                "signals": set(),
                "non_bibliographic_hits": 0,
                "detail_url": hit.detail_url,
                "viewer_url": hit.viewer_url,
                "best_snippet": "",
                "best_score": -1.0,
            },
        )
        record["aggregate_score"] = float(record["aggregate_score"]) + hit.score
        record["signal_count"] = int(record["signal_count"]) + 1
        cast_signals = record["signals"]
        assert isinstance(cast_signals, set)
        cast_signals.add(hit.term)
        if "Bibliographic" not in hit.section:
            record["non_bibliographic_hits"] = (
                int(record["non_bibliographic_hits"]) + 1
            )
        if hit.score > float(record["best_score"]):
            record["best_score"] = hit.score
            record["best_snippet"] = hit.snippet

    final: list[dict[str, object]] = []
    for record in records.values():
        signals_set = record.pop("signals")
        assert isinstance(signals_set, set)
        record["signals"] = "; ".join(sorted(signals_set))
        record.pop("best_score")
        record["aggregate_score"] = round(float(record["aggregate_score"]), 2)
        final.append(record)
    return sorted(
        final,
        key=lambda item: (
            int(item["non_bibliographic_hits"]),
            float(item["aggregate_score"]),
            int(item["signal_count"]),
        ),
        reverse=True,
    )


def write_survey_outputs(hits: list[SearchHit], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    raw_path = output / "signal_hits.csv"
    with raw_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(hits[0]).keys()) if hits else [
            "shelfmark", "term", "signal_weight", "section", "snippet",
            "detail_url", "viewer_url", "score"
        ])
        writer.writeheader()
        writer.writerows(asdict(hit) for hit in hits)

    ranked = aggregate_hits(hits)
    ranked_path = output / "ranked_candidates.csv"
    fieldnames = [
        "shelfmark",
        "aggregate_score",
        "signal_count",
        "signals",
        "non_bibliographic_hits",
        "detail_url",
        "viewer_url",
        "best_snippet",
    ]
    with ranked_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ranked)

    summary = {
        "queries": len({hit.term for hit in hits}),
        "raw_hits": len(hits),
        "unique_manuscripts": len(ranked),
        "generated_at_epoch": int(time.time()),
        "method": "DigiVatLib metadata-only keyword signal survey",
    }
    (output / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )


def parse_detail_profile(shelfmark: str, page: str) -> dict[str, object]:
    body_start = page.find('<div id="region-detail-body"')
    body_end = page.find("</section>", body_start)
    if body_start < 0:
        raise ValueError(f"Could not locate detail body for {shelfmark}.")
    if body_end < 0:
        body_end = len(page)
    body = page[body_start:body_end]

    bibliography_marker = body.find("Bibliographic References:")
    if bibliography_marker < 0:
        content_html = body
        bibliography_html = ""
    else:
        content_html = body[:bibliography_marker]
        bibliography_html = body[bibliography_marker:]

    content_entries = len(
        re.findall(r'class="block-detail-record(?:\s|")', content_html)
    )
    bibliography_entries = len(
        re.findall(r'class="block-detail-record(?:\s|")', bibliography_html)
    )
    content_text = _strip_markup(content_html)
    bibliography_text = _strip_markup(bibliography_html)

    description_gap_score = 5
    if content_entries >= 15:
        description_gap_score = 1
    elif content_entries >= 8:
        description_gap_score = 2
    elif content_entries >= 4:
        description_gap_score = 3
    elif content_entries >= 2:
        description_gap_score = 4

    saturation_penalty = min(5, bibliography_entries // 5)
    low_quality = "low-quality" in page.lower()

    return {
        "shelfmark": shelfmark,
        "content_entries": content_entries,
        "bibliography_entries": bibliography_entries,
        "description_gap_score": description_gap_score,
        "saturation_penalty": saturation_penalty,
        "low_quality": int(low_quality),
        "catalog_description": content_text[:4000],
        "bibliography_preview": bibliography_text[:1500],
    }


def profile_ranked_candidates(
    *,
    ranked_csv: str | Path,
    output_csv: str | Path,
    cache_directory: str | Path,
    limit: int = 25,
    delay_seconds: float = 1.5,
) -> list[dict[str, object]]:
    with Path(ranked_csv).open(newline="", encoding="utf-8") as handle:
        ranked = list(csv.DictReader(handle))[:limit]

    cache = Path(cache_directory)
    cache.mkdir(parents=True, exist_ok=True)
    client = VaticanCatalogClient(delay_seconds=delay_seconds)
    profiles: list[dict[str, object]] = []
    for candidate in ranked:
        shelfmark = candidate["shelfmark"]
        cache_path = cache / f"{urllib.parse.quote(shelfmark, safe='.')}.html"
        if cache_path.exists():
            page = cache_path.read_text(encoding="utf-8")
        else:
            page = client.detail(shelfmark)
            cache_path.write_text(page, encoding="utf-8")
        profile = parse_detail_profile(shelfmark, page)
        base_score = float(candidate["aggregate_score"])
        adjusted_score = (
            base_score
            + float(profile["description_gap_score"]) * 1.5
            - float(profile["saturation_penalty"]) * 2.0
            - float(profile["low_quality"]) * 2.0
        )
        profiles.append(
            {
                **candidate,
                **profile,
                "adjusted_signal_score": round(adjusted_score, 2),
                "review_status": "unreviewed",
                "impact_ceiling": "",
                "research_question": "",
                "reject_reason": "",
            }
        )

    profiles.sort(
        key=lambda item: float(item["adjusted_signal_score"]), reverse=True
    )
    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if profiles:
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(profiles[0].keys()))
            writer.writeheader()
            writer.writerows(profiles)
    return profiles
