# ARCHIVUM/angles/ â€” BibliothÃ¨que d'angles d'attaque

> *Les patterns d'angle que ANGLESMITH peut combiner.*
> *CouplÃ© Ã  `angle_performance.json` qui suit la perf rÃ©elle (poids nul si < 50 packs).*

---

## Fichiers attendus

### `angle_patterns.json`

Catalogue des patterns d'angle combinables. Chaque entry combine 4 axes :
- `angle_family` : reframing | emotion | engagement | structural
- `emotion_mode` : tension, joie, inspiration, outrage, admiration, ...
- `engagement_type` : question | confirmation | assertion | cliffhanger
- `reframe_dim` : la transformation de sens (highlight â†’ motivation, etc.)

Chaque pattern a :
- `angle_id` â€” slug unique
- `angle_family`
- `emotion_mode`
- `engagement_type`
- `reframe_dim`
- `hook_style_fit` â€” types de hooks compatibles
- `platforms_fit` â€” ["youtube", "tiktok", "instagram"]
- `markets_fit` â€” ["us_young_english", ...]
- `loop_tech` â€” callback_hook, visual_match_cut, cliffhanger, ...
- `proof_examples` â€” rÃ©fÃ¨re Ã  des exemples dans `demons/`

Exemple :
```json
{
  "angle_id": "reframing_motivation",
  "angle_family": "reframing",
  "emotion_mode": "inspiration",
  "engagement_type": "assertion",
  "reframe_dim": "highlight_to_motivation",
  "hook_style_fit": ["stat_choc", "declaration", "question"],
  "platforms_fit": ["youtube", "tiktok", "instagram"],
  "markets_fit": ["us_young_english"],
  "loop_tech": "callback_hook",
  "proof_examples": ["demon_id_1", "demon_id_2"]
}
```

### `angle_performance.json`

Perf historique par angle Ã— plateforme Ã— marchÃ©. Au dÃ©but (0 pack exÃ©cutÃ©), vide. Au fil des campagnes closes (via F06_TRACKER), se remplit.

Structure :
```json
{
  "cumulative_packs_executed": 0,
  "eligible_for_weighting": false,
  "angle_performance": []
}
```

RÃ¨gle : `eligible_for_weighting` reste `false` tant que `cumulative_packs_executed < 50`. Ã€ 50+, passe Ã  `true` et ANGLESMITH utilise `weight` pour pondÃ©rer.

## Ã€ remplir par le Warsmith

- [ ] `angle_patterns.json` â€” le catalogue initiale de patterns (peut partir des patterns de base listÃ©s dans F02_TYRANT_CAMP : contrarian, stat_choc, story, myth-busting, POV, rÃ©action, tuto... + combinatoires)
- [ ] `angle_performance.json` â€” vide initialement (structure squelette)
