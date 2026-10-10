# Benchmark extraction + citation : prompt d'évaluation (categorie + ISO), Apertus 8b

Courriers : 20. Seuil de source : 0.54.

## Global

- JSON exploitable : **95%**
- Catégorie : **70%**
- Délai exact : **80%**
- Montant exact : **85%**
- Citation correcte : **85%**
- Latence moyenne d'extraction : 1.25 s
- Erreurs d'appel : 0 ; recherche de secours (passage de test) : 0

## Par catégorie

| categorie | n | JSON | catégorie | délai | montant | citation |
|---|---|---|---|---|---|---|
| assurance_maladie | 5 | 100% | 80% | 100% | 100% | 100% |
| autre | 4 | 100% | 0% | 100% | 100% | 100% |
| rappel_poursuite | 6 | 100% | 100% | 50% | 67% | 50% |
| sejour | 5 | 80% | 80% | 80% | 80% | 100% |

## Par langue

| langue | n | JSON | catégorie | délai | montant | citation |
|---|---|---|---|---|---|---|
| de | 10 | 90% | 60% | 80% | 80% | 80% |
| fr | 10 | 100% | 80% | 80% | 90% | 90% |

## Montant : avec et sans montant dans le courrier

- Courriers avec montant (16) : 88%
- Courriers sans montant, `null` attendu (4) : 75%

## Détail

| id | catégorie | JSON | catég. | délai | montant | citation |
|---|---|---|---|---|---|---|
| t01 | rappel_poursuite | OK | OK | RATE | OK | OK |
| t02 | assurance_maladie | OK | OK | OK | OK | OK |
| t03 | sejour | OK | OK | OK | OK | OK |
| t04 | rappel_poursuite | OK | OK | RATE | RATE | OK |
| t05 | rappel_poursuite | OK | OK | OK | OK | RATE |
| t06 | rappel_poursuite | OK | OK | OK | OK | RATE |
| t07 | rappel_poursuite | OK | OK | RATE | RATE | OK |
| t08 | assurance_maladie | OK | OK | OK | OK | OK |
| t09 | assurance_maladie | OK | OK | OK | OK | OK |
| t10 | assurance_maladie | OK | OK | OK | OK | OK |
| t11 | assurance_maladie | OK | RATE | OK | OK | OK |
| t12 | sejour | OK | OK | OK | OK | OK |
| t13 | sejour | RATE | RATE | RATE | RATE | OK |
| t14 | sejour | OK | OK | OK | OK | OK |
| t15 | sejour | OK | OK | OK | OK | OK |
| t16 | autre | OK | RATE | OK | OK | OK |
| t17 | autre | OK | RATE | OK | OK | OK |
| t18 | autre | OK | RATE | OK | OK | OK |
| t19 | autre | OK | RATE | OK | OK | OK |
| t20 | rappel_poursuite | OK | OK | OK | OK | RATE |