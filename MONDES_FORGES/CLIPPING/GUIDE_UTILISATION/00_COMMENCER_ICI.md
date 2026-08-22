# 00_COMMENCER_ICI — Le strict minimum pour lancer un siège

> À lire en premier. Après ça, ouvre le guide de ton mode (`01_MODE_LOGO_INFORMATIF.md` par défaut).
> ⏱️ Temps de lecture : 5 minutes.

---

## 1. Les 3 choses à savoir avant tout

1. **Tu es le Champion (Warsmith).** Rien ne se valide sans TOI. Chaque gate = ta signature.
2. **Tout tourne sur du Python stdlib.** Aucune installation de dépendances requise. On lance les scripts depuis leur dossier `CODEBASE/`.
3. **Le dossier `OUT/` des frégates est gitignoré** (sorties runtime). Pour livrer un pack, on le copie dans `EXPORT/` (sinon OMNIS_WATCH ne peut pas le récupérer sur GitHub).

## 2. L'état du siège en un coup d'œil

```bash
cd MONDES_FORGES/CLIPPING/ORCHESTRATOR/CODEBASE
python3 orchestrator.py --status
```

Ou directement dans le ledger :

```bash
python3 -c "import json; d=json.load(open('MONDES_FORGES/CLIPPING/liber_clipping.json')); print('portes:', d.get('portes_validated'), '| current:', d.get('current_porte'), '| status:', d.get('campaign_status'))"
```

- `portes_validated: ['1','2','3']` → tu as validé jusqu'à la gate 3, la gate 4 est la prochaine.
- `current_porte: closed` → siège terminé.
- `campaign_status: active` → la campagne tourne.
- `campaign_status: closed` → siège isolé ; aucun résidu ne doit être repris automatiquement.

La fermeture de la campagne est distincte de la validation d’une Gate : seul le Champion décide des Gates, puis IW_CUSTOS enregistre la clôture après l’export.

## 3. La séquence type d'un siège (résumé)

```
1. Déposer les inputs dans ARCHIVUM/campaign/  (directive + reference_clip + article/joke)
2. orchestrator.py --start-siege               (ouvre le siège)
3. Gate 1 : verdict  →  valider
4. Gate 2 : angles   →  valider
5. Gate 3 : textes   →  valider
6. Gate 4 : pack → valider → copie dans EXPORT/ → transmission à LACRIMAE
7. Après l’export : fermer le siège avec `IW_CUSTOS.py --mode close-campaign`
8. Commit + push GitHub des artefacts de production, sans secrets ni fichiers temporaires
```

Chaque étape détaillée est dans `01_MODE_LOGO_INFORMATIF.md`.

## 4. La clé premium (une seule chose à savoir)

- **Avec clé** : la clé `CLIPPING_PREMIUM_API_KEY` doit être dans API Keys (Freebuff) → les textes sont forgés par le modèle premium.
- **Sans clé (backup)** : ajoute `--oracle` à la commande F04 → l'Oracle (l'assistant) forge les textes à la main. **Le pipeline ne change pas**, tu valides exactement la même chose.

## 5. Les 3 pièges qui font perdre du temps (détail dans _PIEGES_APPRIS.md)

1. **`OUT/` gitignoré** → copie le pack dans `EXPORT/` AVANT de pousser sur GitHub.
2. **Le fair use** doit être la **clause Section 107 (EN)** — pas une vieille note d'illustration.
3. **Le résumé de la description** doit tenir en **2 lignes** (l'utilisateur valide le texte réel, pas un résumé de résumé).

## 6. Les liens utiles

| Quoi | Où |
|---|---|
| Le ledger central | `MONDES_FORGES/CLIPPING/liber_clipping.json` |
| Le log des événements | `MONDES_FORGES/CLIPPING/TRACKING/CLIPPING_LOG.md` |
| La campagne en cours | `MONDES_FORGES/CLIPPING/ARCHIVUM/campaign/` |
| Les règles logo Clipster | `MONDES_FORGES/CLIPPING/PROFILES/logo/CONTRACTS/clipping_rules_logo.md` |
| Les packs livrés | `MONDES_FORGES/CLIPPING/F05_PACKAGER/OUT/` + `EXPORT/` |

---

👉 **Tu es prêt.** Ouvre maintenant le guide du mode choisi ; pour le mode MEME, commence par `04_MODE_MEME.md`, puis lis `05_NOTE_PERTURABO_PACK_MEME.md`.
