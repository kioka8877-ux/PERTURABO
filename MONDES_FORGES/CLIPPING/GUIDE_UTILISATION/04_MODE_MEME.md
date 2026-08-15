# 04_MODE_MEME — Guide complet

> Le mode **logo / meme** : tu fournis un **mot-clé** → F00 scanne la viralité
> sur TOUTES les sources (YouTube, Google Trends, RSS, Reddit, Twitter… ce qui
> est viral US et ce qui marchera en Shorts) → le forge sort **5 angles** avec
> émotion → F04 forge le texte de chaque angle → F05 assemble le pack dans
> EXPORT → **OMNIS_WATCH** charge ce guide pour le montage et sort la vidéo.
>
> Doctrine issue de la dissection visuelle du démon @zdak (Kimi K3, rapport
> `answers/question-2026-08-15-02.md` du repo Scriptorum).
>
> ⚠️ **Ce guide EST le contrat de montage.** Le pack meme référence
> `montage_guide_ref: "GUIDE_UTILISATION/04_MODE_MEME.md"` — OMNIS_WATCH le
> charge pour rendre la vidéo.

---

## 🎯 Le but en 3 lignes

1. Tu donnes un **mot-clé** (ex : `westbrook retirement`) → le forge sait ce qui
   est viral dessus et pourquoi.
2. Le forge sort **5 packs** (un par angle) : **titre en haut** (si nécessaire)
   + **fake tweet** (max 3 lignes) + **texte d'émotion** (milieu, max 4 mots)
   + **émotion** + **durée fourchette**.
3. **OMNIS_WATCH** monte chaque vidéo selon la **doctrine 6 couches** ci-dessous
   et poste → vues suivies par F06.

---

## 🧾 Les inputs (ce que TU fournis)

| Fichier | Rôle | Exemple |
|---|---|---|
| `keyword.txt` | Le **mot-clé** du siège | `westbrook retirement` |
| `directive.md` | Le brief de la campagne | `MEME MODE: keyword ...` |

> ⚠️ **Différence clé avec le mode informatif** : il n'y a **ni F01 ni F03**.
> Aucun clip n'est fourni, aucun asset n'est chassé, aucun segment n'est
> sélectionné. F00 ne **télécharge** rien : il scanne les **stats** (vues,
> tendances, demandes) pour savoir ce qui est viral.

---

## 🗺️ Le chemin complet — les gates avec commandes EXACTES

### Étape 0 — Ouvrir le siège

```bash
cd MONDES_FORGES/CLIPPING/ORCHESTRATOR/CODEBASE
python3 orchestrator.py --start-siege
```

---

### 🚪 GATE 1 — F00 : scan de viralité par mot-clé (multi-sources)

**Frégate** : `F00_CAPTEURS` — scanne **TOUTES** les sources, SANS télécharger.

```bash
cd ../../F00_CAPTEURS/CODEBASE
python3 capteurs.py --scan-meme --keyword westbrook --sources youtube trends rss reddit --max-videos 8
```

**Sortie** : `F00_CAPTEURS/OUT/meme_virality_<keyword>.json` (+ `.md`)

| Champ | Signification |
|---|---|
| `keyword` | le mot-clé fourni |
| `viral_evidence` | ce qui est viral US pour ce mot-clé (URLs réelles + stats) |
| `sources_scanned` | les sources effectivement interrogées |
| `signals` | vues YT, tendance, demande, fraîcheur, etc. (réelles) |
| `recommended_niche` | la niche la plus porteuse (synthèse) |

**Ce que F00 ne fait PAS** : télécharger la vidéo, fournir un clip, inventer
une stat. `signal_vues_youtube` = stats réelles de l'API YouTube.

**Validation** :
```bash
cd ../../ORCHESTRATOR/CODEBASE
python3 orchestrator.py --gate 1 --decision valide --notes "viralité multi-sources pour keyword OK, aucun clip téléchargé"
```

