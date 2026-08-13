# Grand Survey Report 001

Date: 26 July 2026  
Status: reconnaissance, not discovery  
Dataset version: Batch 001 and Batch 002

## Executive result

Project Lumen completed its first live metadata reconnaissance of the Digital
Vatican Library.

- 19 anomaly and under-description queries were completed.
- 1,416 raw catalog signal hits were collected.
- 1,225 unique manuscripts were identified in the broad anomaly pass.
- 14 consequential-name and high-impact phrase queries returned results.
- 230 additional raw hits across 223 manuscripts were collected.
- Complete catalog records were profiled for 45 leading candidates.
- Bibliography-only matches, low-quality images, heavily studied manuscripts,
  and keyword collisions were penalized.

These numbers do not represent new historical findings. They represent a first
research funnel.

## Method

The survey queried only public catalog metadata. It did not bulk-download
manuscript images.

Batch 001 searched for signals including:

- palimpsest and rewritten text;
- fragments;
- unpublished material;
- anonymous or unidentified content;
- disputed attribution;
- autographs and drafts;
- erasures;
- marginalia and postilles.

Batch 002 tested combinations involving historically consequential names and
terms such as autograph, unpublished, lost work, mutilated text, disputed
attribution, and unpublished letter.

The second stage fetched each leading candidate's full public catalog record
and measured:

- number of described internal items;
- number of catalog bibliography entries;
- description sparsity;
- low-quality digitization notices;
- whether a keyword appeared in content metadata or only in bibliography.

## Important negative result

Keyword ranking alone is unreliable.

Examples:

- `Vat.lat.3110` initially ranked highly for anonymous and palimpsest signals,
  but its catalog contains 34 bibliography entries. It is a valuable manuscript
  but a poor first novelty target.
- `Chig.L.V.176`, the Boccaccio autograph collection of Dante and Petrarch
  texts, generated several high-impact name signals but has 122 catalog
  bibliography entries. It is heavily studied.
- `Vat.lat.3196`, Petrarch's *Rerum vulgarium fragmenta*, has 220 catalog
  bibliography entries and should be a control, not a first discovery target.
- Combined keyword searches sometimes matched unrelated names in different
  records or references. These collisions require full-record inspection.

This validates the decision to separate lead generation from historical
assessment.

## Preliminary leads

### Lead 001: Cappon.283.pt.1

**Potential question:** Can a 1745 letter help identify or reconstruct the
history of a manuscript presented as a separate unpublished work by Cecco
d'Ascoli?

**Catalog signal:** Folios 117r-118r contain a letter by Filippo Bruni with news
about a manuscript containing an unpublished text by Cecco d'Ascoli.

**Why it could matter:** Cecco d'Ascoli was a medieval physician, astrologer,
poet, and controversial intellectual. A traceable unknown work, version, or
manuscript witness could matter to the history of medieval science and
literature.

**First image-level result:** The note quotes verses from the known
*L'Acerba*, but then explicitly says that *L'Acerba* is printed and contrasts
it with “la presente,” which had supposedly never been seen. Bruni's cover
letter appears to send or arrange inspection of a physical manuscript. This
supports an open hypothesis that the object was presented as a separate work,
not merely an ordinary *L'Acerba* copy.

**Why this may fail:** The distinction requires expert transcription. The
referenced manuscript may be a misidentified or unusual *L'Acerba* witness,
the attribution may be antiquarian error, “unpublished” may describe only its
status in 1745, or the object may have been returned and left no usable trail.
The note's chronological claims are internally suspect.

**Next test:**

1. Obtain two independent specialist transcriptions of folios 117r-118r.
2. Search the surrounding correspondence for the owner, acquisition, return,
   title, incipit, dimensions, or folio count.
3. Compare every clue with modern Cecco d'Ascoli catalogs and editions.
4. Trace Roman bookseller, auction, Capponi, and Ottoboni records after 1745.

**Current status:** L2 open hypothesis. A dated lead to a lost, dispersed, or
misidentified manuscript, not a discovery.

**Investigation dossier:** `docs/INVESTIGATION_001_CECCO.md`

### Lead 002: Borg.lat.565

**Potential question:** Does this large, weakly catalog-bibliographed volume
preserve underused evidence about early modern scientific and diplomatic
exchange between Europe and China?

**Catalog signal:** The volume contains scientific notes associated with Jean
Picard, letters involving Joachim Bouvet and Jean-François Foucquet, and a wide
range of diplomatic, mathematical, and ecclesiastical material.

**Why it could matter:** Bouvet and Foucquet participated in the transmission
of Chinese and European knowledge. Unedited letters or drafts could refine the
history of scientific exchange, chronology, translation, or institutional
decision-making.

**Known caution:** Individual folios from Borg.lat.565 have already been cited
in scholarship on the circulation of Chinese books. The opportunity is not to
declare the volume unknown, but to identify items within it that remain
unedited or disconnected from related correspondence.

**Operational problem:** The Digital Vatican Library marks this item as
low-quality.

**Next test:**

1. Build an item-level inventory of the 168 described units.
2. Identify all senders, recipients, dates, and locations.
3. Compare every letter against published Bouvet and Foucquet correspondence.
4. Rank unmatched items by historical importance.

**Current status:** strong network-reconstruction candidate, not a novelty
claim.

### Lead 003: Barb.lat.1862

