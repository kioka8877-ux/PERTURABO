# _PIEGES_APPRIS — Les leçons du siège test

> Chaque erreur listée ici a **coûté du temps en vrai** pendant le siège TS01_SANDOVAL.
> Les lire AVANT chaque siège évite de les repayer. ⏱️ 5 minutes.

---

## 1. 🗂️ Le dossier `OUT/` des frégates est GITIGNORÉ

**Le problème** : `production_pack_logo.json` vit dans `F05_PACKAGER/OUT/` → gitignoré par design (`**/OUT/*.json`). Résultat : le lien `raw.githubusercontent.com` donnait **404** et OMNIS_WATCH ne pouvait pas récupérer le pack.

**La solution** : copier le pack dans `EXPORT/` (hors OUT) et pousser :
```bash
cp F05_PACKAGER/OUT/production_pack_logo.json EXPORT/production_pack_logo.json
git add MONDES_FORGES/CLIPPING/EXPORT/ && git commit -m "export pack" && git push origin main
```
→ **Règle d'or** : *tout livrable OMNIS_WATCH passe par `EXPORT/`, jamais par `OUT/`.*

## 2. 📝 Le fair use = clause Section 107 (EN), PAS une note d'illustration

**Le problème** : la première version du pack contenait une note « videos serve purely as illustration » (ou la vieille note FR `d'illustration`). Le commanditaire exige le **paragraphe 107 officiel** (Copyright Act 1976), en **anglais US**.

**La solution** : la clause 107 complète est maintenant la valeur par défaut (`FAIR_USE_NOTE` dans `copywriter.py`). Vérification rapide :
```bash
python3 -c "import json; p=json.load(open('MONDES_FORGES/CLIPPING/F05_PACKAGER/OUT/production_pack_logo.json')); print(sum(1 for v in p['videos'] if 'Section 107' in v['metadata']['description']), '/', len(p['videos']), 'clause 107')"
```
→ Si un `< 5` : les descriptions ne sont pas conformes.

## 3. ✂️ Le résumé doit tenir en 2 LIGNES

**Le problème** : la première mouture des descriptions avait un résumé en 1 paragraphe long. La spec exige un **paragraphe de résumé en 2 lignes** en tête de description, puis le paragraphe fair use.

**La leçon** : à la gate 3, on montre le texte RÉEL (pas un « résumé de résumé ») et le résumé doit être court et factuel.

## 4. 🔑 La clé premium n'arrive pas toujours dans le sandbox

**Le problème** : `CLIPPING_PREMIUM_API_KEY` (API Keys) n'était pas lue par F04 pendant le test → `--generate` plantait (« Clé premium absente »).

**La solution** : le mode backup `--oracle` :
```bash
python3 copywriter.py --generate --angle A01 --oracle
```
→ F04 écrit le prompt dans `F04_COPYWRITER/IN/premium_call_A01.json`, l'Oracle forge `OUT/text_payload_raw_A01.json`, on relance, ça passe. **Même pipeline, même validation, juste une source de génération différente.**

## 5. 🚪 Le vocabulaire « porte » vs « gate »

**Le problème** : le ledger utilise `porte` (liber_clipping.json → `portes_validated`, `current_porte`), mais tout le monde dit **gate** en conversation.

**La leçon** : les deux désignent la même chose. `current_porte: p4` = la gate 4 est la prochaine. Ne pas s'étonner en lisant le ledger.

## 6. 🧵 Le `--start-siege` écrase la configuration du mode logo

**Le problème** : re-lancer `--start-siege` peut réinitialiser/écraser l'état du siège en cours (mode logo → défaut).

**La leçon** : ne JAMAIS relancer `--start-siege` en cours de siège. Vérifier l'état avec `--status` avant. Si le siège a tourné par erreur, les logs de `TRACKING/CLIPPING_LOG.md` montrent la trace.

## 7. 📝 Remplacer du texte dans un JSON = RISQUE DE CORRUPTION

**Le problème** : lors du remplacement de la clause fair use par `str_replace` sur les `text_payload_*.json`, un fichier s'est retrouvé **corrompu** (JSON invalide → le pack ne se régénérait pas).

**La leçon** : après toute édition manuelle d'un JSON, **toujours valider** :
```bash
python3 -c "import json; [json.load(open(f'MONDES_FORGES/CLIPPING/F04_COPYWRITER/OUT/text_payload_{a}.json')) for a in ['A01','A02','A03','A04','A05']]; print('JSON OK')"
```

## 8. 🏗️ En mode logo, F03 est SKIPPÉ

**Le problème** : les « Artefact introuvable » affichés lors des validations de gate sont normaux en mode logo — le pipeline attend des artefacts de F03 qui n'existe pas dans ce mode.

**La leçon** : en mode logo, le flux est F01 → F02 (verdict + angles) → F04 (textes) → F05 (pack). Pas de F03. Ce n'est pas une erreur.

---

## 🧭 Comment utiliser ces leçons

- Avant chaque siège : relire cette page.
- Si tu rencontres une erreur **pas encore listée** : la noter ici (et dans `TRACKING/CLIPPING_LOG.md`) pour le prochain champion.

## 9. Le Directeur premium ne remplace pas les preuves

Le premium peut diriger l’interrogation, mais il ne remplace pas les capteurs. Il formule les hypothèses, questions et requêtes ; l’Oracle collecte les réponses et conserve les URLs, dates et métriques. Une question premium n’est jamais une preuve.

Ne jamais laisser le premium remplir un quota de candidats, inventer une URL, compléter une métrique absente, transformer un désert en océan bleu ou présenter une interprétation comme une observation. Si la clé est absente, le fallback déterministe doit rester explicite.

## 10. La boucle adaptative est limitée

Le Directeur dispose de trois tours maximum. Un tour supplémentaire doit répondre à une lacune identifiée : preuve YouTube absente, Démon incomplet, contradiction, doublon ou hypothèse d’océan bleu non vérifiée. Une collecte qui n’améliore plus la preuve doit s’arrêter.

## 11. Faits et interprétations restent séparés

Les réponses brutes de l’Oracle et les analyses du Directeur doivent rester dans des blocs séparés. Avant validation Champion, vérifier `invented = 0`, les URLs autorisées, les sources, le statut de confiance et l’état `warsmith_review`.
