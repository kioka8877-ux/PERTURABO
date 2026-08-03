# F06_TRACKER â€” TRACKING.md

> *"Le siÃ¨ge n'est fin que lorsque la forteresse a rendu compte. Le tracker ne dort pas."*
> *FrÃ©gate post-publication. Active, pas passive. Boucle le learnings.json et ferme la campagne.*

---

## RÃ”LE

F06_TRACKER est la **frÃ©gate post-Pote 4**. Elle prend le relais aprÃ¨s que les N `production_pack.json` ont Ã©tÃ© expÃ©diÃ©s Ã  OMNIS_WATCH. Pour chaque pack postÃ© par le Warsmith, elle :
1. Active la `submission_checklist`
2. Enregistre la soumission (<1h ou en retard â€” flag si en retard)
3. Logge les vues Ã  1h + 24h (relevÃ©s saisis par le Warsmith ou via API si disponible en v2)
4. Calcule le payout rÃ©el observÃ© vs seuil
5. Nourrit `ARCHIVUM/learnings/learnings.json`
6. Ã€ la fermeture de campagne (dÃ©clarÃ©e par le Warsmith), agrÃ¨ge les rÃ©sultats cumulÃ©s et active la pondÃ©ration future de ANGLESMITH (seuil 50 packs).

---

## INPUTS

| Input | Source | Format | Obligatoire |
|---|---|---|---|
| `production_pack_<angle>.json` (N) | F05_PACKAGER (Porte 4) | JSON N | âœ… |
| Noms de compte publiÃ©s | Warsmith (saisie manuelle au moment de poster) | string | âœ… |
| Vues Ã  1h | Warsmith (saisie manuelle â€” API pas encore disponible en v1) | int | âœ… |
| Vues Ã  24h | Warsmith | int | âœ… |
| Payout rÃ©el | Warsmith (depuis dashboard Whop) | float | âœ… |
| DÃ©claration "fin de campagne" | Warsmith | boolÃ©en | Pour clÃ´turer |

---

## OUTPUTS

### `OUT/submission_log.json`

```json
{
  "campaign_id": "...",
  "campaign_status": "ongoing|closed",
  "packs": [
    {
      "angle_id": "...",
      "platform": "...",
      "market": "...",
      "posted_at": "<ISO8601>",
      "posted_by_account": "<account_slug>",
      "submitted_whop_at": "<ISO8601>",
      "submission_within_1h": true|false,
      "views_1h": N,
      "views_24h": N,
      "payout_expected": "<float or null>",
      "payout_observed": "<float or null>",
      "payout_flag": "low|ok",
      "suggested_flags": ["submission_late|low_payout|low_views|..."],
      "items_closed": [...],
      "items_pending": [...]
    }
  ],
  "cumulative": {
    "packs_count": N,
    "eligible_for_learning_weight": false,  // true si >= 50
    "aggregate_cpm": <float or null>
  },
  "log_event": [
    {"at": "<ISO8601>", "event": "pack_posted|submission_done|view_check|campaign_closed|...", "angle_id": "..."}
  ]
}
```

### Ã€ la fermeture de campagne (Warsmith dÃ©clare "fin") :

- Ã‰crit dans `ARCHIVUM/learnings/learnings.json` (agrÃ©gÃ© cumulatif â€” prÃ©serve les campagnes prÃ©cÃ©dentes)
- Marque `campaign_status: "closed"` dans IW_CUSTOS + liber_clipping.json
- GÃ©nÃ¨re `OUT/campaign_summary.md` â€” synthÃ¨se lisible de ce que la campagne a rapportÃ©
- DÃ©clenche une rÃ©arme possible : le Warsmith peut lancer la campagne suivante (avec archivage/effacement de `ARCHIVUM/campaign/`)

---

## MÃ‰CANIQUE LEARNINGS â€” BOUCLÃ‰E

### Seuil de pondÃ©ration
- **`learnings.json` cumul < 50 packs exÃ©cutÃ©s** : poids nul. ANGLESMITH ne pondÃ¨re pas les angles (tous Ã©gaux, neutres).
- **>= 50 packs cumulÃ©s** : activation progressive. Les angles avec meilleur CPM rÃ©el remontent dans la pondÃ©ration ; les perdants descendent.

