# COPYWRITER SYSTEMPROMPT â€” Placeholder

> * STATUT : NON GÃ‰NÃ‰RÃ‰ â€” Ã  gÃ©nÃ©rer par le modÃ¨le premium Ã  l'init. *

---

## Qu'est-ce que ce fichier ?

`copywriter_systemprompt.md` est le **system prompt** utilisÃ© par F04_COPYWRITER Ã  chaque exÃ©cution de Phase B (premium_generation).

Il est **figÃ© aprÃ¨s initialisation**. Il n'est jamais rÃ©Ã©crit sauf si le Warsmith dÃ©cide volontairement de refaire une init (par exemple aprÃ¨s une mise Ã  jour majeure de `copywriting_doctrine.md`).

---

## Comment est-il gÃ©nÃ©rÃ© ?

ProcÃ©dure one-time :

```
1. Le Warsmith remplit CONTRACTS/copywriting_doctrine.md (toutes les sections I-X)
2. Le Warsmith peuple ARCHIVUM/copywriting/ (8 sous-dossiers) avec son savoir
3. Le Warsmith exÃ©cute un script d'init (Ã  implÃ©menter) :
   python copywriter.py --init-systemprompt
4. Ce script :
   - Lit copywriting_doctrine.md
   - Lit ARCHIVUM/copywriting/ (8 sous-dossiers)
   - Lit ARCHIVUM/knowledge_base/ (sites, docs, transcripts)
   - Lit ARCHIVUM/rules/ (clipping_rules, whop_rules, platform_*)
   - Construit un meta-prompt qui demande au modÃ¨le premium 
     "GÃ©nÃ¨re le system prompt final pour F04_COPYWRITER 
     Ã  partir de toute cette matiÃ¨re"
   - Premium gÃ©nÃ¨re
   - Sauvegarde dans copywriter_systemprompt.md
5. Ce fichier est figÃ©
6. Ã€ chaque opÃ©ration C04, on utilise ce system prompt
```

---

## Format attendu du system prompt final

- Contexte : rÃ´le de la frÃ©gate, sa singularitÃ© (4 phases, premium direct)
- Doctrine : rÃ©sumÃ© des 10 sections de copywriting_doctrine.md
- CapacitÃ©s : ce que la frÃ©gate DOIT produire (3 titres + paragraphe + caption + hashtags + on-screen + cta)
- Contraintes : format de sortie JSON strict (cf. `text_payload_*.json` schema dans `F04_COPYWRITER/CODEBASE/TRACKING.md`)
- Garde-fous : anti-bullshit, FTC, hÃ©rÃ©sies (section X de la doctrine)

---

## STATUT

Le fichier est vide (placeholder). Ã€ gÃ©nÃ©rer Ã  la premiÃ¨re init.
