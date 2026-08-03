# F01_SCOUT â€” TRACKING.md

> *"Le fer qui voit en premier. La forteresse n'est pÃ©nÃ©trÃ©e qu'aprÃ¨s avoir Ã©tÃ© vue."*
> *FrÃ©gate de reconnaissance. Jamais elle ne chasse hors des assets de la campagne â€” cela serait hÃ©rÃ©sie.*

---

## RÃ”LE

F01_SCOUT est la **frÃ©gate d'acquisition**. Elle prend en entrÃ©e les **assets fournis par la campagne** (URLs de vidÃ©os longues, docs, briefs) et produit un `source_specimen.json` unifiÃ© consommÃ© par F02_TYRANT_CAMP (Porte 1) et F03_SOURCE_HUNTER (Porte 3).

Elle **n'inventorie que ce que la campagne fournit**. Toute source non-issue des assets de la campagne est rejetÃ©e comme hÃ©rÃ©sie (cf. `CONTRACTS/clipping_rules.md` rÃ¨gle de strict-source).

---

## INPUTS

| Input | Source | Format | Obligatoire |
|---|---|---|---|
| `directive.md` (campaign goal doc) | Warsmith â†’ `ARCHIVUM/campaign/directive.md` | Markdown | âœ… |
| `reference_clip_url` | Warsmith â†’ `ARCHIVUM/campaign/reference_clip.json` (URL + mÃ©tadonnÃ©es) | JSON | âœ… |
| `assets_urls[]` | Extrait de `directive.md` (section "assets" ou "sources fournies") | Liste d'URLs | âœ… |

Les assets peuvent Ãªtre : vidÃ©os YouTube longues, vidÃ©os sponsor longues, archives de podcasts, streams Twitch, docs PDF (rare). Pas de rÃ©cupÃ©ration externe, jamais.

---

## OUTPUTS

### `OUT/source_specimen.json`

Format alignÃ© sur le pattern specimen.json de `F01_SENTINEL` du core (YOUTUBE). Structure attendue :

```json
{
  "campaign_id": "...",
  "scanned_at": "<ISO8601>",
  "reference_clip": {
    "url": "...",
    "video_id": "...",
    "title": "...",
    "duration_sec": N,
    "view_count": N,
    "thumbnail": "...",
    "outlier_score": <float>,    // view_count / channel_shorts_baseline
    "platform": "youtube|tiktok|instagram",
    "metrics_extracted": {...}
  },
  "assets": [
    {
      "asset_id": "...",
      "url": "...",
      "type": "video_long|podcast|stream|doc",
      "duration_sec": N,
      "title": "...",
      "channel": "...",
      "transcript_available": true|false,
      "transcript_path": "ARCHIVUM/campaign/...",
      "thumbnail": "..."
    }
  ],
  "check_in_iw_custos": "<ISO8601>"
}
```

### Autres outputs
- `OUT/scout_report.md` â€” synthÃ¨se lisible par le Warsmith (rÃ©sumÃ© de la forteresse, ce qu'il y a Ã  clipper) â€” utile pour le dialogue Porte 1
- `ARCHIVUM/campaign/reference_skeleton.json` â€” squelette viral extrait du clip de rÃ©fÃ©rence (prÃ©-rempli pour C02)

---

## PATTERN D'EXÃ‰CUTION

F01_SCOUT suit le pattern **3-phases standard** du core YOUTUBE :

```
Phase 1 : prepare
   python scout.py --prepare --directive ../ARCHIVUM/campaign/directive.md
   â†’ gÃ©nÃ¨re IN/scout_prompt.json (prompt pour l'IRON)

Phase 2 : IRON (Claude sandbox)
   Le Warsmith copie le prompt dans Claude sandbox.
   L'IRON analyse les assets, extrait mÃ©tadonnÃ©es, calcule l'outlier_score,
   prÃ©-squelette le clip de rÃ©fÃ©rence.
   â†’ Ã‰crit OUT/source_specimen.json

Phase 3 : finalize
   python scout.py --finalize
   â†’ Valide cohÃ©rence + check-in IW_CUSTOS.py
   â†’ Met Ã  jour liber_clipping.json (statut C01 = done)
```

---

## CONTRATS RÃ‰FÃ‰RENCÃ‰S (ce que C01 doit lire)

- `ARCHIVUM/rules/clipping_rules.md` â€” rÃ¨gle de strict-source
- `ARCHIVUM/rules/whop_rules.md` â€” formatted des assets acceptables (vidÃ©os sponsor, etc.)
- `ARCHIVUM/platform_generator/{plateforme}_profile.md` â€” pour le choix de platform du skeleton
- `CONTRACTS/anti_bullshit.md` (liens core HERESIE/CONTRACTS/) â€” garde-fous

---

## DÃ‰PENDANCES

- **Amont** : Warsmith (remplit `directive.md` + `reference_clip.json`)
- **Downstream** : F02_TYRANT_CAMP (consomme `source_specimen.json`), F03_SOURCE_HUNTER (consomme `assets[]`)

---

## HÃ‰RÃ‰SIES (ce que C01 ne fait jamais)

- âŒ Chercher des vidÃ©os hors des assets de la campagne
- âŒ Extension du territoire de chasse "en adjacence"
- âŒ Modification/coupe/montage des vidÃ©os sources (cela est boulot d'OMNIS_WATCH)
- âŒ Aucun scrape de concurrents â€” CAPTEURS s'en charge, pas C01

---

## STATUT

| Phase | Ã‰tat | Notes |
|---|---|---|
| Arborescence crÃ©Ã©e | âœ… | CODEBASE/libs + IN + OUT + TRACKING |
| TRACKING.md rÃ©digÃ© | âœ… | Ce fichier |
| Code Python implÃ©mentÃ© | âŒ | Ã€ implÃ©menter par autre model, en suivant ce doc |
| `scout.py` | âŒ | Wrapper orchestrateur (prÃ©vu) |
| `recon.py` (libs/) | âŒ | Extraction URLs depuis directive.md |
| `scribe.py` (libs/) | âŒ | Transcription des vidÃ©os longues (yt-dlp + fallback) |
| `enrich.py` (libs/) | âŒ | Enrichissement mÃ©tadonnÃ©es yt-dlp --dump-json |
| `requirements_c01.txt` | âŒ | DÃ©pendances Python Ã  figer |

Le futur implÃ©menteur doit s'inspirer de `MONDES_FORGES/YOUTUBE/F01_SENTINEL/CODEBASE/sentinel.py` comme squelette de rÃ©fÃ©rence (probablement 80% de rÃ©utilisation logique).

*Fer au-dedans, Fer au-dehors.*
