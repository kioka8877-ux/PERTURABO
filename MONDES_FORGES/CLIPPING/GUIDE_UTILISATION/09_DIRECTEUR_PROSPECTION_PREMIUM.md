# 09_DIRECTEUR_PROSPECTION_PREMIUM — Le Directeur de prospection

## Rôle

Le Directeur de prospection est la couche premium facultative de F00_CAPTEURS. Il ne remplace pas les capteurs et ne constitue pas une source de vérité. Il formule les hypothèses, les questions, les requêtes et les besoins de vérification ; l’Oracle exécute ensuite les recherches autorisées et conserve les réponses brutes.

> Le Directeur choisit les bonnes questions. L’Oracle collecte les réponses réelles. Le Champion valide la décision.

## Activation

Le mode déterministe reste le défaut :

```bash
python3 capteurs.py --discover-market \
  --market "US residents age 25-45 interested in @Zdak" \
  --platform youtube_shorts \
  --discovery-horizon 3d
```

Le Directeur premium est demandé explicitement :

```bash
python3 capteurs.py --discover-market \
  --market "US residents age 25-45 interested in @Zdak" \
  --platform youtube_shorts \
  --discovery-horizon 3d \
  --premium-director
```

La clé premium doit rester dans la configuration secrète existante. Elle ne doit jamais être écrite dans GitHub, les sorties JSON, les logs ou les prompts archivés.

## Boucle de prospection

Le Directeur intervient avant la collecte. Il produit un plan de questions avec un objectif, des requêtes, des sources autorisées et les preuves attendues. Les requêtes validées sont ensuite transmises aux capteurs.

```text
Marché / plateforme / horizon
        ↓
Questions et requêtes du Directeur
        ↓
Validation des sources et limites
        ↓
Collecte Oracle réelle
        ↓
Payload brut avec URLs, dates et métriques
        ↓
Démons, déduplication, océans rouge/bleu
        ↓
Validation du Champion
```

La session autorise au maximum trois tours, dix questions par tour et six requêtes par question. Un nouveau tour doit correspondre à une lacune identifiée : preuve YouTube insuffisante, Démon non cartographié, doublon, contradiction ou hypothèse d’océan bleu à vérifier.

## Anti-invention

Le Directeur peut proposer une question, mais il ne peut pas déclarer un résultat que les capteurs n’ont pas observé. Les faits bruts et l’interprétation premium restent dans des blocs séparés. Toute URL ou métrique absente du payload est bloquée par le garde-fou.

Si la clé est absente ou si l’appel premium échoue, le système conserve les questions déterministes et signale l’état `premium_unavailable` ou `error`. Il ne simule jamais une analyse premium.

## Sorties

La proposition de découverte contient `prospection_session`, `question_plan`, `demon_map`, les candidats, les scores et les preuves. La session conserve l’identité du marché, les tours, les questions, les réponses et l’état `warsmith_review`.

Le Champion examine d’abord les questions et les preuves, puis valide, rejette ou demande un nouveau tour. Aucun siège n’est déclenché automatiquement.
