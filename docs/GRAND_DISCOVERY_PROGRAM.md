# Grand Discovery Program

Date established: 13 August 2026  
Role: primary Project Lumen research program  
Starting evidence level: L0 lead generation

## Objective

Find the most historically consequential Vatican-held material that is
digitally accessible or can be identified through lawful public metadata and
that may be unedited, untranslated, unidentified, misattributed, overlooked, or
disconnected from the scholarship that would reveal its importance.

The program is subject-neutral. It is not centered on Thomas A. Donlan,
François de Sales, Cecco d'Ascoli, Catholic history, Latin, Europe, or any other
single topic. Focused investigations are useful tests inside a much larger
search.

## What counts as a high-value lead

A lead needs both:

1. a credible status gap, such as no identified edition, no verified modern
   translation, disputed authorship, sparse description, uncataloged internal
   items, unexplained marginalia, erased writing, an unknown witness, or a
   broken provenance trail; and
2. a credible consequence, such as the ability to change authorship,
   chronology, causation, transmission, geography, intellectual networks,
   institutional decisions, or understanding of an important event or idea.

An untranslated routine receipt is low priority. A translated text can remain
high priority if a draft, variant, annotation, or attribution changes history.

## Discovery classes

The survey must search across all available languages, regions, periods, and
subjects for:

- lost works or references precise enough to trace one;
- unknown or substantially different versions of influential texts;
- anonymous, pseudonymous, or disputed material with plausible important
  authors or institutional origins;
- drafts, corrections, suppressed passages, instructions, or private
  correspondence behind consequential decisions;
- palimpsests, erased writing, reused fragments, damaged layers, and binding
  waste;
- marginalia revealing ownership, readership, dissent, censorship, scientific
  observation, transmission, or provenance;
- scientific, mathematical, astronomical, medical, geographic, cartographic,
  engineering, and technological records that alter timelines or networks;
- diplomatic, political, legal, financial, missionary, and administrative
  records connecting important actors or events;
- evidence from underrepresented languages or communities that was cataloged
  through a European or ecclesiastical lens and may be poorly indexed;
- materials whose contents are known in one specialist field but disconnected
  from another field where they would matter more.

## Four separate status questions

Never collapse these into the word `unknown`:

| Question | Required evidence |
|---|---|
| Is the original text unedited? | Critical editions, manuscript catalogs, bibliographies, and exact shelfmark searches |
| Is it untranslated into English? | English editions, books, articles, dissertations, and translation catalogs |
| Is it untranslated into any modern language? | Multilingual searches in the source language and major scholarly languages |
| Is it unstudied or historically unused? | Citation tracing and specialist review, not search-engine silence |

Allowed labels before verification are `edition not yet located`, `English
translation not yet located`, `modern translation not yet located`, and
`specialist discussion not yet located`.

## Balanced search lanes

Every major survey batch should draw from multiple lanes so the project does
not mistake Latin catalog visibility for historical importance:

1. Latin and European-language manuscripts.
2. Greek, Syriac, Hebrew, Arabic, Armenian, Georgian, Coptic, Ethiopic, Persian,
   Ottoman Turkish, and other Asian or African language collections.
3. Indigenous American, missionary, colonial, and cross-cultural records.
4. Scientific, medical, mathematical, geographic, and technical material.
5. Diplomatic, political, legal, economic, and institutional records.
6. Literary, philosophical, theological, and textual-transmission material.
7. Physical anomalies, including palimpsests, fragments, bindings, erased text,
   unusual inks, inserted leaves, and mixed hands.

The lane list is an anti-bias mechanism, not a quota. Final rank is based on
impact and evidence.

## Ranking model

Score each exact item from 0 to 5 on:

- historical impact ceiling;
- strength of the status-gap evidence;
- specificity of the research question;
- description gap;
- availability of exact folios or internal items;
- comparison material;
- feasibility of transcription and language review;
- ability to falsify the hypothesis;
- rights and access tractability;
- existing scholarly saturation.

Apply penalties for:

- famous-name keyword collisions;
- signals found only in bibliography;
- claims based only on catalog silence;
- no exact shelfmark or folio;
- inaccessible source images;
- no competent language-review route;
- importance based only on publicity value.

## Funnel

### Stage 1: Metadata discovery

Search collection inventories and item descriptions using multilingual anomaly
terms, document types, material features, uncertain attribution terms, and
historically consequential entities. Preserve zero-result queries.

### Stage 2: Full-record profiling

Inspect the complete catalog record, internal-item count, bibliography,
digitization quality, rights, and whether the signal describes the manuscript
itself or merely appears in a citation.

### Stage 3: Cross-catalog matching

Search exact shelfmarks, titles, incipits, explicits, senders, recipients,
dates, old shelfmarks, provenance marks, and variant names across WorldCat,
manuscript portals, critical editions, dissertations, articles, and
language-specific scholarship.

### Stage 4: Status verification

Assign only provisional status labels until searches cover the original
language, English, Italian, French, German, Spanish, and other relevant
scholarly languages. Record databases and date searched.

### Stage 5: Image-level investigation

For accessible targets, isolate exact folios and produce two independent
transcriptions. Preserve diplomatic text, normalized text, literal translation,
readable translation, uncertainty, and image coordinates separately.

### Stage 6: Historical testing

State the best claim, strongest alternatives, contradicting evidence, and a
falsification test. Compare with dated scholarship and related documents.

### Stage 7: Expert and rights review

No lead becomes a discovery announcement until appropriate language,
paleography, subject, novelty, and image-rights review is complete.

## Required batch output

Each batch must produce:

- a query log, including zero results;
- a deduplicated item-level candidate table;
- reasons for promotion or rejection;
- a top-25 shortlist balanced across search lanes;
- no more than five image-level recommendations;
- one paragraph explaining the likely blind spots of the batch;
- a next batch designed to correct those blind spots.

Use `data/discovery_queue_template.csv` for exact candidates.

## Relationship to focused tracks

Focused tracks can test the system against a known scholar, book, historical
question, or collection. They must remain separately labeled and cannot become
the sole queue. At any time, Project Lumen should be able to report:

- the top broad-discovery candidates;
- active focused investigations;
- why each is active;
- the next falsifiable step for each;
- which work is blocked by access or expertise.

## First bounded Codex prompt

```text
Read AGENTS.md, README.md, docs/RESEARCH_PROTOCOL.md,
docs/HIGH_IMPACT_SEARCH.md, docs/FIRST_SURVEY_REPORT.md, and
docs/GRAND_DISCOVERY_PROGRAM.md. Treat the Grand Discovery Program as the
primary track and Donlan as only one separate focused workstream. Do not
translate random manuscripts yet. Audit the two existing Grand Survey batches
for language, collection, subject, and catalog-keyword bias. Then design Batch
003 as a balanced metadata-only search across at least five search lanes,
including at least two non-Latin lanes and one scientific or technical lane.
Create the query plan and candidate-output structure, but do not make network
requests until you have documented rate limits, caching, stop conditions, and
how you will distinguish: no edition located, no English translation located,
no modern translation located, and no scholarship located. Preserve zero-result
queries. End with the exact completion sections required by AGENTS.md.
```
