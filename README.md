# Project Lumen

**AI-assisted manuscript research with evidence, provenance, and expert review.**

Project Lumen exists to turn digitized manuscripts into defensible historical
knowledge. It combines handwriting recognition, translation, entity extraction,
authorship analysis, bibliographic research, and human review. It does not treat
model output as a discovery.

The first image-level dossier is
[`docs/INVESTIGATION_001_CECCO.md`](docs/INVESTIGATION_001_CECCO.md), an open
investigation into a 1745 report of a manuscript presented as an unpublished
work by Cecco d'Ascoli. It is an L2 hypothesis, not a discovery claim.

## Founding thesis

Digitization creates images. Scholarship creates knowledge.

The Vatican Library has placed tens of thousands of manuscripts online, while
many collections remain incompletely cataloged or unevenly studied. Project
Lumen will systematically identify promising material, produce auditable
transcriptions and translations, test historical hypotheses, and publish only
claims that survive adversarial review.

The primary program is the subject-neutral **Grand Discovery Program**. The
Donlan source census is one bounded test case, not the project's central topic.

## Initial research frontier

The first discovery campaign is subject-neutral. It searches for the highest
plausible historical impact across all accessible collections, especially:

- unidentified or disputed authorship involving historically important people;
- unknown versions of influential religious, political, scientific, legal, or
  literary texts;
- evidence that changes the date, origin, transmission, or meaning of a major
  event or idea;
- erased, overwritten, damaged, or reused text;
- correspondence, drafts, corrections, and marginalia that reveal decisions;
- references to lost works, unknown intermediaries, or hidden networks;
- manuscripts whose digital records have sparse descriptions or thin
  bibliographies.
- potentially important texts never edited in the original language or never
  translated into a modern language, provided that status is actually verified;
- underrepresented languages and traditions whose low search visibility may
  conceal important scientific, political, religious, literary, legal,
  diplomatic, medical, geographic, or social evidence.

No topic, region, institution, or historical period receives priority merely
because it is personally interesting. Famous manuscripts may be used as
controls, but the main effort targets under-described material with a high
impact ceiling.

## Non-negotiable rules

1. Manuscript images remain tied to their authoritative shelfmark and source.
2. Diplomatic transcription is separated from normalized text and translation.
3. Unclear readings remain marked as unclear.
4. Every historical claim cites exact manuscript evidence and prior scholarship.
5. Authorship is expressed as a hypothesis with alternatives, never as model
   intuition.
6. Novelty is not claimed until targeted literature searches and expert review
   are complete.
7. Rights restrictions are recorded before any image is downloaded or
   republished.
8. Rejected hypotheses stay in the audit trail.

## Claim ladder

| Level | Label | Meaning |
|---|---|---|
| L0 | Model suggestion | Unchecked machine output |
| L1 | Transcription candidate | Anchored to a folio and region |
| L2 | Research hypothesis | Evidence and alternatives recorded |
| L3 | Corroborated finding | Independent evidence supports it |
| L4 | Expert-reviewed finding | Domain reviewer has signed off |
| L5 | Publishable contribution | Novelty and rights review completed |

## Repository contents

- `AGENTS.md`: durable evidence rules and required Codex reporting format.
- `docs/CODEX_START_HERE.md`: setup, first prompt, and human/AI responsibilities.
- `docs/PROJECT_CHARTER.md`: mission, organization, and 90-day launch.
- `docs/RESEARCH_PROTOCOL.md`: end-to-end scholarly workflow.
- `docs/HIGH_IMPACT_SEARCH.md`: grand-prize discovery classes and triage.
- `docs/GRAND_DISCOVERY_PROGRAM.md`: the primary unknown-document discovery
  workflow, verification gates, and first Codex operation.
- `docs/FIRST_SURVEY_REPORT.md`: live reconnaissance results and first leads.
- `docs/INVESTIGATION_001_CECCO.md`: first image-level investigation dossier.
- `docs/DONLAN_EVIDENCE_GAP_MAP.md`: a bounded research track testing whether
  underused Savoy nunciature records could extend Thomas A. Donlan's work.
- `docs/PUBLICATION_STANDARD.md`: rules for public claims and papers.
- `data/corpus_registry.csv`: initial collection-level reconnaissance.
- `data/investigations/`: structured evidence and claim records.
- `data/discovery_queue_template.csv`: fields for ranking exact document leads.
- `schemas/research_record.schema.json`: machine-readable research record.
- `src/project_lumen/`: dependency-free SQLite research ledger and CLI.
- `tests/`: integrity tests for the ledger and scoring system.

## Quick start

Requires Python 3.11 or later.

```bash
python -m project_lumen.cli init-db lumen.db
python -m project_lumen.cli rank-corpora data/corpus_registry.csv
python -m project_lumen.cli demo lumen.db
python -m project_lumen.cli audit lumen.db
```

When running from the repository without installation:

```bash
PYTHONPATH=src python -m project_lumen.cli init-db lumen.db
```

Run the integrity tests with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## First 90-day success test

Project Lumen succeeds if it produces:

- a rights-safe metadata inventory of the digitized collections;
- a ranked shortlist of 50 manuscripts based primarily on impact ceiling,
  novelty potential, and evidentiary tractability;
- three pilot manuscripts selected with expert input;
- at least 100 human-corrected pages;
- one reproducible authorship or provenance case study;
- one expert-reviewed research note;
- a public-facing site that distinguishes evidence from speculation.

Anything less is preparation, not a historical contribution.
