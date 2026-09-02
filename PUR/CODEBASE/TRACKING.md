# TRACKING.md — PUR Mode
> Script dédié au mode PUR : extraction de moments viraux depuis des podcasts/long-forms.
> Connecté au réseau CLIPPING via ARCHIVUM et EXPORT.
---

## 🎯 Rôle du PUR

Le mode PUR extrait des **moments viraux** depuis des **podcasts/long-forms** et produit des **clips courts** (15-60s) avec :
- Sélection scoringuée des segments
- Hooks psychologiques
- B-roll scoringué
- Anti-detection intégrée
- Instructions de montage complètes

## 📂 Architecture

```
PUR/
├── CODEBASE/
│   ├── pur.py                    ← Script principal
│   ├── libs/
│   │   ├── transcript_analyzer.py ← Analyse le transcript
│   │   ├── broll_scorer.py       ← Scoring B-roll
│   │   ├── anti_detection.py     ← Instructions anti-détection
│   │   └── montage_builder.py    ← Assemble les instructions
│   ├── TRACKING.md               ← Ce fichier
│   └── requirements_pur.txt
├── IN/                           ← Inputs (transcript, directive, B-roll)
├── OUT/                          ← Outputs (production_pack_pur.json)
└── TRACKING/
```

## 🔄 Connexions au réseau

| Connexion | Usage |
|-----------|-------|
| `ARCHIVUM/montage/patterns/` | Patterns de style, scoring, anti-detection |
| `ARCHIVUM/montage/sources/` | Transcripts collectés |
| `ARCHIVUM/broll/` | Bibliothèque B-roll |
| `ARCHIVUM/learnings/` | Learnings passés |
| `F02/` (import) | Logique de verdict |
| `F03/` (import) | Logique de sélection |
| `F04/` (import) | Logique de copywriting |
| `F05/` (import) | Logique d'assemblage |
| `EXPORT/` | Export du pack final |

## ⚔️ Les 4 Gates

### Gate 1 — Verdict (F02)
**Input** : transcript.json + directive.md
**Output** : campaign_verdict.json (GO/NO-GO)
**Commande** : `python3 pur.py --verdict`

### Gate 2 — Sélection segment (F03)
**Input** : transcript.json + verdict
**Output** : segment.json (5 moments scoringués)
**Commande** : `python3 pur.py --select`

### Gate 3 — Textes + hooks (F04)
**Input** : segment.json + style
**Output** : text_payload.json (titres, captions, B-roll prompts)
**Commande** : `python3 pur.py --text --style ranking`

### Gate 4 — Assemblage pack PUR (F05 + F06)
**Input** : segment + textes + B-roll + anti-detection
**Output** : production_pack_pur.json
**Commande** : `python3 pur.py --assemble --style blur --finalize`

### Gate 5 — Enrichissement Split Scene (F06_DIRECTOR)
**Input** : production_pack_pur.json (style=split_scene)
**Output** : production_pack_pur.json enrichi avec instructions split_scene
**Commande** : `python3 pur.py --direct`
**Note** : Gate 5 spécifique au mode split_scene — layout, sous-layout, broll fullscreen

## 📊 Styles supportés

| Style | Description | B-roll | Gate 5 |
|-------|-------------|--------|--------|
| `ranking` | 5 moments, countdown 5→1 | 4-6 par clip | Non |
| `reframing` | Zoom simple 9:16 | 1-3 par clip | Non |
| `blur` | Dupliquer + blur + centrer | 1-3 par clip | Non |
| `split_scene` | Podcast haut + titre centre + bas variable | Full-screen overlay | **Oui** |

## 🛡️ Anti-detection

Chaque clip doit avoir :
- Au moins 1 traitement visuel (mirror OU zoom OU crop)
- Au moins 1 traitement audio (musique OU SFX OU pitch)
- Zoom invisible quasi permanent
- 1-2 SFX aux moments clés

## 🎬 B-roll

Scoring par segment :
- visual_trigger : +3
- context_gap : +3
- enumeration : +2
- description_word : +2
- dead_air : +2
- emotion_peak : +1 (PAS de B-roll)

Minimum 5 secondes entre chaque B-roll.

## ⚠️ Hérésies interdites

1. Jamais de clip sans anti-detection
2. Jamais de B-roll sur le hook (0-3s)
3. Jamais de B-roll sur l'emotion_peak
4. Jamais de clip < 10 secondes
5. Jamais de clip > 60 secondes (sauf ranking)
6. Jamais de push sans validation du Warsmith

## 📈 Statut

| Élément | Statut |
|---------|--------|
| Structure | ✅ Créée |
| Patterns ARCHIVUM | ✅ En place (7 fichiers + style_split_scene) |
| Guides | ✅ En place (11_MODE_PUR + 12_NOTE_TECHNIQUE + _PIEGES_APPRIS) |
| Scripts Python | ✅ En place (pur.py + 4 libs, 5 gates) |
| Split Scene | ✅ Implémenté (pattern + pur.py + docs) |
| Tests | ⏳ En attente |
