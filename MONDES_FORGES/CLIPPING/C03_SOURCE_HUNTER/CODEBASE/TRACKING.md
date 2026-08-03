# C03_SOURCE_HUNTER — TRACKING.md

> *"On ne pompe pas le fer au hasard. On choisit la seam, on trace la veinule."*
> *Frégate de sélection des sources. Le Warsmith valide quoi chasser avant la coupe.*

---

## RÔLE

C03_SOURCE_HUNTER est la **frégate de sélection**. À la Porte 3, elle prend les N angles forgés par F02_ANGLESMITH à la Porte 2 et identifie, pour chaque angle, **quelle vidéo longue des assets de la campagne** est la meilleure source à clipper — ainsi que les **segments pertinents** dans cette vidéo.

Elle produit un `source_specimen.json` enrichi (un par angle) qui alimente directement C04_COPYWRITER (qui forge le texte) et C05_PACKAGER (qui emballe le pack).

---

## INPUTS

| Input | Source | Format | Obligatoire |
|---|---|---|---|
| `angles.json` | F02_ANGLESMITH (Porte 2) | JSON | ✅ |
| `source_specimen.json` (assets) | C01_SCOUT | JSON | ✅ |
| `verdict.json` (squelette + blue_ocean) | C02_TYRANT_CAMP | JSON | ✅ |
| `platform_target` | Warsmith | string | ✅ |
| `market_target` | Warsmith | string | ✅ |
| Transcripts des assets | C01_SCOUT (chemin transcript dans ARCHIVUM/campaign/) | JSON | ✅ |

---

## OUTPUTS

### Pour chaque angle, un `OUT/source_specimen_<angle_id>.json`

```json
{
  "campaign_id": "...",
  "angle_id": "...",
  "asset_selected": {
    "asset_id": "...",
    "url": "...",
    "title": "...",
    "duration_sec": N,
    "rationale": "Pourquoi cet asset est le meilleur carrier pour cet angle"
  },
  "suggested_segments": [
    {
      "start_sec": N,
      "end_sec": N,
      "duration_sec": N,
      "rationale": "Ce segment porte l'émotion/engagement que l'angle réclame",
      "extracted_text_snippet": "..."
    }
  ],
  "blue_ocean_reframe_applied": true|false,
  "platform_fit": <0-10>,
  "market_fit": <0-10>,
  "check_in_iw_custos": "<ISO8601>"
}
```

### Autres
- `OUT/source_summary.md` — synthèse lisible Warsmith : "Pour les N angles, voici les sources et segments"

---

## MÉTHODE

### Sélection d'asset par angle
Pour chaque angle, C03 cherche dans `assets[]` (de C01) la vidéo dont le **contenu transcriptuel** match le `reframe_dim` + l'`emotion_mode` de l'angle. L'IRON fait l'analyse qualitative via le transcript, le Warsmith valide le choix.

### Suggested segments
Pour chaque asset sélectionné, C03 propose des **fenêtres temporelles** (start_sec, end_sec) pertinentes pour l'angle. Ces segments sont des **directives** (pas des coupes — la coupe reste à D-F02 d'OMNIS_WATCH). Chaque segment a une `rationale` qualitative.

Règle de durée :
- `clip_max_duration` vient de `platform_generator/{plateforme}_profile.md`
- `clip_min_duration` vient de la même source
- Chaque segment doit être dans la fourchette `[min, max]` de la plateforme cible

### Blue ocean reframe
Si l'angle est en zone océan bleu (cf. `verdict.json`), C03 applique le re-ciblage dans le choix du segment : cherche le segment dont le **sens peut être re-frame** par le texte (cf. `reframe_dim`).

---

## PATTERN D'EXÉCUTION

Pattern **3-phases standard** :

```
Phase 1 : prepare
   python source_hunter.py --prepare --angles ../C02/OUT/angles.json
   → génère IN/source_hunter_prompt.json

Phase 2 : IRON (Claude sandbox)
   Le Warsmith copie-colle le prompt.
   L'IRON lit les transcripts des assets (depuis ARCHIVUM/campaign/),
   les match avec chaque angle, sélectionne asset + segments.
   → Écrit OUT/source_specimen_<angle_id>.json (un par angle)

Phase 3 : finalize
   python source_hunter.py --finalize
   → Valide cohérence + check-in IW_CUSTOS.py
   → Met à jour liber_clipping.json (statut C03 = done, N specimens prêts pour C04)
```

---

## CONTRATS RÉFÉRENCÉS

- `ARCHIVUM/rules/clipping_rules.md` — strict source, jamais sortir des assets
- `ARCHIVUM/platform_generator/{plateforme}_profile.md` — format + durations
- `ARCHIVUM/market_generator/{marché}.md` — contraintes culturelles
- `ARCHIVUM/angles/angle_patterns.json` — patterns d'angles
- `ARCHIVUM/angles/angle_performance.json` — perf passée par angle (poids nul si < 50)
- `CONTRACTS/anti_bullshit.md` (liens core)

---

## DÉPENDANCES

- **Amont** : C01_SCOUT (assets), C02_TYRANT_CAMP (verdict + angles context), F02_ANGLESMITH (angles forgés)
- **Downstream** : C04_COPYWRITER (utilise `suggested_segments` et segments pour forge le texte), C05_PACKAGER (emballe les N specimens + les N text_payloads en N packs)

---

## HÉRÉSIES

- ❌ Sélectionner un asset qui n'est pas dans `source_specimen.assets[]` de C01
- ❌ Couper la vidéo (cela est le boulot de D-F02 dans OMNIS_WATCH — pas C03)
- ❌ Suggérer des segments dont la durée sort de la fourchette plateforme
- ❌ Ignorer `blue_ocean_reframe_applied` quand l'angle est en zone océan bleu

---

## STATUT

| Phase | État | Notes |
|---|---|---|
| Arborescence créée | ✅ | |
| TRACKING.md rédigé | ✅ | Ce fichier |
| Code Python | ❌ | À implémenter |
| `source_hunter.py` | ❌ | Wrapper orchestrateur |
| `libs/transcript_loader.py` | ❌ | Charge transcripts depuis ARCHIVUM/campaign/ |
| `libs/segment_matcher.py` | ❌ | Match angle ↔ segment transcript |
| `libs/duration_guard.py` | ❌ | Vérification min/max par plateforme |
| `requirements_c03.txt` | ❌ | |

*Fer au-dedans, Fer au-dehors.*
