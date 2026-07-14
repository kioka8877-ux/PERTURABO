# F05_GRAND_COMPASS — Journal de Mission — Monde-Forge API

> Le Compas — Validation blue ocean et cartographie marché
> Pipeline : scored_target.json + Tavily (recherche web) → blue_ocean_report.json → ARCHIVUM/markets/

| Champ | Valeur |
|-------|--------|
| Frégate | F05_GRAND_COMPASS |
| Rôle | Le Compas — Validation blue ocean et cartographie marché |
| Moteur | anthropic/claude-sonnet-4.6 via AI Gateway |
| IA | IRON — analyse blue ocean + Tavily pour veille web |

## Workflow

```
python grand_compass.py --prepare
# IRON lit iron_prompt.txt → produit blue_ocean_report.json
python grand_compass.py --finalize
```

## Détail

| Analyse | Source |
|---------|--------|
| Marchés adjacents | IRON + ARCHIVUM/rules/ |
| Validation blue ocean | Tavily (recherche live) |
| Cartographie catégories | ARCHIVUM/markets/ (couche froide) |

## Historique des missions

*(Généré automatiquement par grand.py lors des sièges)*
