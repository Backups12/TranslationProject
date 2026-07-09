# Arabic Romanization Table (2012) — Full Project Reference

This document combines:
1. The **full extracted text** of the 2012 Arabic Romanization Table PDF (letters, vowels, notes, and all 26 rules verbatim).
2. **Rule-by-rule explanations, worked examples, and clarifications** built up through discussion (all 26 rules).
3. **Project-specific engineering notes** — how each rule maps onto a real transliteration pipeline, what can be handled deterministically, and what requires an external diacritization/vocalization tool.
4. A **core parsing algorithm** for detecting long vowels vs. diphthongs vs. plain consonants, developed through worked examples.

---

## PART 1 — FULL EXTRACTED PDF CONTENT

### Letters of the Alphabet

| Letter | Romanization |
|---|---|
| ا | (omit — see Note 1) |
| ب | b |
| ت | t |
| ث | th |
| ج | j |
| ح | ḥ |
| خ | kh |
| د | d |
| ذ | dh |
| ر | r |
| ز | z |
| س | s |
| ش | sh |
| ص | ṣ |
| ض | ḍ |
| ط | ṭ |
| ظ | ẓ |
| ع | ' (ayn) |
| غ | gh |
| ف | f (see Note 2) |
| ق | q (see Note 2) |
| ك | k |
| ل | l |
| م | m |
| ن | n |
| ه / ة | h (see Note 3) |
| و | w |
| ي | y |

### Vowels and Diphthongs

| Sign | Romanization |
|---|---|
| َ◌ (fatḥah) | a |
| ُ◌ (ḍammah) | u |
| ِ◌ (kasrah) | i |
| اَ◌ | ā (see Rule 5) |
| ى | á (see Rule 6a) |
| و | ū |
| ْو َ◌ | aw |
| ْى َ◌ | ay |
| ى ِ◌ | ī |

### Letters Representing Non-Arabic Consonants
(Not exhaustive; romanization varies by region.)

| Letter | Romanization |
|---|---|
| گ | g |
| چ | ch |
| ڤ | v |
| ۋ | v |
| چ | zh |
| ڴ | ñ |
| ڥ | v |
| ژ | zh |
| پ | p |

### Notes
1. For alif supporting hamzah, see Rule 2. For hamzah romanized by the consonantal sign ' (alif), see Rule 8(a). For other orthographic uses of alif, see Rules 3–5.
2. The Maghribī variants ڢ and ڧ are romanized f and q respectively.
3. ة in a word in the construct state is romanized t. See Rule 7(b).

---

## PART 2 — RULES OF APPLICATION — FULL TEXT + EXPLANATIONS

### Rule 1 — و and ي represent three things

(a) Consonants w and y: وضع waḍ', عوض 'iwaḍ, دلو dalw, يد yad, حيل ḥiyal, طهي ṭahy
(b) Long vowels ū, ī, ā: أولى ūlá, صورة ṣūrah, ذو dhū, إيمان īmān, جيل jīl, في fī, كتاب kitāb, سحاب saḥāb, جمان jumān
(c) Diphthongs aw, ay: أوج awj, نوم nawm, لو law, أيسر aysar, شيخ shaykh, عيني 'aynay

**Project logic:** و/ي are context-dependent — same letter, three totally different romanized outputs depending on whether it's acting as a consonant, part of a long vowel, or part of a diphthong. Fully resolved by the parsing algorithm in Part 4 below.

### Rule 2 — Alif/wāw/yā' as hamzah "seats"

ا, و, ى when used to *support* hamzah (ء) are not romanized for their own sound. See Rule 8(a).

**Project logic:** These "seat" letters are just visual scaffolding holding up the hamzah glyph — not real w/y/ā sounds. The seat contributes nothing; the hamzah itself (Rule 8) and any vowel mark also attached to that same seat position determine the output.

### Rule 3 — Alif supporting waṣlah/maddah

Alif supporting waṣlah (ٱ) or maddah (آ) is not itself romanized. See Rules 9 and 10.

### Rule 4 — Silent alif/wāw (orthographic signs, no phonetic value)

Examples: فعلوا fa'alū (plural-protector alif after past-tense verbs), أولائك ulā'ika (silent wāw), أوقية ūqīyah. Also the internal alif in مائة (see Rule 26).

