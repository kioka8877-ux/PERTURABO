# F03_SOURCE_HUNTER â€” TRACKING.md

> *"On ne pompe pas le fer au hasard. On choisit la seam, on trace la veinule."*
> *FrÃ©gate de sÃ©lection des sources. Le Warsmith valide quoi chasser avant la coupe.*

---

## RÃ”LE

F03_SOURCE_HUNTER est la **frÃ©gate de sÃ©lection**. Ã€ la Porte 3, elle prend les N angles forgÃ©s par ANGLESMITH Ã  la Porte 2 et identifie, pour chaque angle, **quelle vidÃ©o longue des assets de la campagne** est la meilleure source Ã  clipper â€” ainsi que les **segments pertinents** dans cette vidÃ©o.

Elle produit un `source_specimen.json` enrichi (un par angle) qui alimente directement F04_COPYWRITER (qui forge le texte) et F05_PACKAGER (qui emballe le pack).

---

## INPUTS

| Input | Source | Format | Obligatoire |
|---|---|---|---|
| `angles.json` | ANGLESMITH (Porte 2) | JSON | âœ… |
| `source_specimen.json` (assets) | F01_SCOUT | JSON | âœ… |
| `verdict.json` (squelette + blue_ocean) | F02_TYRANT_CAMP | JSON | âœ… |
| `platform_target` | Warsmith | string | âœ… |
| `market_target` | Warsmith | string | âœ… |
| Transcripts des assets | F01_SCOUT (chemin transcript dans ARCHIVUM/campaign/) | JSON | âœ… |

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
      "rationale": "Ce segment porte l'Ã©motion/engagement que l'angle rÃ©clame",
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
- `OUT/source_summary.md` â€” synthÃ¨se lisible Warsmith : "Pour les N angles, voici les sources et segments"

---

## MÃ‰THODE

### SÃ©lection d'asset par angle
Pour chaque angle, C03 cherche dans `assets[]` (de C01) la vidÃ©o dont le **contenu transcriptuel** match le `reframe_dim` + l'`emotion_mode` de l'angle. L'IRON fait l'analyse qualitative via le transcript, le Warsmith valide le choix.

### Suggested segments
Pour chaque asset sÃ©lectionnÃ©, C03 propose des **fenÃªtres temporelles** (start_sec, end_sec) pertinentes pour l'angle. Ces segments sont des **directives** (pas des coupes â€” la coupe reste Ã  D-F02 d'OMNIS_WATCH). Chaque segment a une `rationale` qualitative.

RÃ¨gle de durÃ©e :
- `clip_max_duration` vient de `platform_generator/{plateforme}_profile.md`
- `clip_min_duration` vient de la mÃªme source
- Chaque segment doit Ãªtre dans la fourchette `[min, max]` de la plateforme cible

### Blue ocean reframe
Si l'angle est en zone ocÃ©an bleu (cf. `verdict.json`), C03 applique le re-ciblage dans le choix du segment : cherche le segment dont le **sens peut Ãªtre re-frame** par le texte (cf. `reframe_dim`).

---

## PATTERN D'EXÃ‰CUTION

Pattern **3-phases standard** :

```
Phase 1 : prepare
   python source_hunter.py --prepare --angles ../F02/OUT/angles.json
   â†’ gÃ©nÃ¨re IN/source_hunter_prompt.json

Phase 2 : IRON (Claude sandbox)
   Le Warsmith copie-colle le prompt.
   L'IRON lit les transcripts des assets (depuis ARCHIVUM/campaign/),
   les match avec chaque angle, sÃ©lectionne asset + segments.
   â†’ Ã‰crit OUT/source_specimen_<angle_id>.json (un par angle)

Phase 3 : finalize
   python source_hunter.py --finalize
   â†’ Valide cohÃ©rence + check-in IW_CUSTOS.py
   â†’ Met Ã  jour liber_clipping.json (statut C03 = done, N specimens prÃªts pour C04)
```

---

## CONTRATS RÃ‰FÃ‰RENCÃ‰S

- `ARCHIVUM/rules/clipping_rules.md` â€” strict source, jamais sortir des assets
- `ARCHIVUM/platform_generator/{plateforme}_profile.md` â€” format + durations
- `ARCHIVUM/market_generator/{marchÃ©}.md` â€” contraintes culturelles
- `ARCHIVUM/angles/angle_patterns.json` â€” patterns d'angles
- `ARCHIVUM/angles/angle_performance.json` â€” perf passÃ©e par angle (poids nul si < 50)
- `CONTRACTS/anti_bullshit.md` (liens core)

---

## DÃ‰PENDANCES

- **Amont** : F01_SCOUT (assets), F02_TYRANT_CAMP (verdict + angles context), ANGLESMITH (angles forgÃ©s)
- **Downstream** : F04_COPYWRITER (utilise `suggested_segments` et segments pour forge le texte), F05_PACKAGER (emballe les N specimens + les N text_payloads en N packs)

---

## HÃ‰RÃ‰SIES

- âŒ SÃ©lectionner un asset qui n'est pas dans `source_specimen.assets[]` de C01
- âŒ Couper la vidÃ©o (cela est le boulot de D-F02 dans OMNIS_WATCH â€” pas C03)
- âŒ SuggÃ©rer des segments dont la durÃ©e sort de la fourchette plateforme
- âŒ Ignorer `blue_ocean_reframe_applied` quand l'angle est en zone ocÃ©an bleu

---

## STATUT

| Phase | Ã‰tat | Notes |
|---|---|---|
| Arborescence crÃ©Ã©e | âœ… | |
| TRACKING.md rÃ©digÃ© | âœ… | Ce fichier |
| Code Python | âŒ | Ã€ implÃ©menter |
| `source_hunter.py` | âŒ | Wrapper orchestrateur |
| `libs/transcript_loader.py` | âŒ | Charge transcripts depuis ARCHIVUM/campaign/ |
| `libs/segment_matcher.py` | âŒ | Match angle â†” segment transcript |
| `libs/duration_guard.py` | âŒ | VÃ©rification min/max par plateforme |
| `requirements_c03.txt` | âŒ | |

*Fer au-dedans, Fer au-dehors.*
