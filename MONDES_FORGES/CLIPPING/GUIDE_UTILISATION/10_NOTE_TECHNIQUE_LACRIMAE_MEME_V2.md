# Note technique — Intégration LACRIMAE / MEME V2

**Version :** 1.0  
**Statut :** proposition de contrat d’intégration  
**Producteur :** PERTURABO  
**Consommateur :** LACRIMAE  
**Mode :** MEME V2 — source sociale fournie manuellement

> Cette note définit comment LACRIMAE doit consommer un pack MEME V2. Elle sépare strictement la source originale du post et la contribution créative de PERTURABO. Elle ne donne aucun droit automatique de réutilisation ni aucune garantie de monétisation.

## 1. Objectif

LACRIMAE reçoit un pack prêt à produire. Le pack contient une capture PNG du tweet ou post original, la copie textuelle de cette source, un `reaction_tweet` original, un `text_emotion` court et les métadonnées éditoriales. LACRIMAE doit rendre une vidéo courte dans laquelle le spectateur comprend immédiatement ce qui vient de la source et ce qui constitue la réaction PERTURABO.

LACRIMAE ne doit pas inventer une nouvelle blague, réécrire la source, remplacer la réaction ou fabriquer des métadonnées. Sa responsabilité est le rendu audiovisuel, la lisibilité, le rythme, la séparation visuelle des couches et le retour d’un statut de production.

## 2. Contrat minimal d’entrée

Le pack doit contenir une entrée par angle. En MEME V2, le champ `source_post` est obligatoire et le champ `perturabo_reaction` est séparé.

```json
{
  "schema_version": "meme_v2.1",
  "pack_id": "meme_v2_<campaign_id>_<angle_id>",
  "campaign_id": "...",
  "angle_id": "A01",
  "mode": "meme_v2",
  "meme_tag": "M1",
  "target": {
    "platform": "youtube_shorts",
    "market": "US",
    "language": "en"
  },
  "source_post": {
    "text": "copie exacte du tweet ou post original",
    "screenshot_png": "assets/source_A01.png",
    "url": "https://...",
    "author": "@source_account",
    "observed_at": "2026-08-24T12:00:00Z",
    "metrics": {
      "likes": null,
      "views": null,
      "comments": null,
      "reposts": null
    },
    "credit_display": "Source: @source_account"
  },
  "perturabo_reaction": {
    "reaction_angle": "...",
    "reaction_tweet": "commentaire original et transformateur",
    "text_emotion": "Student borrowers seeing this:",
    "emotion": "incredulous"
  },
  "metadata": {
    "title": "...",
    "description": "...",
    "tags": ["..."],
    "hashtags": ["..."]
  },
  "render": {
    "duration_sec": 8,
    "aspect_ratio": "9:16",
    "source_position": "upper",
    "reaction_position": "lower",
    "motion_position": "center"
  }
}
```

Les chemins sont relatifs à la racine du pack ou à l’URI d’assets fournie par l’interface. Les métriques inconnues doivent rester `null` ; LACRIMAE ne doit jamais les compléter par une estimation.

## 3. Rôle de chaque élément

| Élément | Usage par LACRIMAE | Interdiction |
|---|---|---|
| `source_post.screenshot_png` | Capture visuelle du post original | Ne pas la retoucher au point de changer son sens |
| `source_post.text` | Référence de contrôle et, si nécessaire, sous-titrage accessible | Ne pas la présenter comme un texte PERTURABO |
| `source_post.credit_display` | Attribution visible ou crédit de description | Ne pas supprimer l’attribution fournie |
| `perturabo_reaction.reaction_tweet` | Commentaire original central | Ne pas le paraphraser ou le remplacer |
| `perturabo_reaction.text_emotion` | Texte motion court au centre de la composition | Ne pas utiliser un personnage absent ou un résidu d’un autre siège |
| `metadata` | Titre, description, tags et hashtags de publication | Ne pas ajouter de promesse de fair use ou de monétisation |
| `meme_tag` | Sélection du format visuel, ici `M1` | Ne pas le confondre avec l’ID de la source |

## 4. Pipeline de rendu recommandé

LACRIMAE doit suivre les étapes suivantes pour chaque entrée :

