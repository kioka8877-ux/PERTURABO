# TYRANT â€” TRACKING.md (Monde Forge CLIPPING)

> *"L'Oracle voit les DÃ©mon avant que les Warsmith ne les pointent du doigt. L'Oracle voit les ocÃ©ans bleus avant que les mers ne vident."*
> *FrÃ©gate-Oracle, mode prospectif. Veille DÃ©mon dominants hors campagne, cartographie les ocÃ©ans bleus.Common nourrit ARCHIVUM/demons/.*

---

## RÃ”LE (MODE PROSPECTIF UNIQUEMENT ICI)

`TYRANT/` (Ã  la racine de MONDES_FORGES/CLIPPING/) est la **frÃ©gate-Oracle en mode prospectif**. Ã€ l'inverse de F02_TYRANT_CAMP (qui analyse une campagne fournie = mode rÃ©actif), TYRANT prospectif scanne le **wild clipping** (hors campagne) pour identifier des **DÃ©mon dominants** et cartographier leurs **ocÃ©ans bleus unlocked**.

Le Warsmith dÃ©clenche TYRANT prospectif sur commande, hors campagne active. La sortie nourrit `ARCHIVUM/demons/` que F02_TYRANT_CAMP lira ensuite pour proposer des ocÃ©ans bleus sur les campagnes futures.

---

## INPUTS

| Input | Source | Format | Obligatoire |
|---|---|---|---|
| Liste de comptes/chaÃ®nes Ã  scanner | Warsmith (saisie libre â€” chaÃ®nes clipping virales rÃ©centes) | Liste URLs | âœ… |
| CritÃ¨res de seuil | Defaults dans `TYRANT/IN/tyrant_config.json` (outlier_score > 3x, niche bending) | JSON | âœ… |

---

## OUTPUTS

### `OUT/tyrant_eclaircissement.json`

```json
{
  "scan_id": "...",
  "scanned_at": "<ISO8601>",
  "demons_identified": [
    {
      "demon_id": "<slug>",
      "demon_url": "...",
      "platform": "youtube|tiktok|instagram",
      "views": N,
      "dominant_emotion": "drame|joie|outrage|inspiration|...",
      "dominant_engagement_type": "question|assertion|cliffhanger|...",
      "exploited_territories": ["drame"],         // ce que le DÃ©mon couvre
      "blue_ocean_unlocked": [                    // territoires adjacents non saturÃ©s
        {
          "territory": "grossophobie",
          "rationale": "...",
          "estimated_saturation": "low|medium|high",
          "blue_ocean_depth": 1                   // toujours 1 â€” pas 2+
        }
      ],
      "skeleton_extract": {                       // squelette viral du DÃ©mon
        "hook_type": "...",
        "loop_technique": "...",
        "structure_narrative": "..."
      }
    }
  ],
  "check_in_iw_custos": "<ISO8601>"
}
```

### Canonical copies
- `ARCHIVUM/demons/<demon_id>.json` â€” un fichier par DÃ©mon, qui sera lu par F02_TYRANT_CAMP plus tard

---

## MÃ‰THODE â€” OCÃ‰AN BLEU 1 COUCHE

Le DÃ©mon a une Ã©motion dominante (ex : `drame`). TYRANT prospectif propose des re-ciblages non saturÃ©s sur la mÃªme forme narrative â€” mais **1 couche de profondeur seulement**.

Exemple validÃ© :
```
DÃ©mon â†’ drame
  â””â†’ blue_ocean_unlocked[0] = grossophobie  (depth=1)
  â””â†’ blue_ocean_unlocked[1] = gens toxiques (depth=1)
  
INTERDIT :
  grossophobie â†’ violence verbale (depth=2) = hÃ©rÃ©sie
```

Si F02_TYRANT_CAMP tente d'empiler 2 couches, elle doit rejeter.

---

## PATTERN D'EXÃ‰CUTION

```
Phase 1 : prepare
   python tyrant.py --prepare --scan-list IN/scan_list.json
   â†’ gÃ©nÃ¨re IN/tyrant_prompt.json

Phase 2 : IRON (Claude sandbox)
   Le Warsmith copie-colle le prompt.
   L'IRON scanne les clips (via yt-dlp metrics + transcripts locaux si disponibles),
   identifie les DÃ©mon (outlier_score > 3x), cartographie les Ã©motions dominantes,
   propose les ocÃ©ans bleus 1 couche.
   â†’ Ã‰crit OUT/tyrant_eclaircissement.json

Phase 3 : finalize
   python tyrant.py --finalize
   â†’ Copie chaque dÃ©mon vers ARCHIVUM/demons/<demon_id>.json
   â†’ Check-in IW_CUSTOS.py
```

---

## CONTRATS RÃ‰FÃ‰RENCÃ‰S

- `ARCHIVUM/rules/clipping_rules.md`
- `HERESIE/CONTRACTS/tyrant_prompt.md` (liens core) â€” modÃ¨le de prompt Oracle
- `HERESIE/CONTRACTS/anti_bullshit.md` (liens core)
- `ARCHIVUM/knowledge_base/transcripts/` â€” pour lire les transcripts des DÃ©mon dÃ©jÃ  scrapÃ©s

---

## DÃ‰PENDANCES

- **Amont** : Warsmith (scan_list)
- **Downstream** : `ARCHIVUM/demons/` (nourri) â†’ F02_TYRANT_CAMP (lit)
- **Auxiliaire** : peut utiliser `CAPTEURS/` pour scrap les mÃ©triques des DÃ©mon

---

## HÃ‰RÃ‰SIES

- âŒ Re-ciblage au-delÃ  de 1 couche
- âŒ Identifier des DÃ©mon sans preuve (outlier_score quantitatif obligatoire)
- âŒ SuggÃ©rer des sources alternatives Ã  la future campagne (TYRANT prospectif ne voit que le wild, pas les assets d'une campagne spÃ©cifique)

---

## STATUT

| Phase | Ã‰tat | Notes |
|---|---|---|
| Arborescence crÃ©Ã©e | âœ… | |
| TRACKING.md rÃ©digÃ© | âœ… | Ce fichier |
| Code Python implÃ©mentÃ© | âŒ | Ã€ implÃ©menter |
| `tyrant.py` | âŒ | Wrapper Oracle prospectif |
| `libs/outlier_scorer.py` | âŒ | Calcul outlier_score > 3x |
| `libs/emotion_classifier.py` | âŒ | Classification Ã©motion dominante |
| `libs/blue_ocean_mapper.py` | âŒ | Mapper territoires adjacents 1 couche |
| `libs/demon_archivist.py` | âŒ | Ã‰crit demon_id.json dans ARCHIVUM/demons/ |
| `requirements_tyrant.txt` | âŒ | yt-dlp + youtube-transcript-api |

RÃ©fÃ©rence d'implÃ©mentation : `HERESIE/TYRANT/CODEBASE/tyrant.py` dans le core (squelette structurel probablement rÃ©utilisable, mais adapter au prospectif clipping).

*Fer au-dedans, Fer au-dehors.*