---

### 🚪 GATE 2 — Les angles (ANGLESMITH, mode meme)

**Frégate** : `F02_TYRANT_CAMP` (ANGLESMITH) — forge 5 angles, **règle anti-spam**.

```bash
cd ../../F02_TYRANT_CAMP/CODEBASE
python3 anglesmith.py --auto --n-angles 5 --sub-mode meme --finalize
```

**Sortie** : `F02_TYRANT_CAMP/OUT/angles.json`

Chaque angle porte en plus du schéma standard :
| Champ | Règle |
|---|---|
| `emotion` | l'émotion de l'angle (ex : poignant, drôle, choc, émerveillé, tendu) |
| `duration_sec_range` | fourchette conseillée (défaut 5-7s) |

**Règle anti-spam sur les émotions** : une même émotion ne peut couvrir que
**2 angles max** sur les 5 — les 3 autres doivent être différentes. La règle
de voisinage est douce (pas 2 mêmes émotions côte à côte).

**Validation** :
```bash
cd ../../ORCHESTRATOR/CODEBASE
python3 orchestrator.py --gate 2 --decision valide --notes "5 angles meme forgés, anti-spam émotions OK"
```

---

### 🚪 GATE 3 — Les textes (F04 COPYWRITER, mode meme)

**Frégate** : `F04_COPYWRITER` — forge les 5 text_payloads meme.

Pour CHAQUE angle (A01 → A05) :

```bash
cd ../../F04_COPYWRITER/CODEBASE
python3 copywriter.py --setup-context --angle A01 --sub-mode meme
python3 copywriter.py --generate --angle A01 --sub-mode meme   # AVEC clé premium
python3 copywriter.py --ordonnance --angle A01 --auto-ord
python3 copywriter.py --finalize --angle A01
```

**Sortie** : `F04_COPYWRITER/OUT/text_payload_A0X.json`

| Champ du payload | Règle verrouillée |
|---|---|
| `title` (titre en haut) | **si nécessaire**, ≤ 6 mots, jamais de clickbait vide |
| `tweet_text` (fake tweet) | **max 3 lignes**, format post X/Twitter |
| `reaction_text` (milieu) | **max 4 mots**, l'émotion en texte |
| `emotion` | l'émotion de l'angle (ajustable par l'opérateur) |
| `duration_sec_range` | fourchette (défaut 5-7s) |

> 🧙 Si la clé premium est absente : `--generate --oracle` → l'Oracle (l'assistant)
> forge `F04_COPYWRITER/OUT/text_payload_raw_<angle>.json`, puis relance
> `--generate --oracle` (détecte le raw).

**Validation** :
```bash
cd ../../ORCHESTRATOR/CODEBASE
python3 orchestrator.py --gate 3 --decision valide --notes "5 textes meme validés (tweet<=3 lignes, reaction<=4 mots)"
```

---

### 🚪 GATE 4 — Le pack assemblé → EXPORT → OMNIS_WATCH

**Frégate** : `F05_PACKAGER`

```bash
cd ../../F05_PACKAGER/CODEBASE
python3 packager.py --assemble --sub-mode meme --finalize
```

**Sortie** : `F05_PACKAGER/OUT/production_pack_logo.json` (mode meme)

Le pack contient : `sub_mode: "meme"`, `meme_source.keyword`, `meme_source.montage_guide_ref`,
les textes verrouillés + `emotion` + `duration_sec_range` par vidéo.

**Expédition** :

```bash
cd MONDES_FORGES/CLIPPING
cp F05_PACKAGER/OUT/production_pack_logo.json EXPORT/production_pack_meme.json
```

**Validation** :
```bash
cd ../../ORCHESTRATOR/CODEBASE
python3 orchestrator.py --gate 4 --decision valide --notes "pack meme conforme → OMNIS_WATCH (monte via 04_MODE_MEME.md)"
```

