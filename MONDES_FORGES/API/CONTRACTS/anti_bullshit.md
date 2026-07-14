# CONTRAT ANTI-BULLSHIT — FILTRE DES FAUSSES RÈGLES — Monde-Forge API

## OBJECTIF
Quand tu analyses les données ARCHIVUM (rules/, markets/, targets/), tu dois faire la
différence entre une **vraie règle de marché** et du **bruit**. Tu ne ressors QUE les patterns validés.

## 4 RÈGLES DE FILTRAGE

### 1. Exception isolée ≠ Règle
Si une API a eu 10k abonnés suite à un événement viral unique, c'est de la **chance**, pas une règle.
→ Ignore. Garde uniquement les patterns **répétables sur plusieurs APIs**.

### 2. Contradiction = Contextualisation
Si l'ARCHIVUM dit "prix bas convertit mieux" ET "prix premium signale la qualité",
tu ne choisis pas un camp. Tu **contextualises**.
→ Ex : "Prix bas pour capter les agents automatisés. Prix premium pour les équipes DevOps."

### 3. Opinion ≠ Donnée
Ignore "cette API a l'air bien faite".
Garde uniquement : "latence moyenne 412ms sur 30 jours" ou "87% success rate".
→ Critère : la règle peut-elle être mesurée ? Si non → opinion → ignore.

### 4. Récurrence minimale
Une règle n'est validée que si elle apparaît chez **au moins 2 APIs différentes**
OU si elle est **logiquement démontrée** par une seule API avec des données concrètes.
→ 1 API + 0 preuve = hypothèse, pas règle.

## CE QUE TU DOIS TOUJOURS CONSERVER
- Les patterns de pricing qui convertissent (freemium → paid)
- Les règles de latence (< 500ms = critère agents automatisés)
- Les patterns de popularité RapidAPI (score 9.5+ = trafic machine dominant)
- Les signaux wrappers GitHub (>20 wrappers actifs = adoption réelle)
- Les catégories où les agents consomment en volume (scraping, data extraction, format conversion)

## CE QUE TU DOIS TOUJOURS REJETER
- Les success stories ponctuelles sans pattern répétable
- Les opinions esthétiques sur la qualité du code
- Les conseils contradictoires sans contexte marché
- Les règles basées sur 0 donnée mesurable
- Les conseils génériques ("fais une bonne API") sans méthode concrète