**Project logic:** These letters are pure spelling artifacts — completely ignore them in romanization. Key triggers: plural-protector alif on فعلوا-type verbs, silent wāw in specific words/names (also عمرو → 'Amr), and the internal alif in مائة.

### Rule 5 — Alif = long ā

فاعل fā'il, رضا riḍā. Medial alif is sometimes omitted in Arabic script but always shown in romanization (see Rule 19 — dhālika, ru'ūs).

### Rule 6 — Final ى special cases

**(a)** Alif maqṣūrah (ى, dotless) representing ā → romanized **á**: حتَّى ḥattá, مضَى maḍá, كبرَى kubrá, يحيَى Yaḥyá, مسمَّى musammá, مصطفَى Muṣṭafá.

**(b)** Final ّى ِ (dotted yā', with shaddah) in fā'īl-pattern nouns/adjectives from **defective roots** → romanized **ī**, not īy, *regardless of the shaddah*: رضي الدين Raḍī al-Dīn. (Compare الرضى without shaddah → al-Raḍī.)

**(c)** Final ّى ِ (dotted yā', with shaddah) as the **nisbah** (relative adjective of origin) ending → also romanized **ī**, not īy: المصرِيّ al-Miṣrī. (Compare ةّيِالمصر al-Miṣrīyah, feminine form, medial — see Rule 11b1.)

**Project logic:**
- Dotless ى (alif maqṣūrah) → always á, never carries shaddah, no exceptions (Rule 6a).
- Dotted ي, final position, with shaddah → shaddah is explicitly overridden/ignored → clean ī (Rules 6b/6c). Only in **final** position; the same letter+shaddah **medially** behaves differently (→ īy, Rule 11b1).
- Distinguishing 6(b) vs 6(c) requires knowing whether the word is a defective-root fā'īl-pattern noun/adjective, or a nisbah adjective — a morphological classification requiring lookup/dictionary knowledge, not derivable from the bare letters alone.

### Rule 7 — Tā' marbūṭah (ة)

Etymology note: ة is a hybrid letter — the body shape of ه (hā') with the two dots of ت (tā') placed on top. It exists specifically as a word-final marker (mostly feminine singular nouns/adjectives) and never appears initial/medial. Its dual ancestry (hā' + tā') explains why it alternates between h and t sounds depending on context.

**(a)** Indefinite or definite-article-preceded noun/adjective ending in ة → romanized **h** (often also spelled with ه in casual writing): صلاة ṣalāh, الرسالة البهية al-Risālah al-bahīyah, مرآة mir'āh, أرجوزة فى الطب Urjūzah fī al-ṭibb.

**(b)** Word ending in ة in the **construct state** (muḍāf wa-muḍāf ilayh / iḍāfah) → romanized **t**: وزارة التربية Wizārat al-Tarbiyah, مرآة الزمان Mir'āt al-zamān.

**(c)** Word ending in ة used **adverbially** (vocalized ًة, tanwīn al-fatḥ) → romanized **tan**: فجأة faj'atan. See Rule 12(b).

**Project logic:** ة is a chameleon — its output depends entirely on grammatical context (standalone/definite vs. construct-state vs. adverbial), not on the letter itself. Requires syntactic/contextual classification.

### Rule 8 — Hamzah (ء)

**(a)** Initial position (start of word, after a prefixed preposition/conjunction, or after the definite article) → **not romanized at all**. Medial or final position → romanized as **'** (prime), regardless of which letter (alif/wāw/yā') is acting as the seat.

Examples: أسد asad, أنس uns, إذا idhā (all initial, dropped) / مسألة mas'alah, مؤتمر mu'tamar, دائم dā'im, ملأ mala'a, خطئ khaṭi'a (all medial/final, → ').

**(b)** ء, when replaced by the sign ٱ (waṣlah) and then known as **hamzat al-waṣl**, is not represented in romanization. See Rule 9.

