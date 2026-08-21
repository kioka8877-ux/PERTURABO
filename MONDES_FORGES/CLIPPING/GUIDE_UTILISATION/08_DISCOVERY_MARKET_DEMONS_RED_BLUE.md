# 08_DISCOVERY_MARKET_DEMONS_RED_BLUE — Découverte stratégique

## Principe

Ce mode permet au Champion de fournir uniquement un **marché**, une **plateforme** et un **horizon**. F00_CAPTEURS recherche alors les candidats à partir de preuves observées. Il ne reçoit pas un mot-clé imposé et n’invente jamais de candidats pour remplir un quota.

## Commande

Depuis `MONDES_FORGES/CLIPPING/F00_CAPTEURS/CODEBASE/` :

```bash
python3 capteurs.py --discover-market \
  --market "US residents age 25-45 interested in @Zdak" \
  --platform youtube_shorts \
  --discovery-horizon 3d
```

Pour demander dix angles après la sélection :

```bash
python3 capteurs.py --discover-market \
  --market "US residents age 25-45 interested in @Zdak" \
  --platform youtube_shorts \
  --discovery-horizon 3d \
  --discovery-angles 10 \
  --blue-angles 6 \
  --red-angles 4
```

Le système écrit `OUT/market_discovery_proposal.json`, `OUT/market_discovery_proposal.md` et les copies dans `EXPORT/`. Aucun siège n’est lancé automatiquement.

## Démons

Un Démon est un créateur, une chaîne ou un pattern dominant observé dans le territoire de la cible. Le système conserve son identité, ses titres observés, ses vues, ses URLs, sa pression et son statut. Un Démon n’est pas automatiquement un ennemi : il peut révéler une demande, une saturation ou une faille exploitable.

## Candidats et océans

Le système tente de produire jusqu’à 30 candidats réellement observés. Il ne complète pas artificiellement le quota.

| Camp | Définition |
|---|---|
| Océan rouge | Demande et preuve vidéo fortes, avec pression concurrentielle observée |
| Océan bleu | Demande suffisante, espace moins saturé et hypothèse vérifiable |
| Désert | Faible concurrence sans demande prouvée ; non classé comme bleu |

La répartition 15/15 est une cible d’analyse, pas une obligation. Les horizons disponibles sont `2h`, `6h`, `12h`, `24h`, `3d`, `7d` et `30d`. Une sortie peut contenir moins de 30 candidats ou moins de 15 bleus si les preuves ne suffisent pas.

## Anti-invention et anti-doublons

Les requêtes dérivées du marché sont seulement des sondes. Un candidat doit posséder `observed: true` et des `evidence_urls`. Les candidats similaires sont regroupés par clé normalisée ; le meilleur représentant est conservé et les autres sont enregistrés comme doublons.

Le Champion doit examiner le nombre de candidats inventés, qui doit toujours être égal à zéro, le nombre de doublons supprimés et les preuves de chaque candidat.

## Packs et angles

Les packs de deux candidats sont proposés seulement après le classement. Ils utilisent une ancre de demande et un contraste distinct. L’allocation d’angles est indépendante de la répartition initiale : `6 bleu + 4 rouge` est possible si les deux camps ont assez de candidats disponibles. Sinon, le système retourne `insufficient_candidates` et demande une décision du Champion.

## Validation

L’état de sortie est `warsmith_review`. Le Champion peut valider des candidats, rejeter des doublons, demander des remplacements ou refuser toute la liste. La validation ne doit être suivie d’une production qu’après lecture des preuves, des Démons, du camp et du niveau de confiance.
