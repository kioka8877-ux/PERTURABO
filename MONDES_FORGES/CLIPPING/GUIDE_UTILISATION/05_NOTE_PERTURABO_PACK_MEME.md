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
| `meme_001` | format de meme n°1 |
| `meme_002` | format de meme n°2 |

> ⚠️ **Ne PAS** utiliser `meme_1` / `meme_2` : ces noms ne correspondent à
> aucun fichier de la méméthèque. Seuls `meme_001` / `meme_002` matchent.

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

- [ ] `meme` = `meme_001` ou `meme_002` (jamais `meme_1` / `meme_2`)
- [ ] `keywords_style` = dict `{"green": [...], "red": [...]}` (jamais une liste)
- [ ] chaque mot de `green`/`red` est **un mot seul** présent mot à mot dans `tweet.text`
- [ ] pas de phrase multi-mots dans les couleurs