**Project logic:** Position (initial vs. medial/final) is the only variable — the seat letter (أ/ؤ/ئ) is irrelevant to the outcome, and contributes nothing of its own (see Rule 2). "Initial" is broader than "first letter of the word" — also covers post-prefix and post-article positions. Importantly: **the seat letter can also carry its own separate vowel mark**, which is a completely different, additional sound coming right after the hamzah's '  — see مائة worked example in Part 4.

### Rule 9 — Waṣlah (ٱ) / hamzat al-waṣl

Like initial hamzah, waṣlah itself is never romanized as a symbol. But **when the word actually starts an utterance/citation unit with nothing preceding it, some vowel must still be pronounced/written to launch the word:**

- If the alif supporting waṣlah belongs to the article **ال** → the initial vowel is romanized **a** (→ "al-").
- For **any other word** beginning with hamzat al-waṣl → the initial vowel is romanized **i**.

Examples: رحلة ٱبن جبير Riḥlat Ibn Jubayr (i — not the article), الإستدراك al-istidrāk (a for the article; a *second*, separate hamzat al-waṣl inside "istidrāk" also resolves to i), كتب ٱقتنتها kutub iqtanat'hā (i), باهتمام عبد ٱلمجيد bi-ihtimām 'Abd al-Majīd (bi- attached, but still i on ihtimām; al- on al-Majīd → a).

**Project logic (fully corrected after discussion):**
- The **sign** (waṣlah curl) itself is never separately represented in romanization.
- The **vowel** underneath it (a or i) **is always written**, regardless of sentence/clause position or hyphenation status (written the same whether the word is hyphen-attached to a prefix like bi-/wa-/al- or stands alone).
- **The only decision variable is: is this specific word the definite article, or not?** Article → a. Everything else → i.
- Hamzat al-waṣl will be restored automatically by a proper Arabic diacritization tool as part of normal vocalization — no separate detection logic needed beyond applying the a/i rule once the mark is present.

### Rule 10 — Maddah (˜, the sign making آ)

**(a)** Initial آ → romanized **ā** (hamzah is initial, so dropped per Rule 8a, leaving just the long vowel): آلة ālah, كلية الآداب Kullīyat al-Ādāb.

**(b)** Medial آ, representing the phonetic combination hamzah+ā → romanized **'ā** (hamzah is medial, so → ' per Rule 8a, followed by ā): تآليف ta'ālīf, مآثر ma'āthir.

**(c)** Maddah **otherwise** (not representing a real hamzah+ā fusion) → **not represented at all**; treat it as an ordinary alif/long ā and continue reading the word normally: خلفآء khulafā' (the maddah in the middle is ignored — plain ā; the final ء is a separate, ordinary final hamzah per Rule 8a → ').

**Project logic:** 10(a) and 10(b) are Rule 8(a)'s initial/medial hamzah logic applied to the specific case where hamzah+ā got orthographically fused into one آ glyph. Only 10(c) is a genuinely separate case: maddah as pure spelling noise, contributing nothing to romanization — just read straight through as a plain long ā and continue.

### Rule 11 — Shaddah / tashdīd (doubling mark)

**(a) Over و:**
1. ّوُ (long vowel + consonant) → **ūw**: عدُوّ 'adūw, قُوّة qūwah.
2. ّوَ (diphthong + consonant) → **aww**: شَوّال Shawwāl, صَوّر ṣawwara, جوّ jaww.

**(b) Over ى/ي:**
1. Medial ّىِ (long vowel + consonant) → **īy**: المصرِيّة al-Miṣrīyah.
2. Final ّىِ → **ī** (shaddah ignored — same rule as 6b/6c).
3. Medial/final ّىَ (diphthong + consonant) → **ayy**: أيّام ayyām, سَيّد sayyid, قصَيّ Quṣayy.

**(c) Over any other letter** → double the letter (or digraph) in romanization: الغزّيّ al-Ghazzī, الكشّاف al-Kashshāf (sh doubles as a full digraph → shsh).

**Project logic:**
- و and ي (dotted form) are the two "special" shaddah letters, each splitting into long-vowel-combo vs. diphthong-combo depending on the preceding vowel sign.
- Dotless ى (alif maqṣūrah) never carries shaddah — exclusively Rule 6(a)'s territory (always á).
- Final dotted-ي + shaddah is a recurring override across the table (Rule 6b/6c and 11b2 describe the same phenomenon from two angles) — shaddah is explicitly ignored only in this one specific position (final).
- Every other letter: default = simple doubling, no exceptions, no context-dependence.

