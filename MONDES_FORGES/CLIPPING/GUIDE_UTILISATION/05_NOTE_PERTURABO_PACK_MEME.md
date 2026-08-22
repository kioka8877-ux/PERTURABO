# 05_NOTE_PERTURABO_PACK_MEME — Note de format à l'attention de PERTURABO

> Note envoyée par **LACRIMAE** (le projet qui consomme le pack, successeur
> d'OMNIS_WATCH — il en fait exactement la même chose : monter la vidéo depuis
> le pack). Cette note fait foi sur le format du pack meme.
> PERTURABO doit la suivre à la lettre.

---

## 1. Objet

Ce document précise les corrections **v2.5** du pack meme. Il complète le
contrat de montage `04_MODE_MEME.md` (doctrine 6 couches) référencé par le
pack via `meme_source.montage_guide_ref`.

## 2. Rappel : référence de la méméthèque

Le champ `meme` d'une vidéo du pack doit pointer vers **les fichiers existants
de la méméthèque LACRIMAE** :

| Valeur attendue | Commentaire |
|---|---|
| `meme_001` | format de meme n°1 historique |
| `meme_002` | format de meme n°2 historique |
| `M1` | balise de release mème validée par le Champion ; sa signification opérationnelle est définie dans le pack du siège |

> ⚠️ Ne pas utiliser `meme_1` / `meme_2` comme identifiants de bibliothèque. Les identifiants historiques `meme_001` / `meme_002` restent valides lorsqu’ils existent dans la méméthèque ; une balise de release comme `M1` est valide lorsqu’elle est explicitement choisie par le Champion et inscrite dans le pack.

## 3. Le champ `tweet` d'une vidéo meme

| Champ | Règle |
|---|---|
| `tweet.text` | fake tweet, **max 3 lignes**, affiché comme faux post quart haut |
| `tweet.keywords_style` | coloration des mots-clés — voir **section 4** |
| `text_emotion` | texte d'émotion au milieu, **max 4 mots** |
| `emotion` | l'émotion de l'angle |
| `duration_sec` | durée du clip en secondes (plage 5-30, défaut 8) |

## 4. Les couleurs (`tweet.keywords_style`) — RÈGLES LACRIMAE

### Règle 1 — FORMAT : un dict, PAS une liste

`tweet.keywords_style` doit être un **dict** à clés anglaises :

```json
{
  "keywords_style": {
    "green": ["degree"],
    "red": ["loans", "interest"]
  }
}
```

- Clés autorisées : `green` (valeur positive) et `red` (danger/négatif).
- **Une liste `[{word, color}]` → AUCUNE couleur** : LACRIMAE n'appliquera
  alors aucune coloration sur le tweet. PERTURABO ne doit donc **jamais**
  produire une liste.

### Règle 2 — MOTS : un seul mot, présent dans `tweet.text`

Chaque entrée de `green` / `red` doit être **un mot seul**, présent dans
`tweet.text` :

- Comparaison **mot à mot**, ponctuation ignorée (les apostrophes, virgules,
  `$`, `#`… ne comptent pas).
- **Les phrases multi-mots ("student loans", "owe more") ne matcheront
  jamais** — elles doivent être découpées en mots simples (`loans`, `owe`).

### Exemple conforme

Tweet :

```
Took out $50K in student loans for a degree
Nobody told me the interest would double it
Now I owe more than my parents' mortgage
```

keywords_style conforme :

```json
{
  "keywords_style": {
    "green": ["degree"],
    "red": ["loans", "interest"]
  }
}
```

## 5. Liste de contrôle pour PERTURABO

- [ ] `meme` = une balise existante et validée par le Champion ; pour le siège New York Bagel, la balise est `M1`
- [ ] ne pas confondre une balise de release de siège (`M1`) avec un ancien identifiant de bibliothèque (`meme_001`)
- [ ] `keywords_style` = dict `{"green": [...], "red": [...]}` (jamais une liste)
- [ ] chaque mot de `green`/`red` est **un mot seul** présent mot à mot dans `tweet.text`
- [ ] pas de phrase multi-mots dans les couleurs


## 6. Texte motion contextualisé

Le champ `text_emotion` est une réaction courte placée au milieu de la vidéo. Il doit identifier les personnes réellement présentes dans le fake tweet et se terminer par `:`. Exemples : `My sister and me right now:`, `The two neighbors right now:` ou `My roommate and me right now:`. Les formes génériques, les marqueurs `A:` / `B:`, les personnages absents et les résidus d’un autre siège sont interdits.

Le texte motion ne doit pas être copié mécaniquement d’un angle à l’autre. Le contexte, la relation et le ressort comique doivent être contrôlés angle par angle afin d’éviter le cannibalisme de forme.

## 7. Validation de release

F05 assemble le pack, mais ne décide pas de la Gate. Le Champion examine les dix tweets, les dix textes motion, les métadonnées et la balise mème avant l’export. La copie dans `EXPORT/` et l’expédition à LACRIMAE ne sont permises qu’après cette validation explicite.

La clé premium sert à la génération éditoriale lorsqu’elle est activée ; F05 reste un assembleur déterministe et ne doit pas simuler un appel premium.
