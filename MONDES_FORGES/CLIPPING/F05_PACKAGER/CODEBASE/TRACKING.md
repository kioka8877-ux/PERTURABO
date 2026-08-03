# F05_PACKAGER — TRACKING.md

> *"Le fer est forgé. Les angles sont tracés. La pièce finale est prête pour l'usine. Le ferrier emballe."*
> *Frégate d'assemblage final. Lancier de la Porte 4 — expédie les N packs à OMNIS_WATCH.*

---

## RÔLE

F05_PACKAGER est la **frégate finale de la Porte 4**. Elle assemble tous les artefacts produits par F01 → F04 et forge les N `production_pack.json` qui seront consommés par OMNIS_WATCH.

Un pack = 1 vidéo pour 1 plateforme pour 1 marché. Pour N angles, on a N packs.

---

## INPUTS

| Input | Source | Format | Obligatoire |
|---|---|---|---|
| `angles.json` | ANGLESMITH | JSON | ✅ |
| `source_specimen_<angle>.json` (N) | F03_SOURCE_HUNTER | JSON N | ✅ |
| `text_payload_<angle>.json` (N) | F04_COPYWRITER | JSON N | ✅ |
| `verdict.json` | F02_TYRANT_CAMP | JSON | ✅ |
| `reference_skeleton.json` (style extrait) | F01_SCOUT/F04 → `reference_style` | JSON | ✅ |
| `platform_target` | Warsmith (input 3) | string | ✅ |
| `market_target` | Warsmith (input 4) | string | ✅ |

---

## OUTPUTS

### `OUT/production_pack_<angle_id>.json` (N packs)

Voir `CONTRACTS/production_pack_schema.json` pour le schéma JSON canonique (contrat interface OMNIS_WATCH). Le pack contient les 9 blocs :

1. `IDENTITÉ` — campaign_id, angle_id, pack_index/total
2. `CIBLES` — target_platform, target_market
3. `SOURCE` — url de l'asset, suggested_segments, source_segment_sec (assets uniquement — hérésie sinon)
4. `ANGLE` — family, emotion, engagement, reframe, hook_style_fit, loop_tech, anti_cannibal_diff, blue_ocean
5. `CUT` — clip_max/min_duration, moments_to_chase, moments_to_avoid, forbidden
6. `STYLE` — pacing, energy_level, cut_density, color_palette, text_treatment (ADN observé du clip de référence — matière première brute, OMNIS_WATCH applique ses presets coloring en plus)
7. `TEXT_PAYLOAD` — 3 titres + paragraphe (3 vetos) + caption + hashtags + on-screen + cta
8. `COMPLIANCE` — disclosure "#ad", submit_deadline_min=60, source_permission="campaign_provided"
9. `METADATA` — title_pattern, description_skeleton
+ `SUBMISSION_CHECKLIST` (active, imbriquée)

### Autres
- `OUT/packager_summary.md` — synthèse lisible Warsmith : "N packs prêts à expédier → OMNIS_WATCH"
- `OUT/packs_index.json` — index des N packs pour OMNIS_WATCH

---

## SUBMISSION CHECKLIST (imbriquée dans chaque pack)

Active, pas passive. À chaque pack, F05 génère une checklist que F06_TRACKER activera après Porte 4 :

```json
"submission_checklist": {
  "items": [
    {"id": "post_on_platform", "label": "Poster sur {target_platform}", "status": "pending"},
    {"id": "submit_whop_under_1h", "label": "Soumettre Whop dans l'heure", "deadline_min": 60, "status": "pending"},
    {"id": "log_link_c06", "label": "Logger le lien dans F06_TRACKER", "status": "pending"},
    {"id": "view_check_1h", "label": "Relever vues à 1h", "status": "pending"},
    {"id": "view_check_24h", "label": "Relever vues à 24h", "status": "pending"},
    {"id": "payout_flag_low", "label": "Flag si payout < seuil", "status": "pending"},
    {"id": "feedback_learnings", "label": "Nourrir learnings.json", "status": "pending"}
  ]
}
```

---

## PATTERN D'EXÉCUTION

```
python packager.py --assemble --angles ../F02/OUT/angles.json
# Pour chaque angle :
#   1. Lit source_specimen_<angle>.json
#   2. Lit text_payload_<angle>.json
#   3. Lit verdict.json (pour blue_ocean, reference_skeleton)
#   4. Lit reference_style (depuis F01 ou F04)
#   5. Assemble en production_pack_<angle>.json
#   6. Génère submission_checklist imbriquée

python packager.py --finalize
# Check-in IW_CUSTOS + packs_index.json
```

F05 ne fait **pas** appel à l'IRON — c'est un enchaînement purement déterministe d'assemblage JSON. Pas de "préparation de prompt". La tâche est mécanique : fusion de JSONs.

---

## CONTRATS RÉFÉRENCÉS

- `CONTRACTS/production_pack_schema.json` — schéma canonique (contrat avec OMNIS_WATCH)
- `ARCHIVUM/platform_generator/{plateforme}_profile.md` — pour clip_max_duration, clip_min_duration
- `ARCHIVUM/rules/clipping_rules.md` — pour forbidden[], source_permission

---

## DÉPENDANCES

- **Amont** : tous (F01-F04 + verdict)
- **Downstream** : 
  - OMNIS_WATCH (consomme les N packs via mode `--pack production_pack.json`)
  - F06_TRACKER (lit `submission_checklist` imbriquée, l'active après Porte 4)

---

## HÉRÉSIES

- ❌ Inclure un asset non-F03 dans `SOURCE`
- ❌ Inclure un texte non-F04 dans `TEXT_PAYLOAD`
- ❌ Omettre `reference_style` (matière première brute à transmettre à OMNIS_WATCH)
- ❌ `source_permission` != `"campaign_provided"` = hérésie
- ❌ Inclure des hashtag/caption non validés par F04 → F05 ne forge rien, il assemble

---

## STATUT

| Phase | État | Notes |
|---|---|---|
| Arborescence créée | ✅ | |
| TRACKING.md rédigé | ✅ | Ce fichier |
| Code Python implémenté | ✅ | v1 — commit bdd7013 (tests mock TEST_F05) |
| `packager.py` | ✅ | `--assemble` (N packs) + `--finalize` (validation + packs_index + summary + check-in IW_CUSTOS F05) |
| `libs/schema_validator.py` | ✅ | Validateur draft-07 maison fidèle au schéma canonique (type/required/enum/const/min-maxItems/contains) |
| `libs/reference_style_extractor.py` | ✅ | ADN style : `reference_style.json` campagne → bloc du reference_clip.json → défauts `observed: false` + prompt vision IRON |
| `requirements_c05.txt` | ✅ | stdlib pure (jsonschema optionnel documenté) |

### Décisions v1 (résumé)
- F05 ne forge rien, il assemble : text_payload/blocs strictement copiés depuis F04, video_url strictement dans les assets F01 (règle C1) — hérésies refusées à `--assemble` comme à `--finalize`.
- `blue_ocean` sans null : depth/territory/rationale émis uniquement pour les angles réellement océan bleu (schéma canonique intact, pas de coordination OMNIS_WATCH nécessaire).
- `forbidden` contient obligatoirement `silences > 3s` (contrainte `contains` du schéma).
- `reference_style.observed` (bool, champ additionnel) : distingue ADN réel de l'ADN par défaut — la `note` reste la const figée du contrat.
- Fourchettes cut : profil `ARCHIVUM/platform_generator/{p}_profile.md` (regex `clip_min/max_duration`), défauts déclarés sinon — aligné sur F03 duration_guard.

*Fer au-dedans, Fer au-dehors.*
