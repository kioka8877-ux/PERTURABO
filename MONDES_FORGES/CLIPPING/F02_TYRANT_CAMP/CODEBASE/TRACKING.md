# F02_TYRANT_CAMP â€” TRACKING.md

> *"L'Oracle voit la forteresse. L'Oracle voit l'ocÃ©an bleu. L'Oracle ne ment pas â€” il Ã©claire."*
> *FrÃ©gate-stratÃ¨ge de la Porte 1. Elle ne produit pas des vidÃ©os, elle produit des verdicts.*

---

## RÃ”LE

F02_TYRANT_CAMP est la **frÃ©gate stratÃ¨ge de la Porte 1**. Elle prend en entrÃ©e le `source_specimen.json` produit par F01_SCOUT et sort un **verdict GO/NO-GO** accompagnÃ© de l'identification d'un **ocÃ©an bleu** potentiel â€” sur la MÃŠME source que le DÃ©mon de la campagne (pas d'hÃ©rÃ©sie : on ne re-cible jamais au-delÃ  de 1 couche).

Elle prose aussi le squelette viral du clip de rÃ©fÃ©rence (preuve de ce qui marche).

---

## INPUTS

| Input | Source | Format | Obligatoire |
|---|---|---|---|
| `source_specimen.json` | F01_SCOUT | JSON | âœ… |
| `directive.md` | `ARCHIVUM/campaign/directive.md` | Markdown | âœ… |
| `platform_target` | Warsmith (input 3 du Warsmith) | string | âœ… |
| `market_target` | Warsmith (input 4) | string | âœ… |
| `cartographie_Ã©cosystÃ¨me` | CAPTEURS (si exÃ©cutÃ© avant Porte 1) | JSON | Optionnel mais recommandÃ© |

---

## OUTPUTS

### `OUT/campaign_verdict.json`

```json
{
  "campaign_id": "...",
  "verdict": "GO|NO-GO",
  "verdict_justification": "...",
  
  "reference_skeleton": {
    "hook_type": "...",
    "emotion_dominante": "...",
    "structure_narrative": "...",
    "loop_technique": "...",
    "engagement_type": "...",
    "endroits_preuve": ["..."]    // moments du clip ref qui prouvent le squelette
  },
  
  "demon_analysis": {
    "demon_id": "...",
    "dominant_emotion": "drame|joie|outrage|...",
    "exploited_territories": ["drame"],
    "blue_ocean_unlocked": [
      {
        "territory": "grossophobie",
        "rationale": "mÃªme source, mÃªme forme, mais re-ciblÃ©e sur un angle 
                      non saturÃ© observÃ© sur le scraping",
        "estimated_saturation": "low|medium|high",
        "blue_ocean_depth": 1
      },
      {
        "territory": "gens toxiques",
        "rationale": "...",
        "estimated_saturation": "low",
        "blue_ocean_depth": 1
      }
    ]
  },
  
  "direct_analysis": {
    "campaign_fit_platform": <0-10>,
    "campaign_fit_market": <0-10>,
    "campaign_budget_remaining": "...",
    "cpm_expected": "...",
    "saturation_level": "low|medium|high"
  },
  
  "check_in_iw_custos": "<ISO8601>"
}
```

### Autres outputs
- `ARCHIVUM/campaign/verdict.json` (copie canonique)
- `ARCHIVUM/campaign/reference_skeleton.json` (canonical squelette)
- `OUT/scout_report.md` (synthÃ¨se lisible pour le Warsmith Ã  la Porte 1)

---

## DEUX MODES (C02 + TYRANT)

F02_TYRANT_CAMP et la frÃ©gate `TYRANT/` partagent la capacitÃ© "Oracle". C02 est spÃ©cialisÃ©e sur une campagne (mode rÃ©actif). TYRANT/ est le mode prospectif global (veille DÃ©mon dominants hors campagne).

| Mode | Qui | Quand | Sortie |
|---|---|---|---|
| RÃ©actif | F02_TYRANT_CAMP | Pour chaque campagne fournie par le Warsmith | `campaign_verdict.json` |
| Prospectif | TYRANT/ | Sur commande Warsmith, hors campagne, pour identifier des DÃ©mon dans le wild | `tyrant_eclaircissement.json` qui nourrit `ARCHIVUM/demons/` |

C02 lit `ARCHIVUM/demons/` (synthÃ¨se des DÃ©mon cartographiÃ©s par TYRANT prospectif) pour identifier l'ocÃ©an bleu de la campagne. **DÃ©mon de campagne** et **DÃ©mon veille** peuvent Ãªtre identiques ou diffÃ©rents.

---

## PATTERN D'EXÃ‰CUTION

Pattern **3-phases standard** :

```
Phase 1 : prepare
   python tyrant_camp.py --prepare --specimen ../F01_SCOUT/OUT/source_specimen.json
   â†’ gÃ©nÃ¨re IN/tyrant_camp_prompt.json (prompt pour l'IRON)

Phase 2 : IRON (Claude sandbox)
   Le Warsmith copie le prompt dans Claude.
   L'IRON analyse : le squelette de rÃ©fÃ©rence, le DÃ©mon, les ocÃ©ans bleus,
   le fit plateforme/marchÃ©, la saturation.
   â†’ Ã‰crit OUT/campaign_verdict.json

Phase 3 : finalize
   python tyrant_camp.py --finalize
   â†’ Valide cohÃ©rence + check-in IW_CUSTOS.py
   â†’ Copie vers ARCHIVUM/campaign/verdict.json
   â†’ Met Ã  jour liber_clipping.json (statut C02 = done, verdict disponible Porte 1)
```

---

## MÃ‰THODE OCÃ‰AN BLEU

DÃ©mon = clip dominant avec une Ã©motion dominante (ex : `drame`).
C02 propose des **re-ciblages** sur des territoires adjacents non saturÃ©s, mais **uniquement sur la mÃªme source** que celle de la campagne (assets Whop).

RÃ¨gles strictes :
- Profondeur ocÃ©an bleu : **1 couche maximum**. Exemple DÃ©mon (drame) â†’ grossophobie. On ne re-cible pas une 2e fois (grossophobie â†’ violence verbale en ligne = interdit).
- Le re-ciblage ne change pas la source â€” il change l'angle d'attaque narratif.
- CritÃ¨re de saturation : lu depuis `ARCHIVUM/demons/<demon_id>.json` (champ `blue_ocean_unlocked`) â€” territoire marquÃ© `low` ou `medium` est Ã©ligible ; `high` est rejetÃ©.

---

## CONTRATS RÃ‰FÃ‰RENCÃ‰S

- `ARCHIVUM/rules/clipping_rules.md`
- `ARCHIVUM/rules/whop_rules.md`
- `ARCHIVUM/rules/platform_{plateforme}.md`
- `ARCHIVUM/platform_generator/{plateforme}_profile.md`
- `ARCHIVUM/market_generator/{marchÃ©}.md`
- `ARCHIVUM/demons/<demon_id>.json` (les DÃ©mon veille cartographiÃ©s par TYRANT prospectif)
- `CONTRACTS/anti_bullshit.md` (liens core)

---

## DÃ‰PENDANCES

- **Amont** : F01_SCOUT (`source_specimen.json`), CAPTEURS (`cartographie_Ã©cosystÃ¨me` â€” optionnel mais recommandÃ©), TYRANT prospectif (`ARCHIVUM/demons/`)
- **Downstream** :
  - ANGLESMITH (consomme `verdict.json` pour la Porte 2 â€” forge les N angles sur `direct_analysis` + `blue_ocean_unlocked`)
  - F04_COPYWRITER (consomme `reference_skeleton` pour calibrer hooks)

---

## HÃ‰RÃ‰SIES

- âŒ Re-ciblage au-delÃ  de 1 couche (profondeur > 1 = hÃ©rÃ©sie)
- âŒ SuggÃ©rer des sources alternatives (assets = forteresse fermÃ©e)
- âŒ Verdict sans preuve (chaque assertion du verdict doit Ãªtre tracÃ©e dans le specimen / la cartographie)
- âŒ Ignorer le fit plateforme/marchÃ© â€” chaque verdict doit scorer sur ces axes

---

## STATUT

| Phase | Ã‰tat | Notes |
|---|---|---|
| Arborescence crÃ©Ã©e | âœ… | |
| TRACKING.md rÃ©digÃ© | âœ… | Ce fichier |
| Code Python implÃ©mentÃ© | âŒ | Ã€ implÃ©menter |
| `tyrant_camp.py` | âŒ | Wrapper orchestrateur (prÃ©vu) |
| `libs/skeleton_extractor.py` | âŒ | Extraction squelette viral du clip ref |
| `libs/blue_ocean_finder.py` | âŒ | Identification ocÃ©ans bleus depuis ARCHIVUM/demons/ |
| `libs/fit_scorer.py` | âŒ | Score fit plateforme Ã— marchÃ© Ã— niche |
| `requirements_c02.txt` | âŒ | DÃ©pendances Ã  figer |

RÃ©fÃ©rence d'implÃ©mentation : `HERESIE/TYRANT/CODEBASE/tyrant.py` dans le core (squelette structurel probablement rÃ©utilisable).

*Fer au-dedans, Fer au-dehors.*