### Rule 12 — Tanwīn

Tanwīn (ٌ/ً/ٍ → un/an/in) is **normally dropped entirely** in romanization. Written only in two cases:

**(a)** Indefinite nouns derived from **defective roots**: قاضٍ qāḍin, معنى ma'nan.

**(b)** **Adverbial** use of a noun/adjective → romanized **-an**: طبعًا ṭab'an, فجأة faj'atan (same mechanism as Rule 7c), المشترك وضعاً al-Mushtarik waḍ'an, والمفترق صقعاً wa-al-muftariq ṣuq'an.

**Project logic:** Default = drop. "Defective root" classification is a recurring flag needed across Rules 6, 11(b2), and 12(a) — track as a single reusable morphological property per word. Adverbial-use detection (12b) is the same underlying case as tā' marbūṭah's "-tan" ending (Rule 7c), generalized to non-ة adverbial nouns too.

### Rule 13 — Final inflections of verbs

Retained in romanization **except in pause**.

Examples: من ولي مصر man waliya Miṣr (mid-phrase, vowel kept), معرفة ما يجب لهم ma'rifat mā yajibu la-hum (mid-phrase, kept), صلى الله عليه وسلم ṣallá Allāh 'alayhi wa-sallam (sallam — end of phrase/pause, vowel dropped), اللؤلؤ المكنون في حكم الإخبار عما سيكون al-Lu'lu' al-maknūn fī ḥukm al-ikhbār 'ammā sa-yakūn (sa-yakūn — end of phrase, dropped).

**Project logic — the "hard" rule:**
- The underlying grammatical fact (verb mood: indicative/subjunctive/jussive, determined by sentence syntax) is **not derivable from bare letters or simple rules.** Requires full syntactic parsing or a diacritization tool attempting case/mood restoration — a known weak point (published benchmark: ~3.29% word-level error without case endings vs. ~12.77% with them included).
- **Division of labor:** the diacritization library supplies the predicted full-form ending; your own code handles only the separate, easier task of **pause detection** (is this word the last one before a sentence/clause boundary, via punctuation/tokenization?) and applies a small deterministic **pausal-shortening transformation** (typically: strip the trailing short vowel) if pausal.
- Decision: v1 will use whatever the diacritization library outputs, accepting its error rate on this feature as a known, documented limitation.

### Rule 14 — Final inflections of nouns and adjectives

**(a)** Vocalic endings (case marks) → **not represented**, **except**:
- preceding pronominal suffixes (e.g., tadrīsihā keeps a vowel before -hā), and
- when the text is in **verse/poetry** (meter requires it).

**(b)** Tanwīn → not represented, except as specified in Rule 12.

