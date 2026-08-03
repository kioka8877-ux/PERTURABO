# ARCHIVUM/demons/ â€” Clips qui dominent

> *DÃ©mon (campagne + veille). Cartographie par TYRANT prospectif.*
> *Lu par F02_TYRANT_CAMP pour identifier les ocÃ©ans bleus sur les campagnes futures.*

---

## Deux types de DÃ©mon ici

### 1. DÃ©mon de campaigne
Le clip de rÃ©fÃ©rence fourni par le Warsmith pour une campaigne spÃ©cifique. StockÃ© dans `ARCHIVUM/campaign/reference_clip.json` + `reference_skeleton.json`. **Pas dupliquÃ© ici** â€” vit dans `campaign/`.

### 2. DÃ©mon de veille (ici, dans `demons/`)
IdentifiÃ© par `TYRANT/` (mode prospectif) hors campaigne. Le scanner (CAPTEURS) peut aussi contribuer via `demon_scanner.py`.

Ces DÃ©mon veille sont la mÃ©moire globale du territoire clipping â€” utilisÃ©s par F02_TYRANT_CAMP pour identifier des ocÃ©ans bleus sur les prochaines campagnes.

---

## Structure d'un `<demon_id>.json`

```json
{
  "demon_id": "slug_unique",
  "demon_url": "...",
  "platform": "youtube|tiktok|instagram",
  "views": N,
  "outlier_score": <float>,    // > 3x = DÃ©mon
  "dominant_emotion": "drame|joie|outrage|inspiration|...",
  "dominant_engagement_type": "question|assertion|cliffhanger|...",
  "exploited_territories": ["drame"],
  "blue_ocean_unlocked": [
    {
      "territory": "grossophobie",
      "rationale": "...",
      "estimated_saturation": "low|medium|high",
      "blue_ocean_depth": 1
    }
  ],
  "skeleton_extract": {
    "hook_type": "...",
    "loop_technique": "...",
    "structure_narrative": "..."
  },
  "scanned_at": "<ISO8601>"
}
```

## RÃ¨gle 1-couche

`blue_ocean_depth` est **TOUJOURS 1** dans cette ARCHIVUM. Le scanner TYRANT ne doit jamais proposer une profondeur 2 â€” cela serait hÃ©rÃ©sie (cf. `CONTRACTS/clipping_rules.md` et `TYRANT/CODEBASE/TRACKING.md`).

## Ã€ remplir

Ce dossier est nourri par `TYRANT prospectif` au runtime. Ã€ l'init, vide avec `.gitkeep`. Le Warsmith peut prÃ©-peupler avec quelques DÃ©mon dÃ©jÃ  connus s'il en a (optional â€” TYRANT les trouvera au scan).