### Structure learnings.json

```json
{
  "cumulative_packs_executed": N,
  "eligible_for_weighting": false,  // <- true si N >= 50
  "angle_performance": [
    {
      "angle_family": "...",
      "emotion_mode": "...",
      "engagement_type": "...",
      "reframe_dim": "...",
      "platform": "...",
      "market": "...",
      "packs_count": N,
      "mean_views_24h": N,
      "mean_payout": N,
      "weight": 1.0   // 1.0 = neutre. augmente/diminue progressivement 
                      // quand eligible_for_weighting = true
    }
  ],
  "campaign_history": [
    {"campaign_id": "...", "closed_at": "<ISO8601>", "packs_count": N, "total_payout": N}
  ]
}
```

ANGLESMITH lit `angle_performance[*].weight` pour pondÃ©rer le sÃ©lection d'angles.

---

## PATTERN D'EXÃ‰CUTION

C06 ne fait pas appel Ã  l'IRON ni au modÃ¨le premium. C'est une frÃ©gate purement dÃ©terministe qui:
- Met Ã  jour `submission_log.json` sur saisies Warsmith
- Calcule des agrÃ©gats (CPM, poids)
- Ferme la campagne sur dÃ©claration Warsmith

```
python tracker.py --post --angle <angle_id> --account <slug>   # Marque "postÃ©"
python tracker.py --submit --angle <angle_id>                # Marque "soumis Whop"
python tracker.py --views --angle <angle_id> --1h N --24h N  # Enregistre vues
python tracker.py --payout --angle <angle_id> --amount N     # Enregistre payout
python tracker.py --close-campaign                           # Ferme + agrÃ¨ge learnings
```

---

## CONTRATS RÃ‰FÃ‰RENCÃ‰S

- `ARCHIVUM/rules/whop_rules.md` â€” deadline soumission 1h
- `ARCHIVUM/rules/clipping_rules.md` â€” seuil low payout
- `ARCHIVUM/channels/<account>/performance.json` â€” mis Ã  jour avec chaque pack postÃ©

---

## DÃ‰PENDANCES

- **Amont** : F05_PACKAGER (production packs avec submission_checklist imbriquÃ©e), Warsmith (saisies de vues/payouts)
- **Downstream** :
  - `ARCHIVUM/learnings/learnings.json` (nourri)
  - ANGLESMITH (lit les poids pour pondÃ©ration â€” se dÃ©clenche seulement Ã  partir de 50 packs cumulÃ©s)
  - IW_CUSTOS.py (statut campagne = closed sur action Warsmith)

---

## HÃ‰RÃ‰SIES

- âŒ Auto-poster ou auto-submit (l'opÃ©rateur poste ; C06 logge seulement)
- âŒ Invoquer l'IRON ou le premium (c'est pur mÃ©canique de log + calcul)
- âŒ Activer la pondÃ©ration avant 50 packs cumulÃ©s
- âŒ Omettre la fermeture de campagne (sans `--close-campaign`, la campaign/ reste "ongoing" et CAPTEURS continue Ã  scraper â€” ce qui n'est pas dÃ©sirÃ©)

---

## STATUT

| Phase | Ã‰tat | Notes |
|---|---|---|
| Arborescence crÃ©Ã©e | âœ… | |
| TRACKING.md rÃ©digÃ© | âœ… | Ce fichier |
| Code Python implÃ©mentÃ© | âŒ | Ã€ implÃ©menter |
| `tracker.py` | âŒ | CLI multi-commandes (post/submit/views/payout/close) |
| `libs/learnings_aggregator.py` | âŒ | Calcule poids (seuil 50) |
| `libs/channel_performance_updater.py` | âŒ | Met Ã  jour `ARCHIVUM/channels/<slug>/performance.json` |
| `libs/readings_validator.py` | âŒ | VÃ©rifie cohÃ©rence saisies Warsmith |
| `requirements_c06.txt` | âŒ | Standard lib Python (json, datetime) â€” pas de SDK premium |

*Fer au-dedans, Fer au-dehors. Le siÃ¨ge est fini quand le tracker a fermÃ© le ledger.*