1. **Valider l’entrée.** Vérifier les champs obligatoires, l’existence du PNG, la présence du tweet réaction et la cohérence entre `angle_id`, texte et métadonnées. Si une donnée manque, retourner `blocked` plutôt que d’inventer.
2. **Afficher la source.** Introduire la capture originale assez longtemps pour être lisible. Préserver l’interface et le contexte utiles ; ne pas masquer le crédit lorsque celui-ci est fourni.
3. **Afficher le texte motion.** Utiliser `text_emotion` comme réaction visuelle courte, avec une typographie lisible et un emplacement stable. Le motion doit être affiché exactement comme fourni, sauf adaptation technique de casse ou de longueur validée.
4. **Afficher ou mettre en scène la réaction.** La réaction PERTURABO doit être clairement séparée de la capture source. Elle peut apparaître comme texte overlay ou sous-titrage selon la configuration de LACRIMAE, mais elle doit rester le commentaire ajouté, pas une fausse citation de l’auteur original.
5. **Créer la chute.** Le montage doit donner priorité au `reaction_tweet` et à sa chute. Aucun nouveau contenu narratif ne doit être inventé par LACRIMAE.
6. **Contrôler la sortie.** Vérifier la lisibilité sur mobile, l’absence de texte coupé, la présence du crédit, la correspondance avec l’angle et l’absence de résidu d’un autre pack.
7. **Retourner le statut.** Émettre `ready`, `needs_revision` ou `blocked` avec les erreurs détaillées et le hash du pack consommé.

## 5. Chronologie indicative pour une vidéo de 8 secondes

La durée exacte vient du pack. Pour une durée de 8 secondes, le découpage recommandé est indicatif et peut être ajusté par LACRIMAE sans changer le contenu éditorial :

| Temps | Couche | Fonction |
|---:|---|---|
| 0,0–0,8 s | Capture + hook visuel | Identifier rapidement la source |
| 0,8–2,0 s | `text_emotion` | Montrer qui réagit ou quelle audience se reconnaît |
| 2,0–6,8 s | `reaction_tweet` | Déployer l’observation et le contraste |
| 6,8–8,0 s | Chute / maintien | Laisser la chute lisible et permettre une boucle propre |

Cette chronologie ne doit pas forcer une réaction à être raccourcie jusqu’à devenir incompréhensible. Si le texte ne tient pas dans la durée, LACRIMAE retourne `needs_revision` ; il ne réécrit pas silencieusement.

## 6. Règles visuelles obligatoires

La capture source doit être identifiable comme une capture d’un post réel. Le commentaire PERTURABO doit avoir un traitement visuel distinct : position, hiérarchie typographique ou fond différent. La source ne doit pas être présentée comme si elle avait été écrite par PERTURABO.

Le `text_emotion` est court, généralement inférieur ou égal à quatre mots utiles avant le deux-points, et doit correspondre au contexte. Des exemples acceptables sont `Young adults seeing this:`, `Student borrowers seeing this:`, `My sister and me right now:` et `The neighbors watching this:`. Les marqueurs `A:` et `B:`, les personnes absentes et les formules héritées d’une ancienne campagne sont interdits.

Le même `meme_tag` M1 peut être utilisé pour plusieurs angles si le Champion l’a décidé. Cette réutilisation du format visuel ne doit pas entraîner la réutilisation du même `reaction_tweet`, de la même chute ou du même `text_emotion`.

## 7. Métadonnées de publication

LACRIMAE doit transmettre les métadonnées sans les mélanger avec la source. Le titre doit refléter la réaction et le marché sans prétendre être le titre du post original. La description doit pouvoir créditer la source et décrire la contribution PERTURABO. Les tags et hashtags doivent rester ceux du pack validé.

Le pack ne doit pas utiliser le mot `fair use` comme argument marketing ou comme garantie. Une transformation créative, une attribution et une analyse de conformité peuvent être documentées, mais la décision de publication et la monétisation dépendent des faits, des droits concernés et des règles de la plateforme.

## 8. États et retour d’exécution

LACRIMAE doit retourner un résultat machine-readable par `pack_id` :

```json
{
  "pack_id": "meme_v2_<campaign_id>_<angle_id>",
  "status": "ready|needs_revision|blocked",
  "rendered_asset": "...",
  "input_sha256": "...",
  "checks": {
    "source_png_readable": true,
    "source_credit_present": true,
    "reaction_present": true,
    "motion_present": true,
    "metadata_present": true,
    "source_reaction_separated": true,
    "foreign_siege_residue": false
  },
  "errors": [],
  "rendered_at": "2026-08-24T12:00:00Z"
}
```

`ready` signifie que le rendu respecte le contrat technique ; cela ne signifie pas que le Champion a validé la publication. `needs_revision` indique une correction de rendu ou de lisibilité. `blocked` indique une absence de source, d’asset, de crédit ou de champ obligatoire.