**(c)** ة (tā' marbūṭah) → h or t, as specified in Rule 7.

**(d)** Nisbah ending → ī, as specified in Rule 6(c).

**Project logic:** (b), (c), (d) are cross-references to rules already built (12, 7, 6c). The only new piece is (a): **default = drop the case ending** — the *opposite* default from verbs (Rule 13, default = keep). Two exceptions restore it: pronominal-suffix-following position, and verse.

### Rule 15 — Pronouns, pronominal suffixes, and demonstratives

**(a)** Vocalic endings are **retained** in romanization (same default direction as verbs, opposite of nouns): انا وانت anā wa-anta, هذه الحال hādhihi al-ḥāl, مؤلفاته وشروحها mu'allafātuhu wa-shurūḥuhā.

**(b)** At the close of a phrase or sentence, the ending is romanized in its **pausal form**: حياته وعصره ḥayātuhu wa-'aṣruh (same suffix -hu, full form "-tuhu" mid-phrase vs. pausal "-ruh" at phrase-end), توفيق الحكيم، أفكاره، آثاره Tawfīq al-Ḥakīm, afkāruh, āthāruh (list items at pause points, all shortened).

**Project logic:** Same pause-detection mechanism as Rule 13 (fully reusable) — detect sentence/clause-final position, and if pausal, apply a deterministic shortening transformation (e.g., -hu → -h) to whatever full-form ending the diacritization library supplied.

### Rule 16 — Prepositions and conjunctions

**(a)** Final vowels of **separable** prepositions/conjunctions are retained: أن anna, أنه annahu, بين يديه bayna yadayhi. Special cases: مما mimmā, ممن mimman.

**(b)** **Inseparable** prepositions, conjunctions, and other prefixes are connected with what follows by a **hyphen**: به bi-hi, ومعه wa-ma'ahu, لاسلكي lā-silkī.

**Project logic:** This is a closed-set vocabulary classification (prepositions/conjunctions are a small, finite word class) — hard-code a lookup table of which ones are inseparable (bi-, wa-, li-, always hyphenated, fixed invariant prefix form) vs. separable (own standalone word, own vowel per normal noun/verb-adjacent logic). The diacritization step supplies the actual vowel content in both cases; the classification only determines hyphen-vs-space formatting and whether the token needs full word-ending logic applied.

### Rule 17 — The definite article

**(a)** Romanized form **al** is connected with the following word by a **hyphen**: الكتاب الثاني al-kitāb al-thānī, الإتحاد al-ittiḥād, الأصل al-aṣl, الآثار al-āthār.

**(b)** al is **always** romanized al regardless of whether the preceding word ends in a vowel or consonant: الى الآن ilá al-ān, ابو الوفاء Abū al-Wafā', مكتبة النهضة المصرية Maktabat al-Nahḍah al-Miṣrīyah, بالتمام والكمال bi-al-tamām wa-al-kamāl. Exception: لـ + ال → **lil-**: للشربيني lil-Shirbīnī (see also Rule 23).

**(c)** The ل of the article is **always** romanized l, sun letter or not: الحروف الأبجدية al-ḥurūf al-abjadīyah, ابو الليث السمرقندي Abū al-Layth al-Samarqandī.

**Project logic:** Compresses to one idea — **al is a fixed, invariant token**: always hyphenated to what follows (17a), never changes spelling regardless of what precedes it (17b) or what follows it — including sun-letter assimilation, which is ignored entirely in spelling (17c). One hardcoded exception: li- + al- → lil-.

### Rule 18 — Capitalization

**(a)** Standard English capitalization rules apply, **except** the article al is always lower case, in all positions.

**(b)** Diacritics are used with both upper- and lower-case letters: الايجي al-Ījī, الآلوسي al-Ālūsī.

**Project logic:** One exception (al always lowercase) + a formatting confirmation (diacritics survive capitalization).

### Rule 19 — The macron or acute accent for long vowels

Used to indicate **all** long vowels, including those written defectively in Arabic script. Retained over final long vowels even when shortened in pronunciation before hamzat al-waṣl.

إبراهيم ، إبرهيم Ibrāhīm, داؤود ، داؤد Dā'ūd, ابو الحسن Abū al-Ḥasan, رؤوس ru'ūs, ذلك dhālika, على العين 'alá al-'ayn.

**Project logic:** Reinforces Rules 1, 5, 6(a) — never shorten a long vowel just because the Arabic script wrote it "defectively" (missing weak letter, e.g. dagger-alif words like dhālika) or because spoken pronunciation would clip it before hamzat al-waṣl. Once the diacritization tool confirms a vowel is long, always render it long.

### Rule 20 — The Hyphen

Consolidates three already-covered hyphen rules into one index:
**(a)** Connects al to its word (Rule 17a).
**(b)** Connects an inseparable prefix to what follows (Rules 16b, 17b).
**(c)** Connects bin to the following element in personal names written as one word in Arabic (Rule 25).

**Project logic:** No new mechanics — pure index/checklist of where hyphens apply.

### Rule 21 — The Prime ( ʹ )

**(a)** Separates two letters representing distinct consonantal sounds where the combination could otherwise misread as a digraph: أدهم Ad'ham, أكرمتها akramat'hā.

*Explanation:* The romanization system uses digraphs (dh, th, sh, kh, gh) for single Arabic sounds. When a word genuinely has two separate, unrelated consonants sitting next to each other (e.g., د then ه) that would spell out looking like a digraph (dh), the prime disambiguates: "Ad'ham" signals "d, then h, two separate sounds" — not the single dh sound.

**(b)** Marks the use of a letter in its final form when it occurs mid-word: جىقلعه Qal'ah'jī, شيخزاده Shaykh'zādah.

*Explanation:* Some letters have a special shape reserved for word-final position. In compound words (often foreign/Persian/Turkish-influenced names, e.g. Qal'ah + jī, Shaykh + zādah, fused into one continuous written string), the letter that used to be at the end of the *first* original word-part keeps its final-position shape — even though it's no longer visually at the end of the overall combined word. The prime marks this hidden seam: "a word-boundary used to be here, even though the spelling is now continuous." Loosely analogous to how a hyphen in English compounds ("well-known") marks a joined-but-distinct origin, though for a different (visual letter-shape) reason.

**Project logic (both sub-rules):** Low-frequency, mostly name-specific edge cases. Best handled as a small lookup/exception list for known ambiguous sequences (21a) and known compound name patterns (21b), rather than a generally derivable rule.

### Rule 22 — Foreign words in Arabic context

Romanized per standard Arabic rules, not reconstructed to original spelling: جارمانوس Jārmānūs (not Germanos/Germanus), لورد غرانفيل Lūrd Ghrānfīl (not Lord Granville), ايساغوجي Īsāghūjī (not Isagoge). For unindicated short vowels, supply the Arabic vowel nearest the original pronunciation: غرسيا خين Gharsiyā Khayin (not García Jaén).

**Project logic:** No special handling — foreign loanwords flow through the normal rule engine like any Arabic word. Only nuance: short-vowel supply for unvocalized foreign names, same job as the diacritization tool does elsewhere.

### Rule 23 — الله (Allāh) and combinations

الله Allāh, بالله billāh, لله lillāh, بسم الله bismillāh, المستنصر بالله al-Mustanṣir billāh.

**Project logic:** Pure lookup/exception list — fused spellings (double-l pattern) don't derive cleanly from general rules; hardcode them.

### Rule 24 — Specific personal names

طه Ṭāhā, يس/يسن Yāsīn, عمرو 'Amr, بهجت/بهجة Bahjat.

**Project logic:** Pure lookup/exception list of irregular name spellings.

### Rule 25 — ابن/بن → ibn

Both spellings always romanize as **ibn** in normal use: أحمد بن محمد بن أبي الربيع Aḥmad ibn Muḥammad ibn Abī al-Rabī'. Exception: modern (typically North African) names where بن is pronounced **bin**: بن خده Bin Khiddah, بنعبدالله Bin-'Abd Allāh (hyphenated per Rule 20c when fused into one word in Arabic).

**Project logic:** Default ابن/بن → "ibn", with a small exception list for known modern/North African "bin" names.

### Rule 26 — مائة (100), anomalous spelling

مائة is romanized **mi'ah**, not the "expected" reading a naive letter-by-letter application of the rules would produce.

**Project logic:** This connects directly to Rule 4 — the internal alif in مائة is silent/purely orthographic, with no phonetic value, despite sitting right after a fatḥah in a position that would normally trigger elongation (Rule 5). See the full worked breakdown in Part 4 below for exactly how this parses letter-by-letter.

---

## PART 3 — CROSS-CUTTING PROJECT ENGINEERING NOTES

### The two-layer pipeline

1. **Diacritization/vocalization layer** (outsourced, not built from scratch):
   - Input: bare/unvocalized Arabic text.
   - Output: fully vocalized text (all ḥarakāt, shaddah, tanwīn, hamzah, waṣlah, maddah restored).
   - Candidate tools identified: **CAMeL Tools** (Python, NYU Abu Dhabi CAMeL Lab — full morphological analysis/disambiguation/diacritization), **libtashkeel/pylibtashkeel** (Rust/Python neural diacritizer, simple API), **Shakkala/Shakkelha** (deep-learning models, ONNX format), **MADAMIRA** (Java, comprehensive but slower, non-open-source terms).
   - **Known weak point:** case-ending/mood-ending restoration (Rules 13/14) is significantly less accurate than general diacritization — one published benchmark shows ~3.29% word-level error without case endings vs. ~12.77% with them included. Treat this as an accepted, documented limitation for v1.
   - **Idempotency caveat:** untested assumption — feeding already-vocalized text into these tools may cause them to strip and re-predict diacritics rather than preserving existing correct marks. **Recommended guard:** check whether input text already contains diacritic marks (regex/Unicode scan) and skip the diacritizer step if so. Test explicitly before relying on it.

2. **Romanization rule layer** (the actual project — deterministic, rule-based, fully your own logic):
   - Takes fully vocalized text as input.
   - Applies Rules 1–26 mechanically.
   - No ML needed here — a big structured mapping/decision tree once vocalized input is available.

### Recurring classifications your pipeline needs to track per word

- **Defective root?** (root ends in و/ي/ا) — affects Rules 6(b), 11(b2), 12(a).
- **Nisbah adjective?** — affects Rule 6(c), cross-referenced in 14(d).
- **Construct state (iḍāfah)?** — affects Rule 7(b).
- **Adverbial use?** — affects Rules 7(c), 12(b).
- **Definite article vs. other word (for hamzat al-waṣl)?** — affects Rule 9.
- **Pausal position** (last word before sentence/clause boundary)? — affects Rules 13, 14(a) partially, 15(b). Simple, punctuation/tokenization-based detection — NOT dependent on deep grammar.
- **Verb mood / noun case** — the one genuinely hard, non-deterministic classification; outsourced to the diacritization library, accepted at its native error rate.
- **Followed by a pronominal suffix?** — affects Rule 14(a) exception.
- **Verse/poetry context?** — affects Rule 14(a) exception (edge case, low priority for v1).
- **Inseparable prefix (bi-/wa-/li-/al-)?** — affects Rule 16 hyphenation, closed-set lookup.
- **Known irregular/exception word** (الله forms, specific personal names, ابن vs. bin names, مائة, lil-Shirbīnī-type fusions)? — Rules 17b exception, 21, 23, 24, 25, 26 — all best handled as a hardcoded exception dictionary layered on top of the rule engine.

---

## PART 4 — CORE PARSING ALGORITHM: Long Vowels vs. Diphthongs vs. Plain Consonants

Developed through worked examples; this is the mechanical engine underlying Rule 1 (and touching Rules 5, 6a, 19).

### The foundational principle

Every consonant letter needs a vowel mark to be pronounceable. This is universal — true of ب, ت, ك, hamzah, all of them — nothing is special-cased by default.

**ا (alif) is the one true exception:** it never independently carries a short vowel mark. Its only roles are: (1) partnering with a preceding matching fatḥah to form long ā, (2) acting as a seat for hamzah, or (3) supporting waṣlah/maddah.

**و and ي are dual-purpose:** their *default* identity is as ordinary consonants (w and y respectively), and like any consonant they normally carry their own vowel mark (يد yad, وضع waḍa'a). They only stop behaving as an independent consonant in the specific case where they appear **bare** (no vowel mark of their own) immediately after a short vowel mark on the preceding letter.

### The decision tree (applied consonant-by-consonant, scanning left to right through a word)

For each consonant + its vowel mark, check what letter comes next:

1. **Is the next letter و or ي, and is it bare (no vowel mark of its own)?**
   - **No** (it's a different consonant, or it's و/ي but carrying its own vowel mark, or it's the end of the word) → the current consonant is just **itself + its own short vowel**. Nothing combines. Move to the next letter and repeat the check from there. (If the next letter is و/ي *with* its own mark, that's a fresh, independent consonant — evaluate it on its own next pass, not tied to what came before.)
   - **Yes** (bare و or ي follows) → go to step 2.

2. **Does the current short vowel mark match the bare weak letter that follows?** (fatḥah+ا, ḍammah+و, kasrah+ي = matching pairs)
   - **Match** → this is **elongation**. Collapse the pair into a long vowel: ā, ū, or ī (or á for the special word-final alif maqṣūrah case, Rule 6a). Do not separately romanize the weak letter as w/y.
   - **Mismatch** (e.g., fatḥah followed by bare و, or fatḥah followed by bare ي) → this is a **diphthong**: aw or ay (Rule 1c).

3. **Special case — the "dagger alif":** occasionally a word requires elongation (fatḥah → ā) even though the alif that would normally complete the pattern is **not physically written** in the Arabic script at all (a historical scribal shortcut, e.g. ذلك → dhālika). This can't be detected by the adjacency-scanning rule above, since there's no letter there to check — it requires lexical/dictionary knowledge that this specific word takes that pronunciation. Rule 19 confirms: always render these long, regardless of the "defective" (incomplete) spelling.

### Worked example: مائة (mi'ah) — full letter-by-letter trace

This example demonstrates the algorithm plus the Rule 4/Rule 26 silent-alif exception, plus how hamzah's seat can carry its own separate vowel mark.

Letters: **م - ا - ئ - ة**

| Step | Letter | Vowel mark | What happens | Output |
|---|---|---|---|---|
| 1 | م (mīm) | kasrah (short i) | Ordinary consonant + its own vowel. Next letter is ا, which per Rule 4/26 is flagged (via lexical exception) as silent/non-phonetic in this specific word — so no elongation check even applies here; the alif simply contributes nothing. | **mi** |
| 2 | ا (alif) | — | Silent, orthographic-only (Rule 4/26 exception) | *(nothing)* |
| 3 | ئ (hamzah on a yā'-shaped seat) | fatḥah (short a) | The seat-shape itself contributes nothing (Rule 2). The hamzah consonant, medial position, romanizes as **'** (Rule 8a). The seat *also* carries its own separate vowel mark (fatḥah) — same as any consonant needing a vowel — contributing an additional **a** right after the hamzah. | **'a** |
| 4 | ة (tā' marbūṭah) | — | Standalone/indefinite word → **h** (Rule 7a) | **h** |

**Concatenated: mi + 'a + h = mi'ah**

**Key clarification locked in from this example:** hamzah itself is only ever the glottal-stop sound ('), with no vowel of its own. But hamzah, like every consonant, still requires its own vowel mark to be pronounced as a full syllable — and that vowel mark is physically attached to the same seat-letter position as the hamzah symbol (since the seat is the only available "container" at that point in the spelling). So a sequence like **'a** isn't "hamzah having a vowel" in some unique sense — it's just the ordinary next vowel in the word, which happens to be written on hamzah's seat-letter. This is the same pattern seen in مسألة (mas'alah, Rule 8a) — 'alah, not just 'lah.

**Contrast — the "naive," incorrect reading if Rule 4/26's exception were not known:** treating the alif as a normal elongation partner (fatḥah on mīm + following alif = matching pair → elongate) would incorrectly produce **mā** instead of **mi** for the first syllable, giving the wrong result **mā'ah**. This is exactly why Rule 26 flags مائة as anomalous: the general elongation algorithm alone gets it wrong here, and it must be hardcoded as a lexical exception.

---

## STATUS

**Completed in full:** All 26 rules read, explained, and discussed in depth, including the underlying parsing mechanics for long vowels/diphthongs/consonants (Part 4) and a fully worked exception case (مائة).

**Key corrected misunderstandings from this session (for accuracy going forward):**
- Rule 9 (hamzat al-waṣl) is **not** about sentence-start/pause/connected-speech position. It is purely: article → a, all other words → i, regardless of position or hyphenation.
- The dotted circle (◌) in rule notation (e.g., ّ◌, ˜◌) is not a real letter — it's a placeholder showing where a diacritic sits on top of whatever real letter is present in an actual word.
- Dotless ى (alif maqṣūrah) and dotted ي (yā') are distinct letters with distinct rule sets — only dotted ي participates in the shaddah-related rules (6b/6c/11b2); dotless ى is exclusively Rule 6(a).
- "Fatḥah" = short a vowel mark (not a typo-worthy new term — same category as ḍammah/kasrah).

**Next planned step:** begin building the deterministic romanization engine. Plan: (1) select and test a diacritization library, including an idempotency check for already-vocalized input; (2) implement Part 4's parsing algorithm as the core vowel/consonant classifier; (3) layer Rules 2–21's contextual logic on top; (4) build a hardcoded exception dictionary for Rules 17(b) exception, 21, 23, 24, 25, 26; (5) accept verb-mood/noun-case prediction error as a known limitation inherited from the diacritization library, with pause-detection and pausal-shortening handled locally per Rules 13/15.
