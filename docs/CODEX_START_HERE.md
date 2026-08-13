# Codex Start Here

This is the operational handoff for continuing Project Lumen with Codex.

## 1. Open the repository

The canonical repository is
[`aibarraza22-web/vatican`](https://github.com/aibarraza22-web/vatican).
Open that repository in Codex, or clone it and open the resulting folder.

For Codex CLI:

```bash
git clone https://github.com/aibarraza22-web/vatican.git
cd vatican
codex
```

Codex reads the repository's `AGENTS.md` when a new session starts. Start a new
session after changing that file.

## 2. Establish a safe checkpoint

```bash
git status
```

Do not commit files under `research/`, catalog caches, local databases, secrets,
or generated ZIP files.

## 3. Create the Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

Expected result: seven tests pass. If any test fails, stop research automation
and ask Codex to diagnose the failure before collecting more data.

## 4. First prompt to paste into Codex

```text
Read AGENTS.md, README.md, docs/RESEARCH_PROTOCOL.md,
docs/FIRST_SURVEY_REPORT.md, and docs/INVESTIGATION_001_CECCO.md. Do not edit
anything yet. Verify the repository setup, run the full test suite, inspect the
structured Investigation 001 record, and report: (1) what is reproducible,
(2) what evidence is missing, (3) any inconsistency between the dossier and the
JSON record, and (4) the smallest next research task. Follow the required
completion-report format in AGENTS.md.
```

## 5. Division of responsibility

### Codex and ChatGPT can do

- write and test collection, ranking, and evidence-ledger code;
- inspect public catalog metadata and permitted digital sources;
- generate provisional transcriptions and translations;
- compare sources and track alternative hypotheses;
- prepare outreach drafts, research dossiers, and publication-ready data;
- maintain reproducibility, citations, and rejected-hypothesis records.

### Aiden must do

- approve major changes in research direction;
- make accounts available locally when a site or service requires them;
- request or approve manuscript-image publication rights;
- contact and identify human specialists, unless an authorized connector is
  explicitly used to draft or send outreach;
- judge whether to spend money or share unpublished findings;
- personally review any public statement made under his name.

### Qualified specialists must do

- validate difficult paleography and damaged readings;
- evaluate authorship, dating, codicology, and historical significance;
- confirm whether a supposed contribution is actually new to scholarship;
- approve claims before they advance to L4 or L5.

## 6. Current project state

- Two metadata survey batches exist.
- Batch 001 recorded 1,416 signal hits across 1,225 manuscripts.
- Thirty records were profiled in the first batch and fifteen in the second.
- `Cappon.283.pt.1`, ff. 117r-118r is the first image-level investigation.
- The Cecco d'Ascoli case is an L2 hypothesis, not a discovery.
- The immediate research need is independent transcription and provenance
  tracing, not publicity.

## 7. Update cadence

Each work cycle should be bounded to one deliverable, such as one catalog batch,
one folio transcription, one provenance search, or one dossier revision. At the
end of every cycle, Codex must say exactly what it completed and exactly what
Aiden needs to do next.

## 8. Optional Donlan research track

The Cecco investigation and the Thomas A. Donlan research track are separate.
To work on the latter, read `docs/DONLAN_EVIDENCE_GAP_MAP.md` and use the bounded
prompt at the end of that file. Do not imply that any exact Vatican document is
unpublished or untranslated until the source census is complete.