## 9. Contrôles anti-erreur

LACRIMAE doit bloquer le pack dans les cas suivants : PNG absent ou illisible, source et réaction fusionnées de manière trompeuse, texte motion absent, réaction vide, métadonnées provenant d’un autre angle, crédit supprimé, résidu détecté d’un autre siège, durée impossible ou texte coupé. LACRIMAE doit également refuser de produire une citation attribuée à l’auteur lorsque le texte est une réaction PERTURABO.

Le contrôle de similarité doit comparer les `reaction_tweet`, les `text_emotion` et les structures de rendu des angles d’un même pack. Si plusieurs angles sont quasi identiques, LACRIMAE retourne un signal de révision ; la correction éditoriale revient à PERTURABO et au Champion, pas au moteur de rendu.

## 10. Interfaces et ordre des opérations

La première version peut fonctionner par dépôt de fichiers : LACRIMAE lit le JSON du pack, charge le PNG relatif, rend les vidéos dans un répertoire de sortie et écrit le rapport de statut. Une interface API pourra ensuite exposer `POST /meme-v2/render`, `GET /meme-v2/jobs/{pack_id}` et `GET /meme-v2/assets/{pack_id}` ; cette API ne doit être implémentée qu’après accord sur le schéma d’authentification et le stockage.

L’ordre opérationnel est :

```text
PERTURABO crée le pack
→ Champion valide le contenu
→ F05 assemble hors EXPORT
→ Champion valide le pack
→ pack copié dans EXPORT
→ LACRIMAE ingère le pack
→ LACRIMAE rend et contrôle
→ LACRIMAE retourne le statut
→ publication éventuelle
→ F06 suit les résultats
```

LACRIMAE ne doit jamais publier directement sur la seule réception d’un pack `ready` si la signature de validation Champion n’est pas présente dans le manifeste. Le rendu technique et l’autorisation éditoriale sont deux états différents.

## 11. Critères d’acceptation

L’intégration MEME V2 sera considérée comme fonctionnelle lorsque LACRIMAE pourra ingérer un pack contenant un PNG, une source textuelle, une réaction, un motion et des métadonnées ; produire une vidéo verticale lisible ; séparer visuellement source et transformation ; conserver le crédit ; retourner un statut déterministe ; et bloquer proprement les packs incomplets ou contaminés.

Cette note est une **proposition de contrat technique**. Elle devient la référence d’implémentation après validation du Champion et doit ensuite être synchronisée avec le schéma JSON et le guide de production LACRIMAE.

## Références internes

- `GUIDE_UTILISATION/04_MODE_MEME.md`
- `GUIDE_UTILISATION/05_NOTE_PERTURABO_PACK_MEME.md`
- `F05_PACKAGER/CODEBASE/TRACKING.md`
- `EXPORT/production_pack_meme_new_york_bagel.json`


## Addendum contractuel — source sociale et rendu final

Le modèle définitif du mode MEME V2 distingue la **copie textuelle interne** de la **capture PNG de production**. Le Champion fournit à PERTURABO le texte copié et la capture pour permettre l’analyse sans modèle de vision obligatoire. Le texte copié sert à F01, ANGLESMITH et F04 ; il n’est pas une couche obligatoire du pack final.

La capture PNG, en revanche, est un asset obligatoire du pack final : elle contient déjà le tweet et son image et doit être affichée au-dessus de la vidéo mème par LACRIMAE. La vidéo mème de base provient de la release LACRIMAE et est référencée par `clip_id` et `meme_tag`. La chaîne de destination `channel_id` est fournie par l’Opérateur pour chaque clip.

Le rendu final attendu est donc :

```text
capture PNG du tweet en haut
+ vidéo mème de la release en bas
+ reaction_tweet PERTURABO
+ text_emotion contextualisé
+ métadonnées de publication
```

Dans le pack MEME V2, `source_post.screenshot_png` est obligatoire, tandis que `source_post.text` reste dans l’archive F01 et dans les inputs internes de PERTURABO. F05 doit transmettre la capture, la provenance, le `clip_id`, le `meme_tag`, le `channel_id`, la réaction, le motion et les métadonnées ; il ne doit pas transmettre la copie textuelle brute comme couche éditoriale séparée.

LACRIMAE réalise la vidéo finale, mais ne choisit ni le tag du mème ni la chaîne. Il doit bloquer le pack si la capture, le clip, le tag ou la chaîne manquent, sans inventer de valeur.