---

## 🎬 LA DOCTRINE DE MONTAGE EN 6 COUCHES (ce que OMNIS_WATCH lit dans CE guide)

> Source : dissection visuelle du démon @zdak (2.42M abonnés, 9.56 Mds vues).
> La vidéo cible "This Teacher MIGHT Be Picasso" : 5.6s, zéro dialogue, muet-compréhensible.

### Couche 1 — SETUP / FAUX POST (quart haut, fixe)
- Le faux post (tweet) est affiché dans le **quart supérieur**, **fixe** (pas d'animation).
- **Max 1.5 ligne** visible. Mots-clés **colorés** : vert (valeur) / rouge (danger).
- Le titre en haut (si présent) est court : max 1.5 ligne.

### Couche 2 — PREUVE VISUELLE (card dès la première frame)
- Une **card lumineuse** (le "proof") apparaît dès la **frame 1** — rien d'attendu :
  tout est visible immédiatement.
- Card = l'image/le visuel qui prouve le post.

### Couche 3 — LABEL NARRATIF (un seul mot change)
- Format : `[sujet] at [A]:` → `[sujet] at [B]:`
- **Un seul mot change** entre la version A et la version B (~50% par version).
- Exemple démon : "this teacher at school:" → "this teacher at home:" — tout le
  contexte est posé en changeant UN mot.

### Couche 4 — RÉACTEUR ÉMOTIONNEL (contraste extrême)
- 2 clips d'une **même œuvre pop-culture** au contraste extrême (ex : All Quiet —
  un homme pleure → le même homme danse).
- C'est la **méta-blague** : le réacteur visuel exprime l'émotion du post.

### Couche 5 — TRANSITION-PIVOT (flash/cut sec + impact sonore)
- La bascule A→B se fait par **flash ou cut sec** + **impact sonore**.
- Positionné à **50-55% du runtime** (≈ 3s sur 5.6s).

### Couche 6 — WATERMARK (semi-transparent, bas-gauche)
- Watermark du logo en **semi-transparent**, **bas-gauche**.

### Règles d'assemblage (non négociables)
| Règle | Valeur |
|---|---|
| Durée | **5-7s max** |
| Premier visuel | **tout visible dès frame 1** |
| Nombre de bascules | **une seule** (A→B) |
| Son | muet-compréhensible (impact sonore OK) |
| Mouvement | **un seul objet en mouvement** par moment |
| Boucle | boucle invisible en bonus |
| Ratio | 9:16 (1080×1920) |
| Logo | image transparente campagne, bas-gauche |

---

## ⚙️ Les règles verrouillées (garde-fous mode meme)

| Règle | Valeur |
|---|---|
| Titre en haut | **si nécessaire**, ≤ 6 mots |
| Fake tweet | **max 3 lignes** |
| Texte d'émotion (milieu) | **max 4 mots** |
| Émotion anti-spam | une émotion = **2 angles max** sur les 5 |
| Durée | **5-7s** |
| F01 / F03 | **SKIP** (pas de timecodes, pas de segments) |
| Pas de clip à télécharger | F00 scanne les stats, jamais le contenu |
| URL de meme dans le pack | **interdit** (les sources restent dans `meme_source.virality_scan`) |

---

## ✅ Checklist rapide

- [ ] `keyword.txt` déposé · [ ] Gate 1 : viralité multi-sources (0 clip téléchargé)
- [ ] Gate 2 : 5 angles, anti-spam émotions OK
- [ ] Gate 3 : tweet ≤ 3 lignes, reaction ≤ 4 mots, titre ≤ 6 mots si présent
- [ ] Gate 4 : pack `sub_mode: meme` + `montage_guide_ref` + copié dans EXPORT/

---

👉 **Prochaine étape après le siège** : `F06_TRACKER` — `python3 tracker.py --post`
une fois les vidéos publiées (suit vues 1h/24h, payout, learnings).
