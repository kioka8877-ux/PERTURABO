# COPYWRITER SYSTEMPROMPT — Placeholder

> * STATUT : NON GÉNÉRÉ — à générer par le modèle premium à l'init. *

---

## Qu'est-ce que ce fichier ?

`copywriter_systemprompt.md` est le **system prompt** utilisé par F04_COPYWRITER à chaque exécution de Phase B (premium_generation).

Il est **figé après initialisation**. Il n'est jamais réécrit sauf si le Warsmith décide volontairement de refaire une init (par exemple après une mise à jour majeure de `copywriting_doctrine.md`).

---

## Comment est-il généré ?

Procédure one-time :

```
1. Le Warsmith remplit CONTRACTS/copywriting_doctrine.md (toutes les sections I-X)
2. Le Warsmith peuple ARCHIVUM/copywriting/ (8 sous-dossiers) avec son savoir
3. Le Warsmith exécute un script d'init (à implémenter) :
   python copywriter.py --init-systemprompt
4. Ce script :
   - Lit copywriting_doctrine.md
   - Lit ARCHIVUM/copywriting/ (8 sous-dossiers)
   - Lit ARCHIVUM/knowledge_base/ (sites, docs, transcripts)
   - Lit ARCHIVUM/rules/ (clipping_rules, whop_rules, platform_*)
   - Construit un meta-prompt qui demande au modèle premium 
     "Génère le system prompt final pour F04_COPYWRITER 
     à partir de toute cette matière"
   - Premium génère
   - Sauvegarde dans copywriter_systemprompt.md
5. Ce fichier est figé
6. À chaque opération F04, on utilise ce system prompt
```

---

## Format attendu du system prompt final

- Contexte : rôle de la frégate, sa singularité (4 phases, premium direct)
- Doctrine : résumé des 10 sections de copywriting_doctrine.md
- Capacités : ce que la frégate DOIT produire (3 titres + paragraphe + caption + hashtags + on-screen + cta)
- Contraintes : format de sortie JSON strict (cf. `text_payload_*.json` schema dans `F04_COPYWRITER/CODEBASE/TRACKING.md`)
- Garde-fous : anti-bullshit, FTC, hérésies (section X de la doctrine)

---

## STATUT

Le fichier est vide (placeholder). À générer à la première init.
