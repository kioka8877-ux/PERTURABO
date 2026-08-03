# ARCHIVUM/learnings/ â€” Boucle rÃ©tro-active

> *MÃ©moire cumulÃ©e des perf rÃ©elles par angle. Nourrit ANGLESMITH pour pondÃ©ration progressive.*

---

## Fichier attendu

### `learnings.json`

```json
{
  "cumulative_packs_executed": 0,
  "eligible_for_weighting": false,
  "angle_performance": [],
  "campaign_history": []
}
```

## MÃ©canique

### Seuil de pondÃ©ration
- `cumulative_packs_executed < 50` : `eligible_for_weighting = false`. ANGLESMITH ne pondÃ¨re pas â€” tous les angles sont neutral (weight = 1.0).
- `cumulative_packs_executed >= 50` : `eligible_for_weighting = true`. ANGLESMITH lit les `weight` et pondÃ¨re les angles (gagnants montent, perdants descendent).

### Structure de `angle_performance[]`

```json
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
  "weight": 1.0
}
```

`weight` commence Ã  1.0 (neutre). Au fil du temps (> 50 packs), augmente/diminue selon la perf relative de l'angle vs mÃ©diane.

### Structure de `campaign_history[]`

```json
{
  "campaign_id": "...",
  "closed_at": "<ISO8601>",
  "packs_count": N,
  "total_payout": N
}
```

## Mise Ã  jour

- Nourri par F06_TRACKER Ã  chaque fermeture de campaigne (`--close-campaign`)
- Lu par ANGLESMITH Ã  la Porte 2 pour pondÃ©rer les angles forgÃ©s

## Statut initial

`squelette.json` prÃ©sent pour servir de dÃ©marrage. F06_TRACKER doit le charger au premier siÃ¨ge, l'enrichir, le sauvegarder.
