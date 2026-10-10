# Benchmark extraction + citation : prompt v3 (écrit après lecture des erreurs : scores optimistes), Apertus 70b

Courriers : 20. Seuil de source : 0.54.

## Global

- JSON exploitable : **100%**
- Catégorie : **80%**
- Délai exact : **85%**
- Montant exact : **95%**
- Citation correcte : **85%**
- Latence moyenne d'extraction : 2.02 s
- Erreurs d'appel : 0 ; recherche de secours (passage de test) : 0

## Par catégorie

| categorie | n | JSON | catégorie | délai | montant | citation |
|---|---|---|---|---|---|---|
| assurance_maladie | 5 | 100% | 100% | 100% | 100% | 100% |
| autre | 4 | 100% | 50% | 100% | 100% | 100% |
| rappel_poursuite | 6 | 100% | 67% | 50% | 83% | 50% |
| sejour | 5 | 100% | 100% | 100% | 100% | 100% |

## Par langue

| langue | n | JSON | catégorie | délai | montant | citation |
|---|---|---|---|---|---|---|
| de | 10 | 100% | 90% | 90% | 100% | 80% |
| fr | 10 | 100% | 70% | 80% | 90% | 90% |

## Montant : avec et sans montant dans le courrier

- Courriers avec montant (16) : 94%
- Courriers sans montant, `null` attendu (4) : 100%

## Détail

| id | catégorie | JSON | catég. | délai | montant | citation |
|---|---|---|---|---|---|---|
| t01 | rappel_poursuite | OK | OK | RATE | OK | OK |
| t02 | assurance_maladie | OK | OK | OK | OK | OK |
| t03 | sejour | OK | OK | OK | OK | OK |
| t04 | rappel_poursuite | OK | OK | RATE | OK | OK |
| t05 | rappel_poursuite | OK | RATE | OK | OK | RATE |
| t06 | rappel_poursuite | OK | OK | OK | OK | RATE |
| t07 | rappel_poursuite | OK | OK | RATE | RATE | OK |
| t08 | assurance_maladie | OK | OK | OK | OK | OK |
| t09 | assurance_maladie | OK | OK | OK | OK | OK |
| t10 | assurance_maladie | OK | OK | OK | OK | OK |
| t11 | assurance_maladie | OK | OK | OK | OK | OK |
| t12 | sejour | OK | OK | OK | OK | OK |
| t13 | sejour | OK | OK | OK | OK | OK |
| t14 | sejour | OK | OK | OK | OK | OK |
| t15 | sejour | OK | OK | OK | OK | OK |
| t16 | autre | OK | RATE | OK | OK | OK |
| t17 | autre | OK | OK | OK | OK | OK |
| t18 | autre | OK | OK | OK | OK | OK |
| t19 | autre | OK | RATE | OK | OK | OK |
| t20 | rappel_poursuite | OK | RATE | OK | OK | RATE |