# Project Lumen Research Protocol

## 1. Intake

Every item begins with an authoritative shelfmark and source URL. Record the
holding institution, collection, manuscript identifier, date range, catalog
description, bibliography, IIIF manifest if supplied, and rights statement.

Do not infer a permissive license from public visibility.

## 2. Corpus triage

Score each candidate on a 0-5 scale:

- `impact_ceiling`: importance of the historical conclusion that could change;
- `description_gap`: sparse cataloging or content-level description;
- `historical_value`: demonstrated importance of the people, event, text, or
  institution involved;
- `network_value`: identifiable people, places, institutions, or events;
- `novelty_potential`: reasonable chance of an under-discussed contribution;
- `feasibility`: script, language, image quality, and available expertise;
- `evidentiary_tractability`: ability to test the question against independent
  evidence;
- `comparison_material`: known texts or hands available for testing;
- `rights_clarity`: ability to research and publish derived work responsibly;
- `saturation_penalty`: depth of existing scholarship.

The preliminary ranking is a prioritization aid, not evidence of novelty.
Impact ceiling receives the largest positive weight. Personal relevance,
publicity value, and thematic preference are excluded from the score.

## 3. Page segmentation

Create stable regions for:

- main text;
- marginalia;
- interlinear additions;
- headings;
- seals, stamps, and ownership marks;
- diagrams and tables;
- erased, overwritten, or damaged text.

Every region receives coordinates or another reproducible locator.

## 4. Transcription

Run at least two independent transcription passes. For difficult material, use
a specialized handwriting-recognition model plus a general multimodal model.

Store:

- exact diplomatic transcription;
- expanded abbreviations;
- normalized text;
- unclear characters;
- alternative readings;
- model identity and settings;
- human corrections;
- character- or token-level confidence where available.

Never silently replace an uncertain reading with a plausible word.

Recommended notation:

- `[abc]`: restored text;
- `[...]`: unreadable or missing text;
- `<abc>`: scribal insertion;
- `⟦abc⟧`: deletion or cancellation;
- `abc(?)`: uncertain reading;
- `sic`: apparently erroneous original form retained.

Project-specific conventions must be documented for each edition.

## 5. Translation

Translations must be generated from the corrected diplomatic or normalized
transcription, never directly from an image without preserving the intermediate
text.

Each translation records:

- source text version;
- literal translation;
- readable translation;
- unresolved words and idioms;
- period-specific technical meanings;
- translator or model;
- reviewer.

## 6. Entity and relation extraction

Extract people, places, offices, institutions, dates, works, events, and quoted
texts. Maintain the original surface form and a normalized identifier.

Relations require evidence spans:

- wrote;
- copied;
- sent;
- received;
- owned;
- cited;
- corrected;
- commissioned;
- witnessed;
- traveled through;
- likely associated with.

The phrase `likely associated with` must not be silently converted into a
factual relationship.

## 7. Authorship and scribal attribution

An attribution dossier must include:

1. candidate generation and why each candidate is plausible;
2. chronological and geographic compatibility;
3. vocabulary and stylistic comparison;
4. spelling, abbreviation, and formula comparison;
5. handwriting comparison if suitable samples exist;
6. ideological or subject-matter compatibility;
7. provenance and transmission evidence;
8. strongest contradictory evidence;
9. plausible unknown-author alternatives;
10. reviewer assessment.

Do not publish a percentage unless it comes from a defined and validated model.
Use ordinal confidence by default: weak, plausible, substantial, strong.

## 8. Historical significance

For every significance claim, answer:

- What exactly is new or better documented?
- What was previously believed?
- Which sources establish the prior state of knowledge?
- Does the manuscript change chronology, causation, attribution, geography,
  transmission, or interpretation?
- Is the contribution local, field-specific, or historically broad?
- What would falsify the claim?

## 9. Novelty search

Search:

- the Vatican catalog and listed bibliographies;
- manuscript-specific shelfmark references;
- Google Scholar and discipline-specific indexes;
- books, articles, critical editions, dissertations, and conference papers;
- variant spellings of names and shelfmarks;
- scholarship in relevant languages.

Absence from an English-language web search is not evidence of novelty.

## 10. Review gates

| Gate | Required approval |
|---|---|
| Transcription complete | second reader |
| Translation complete | language-competent reviewer |
| Attribution claim | relevant historian or paleographer |
| Novelty claim | documented literature search plus specialist |
| Image publication | confirmed institutional permission |
| Public release | research editor and integrity check |

## 11. Reproducibility

Every public finding must preserve:

- source identifiers;
- page or folio references;
- transcription versions;
- evidence spans;
- analysis code or method;
- model names and dates;
- reviewer names or declared anonymous roles;
- corrections after publication.
