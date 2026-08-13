# Project Lumen Codex Instructions

## Mission

Project Lumen uses AI to help identify, transcribe, translate, and investigate
digitized manuscripts. Historical importance is the selection criterion. Do not
prioritize a subject because it is personally interesting to the founder.

The Grand Discovery Program is the primary research track. Scholar-specific
workstreams, including the Donlan track, are bounded side investigations. Never
allow one scholar, person, language, country, religion, or period to dominate
the subject-neutral search for historically consequential material.

Potentially unedited and untranslated material is a priority only when its
contents could matter. Translation absence alone is not historical importance.

## Evidence rules

- Treat model output as a lead, never as a discovery.
- Preserve shelfmark, folio, source URL, and image region for every reading.
- Keep diplomatic transcription, normalized text, translation, and historical
  interpretation separate.
- Mark uncertainty explicitly. Never silently complete damaged or unclear text.
- For every L2 or higher claim, record competing hypotheses and a falsification
  test.
- Do not call a result novel until targeted literature searches and qualified
  human review are complete.
- Do not publish or redistribute manuscript images unless rights have been
  checked and permission obtained where required.
- Keep rejected hypotheses in the audit trail.
- Distinguish `not translated into English`, `not translated into any modern
  language`, `not edited in the original`, and `not discussed in scholarship`.
  These are separate claims requiring separate evidence.
- Never infer unstudied status from sparse catalog metadata or absence from an
  English-language search.

## Repository workflow

- Read `README.md`, `docs/RESEARCH_PROTOCOL.md`, and the relevant investigation
  dossier before changing research records.
- Use Python 3.11 or later.
- Run `PYTHONPATH=src python -m unittest discover -s tests -v` after code or
  schema changes.
- Run the ledger audit after modifying claim data.
- Do not commit raw catalog caches, restricted study images, databases, secrets,
  or generated archives.
- Prefer small, reviewable changes and preserve source provenance.
- Maintain broad-search and focused-investigation queues separately. Advancing
  a focused track must not silently suspend the Grand Discovery Program.

## Required completion report

End every substantial task with these exact sections:

### What I completed

List files changed, commands run, sources checked, results obtained, and any
failed or incomplete work. Distinguish verified facts from hypotheses.

### What Aiden needs to do

Give numbered, concrete actions. State `Nothing right now` when no human action
is needed. Clearly identify actions that require a decision, account access,
rights permission, payment, or specialist judgment.

### Current evidence level

State the highest claim level reached, from L0 through L5, and why.

### Next Codex task

Provide one ready-to-paste prompt for the next bounded task. Do not propose a
public discovery announcement unless the work has reached L5.
