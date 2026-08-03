# ARCHIVUM/campaign/ â€” LA campagne en cours (singulier)

> *Une seule campagne Ã  la fois. Quand on en finit une, on archive ou on efface, et on repart vierge.*
> *Chaque campagne est un cas isolÃ© â€” pas de mÃ©moire comparative en parallÃ¨le.*

---

## Pourquoi singulier ?

Chaque campagne Whop est diffÃ©rente : assets diffÃ©rents, niche diffÃ©rente, mÃ©cÃ¨ne diffÃ©rent. La mÃ©moire comparative n'a pas de valeur sur des unitÃ©s non-comparables. La campagne en cours reste seule, isolÃ©e, comme une forteresse sous siÃ¨ge.

## Fichiers attendus (au runtime)

| Fichier | RÃ´le | Qui l'Ã©crit | Quand |
|---|---|---|---|
| `directive.md` | Goal doc Whop tel quel | Warsmith | Avant Porte 1 |
| `reference_clip.json` | URL + mÃ©triques du clip gagnant | Warsmith | Avant Porte 1 |
| `reference_skeleton.json` | Squelette viral extrait (pourquoi marchÃ©) | F01_SCOUT â†’ C02 | Porte 1 |
| `verdict.json` | Ã‰clairement TYRANT (GO/NO-GO + blue_ocean) | F02_TYRANT_CAMP | Porte 1 |

## Cycle de vie

1. **Init siÃ¨ge** : Warsmith dÃ©pose `directive.md` + `reference_clip.json`
2. **SiÃ¨ge actif** : C01 â†’ C02 Ã©crivent `reference_skeleton.json` + `verdict.json`
3. **SiÃ¨ge en cours** : `directive.md` est lu par toutes les frÃ©gates (assets source)
4. **Fermeture** : Warsmith dÃ©clare `--close-campaign` â†’ C06 agrÃ¨ge learnings
5. **Reset** : Le Warsmith archive (dÃ©place vers un dossier extern) ou efface les 4 fichiers, et repart vierge pour la campaigne suivante.

## Note d'archivage

L'archivage des campagnes passÃ©es n'est pas gÃ©rÃ© par le forge lui-mÃªme â€” c'est une opÃ©ration manuelle du Warsmith. Si tu veux garder l'historique, dÃ©place `campaign/` vers un dossier externe type `ARCHIVES/<campaign_id>/`. Le forge ne garde que la campagne **active**.

## Hist passed campaigns dans `learnings/`

Les rÃ©sultats d'une campaigne close sont **agrÃ©gÃ©s** dans `ARCHIVUM/learnings/learnings.json` (champ `campaign_history`). Donc la mÃ©moire n'est pas perdue mÃªme quand on efface `campaign/`.
