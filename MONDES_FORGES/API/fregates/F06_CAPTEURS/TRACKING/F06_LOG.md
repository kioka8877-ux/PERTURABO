# F06_CAPTEURS — Journal de Mission — Monde-Forge API

> Les Capteurs — Surveillance continue post-déploiement
> Pipeline : deployed_urls.json + ARCHIVUM/ledgers/ → ARCHIVUM/ledgers/ mis à jour + ARCHIVUM/rules/ (patterns gagnants)

| Champ | Valeur |
|-------|--------|
| Frégate | F06_CAPTEURS |
| Rôle | Les Capteurs — Surveillance continue post-déploiement |
| Moteur | anthropic/claude-haiku-4.5 via AI Gateway |
| IA | IRON léger — analyse patterns de survie |

## Workflow

```
python capteurs.py --daily-scan
# Tournant via GitHub Actions — quotidien
python capteurs.py --finalize
```

## Détail

| Surveillance | Seuil d'alerte |
|-------------|---------------|
| Abonnés RapidAPI par Iron Warrior | >= 5 → pattern gagnant |
| Stars GitHub | Croissance anormale → signal |
| Nouveaux entrants catégorie | Détecté → alerte Warsmith |

## Historique des missions

*(Généré automatiquement par capteurs.py lors des sièges)*