**Potential question:** Are any political, humanist, or literary fragments in
this composite fifteenth-century manuscript absent from modern editions?

**Catalog signal:** The catalog describes letters of Pius II, a Petrarch letter
fragment, other humanist correspondence, and musical material.

**Why it could matter:** A previously unedited Pius II draft or a meaningful
Petrarch variant could affect political, diplomatic, or textual history.

**Known caution:** Musicological databases and specialized scholarship already
describe the manuscript as a source of fifteenth-century polyphony. The catalog
record's lack of bibliography does not mean the manuscript lacks scholarship
outside the Vatican catalog.

**Operational problem:** The Digital Vatican Library marks this item as
low-quality.

**Next test:**

1. Separate the manuscript's textual and musical layers.
2. Compare every Pius II item against critical letter editions.
3. Collate the Petrarch fragment against the established textual tradition.
4. Search musicological and humanist bibliographies separately.

**Current status:** composite-manuscript candidate requiring cross-disciplinary
review.

### Lead 004: Chig.I.VII.251

**Potential question:** Which Pius II letters and historical fragments in this
large collection remain unedited, incompletely attributed, or poorly connected
to known events?

**Catalog signal:** The manuscript includes episcopal letters, a historical
fragment concerning Venice, and material marked by unpublished or autograph
signals.

**Why it could matter:** Pius II was pope, diplomat, humanist, and historian.
Unedited drafts or letters could add evidence about fifteenth-century diplomacy
and papal government.

**Why this may fail:** The catalog already lists 12 bibliography entries, and
many Pius II letters have received extensive scholarly attention.

**Next test:** Create a folio-by-folio concordance against published Pius II
letter and historical-text editions.

**Current status:** medium-high importance, moderate saturation.

### Lead 005: Arch.Cap.S.Pietro.F.34

**Potential question:** Do the reused early hagiographic fragments preserve a
meaningful textual variant or provenance clue?

**Catalog signal:** A twelfth- or thirteenth-century Gospel harmony is bound
with earlier hagiographic material, including a fragment of the *Acta sanctae
Caeciliae*.

**Why it could matter:** Early witnesses can alter the textual history,
circulation, or dating of a saint's cult and related liturgy.

**Known caution:** The existence of the flyleaf material is already recorded in
specialist liturgical resources. The research question must concern its exact
text or provenance, not its mere existence.

**Next test:** Diplomatic transcription and collation of the flyleaves against
critical hagiographic and liturgical editions.

**Current status:** feasible textual-variant investigation, medium impact
ceiling.

### Lead 006: Arch.Cap.S.Pietro.E.17

**Potential question:** Does this early pseudo-Clementine witness or its added
fragments contain a meaningful textual or provenance anomaly?

**Catalog signal:** An eleventh-century manuscript contains the
pseudo-Clementine *Recognitiones*, associated material attributed to Clement
and Leo I, and a later papal bull fragment.

**Why it could matter:** A significant variant could affect the transmission
history of influential early Christian literature.

**Why this may fail:** The major texts are identified, and catalog description
alone gives no reason to expect an unknown version.

**Current status:** high raw signal, moderate actual discovery probability.

### Lead 007: Urb.lat.1516-1520

**Potential question:** Does Paganino Gaudenzi's apparently lightly
bibliographed material contribute something new to the early reception of
Machiavelli, prophecy, or political religion?

**Catalog signal:** The grouped manuscripts include an oration against
Machiavelli and a possible disciple, plus a substantial treatise on prophecy.
No bibliography entry was detected in the public record.

**Why it could matter:** It could clarify how Machiavellian ideas were received
and contested in the seventeenth century.

**Why this may fail:** The keyword hit does not involve a Machiavelli autograph,
and the material may already be discussed under Gaudenzi rather than under the
Vatican shelfmark.

**Current status:** under-described intellectual-history candidate.

## Current priority

The first image-level investigation of **Cappon.283.pt.1, folios 117r-118r**
is now open as Investigation 001.

It continues to offer the best combination currently identified:

- a precise two-folio target;
- a concrete claim that can be falsified;
- an explicit but unverified distinction between printed *L'Acerba* and a
  supposedly unseen manuscript;
- a traceable documentary network;
- manageable transcription scope;
- low catalog bibliography saturation.

The immediate work is expert transcription and provenance tracing. The
parallel metadata project should begin with Borg.lat.565 because it offers
the strongest opportunity for a larger network-reconstruction publication.

## What Project Lumen must not claim

At this stage Project Lumen has not:

- discovered a lost work;
- identified an unknown author;
- decoded a secret Vatican document;
- proved that any listed item is unpublished today;
- established that a catalog bibliography is complete;
- received expert manuscript review.

The valid claim is narrower:

> Project Lumen has built and tested a reproducible research funnel and
> identified several specific, falsifiable manuscript investigations with
> plausible historical value.

## Sources and rights

Primary metadata and IIIF identifiers come from the
[Digital Vatican Library](https://digi.vatlib.it/mss/). Images may be used for
personal study, but authorization is generally required for printed or online
publication. Project Lumen will not redistribute manuscript images without
confirmed permission.

The Vatican Library states that a large proportion of its collections remain
incompletely cataloged and that only about 20 percent had been satisfactorily
cataloged in scholarly form when it described the digitization program:
[Vatican Library digitization project](https://www.vaticanlibrary.va/en/in-digitalizzation/the-initial-digital-project.html).
