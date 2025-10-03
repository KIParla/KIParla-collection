# KIParla-collection

[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

## The collection

The KIParla collection results from the merging of the available modules.

At the moment, available modules are:

| Module      | repository                         |
| ----------- | ---------------------------------- |
| KIP         | https://github.com/KIParla/KIP     |
| ParlaBO     | https://github.com/KIParla/ParlaBO |
| ParlaTO     | https://github.com/KIParla/ParlaTO |
| KIPasti     | https://github.com/KIParla/KIPasti |

Should you find inconsistencies in the data, please refer to the [original module](./modules.md) to correct them.
This is not a working environment, it is purely meant as a joint repository for consultation.

## Repository organization

This repository contains:

* metadata for both speakers and conversations, in the [`metadata`](./metadata/) subfolder (see [metadata](#metadata) section below)
* descriptions of the set of transcription conventions used for this module ([Transcription conventions](./jefferson-notation.md))

For each conversation you will find:

* `.eaf` file in [`eaf/`](./eaf/) folder: time-aligned Jefferson-style transcriptions (open with [ELAN]()).
* `.txt` file in [`linear-jefferson/`](./linear-jefferson/) folder: linearized Jefferson-style transcription.
* `.txt` file in [`linear-orthographic/`](./linear-orthographic/) folder: linearized transcription retaining only orthographic words.
* `.tsv` file in [`tsv/`](./tsv/) folder: verticalized version of the transcription, with Jefferson-style information decoupled from the text as features See [verticalized-content](#verticalized-content) for more information.

Linear files in [`linear-jefferson/`](./linear-jefferson/) and [`linear-orthographic/`](./linear-orthographic/) contain one Transcription Unit (TU) per line. Each line has two columns: the first is the speaker code, and the second is the transcription. TUs are sorted by their start time.

## Metadata

Each participant and each conversation are associated to a series of metadata, that can be found in the
[`metadata/participants.tsv`](metadata/participants.tsv) and [`metadata/conversations.tsv`](metadata/conversations.tsv) fils.
Metadata is to be interpreted as follows:

1. Participants metadata:
	- `code`: unique anonymized 5-char identifier for each participant. Unknown, occasional participants
	 to conversations are associated with a special `???` code.
	- `gender`: either `M` for masculine or `F` for feminine
	- `age-range`: 5 years range including the participant’s age.
	- `birth-region`: Italian region[^1] where the participant was born. If outside Italy, the label `estero` is used.
	- `occupation`: occupation of the participant, according to [ISTAT categories](https://professioni.istat.it/). For more information see [occupation label](./occupation-levels.md)
	- `study-level`: highest completed level of education[^3]
	- Additionally, the [`metadata/participants.tsv`](metadata/participants.tsv) also contains a `conversations` colum that summarizes the conversations in which the participant appears.

2. Conversations metadata:
   - `code`: unique identifier for conversation
   - `type`: type of interaction, for this module all conversation are `semistructured-interview`
   - `duration`: duration of the conversation, expressed in `hh:mm:ss` format
   - `participants-number`: number of participants in the conversation
   - `participants-relationship`: relation, asymmetric for this module
   - `moderator`: presence of a moderator
   - `topic`: fixed for this module
   - `year`: year of collection
   - `collection-point`: two-letter code of the collection area: `BO` for Bologna for this module.
   - Additionally, the [`metadata/conversations.tsv`](metadata/conversations.tsv) also contains a `participants` field that recaps the codes of the participants to that conversation

[^1]: `abruzzo`, `basilicata`, `calabria`, `campania`, `emilia-romagna`, `friuli-venezia-giulia`, `lazio`, `liguria`, `lombardia`, `marche`, `molise`, `piemonte`, `puglia`, `sardegna`, `sicilia`, `toscana`, `trentino-alto-adige`, `umbria`, `valle-d-aosta`, `veneto`
[^3]: `elementary-school`, `liceo-diploma`, `middle-school`, `phd`, `technical-vocational-diploma`, `university-degree`, `university-degree-ongoing`

## Verticalized content

Conversations are also available in a vertical, pseudo-tokenized version in [`tsv/`](./tsv/).
Tokenization is obtained by validating the Jefferson transcription using custom [tools](https://github.com/LaboratorioSperimentale/kiparla-tools)and splitting on token boundaries: whitespaces, prosodic links (`=`), and apostrophes used for elision in Italian orthography. Each transcription-derived token is then documented on one row.

Each token is represented as 13 columns, as follows:

1. `token_id`: unique token identifier within the conversation
2. `speaker`: speaker `code` as it can be found in [`metadata/participants.tsv`](metadata/participants.tsv)
3. `tu_id`: progressive identifier assigned to transcription units
4. `span`: portion of the original jefferson transcription containing the token
5. `form`: orthographic form of the token. This differs from the `span` as special symbols are stripped out and represented as `jefferson_feats`. Moreover, shortpauses (`(.)` in the transcription) are represented as `[PAUSE]` and unintelligible tokens (sequences of `x` in the transcription) are represented as `x`
6. `type`: one of
   - `linguistic`: everything that is considered to be a content linguistic token
   - `nonverbalbehavior` used for transcribed non verbal behaviors, such as laughing or sighing
   - `shortpause` that identify pauses
   - `unknown` that identify unintelligible spans in transcription
   - `error` is a residual class to mark cases where the transcription is not well formed according to Jefferson format. Therefore, the token is not analyzed and transcription will be corrected in future releases.
7. `jefferson_feats`: the column collects a list of word-level features derived from the transcription in Jefferson format. More specifically:
   - `SpaceAfter=No`: no whitespace between this token and the next (e.g., `l'` in `l'anno`)
   - `ProsodicLink=Yes`: a prosodic link (=) to the following token,
   - `Intonation` can assume values `Falling`, `Rising` or `WeaklyRising` and translates word final punctuation sign in Jefferson transcriptions (i.e., `.`, `?` and `,` respectively)
   - `Interrupted=Yes`: words interrupted in speech, transcribed with final, transcribed with final `~`
   - `Truncated=Yes`: truncated forms (e.g., `anda'` for `andare`, common in some Italian varieties)
   - `Volume` can assume values `High` or `Low` and translated Jefferson's uppercase and `°` respectively
8. `align`: alignment features for the first and last token of each TU, through `AlignBegin` and `AlignEnd` features expressed in milliseconds
9.  `prolongations`: positions of sound prolongations (colons `:`) within the word, encoded as a comma-separated list of `<char_id>x<count>` pairs
	- `char_id` is the zero-based index of the character in the token's orthographic form.
	- `count` is the number of consecutive colons immediately following that character in the original span
	- example: for span = `ese::mpio:`, its orthographic form is `esempio` and the prolongations field would assume value `2x2,6x1` (the 3rd letter `e` has 2 colons; the 7th letter `o` has 1 colon).
10. `pace`: marks whether the token participates in a fast or slow paced span within the word.
	- Format: `Fast=<char_id_start>-<char_id_end>` or `Slow=<char_id_start>-<char_id_end>`
	- Indices are zero-based, inclusive, and refer to character positions in form
11. `guesses`: character span(s) transcribed as uncertain (i.e., in round brackets in the Jefferson transcription).
	- Format: `<char_id_start>-<char_id_end>` (zero-based, inclusive, over form)
12. `overlaps`: comma-separated list of character spans participating in simultaneous speech, with an overlap group identifier.
	- Format: `<char_id_start>-<char_id_end>(<overlap_id>)`, where indices are are zero-based, inclusive indices over form and `overlap_id` is the progressive number of the overlapping group within the TU
	- Examples: the span `e[se]mp[i` would be encoded as `1-3(2),5-6(3)` meaning that characters from position one (inclusive) to three (exclusive) participate to span number 2 while the last character (with id 5) participates to the third overlapping span of the transcription unit. When the overlapping id was not decidable, a `?` is used

## Data access

Due to GDPR restrictions, pseudo-anonymized audio files (MP3) are available under a restricted-access license. To request access, please contact the corpus coordinators through the KIParla website and follow the provided procedure.

## How to cite

To cite this module please include

> Mauri, C., Ballarè, S., & Zucchini, E. (2024). Modulo ParlaBO (Version 1.0.0) [Data set]. https://doi.org/https://doi.org/10.60760/unibo/parlabo

in your references

```bibtex
	@misc{Mauri_Modulo_ParlaBO_2024,
		author = {Mauri, Caterina and Ballarè, Silvia and Zucchini, Eleonora},
		doi = {https://doi.org/10.60760/unibo/parlabo},
		month = oct,
		title = {{Modulo ParlaBO}},
		url = {https://github.com/KIParla/ParlaBO},
		year = {2024}
	}
```


-----

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

<!-- [![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa] -->

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg