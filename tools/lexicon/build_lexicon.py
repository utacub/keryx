# Builds the word-prediction lexicons of UTAC Keryx (lex/<lang>.json), one per app language.
# GPL-3.0-or-later for this script; the data files it writes keep the licences of their sources (see SOURCES).
#
# Each file holds:
#   words  : the vocabulary, most frequent first, "\n"-joined (lower case, or the usual casing for words such as "I"
#            or place names when the treebank shows they are normally capitalised)
#   zipf   : Zipf frequency x 10 of each word (log10 of occurrences per billion words, x 10, rounded)
#   next   : for word-pair prediction: {"<index of w1>": [total, i2, count2, i3, count3, ...]}, index -1 = sentence start
#   src    : short attribution text shown in Keryx > Information
#
# Sources (all downloaded from raw.githubusercontent.com or bundled in the wordfreq package):
#   ca, es, en, fr word frequencies: wordfreq 3.x large lists (Speer, 2022), data CC BY-SA 4.0
#   eu, gl word frequencies: FrequencyWords 2018 (Hermit Dave, from OpenSubtitles2018), content CC BY-SA 4.0
#   word pairs: Universal Dependencies treebanks, train + dev only (test kept apart for evaluation):
#     ca UD_Catalan-AnCora (CC BY 4.0), es UD_Spanish-AnCora (CC BY 4.0), en UD_English-EWT (CC BY-SA 4.0),
#     fr UD_French-Rhapsodie + UD_French-ParisStories (both CC BY-SA 4.0, spoken French).
#   eu and gl have no freely licensed treebank compatible with CC BY-SA (BDT and CTG are non-commercial),
#   so they ship without word pairs: next-word prediction there comes only from what the person writes.
#
# Usage: pip install wordfreq; python3 build_lexicon.py <sources dir> <output dir>
#   The sources dir must hold the .conllu files and hd_eu.txt / hd_gl.txt (see fetch() for the URLs).
import sys, os, json, re, math, collections, unicodedata, urllib.request

SRC, OUT = sys.argv[1], sys.argv[2]
UD = 'https://raw.githubusercontent.com/UniversalDependencies'
TREEBANKS = {
    'ca': [('UD_Catalan-AnCora', 'ca_ancora')],
    'es': [('UD_Spanish-AnCora', 'es_ancora')],
    'en': [('UD_English-EWT', 'en_ewt')],
    'fr': [('UD_French-Rhapsodie', 'fr_rhapsodie'), ('UD_French-ParisStories', 'fr_parisstories')],
    'eu': [], 'gl': [],
}
SOURCES = {
    'ca': 'wordfreq (Speer, 2022), CC BY-SA 4.0; UD Catalan-AnCora, CC BY 4.0',
    'es': 'wordfreq (Speer, 2022), CC BY-SA 4.0; UD Spanish-AnCora, CC BY 4.0',
    'en': 'wordfreq (Speer, 2022), CC BY-SA 4.0; UD English-EWT, CC BY-SA 4.0',
    'fr': 'wordfreq (Speer, 2022), CC BY-SA 4.0; UD French-Rhapsodie and French-ParisStories, CC BY-SA 4.0',
    'eu': 'FrequencyWords 2018 (Hermit Dave, OpenSubtitles2018), CC BY-SA 4.0',
    'gl': 'FrequencyWords 2018 (Hermit Dave, OpenSubtitles2018), CC BY-SA 4.0',
}
VOCAB = 60000
MAX_NEXT = 40          # successors kept per word
ELIDING = {'ca': True, 'fr': True}
# wordfreq splits elisions (l'home -> l + home); Keryx keeps the elided form with its apostrophe as a context word.
ELIDED = {'ca': {'l', 'd', 's', 'm', 't', 'n'},
          'fr': {'l', 'd', 'j', 'c', 'qu', 'n', 's', 'm', 't', 'jusqu', 'lorsqu', 'puisqu', 'quoiqu'}}
# hesitations of spoken French that should never be proposed
FILLERS = {'fr': {'euh', 'mh', 'hum', 'bah', 'ben', 'hein', 'heu', 'mm', 'mhm', 'ah', 'oh'}}
WORD = re.compile(r"^[^\W\d_](?:[^\W\d_]|['·-](?=[^\W\d_]))*$")

def fetch():
    for lang, tbs in TREEBANKS.items():
        for repo, stem in tbs:
            for split in ('train', 'dev', 'test'):
                path = os.path.join(SRC, f'{stem}-{split}.conllu')
                if not os.path.exists(path):
                    urllib.request.urlretrieve(f'{UD}/{repo}/master/{stem}-ud-{split}.conllu', path)
    for lang in ('eu', 'gl'):
        path = os.path.join(SRC, f'hd_{lang}.txt')
        if not os.path.exists(path):
            urllib.request.urlretrieve(f'https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/{lang}/{lang}_50k.txt', path)

def clean(w):
    return unicodedata.normalize('NFC', w.replace('’', "'"))

def sentences(lang, splits=('train', 'dev')):
    """Surface tokens of each sentence (multiword tokens such as 'del' kept whole, their parts skipped)."""
    for repo, stem in TREEBANKS[lang]:
        for split in splits:
            path = os.path.join(SRC, f'{stem}-{split}.conllu')
            if not os.path.exists(path):
                continue
            toks, skip = [], 0
            for line in open(path, encoding='utf-8'):
                line = line.rstrip('\n')
                if not line:
                    if toks:
                        yield toks
                    toks, skip = [], 0
                    continue
                if line.startswith('#'):
                    continue
                cols = line.split('\t')
                if '-' in cols[0]:
                    a, b = cols[0].split('-'); skip = int(b) - int(a) + 1; toks.append(clean(cols[1])); continue
                if '.' in cols[0]:
                    continue
                if skip:
                    skip -= 1; continue
                toks.append(clean(cols[1]))
            if toks:
                yield toks

def join_tokens(lang, toks):
    """Glue English clitics (do + n't, I + 'm) so tokens look like what people type."""
    if lang != 'en':
        return toks
    out = []
    for t in toks:
        if out and (t.lower() in ("n't", "'m", "'s", "'re", "'ve", "'ll", "'d")):
            out[-1] = out[-1] + t
        else:
            out.append(t)
    return out

def unigrams(lang):
    if lang in ('eu', 'gl'):
        rows = []
        for line in open(os.path.join(SRC, f'hd_{lang}.txt'), encoding='utf-8'):
            w, n = line.rsplit(' ', 1); rows.append((clean(w).lower(), int(n)))
        total = sum(n for _, n in rows)
        return [(w, math.log10(n / total * 1e9)) for w, n in rows]
    import wordfreq
    out = []
    for w in wordfreq.iter_wordlist(lang, 'large'):
        out.append((clean(w), wordfreq.zipf_frequency(w, lang, 'large')))
        if len(out) >= VOCAB * 3:
            break
    return out

def build(lang):
    rows, seen, words, zipf = unigrams(lang), set(), [], []
    for w, z in rows:
        if w in ELIDED.get(lang, ()):
            w = w + "'"
        elif not WORD.match(w) or w in seen:
            continue
        if w in seen:
            continue
        if len(w) == 1 and z < 5.0:     # stray letters
            continue
        seen.add(w); words.append(w); zipf.append(max(0, min(99, round(z * 10))))
        if len(words) >= VOCAB:
            break
    # usual casing and word pairs from the treebanks
    caps, low, pairs, starts = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    for toks in sentences(lang):
        toks = join_tokens(lang, toks)
        prev = None
        for i, t in enumerate(toks):
            if t.lower() in FILLERS.get(lang, ()):
                continue
            if WORD.match(t) or (ELIDING.get(lang) and re.match(r"^[^\W\d_]{1,3}'$", t)):
                l = t.lower()
                if i > 0 and prev is not None:
                    (caps if t[:1].isupper() else low)[l] += 1
                if prev is None and i == 0:
                    starts[l] += 1
                elif prev is not None:
                    pairs[(prev, l)] += 1
                prev = l
            else:
                prev = None if t not in (',', ';', ':') else None
    index = {w: i for i, w in enumerate(words)}
    for i, w in enumerate(words):
        if len(w) > 1 and caps[w] >= 3 and caps[w] > 4 * low[w]:
            # proper nouns, "I": the usual written form
            words[i] = w[:1].upper() + w[1:] if w != 'i' else 'I'
    nxt = collections.defaultdict(list); totals = collections.Counter()
    for (a, b), n in pairs.items():
        if a in index and b in index:
            totals[a] += n
            if n >= 2:
                nxt[a].append((n, b))
    for b, n in starts.items():
        if b in index:
            totals['<s>'] += n
            if n >= 2:
                nxt['<s>'].append((n, b))
    nxt_out = {}
    for a, lst in nxt.items():
        lst.sort(reverse=True)
        key = '-1' if a == '<s>' else str(index[a])
        row = [totals[a]]
        for n, b in lst[:MAX_NEXT]:
            row += [index[b], n]
        nxt_out[key] = row
    data = {'v': 1, 'lang': lang, 'src': SOURCES[lang], 'words': '\n'.join(words), 'zipf': zipf, 'next': nxt_out}
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f'{lang}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print(lang, len(words), 'words', len(nxt_out), 'contexts', os.path.getsize(path) // 1024, 'KB')

if __name__ == '__main__':
    os.makedirs(SRC, exist_ok=True)
    fetch()
    for lang in TREEBANKS:
        build(lang)
