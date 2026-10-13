# Score de recherche (top-3, requête=oracle, avec dédoublonnage FR/DE)

Courriers évalués : 16 (sur 20)

## Global

- hit@3 : **75%**
- rappel@3 : **75%**
- MRR : **0.58**

## Par catégorie

| categorie | n | hit@3 | rappel@3 | MRR |
|---|---|---|---|---|
| assurance_maladie | 5 | 80% | 80% | 0.60 |
| rappel_poursuite | 6 | 50% | 50% | 0.50 |
| sejour | 5 | 100% | 100% | 0.67 |

## Par langue

| langue | n | hit@3 | rappel@3 | MRR |
|---|---|---|---|---|
| de | 8 | 62% | 62% | 0.50 |
| fr | 8 | 88% | 88% | 0.67 |

## Détail

| id | catégorie | attendu | obtenu | hit |
|---|---|---|---|---|
| t01 | rappel_poursuite | schkg_art69, schkg_art74 | schkg_art69, schkg_art74, kvg_art64a | OK |
| t02 | assurance_maladie | kvg_art64a | kvg_art65, kvg_art64a, schkg_art69 | OK |
| t03 | sejour | lei_art33 | lei_art12, lei_art33, lei_art34 | OK |
| t04 | rappel_poursuite | schkg_art69, schkg_art74 | schkg_art74, schkg_art69, schkg_art67 | OK |
| t05 | rappel_poursuite | schkg_art67 | kvg_art64a, schkg_art69, schkg_art74 | RATE |
| t06 | rappel_poursuite | schkg_art67 | kvg_art64a, schkg_art69, kvg_art65 | RATE |
| t07 | rappel_poursuite | schkg_art69, schkg_art74 | schkg_art69, schkg_art74, kvg_art64a | OK |
| t08 | assurance_maladie | kvg_art64a | kvg_art65, kvg_art64a, kvg_art64 | OK |
| t09 | assurance_maladie | kvg_art3 | kvg_art64a, schkg_art69, kvg_art65 | RATE |
| t10 | assurance_maladie | kvg_art64 | kvg_art64, kvg_art64a, schkg_art69 | OK |
| t11 | assurance_maladie | kvg_art65 | kvg_art65, schkg_art67, schkg_art74 | OK |
| t12 | sejour | lei_art33 | lei_art33, lei_art12, lei_art34 | OK |
| t13 | sejour | lei_art12 | lei_art12, schkg_art67, lei_art34 | OK |
| t14 | sejour | lei_art62 | schkg_art74, schkg_art67, lei_art62 | OK |
| t15 | sejour | lei_art34 | lei_art12, lei_art34, schkg_art69 | OK |
| t16 | autre | (aucune) | schkg_art69, kvg_art64a, schkg_art74 | - |
| t17 | autre | (aucune) | schkg_art69, kvg_art64a, schkg_art74 | - |
| t18 | autre | (aucune) | schkg_art69, kvg_art64a, schkg_art74 | - |
| t19 | autre | (aucune) | schkg_art69, schkg_art74, kvg_art64a | - |
| t20 | rappel_poursuite | schkg_art67 | schkg_art69, kvg_art64a, kvg_art64 | RATE |

## Courriers sans source attendue (seuil possible)

- t16 (autre) : meilleur passage = schkg_art69, score 0.5689
- t17 (autre) : meilleur passage = schkg_art69, score 0.5439
- t18 (autre) : meilleur passage = schkg_art69, score 0.5689
- t19 (autre) : meilleur passage = schkg_art69, score 0.5171

Courriers avec source : score du meilleur passage, min 0.531, moyenne 0.589, max 0.710
Un seuil n'est fiable que si le MIN des courriers avec source reste au-dessus du MAX des courriers hors périmètre.