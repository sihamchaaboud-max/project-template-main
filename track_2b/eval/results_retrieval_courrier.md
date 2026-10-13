# Score de recherche (top-3, requête=courrier, avec dédoublonnage FR/DE)

Courriers évalués : 16 (sur 20)

## Global

- hit@3 : **88%**
- rappel@3 : **88%**
- MRR : **0.79**

## Par catégorie

| categorie | n | hit@3 | rappel@3 | MRR |
|---|---|---|---|---|
| assurance_maladie | 5 | 100% | 100% | 1.00 |
| rappel_poursuite | 6 | 67% | 67% | 0.56 |
| sejour | 5 | 100% | 100% | 0.87 |

## Par langue

| langue | n | hit@3 | rappel@3 | MRR |
|---|---|---|---|---|
| de | 8 | 75% | 75% | 0.75 |
| fr | 8 | 100% | 100% | 0.83 |

## Détail

| id | catégorie | attendu | obtenu | hit |
|---|---|---|---|---|
| t01 | rappel_poursuite | schkg_art69, schkg_art74 | schkg_art69, schkg_art74, kvg_art64a | OK |
| t02 | assurance_maladie | kvg_art64a | kvg_art64a, kvg_art65, kvg_art64 | OK |
| t03 | sejour | lei_art33 | lei_art33, lei_art34, lei_art12 | OK |
| t04 | rappel_poursuite | schkg_art69, schkg_art74 | schkg_art69, schkg_art74, schkg_art67 | OK |
| t05 | rappel_poursuite | schkg_art67 | schkg_art69, schkg_art74, schkg_art67 | OK |
| t06 | rappel_poursuite | schkg_art67 | schkg_art69, schkg_art74, kvg_art64a | RATE |
| t07 | rappel_poursuite | schkg_art69, schkg_art74 | schkg_art69, schkg_art74, schkg_art67 | OK |
| t08 | assurance_maladie | kvg_art64a | kvg_art64a, kvg_art65, kvg_art64 | OK |
| t09 | assurance_maladie | kvg_art3 | kvg_art3, kvg_art64a, lei_art12 | OK |
| t10 | assurance_maladie | kvg_art64 | kvg_art64, kvg_art65, kvg_art64a | OK |
| t11 | assurance_maladie | kvg_art65 | kvg_art65, schkg_art74, kvg_art64a | OK |
| t12 | sejour | lei_art33 | lei_art33, lei_art34, lei_art12 | OK |
| t13 | sejour | lei_art12 | lei_art12, lei_art34, kvg_art3 | OK |
| t14 | sejour | lei_art62 | lei_art33, lei_art34, lei_art62 | OK |
| t15 | sejour | lei_art34 | lei_art34, lei_art12, schkg_art74 | OK |
| t16 | autre | (aucune) | schkg_art69, kvg_art64, kvg_art64a | - |
| t17 | autre | (aucune) | kvg_art64a, schkg_art74, schkg_art69 | - |
| t18 | autre | (aucune) | kvg_art64, kvg_art65, schkg_art69 | - |
| t19 | autre | (aucune) | kvg_art64, kvg_art64a, kvg_art65 | - |
| t20 | rappel_poursuite | schkg_art67 | kvg_art64a, schkg_art74, schkg_art69 | RATE |

## Courriers sans source attendue (seuil possible)

- t16 (autre) : meilleur passage = schkg_art69, score 0.5226
- t17 (autre) : meilleur passage = kvg_art64a, score 0.4677
- t18 (autre) : meilleur passage = kvg_art64, score 0.5053
- t19 (autre) : meilleur passage = kvg_art64, score 0.4818

Courriers avec source : score du meilleur passage, min 0.548, moyenne 0.662, max 0.777
Un seuil n'est fiable que si le MIN des courriers avec source reste au-dessus du MAX des courriers hors périmètre.