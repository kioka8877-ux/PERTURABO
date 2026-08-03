# F05_PACKAGER â€” TRACKING.md

> *"Le fer est forgÃ©. Les angles sont tracÃ©s. La piÃ¨ce finale est prÃªte pour l'usine. Le ferrier emballe."*
> *FrÃ©gate d'assemblage final. Lancier de la Porte 4 â€” expÃ©die les N packs Ã  OMNIS_WATCH.*

---

## RÃ”LE

F05_PACKAGER est la **frÃ©gate finale de la Porte 4**. Elle assemble tous les artefacts produits par C01 â†’ C04 et forge les N `production_pack.json` qui seront consommÃ©s par OMNIS_WATCH.

Un pack = 1 vidÃ©o pour 1 plateforme pour 1 marchÃ©. Pour N angles, on a N packs.

---

## INPUTS

| Input | Source | Format | Obligatoire |
|---|---|---|---|
| `angles.json` | ANGLESMITH | JSON | âœ… |
| `source_specimen_<angle>.json` (N) | F03_SOURCE_HUNTER | JSON N | âœ… |
| `text_payload_<angle>.json` (N) | F04_COPYWRITER | JSON N | âœ… |
| `verdict.json` | F02_TYRANT_CAMP | JSON | âœ… |
| `reference_skeleton.json` (style extrait) | F01_SCOUT/C04 â†’ `reference_style` | JSON | âœ… |
| `platform_target` | Warsmith (input 3) | string | âœ… |
| `market_target` | Warsmith (input 4) | string | âœ… |

---

## OUTPUTS

### `OUT/production_pack_<angle_id>.json` (N packs)

Voir `CONTRACTS/production_pack_schema.json` pour le schÃ©ma JSON canonique (contrat interface OMNIS_WATCH). Le pack contient les 9 blocs :

1. `IDENTITÃ‰` â€” campaign_id, angle_id, pack_index/total
2. `CIBLES` â€” target_platform, target_market
3. `SOURCE` â€” url de l'asset, suggested_segments, source_segment_sec (assets uniquement â€” hÃ©rÃ©sie sinon)
4. `ANGLE` â€” family, emotion, engagement, reframe, hook_style_fit, loop_tech, anti_cannibal_diff, blue_ocean
5. `CUT` â€” clip_max/min_duration, moments_to_chase, moments_to_avoid, forbidden
6. `STYLE` â€” pacing, energy_level, cut_density, color_palette, text_treatment (ADN observÃ© du clip de rÃ©fÃ©rence â€” matiÃ¨re premiÃ¨re brute, OMNIS_WATCH applique ses presets coloring en plus)
7. `TEXT_PAYLOAD` â€” 3 titres + paragraphe (3 vetos) + caption + hashtags + on-screen + cta
8. `COMPLIANCE` â€” disclosure "#ad", submit_deadline_min=60, source_permission="campaign_provided"
9. `METADATA` â€” title_pattern, description_skeleton
+ `SUBMISSION_CHECKLIST` (active, imbriquÃ©e)

### Autres
- `OUT/packager_summary.md` â€” synthÃ¨se lisible Warsmith : "N packs prÃªts Ã  expÃ©dier â†’ OMNIS_WATCH"
- `OUT/packs_index.json` â€” index des N packs pour OMNIS_WATCH

---

## SUBMISSION CHECKLIST (imbriquÃ©e dans chaque pack)

Active, pas passive. Ã€ chaque pack, C05 gÃ©nÃ¨re une checklist que F06_TRACKER activera aprÃ¨s Porte 4 :

```json
"submission_checklist": {
  "items": [
    {"id": "post_on_platform", "label": "Poster sur {target_platform}", "status": "pending"},
    {"id": "submit_whop_under_1h", "label": "Soumettre Whop dans l'heure", "deadline_min": 60, "status": "pending"},
    {"id": "log_link_c06", "label": "Logger le lien dans F06_TRACKER", "status": "pending"},
    {"id": "view_check_1h", "label": "Relever vues Ã  1h", "status": "pending"},
    {"id": "view_check_24h", "label": "Relever vues Ã  24h", "status": "pending"},
    {"id": "payout_flag_low", "label": "Flag si payout < seuil", "status": "pending"},
    {"id": "feedback_learnings", "label": "Nourrir learnings.json", "status": "pending"}
  ]
}
```

---

## PATTERN D'EXÃ‰CUTION

```
python packager.py --assemble --angles ../F02/OUT/angles.json
# Pour chaque angle :
#   1. Lit source_specimen_<angle>.json
#   2. Lit text_payload_<angle>.json
#   3. Lit verdict.json (pour blue_ocean, reference_skeleton)
#   4. Lit reference_style (depuis C01 ou C04)
#   5. Assemble en production_pack_<angle>.json
#   6. GÃ©nÃ¨re submission_checklist imbriquÃ©e

python packager.py --finalize
# Check-in IW_CUSTOS + packs_index.json
```

C05 ne fait **pas** appel Ã  l'IRON â€” c'est un enchaÃ®nement purement dÃ©terministe d'assemblage JSON. Pas de "prÃ©paration de prompt". La tÃ¢che est mÃ©canique : fusion de JSONs.

---

## CONTRATS RÃ‰FÃ‰RENCÃ‰S

- `CONTRACTS/production_pack_schema.json` â€” schÃ©ma canonique (contrat avec OMNIS_WATCH)
- `ARCHIVUM/platform_generator/{plateforme}_profile.md` â€” pour clip_max_duration, clip_min_duration
- `ARCHIVUM/rules/clipping_rules.md` â€” pour forbidden[], source_permission

---

## DÃ‰PENDANCES

- **Amont** : tous (C01-C04 + verdict)
- **Downstream** : 
  - OMNIS_WATCH (consomme les N packs via mode `--pack production_pack.json`)
  - F06_TRACKER (lit `submission_checklist` imbriquÃ©e, l'active aprÃ¨s Porte 4)

---

## HÃ‰RÃ‰SIES

- âŒ Inclure un asset non-C03 dans `SOURCE`
- âŒ Inclure un texte non-C04 dans `TEXT_PAYLOAD`
- âŒ Omettre `reference_style` (matiÃ¨re premiÃ¨re brute Ã  transmettre Ã  OMNIS_WATCH)
- âŒ `source_permission` != `"campaign_provided"` = hÃ©rÃ©sie
- âŒ Inclure des hashtag/caption non validÃ©s par C04 â†’ C05 ne forge rien, il assemble

---

## STATUT

| Phase | Ã‰tat | Notes |
|---|---|---|
| Arborescence crÃ©Ã©e | âœ… | |
| TRACKING.md rÃ©digÃ© | âœ… | Ce fichier |
| Code Python implÃ©mentÃ© | âŒ | Ã€ implÃ©menter |
| `packager.py` | âŒ | Assembler purement dÃ©terministe |
| `libs/schema_validator.py` | âŒ | Valide pack contre `production_pack_schema.json` |
| `libs/reference_style_extractor.py` | âŒ | Extraction style ADN (vision pixel + IRON interpretation) |
| `requirements_c05.txt` | âŒ | PyYAML/Pydantic pour schema validation |

*Fer au-dedans, Fer au-dehors.*
