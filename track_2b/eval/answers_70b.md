# Réponses générées : Apertus 70b (lecture par l'équipe, variantes visibles)


## t01 (rappel_poursuite, fr)

Extraction : `{"type_document": "Commandement de payer", "delai": "20 jours", "montant": "CHF 1'250.00", "action_demandee": "Payer CHF 1'250.00 dans les vingt jours"}`  
Passages : schkg_art69, schkg_art74, kvg_art64a (meilleur score 0.7569)

### full

- شنو كاتقول الرسالة؟
تم تسليم أمر رسمي بالأداء (Commandement de payer) من طرف مكتب تحصيل الديون ديال لوزان، وتطلب منك تخلص مبلغ 1'250.00 فرنك سويسري، بالإضافة إلى مصاريف التحصيل. خاصك تخلص المبلغ في ظرف عشرين يوم، وإلا إذا كنتي ما كنتيش موافق على الدين، عندك الحق تعترض عليه في ظرف عشرة أيام من تاريخ تسليم الرسالة.
- شنو خاصك تدير؟
خاصك تخلص مبلغ 1'250.00 فرنك سويسري في ظرف عشرين يوم، أو إذا كنتي ما كنتيش موافق على الدين، قدم اعتراض رسمي (opposition) لمكتب تحصيل الديون في ظرف عشرة أيام من تاريخ تسليم الأمر بالأداء.
- آخر أجل:
عشرين يوم من تاريخ تسليم الأمر بالأداء (5 أكتوبر 2026).
- المصدر: المادة 69 و74 من قانون تحصيل الديون والإفلاس السويسري (SchKG).
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل بمكتب تحصيل الديون (Office des poursuites) ديال لوزان.

_check.py: ECHEC ['delai : 20'] | arabe 91% | source citée: 1 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
تم تسليم أمر أداء (Commandement de payer) من طرف مكتب تحصيل الديون ديال لوزان، وتطلب منك تدفع مبلغ 1'250.00 فرنك سويسري، بالإضافة إلى مصاريف التحصيل، في ظرف عشرين يوم. وإذا كنتي ما كنتيش موافق على الدين أو جزء منه، عندك الحق تعترض عليه في ظرف عشرة أيام من تاريخ تسليم الرسالة.
- شنو خاصك تدير؟
إذا كنتي موافق على الدين، خاصك تخلص المبلغ كامل (1'250.00 فرنك سويسري) في ظرف عشرين يوم. إذا كنتي ما كنتيش موافق على الدين أو جزء منه، خاصك تقدم اعتراض رسمي (opposition) لمكتب تحصيل الديون في ظرف عشرة أيام من تاريخ تسليم الرسالة.
- آخر أجل:
عشرين يوم من تاريخ تسليم أمر الأداء (5 أكتوبر 2026).
- المصدر: المادة 69 و المادة 74 من قانون تحصيل الديون والإفلاس السويسري (SchKG).
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل بمكتب تحصيل الديون (Office des poursuites) ديال لوزان.

_check.py: ECHEC ['delai : 20'] | arabe 91% | source citée: 1 | non soutenus: -_

### baseline

- Ce que dit le courrier : C’est un commandement de payer. Tu dois payer CHF 1'250.00 dans les 20 jours. Si tu n’es pas d’accord avec la somme, tu peux faire opposition dans les 10 jours.
- Ce que tu dois faire : Tu dois décider si tu paies la somme ou si tu contestes la dette.
- Avant quand : Tu dois payer ou contester avant le 25 octobre 2026 (20 jours après le 5 octobre 2026).
- Source : Courrier reçu le 5 octobre 2026 de l’Office des poursuites de Lausanne.
- Dernière phrase : En cas de doute, contacte directement l’Office des poursuites de Lausanne.

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_


## t02 (assurance_maladie, de)

Extraction : `{"type_document": "Mahnung", "delai": "9. November 2026", "montant": "CHF 432.50", "action_demandee": "Überweisen Sie den Betrag von CHF 432.50 bis zum 9. November 2026"}`  
Passages : kvg_art64a_de, kvg_art65, kvg_art64 (meilleur score 0.5893)

### full

شنو كاتقول الرسالة؟
شركة التأمين الصحي ما توصلاتش بواجب التأمين الصحي ديالك ديال شهر أكتوبر 2026، اللي هو 412.50 فرنك سويسري. أضافو ليه مصاريف التذكير بالخلاص (20.00 فرنك سويسري)، بحيث المبلغ الكلي اللي خاصك تخلصو هو 432.50 فرنك سويسري. خاصك ترسل الفلوس حتى نهار 9 نونبر 2026، وإلا غادي يبداو إجراءات قانونية لتحصيل الدين.
شنو خاصك تدير؟
خاصك تخلص المبلغ الكلي 432.50 فرنك سويسري، إما بالحوالة أو بأي وسيلة أداء معتمدة، حتى آخر أجل هو 9 نونبر 2026.
آخر أجل:
9 نونبر 2026.
المصدر: المادة 64a من قانون التأمين الصحي السويسري (KVG).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بشركة التأمين الصحي (Krankenkasse Muster AG) اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 95% | source citée: 1 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
الشركة ديال التأمين (Krankenkasse Muster AG) كاتقول أن واجب التأمين ديالك ديال شهر أكتوبر 2026 بقيمة 412.50 فرنك سويسري مازال مفتوح، مع غرامة تذكير بقيمة 20 فرنك سويسري، لي مجموعها 432.50 فرنك سويسري. خاصك تخلص المبلغ حتى تاريخ 9 نونبر 2026، وإلا غادي يبداو إجراءات تحصيل الديون ضدك.
- شنو خاصك تدير؟
خاصك تخلص مبلغ 432.50 فرنك سويسري للشركة (Krankenkasse Muster AG) قبل أو في تاريخ 9 نونبر 2026.
- آخر أجل:
9 نونبر 2026.
- المصدر: الفقرة المتعلقة بالإنذار (Mahnung) في النظام السويسري للتأمين الصحي (KVG)، والمذكورة في الرسالة.
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل مباشرة بالشركة ديال التأمين (Krankenkasse Muster AG) اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 86% | source citée: 1 | non soutenus: -_

### baseline

- Ce que dit le courrier : Tu as une facture de prime d'assurance maladie impayée pour octobre 2026. Le montant total à payer est de CHF 432.50 (prime CHF 412.50 + frais de rappel CHF 20.00). Tu dois payer ce montant avant le 9 novembre 2026. Si tu ne paies pas, l'assurance entamera une procédure de poursuite.
- Ce que tu dois faire : Tu dois transférer la somme de CHF 432.50 avant le 9 novembre 2026.
- Avant quand : Avant le 9 novembre 2026.
- Source : Courrier de la Krankenkasse Muster AG (Mahnung).
- Dernière phrase : En cas de doute, contacte directement la Krankenkasse Muster AG.

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_


## t03 (sejour, fr)

Extraction : `{"type_document": "demande de documents complémentaires", "delai": "2 novembre 2026", "montant": null, "action_demandee": "transmettre une attestation de logement et une copie de votre contrat de travail"}`  
Passages : lei_art33, lei_art34, lei_art12_de (meilleur score 0.6698)

### full

شنو كاتقول الرسالة؟
الخدمة ديال السكان تطلب منك توفّر وثيقة إثبات للسكن ونسخة من عقد العمل ديالك، باش تتمكن من معالجة طلب رخصة الإقامة ديالك.
شنو خاصك تدير؟
خاصك ترسل شهادة السكن ونسخة من عقد العمل ديالك قبل 2 نونبر 2026.
آخر أجل:
2 نونبر 2026.
المصدر: الرسالة الرسمية الصادرة عن Service de la population.
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بالService de la population اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 86% | source citée: 0 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
طلب منك الخدمة ديال السكان ديالك تزويدهم بوثيقة سكن ونسخة من عقد العمل ديالك، وإلا ما بعثتيش شي شيء قبل 2 نونبر 2026، غادي يلقوا الملف ديالك.
- شنو خاصك تدير؟
خاصك ترسل للخدمة ديال السكان وثيقة السكن وعقد العمل ديالك قبل 2 نونبر 2026.
- آخر أجل:
2 نونبر 2026.
- المصدر: الرسالة الرسمية الصادرة عن Service de la population.
إلا ما فهميتش شي حاجة أو عندك شك، تاصل مباشرة بالService de la population اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 87% | source citée: 0 | non soutenus: -_

### baseline

- Ce que dit le courrier : Le Service de la population demande de lui envoyer une attestation de logement et une copie de votre contrat de travail avant le 2 novembre 2026. Si vous ne répondez pas, votre dossier sera fermé.
- Ce que tu dois faire : Tu dois envoyer une attestation de logement et une copie de ton contrat de travail au Service de la population avant le 2 novembre 2026.
- Avant quand : Avant le 2 novembre 2026.
- Source : Courrier du Service de la population (voir ci-dessus).
- Dernière phrase : En cas de doute, contacte directement le Service de la population qui a envoyé le courrier.

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_


## t04 (rappel_poursuite, de)

Extraction : `{"type_document": "Zahlungsbefehl", "delai": "20 Tagen", "montant": "CHF 3'480.00 nebst Zins zu 5 % seit dem 1. Juli 2026", "action_demandee": "innert 20 Tagen den Gläubiger zu befriedigen"}`  
Passages : schkg_art69_de, schkg_art74_de, schkg_art67_de (meilleur score 0.6934)

### full

- شنو كاتقول الرسالة؟
تبداو ضدك إجراءات قانونية لتحصيل دين بقيمة 3'480.00 فرنك سويسري، زائد فوائد بنسبة 5% من 1 يوليو 2026، بالإضافة إلى مصاريف التحصيل بقيمة 73.30 فرنك سويسري. خاصك تخلص المبلغ أو تعترض على الدين.
- شنو خاصك تدير؟
إلا كنتي موافق على الدين، خاصك تخلص المبلغ كامل (3'480.00 فرنك سويسري + 73.30 فرنك سويسري) قبل آخر أجل. وإلا كنتي ما كنتيش موافق على الدين أو على جزء منه، خاصك تقدم اعتراض رسمي (Rechtsvorschlag) للـ Betreibungsamt خلال 10 أيام من تاريخ توصلتي بالأمر.
- آخر أجل:
20 أيام من تاريخ توصلتي بالأمر بالأداء.
المصدر: المادة 69 و المادة 74 من قانون تحصيل الديون والإفلاس السويسري (SchKG).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل مباشرة بمكتب تحصيل الديون (Betreibungsamt Musterstadt).

_check.py: OK | arabe 89% | source citée: 1 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
تبداو إجراءات قانونية لتحصيل دين بقيمة 3'480.00 فرنك سويسري، بالإضافة إلى فائدة 5٪ من 1 يوليو 2026، و73.30 فرنك سويسري كتكلفة التحصيل. خاصك تخلص المبلغ أو تعترض على الدين خلال 20 يومًا.
- شنو خاصك تدير؟
إلا كنتي موافق على الدين، خاصك تخلص المبلغ كاملًا (3'480.00 فرنك سويسري + 73.30 فرنك سويسري) خلال 20 يومًا من تاريخ تسليم هذا الأمر بالأداء. وإلا كنتي ما موافقش على الدين أو على جزء منه، خاصك تعترض رسميًا (Rechtsvorschlag) على هذا الأمر خلال 10 أيام من تاريخ تسليمه.
- آخر أجل:
20 يومًا من تاريخ تسليم الأمر بالأداء (6 أكتوبر 2026).
- المصدر: المادة 69 و المادة 74 من قانون تحصيل الديون والإفلاس السويسري (SchKG).
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل بمكتب تحصيل الديون (Betreibungsamt Musterstadt).

_check.py: OK | arabe 91% | source citée: 1 | non soutenus: -_

### baseline

- Ce que dit le courrier : C'est un ordre de paiement (Zahlungsbefehl) pour une somme de CHF 3'480.00 plus des intérêts à 5 % depuis le 1er juillet 2026, plus des frais de CHF 73.30. Tu dois payer ou contester cette somme dans des délais précis.
- Ce que tu dois faire : Tu as 20 jours pour payer la somme demandée ou contester une partie de la dette. Si tu veux contester, tu dois faire un "Rechtsvorschlag" (opposition) dans les 10 jours suivant la réception du courrier.
- Avant quand : Tu dois agir dans les 20 jours pour payer ou contester, et si tu contestes, tu as 10 jours à partir de la date de réception du courrier.
- Source : Courrier reçu le 6 octobre 2026, Betreibungsamt Musterstadt, Betreibung Nr. 2026-48213
- Dernière phrase : En cas de doute, contacte directement le Betreibungsamt Musterstadt.

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_


## t05 (rappel_poursuite, fr)

Extraction : `{"type_document": "rappel de facture", "delai": "20 octobre 2026", "montant": "201.40", "action_demandee": "régler le montant dû d'ici au 20 octobre 2026"}`  
Passages : aucun (règle sans source) (meilleur score 0.5391)

### full

شنو كاتقول الرسالة؟
خدمات صناعية ديال Montclair كاتطلب منك تخلص فاتورة بقيمة 186.40 فرنك سويسري، مع مصاريف تذكير بقيمة 15.00 فرنك سويسري، مجموعها 201.40 فرنك سويسري. خاصك تخلص المبلغ قبل أو فآخر أجل 20 أكتوبر 2026.
شنو خاصك تدير؟
خاصك تخلص المبلغ الكلي 201.40 فرنك سويسري قبل أو فآخر أجل 20 أكتوبر 2026.
آخر أجل:
20 أكتوبر 2026.
المصدر: النص الرئيسي من الرسالة (Services industriels de Montclair).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بخدمات صناعية ديال Montclair اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 86% | source citée: None | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
   وصل آخر تذكير بخصوص فاتورة الكهرباء. خاصك تخلص المبلغ الكلي 201.40 فرنك سويسري قبل تاريخ 20 أكتوبر 2026. وإلا ما خلصتيش، غادي يفتحوا إجراءات قانونية ضدك.
- شنو خاصك تدير؟
   خاصك تخلص مبلغ 201.40 فرنك سويسري قبل أو في تاريخ 20 أكتوبر 2026.
- آخر أجل:
   20 أكتوبر 2026.
- المصدر:
   الرسالة الصادرة عن Services industriels de Montclair.
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل مباشرة بServices industriels de Montclair.

_check.py: OK | arabe 81% | source citée: None | non soutenus: -_

### baseline

- Ce que dit le courrier : C’est un rappel de facture impayée. Il faut payer CHF 201.40 avant le 20 octobre 2026, sinon ils engagent une poursuite.
- Ce que tu dois faire : Tu dois payer la somme de CHF 201.40 avant le 20 octobre 2026.
- Avant quand : Avant le 20 octobre 2026.
- Source : Services industriels de Montclair – Dernier rappel
- Dernière phrase : En cas de doute, contacte directement les Services industriels de Montclair.

_check.py: OK | arabe 0% | source citée: None | non soutenus: -_


## t06 (rappel_poursuite, de)

Extraction : `{"type_document": "Letzte Mahnung vor Einleitung der Betreibung", "delai": "23. Oktober 2026", "montant": "CHF 1'030.00", "action_demandee": "Payer le montant total de CHF 1'030.00 jusqu'au 23 octobre 2026"}`  
Passages : schkg_art69_de, schkg_art74_de, kvg_art64a_de (meilleur score 0.5515)

### full

شنو كاتقول الرسالة؟
شركة تحصيل الديون (Inkasso) كاتطلب منك تخلص مبلغ إجمالي قدره 1'030.00 فرنك سويسري، قبل أو فآخر أجل 23 أكتوبر 2026. وإلا ما خلصتيش، غادي يرسلو طلب باش تبدا إجراءات قانونية لتحصيل الدين (Betreibung).
شنو خاصك تدير؟
خاصك تخلص المبلغ الكلي 1'030.00 فرنك سويسري قبل أو فآخر أجل 23 أكتوبر 2026. وإلا ما عندكش المبلغ كامل، حاول التواصل مع الشركة باش تعرف إذا كان بإمكانك الخلاص بالتقسيط أو إذا كان عندك شي مشكل.
آخر أجل:
23 أكتوبر 2026.
المصدر: الفقرة الأولى من المادة 64a من قانون التأمين الصحي السويسري (KVG).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بشركة Inkasso Beispiel AG اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 92% | source citée: 1 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
الرسالة هي إنذار أخير قبل الشروع في إجراءات تحصيل الدين. عندك دين مفتوح بقيمة 940.00 فرنك سويسري، بالإضافة إلى رسوم تحصيل بقيمة 90.00 فرنك سويسري، أي ما مجموعه 1'030.00 فرنك سويسري. يطلب منك الشركة تسديد المبلغ بالكامل قبل 23 أكتوبر 2026، وإلا سيرسلون طلب التحصيل إلى مكتب تحصيل الديون.
- شنو خاصك تدير؟
خاصك تخلص المبلغ الكلي وهو 1'030.00 فرنك سويسري قبل أو في تاريخ 23 أكتوبر 2026.
- آخر أجل:
23 أكتوبر 2026.
- المصدر: محتوى الرسالة (Inkasso Beispiel AG).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بشركة Inkasso Beispiel AG اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 92% | source citée: 0 | non soutenus: -_

### baseline

- Ce que dit le courrier : C'est une dernière mise en demeure avant de lancer une procédure de poursuite. Tu dois payer la somme totale de CHF 1'030.00 avant le 23 octobre 2026. Sinon, ils vont déposer une demande de poursuite auprès du bureau des poursuites.
- Ce que tu dois faire : Tu dois payer le montant total de CHF 1'030.00 avant le 23 octobre 2026.
- Avant quand : Avant le 23 octobre 2026.
- Source : Courrier de "Inkasso Beispiel AG" (Letzte Mahnung vor Einleitung der Betreibung)
- Dernière phrase : En cas de doute, contacte directement "Inkasso Beispiel AG".

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_


## t07 (rappel_poursuite, fr)

Extraction : `{"type_document": "Commandement de payer", "delai": "20 jours", "montant": "CHF 2'300.00", "action_demandee": "Payer CHF 2'300.00 avec intérêts à 5 % dès le 1er mai 2026 et CHF 73.30 de frais de poursuite dans les vingt jours"}`  
Passages : schkg_art69, schkg_art74, schkg_art67 (meilleur score 0.7357)

### full

شنو كاتقول الرسالة؟
مكتب تحصيل الديون ديال Montclair كيدعوك تخلص مبلغ 2'300.00 فرنك سويسري مع فوائد 5 % من 1 ماي 2026، زائد 73.30 فرنك مصاريف التحصيل، في ظرف عشرين يوم. إلا كنتي ما موافقش على الدين، عندك الحق تعترض عليه في ظرف عشرة أيام من تاريخ تلقي الأمر بالأداء.
شنو خاصك تدير؟
خاصك تخلص المبلغ الكلي (2'300.00 فرنك سويسري + 73.30 فرنك سويسري) في ظرف عشرين يوم، أو إلا كنتي ما موافقش على الدين، خاصك تقدم اعتراض رسمي (opposition) لمكتب تحصيل الديون في ظرف عشرة أيام من تاريخ تلقي هذا الأمر.
آخر أجل:
20 jours من تاريخ تلقي هذا الأمر بالأداء.
المصدر: المادة 69 و 74 من قانون تحصيل الديون والإفلاس السويسري (SchKG).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بمكتب تحصيل الديون (Office des poursuites) ديالك.

_check.py: OK | arabe 91% | source citée: 1 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
الهيئة ديال تحصيل الديون صيفرت لك أمر أداء (Commandement de payer) بديْن بقيمة 2'300.00 فرنك سويسري، مع فائدة 5٪ من 1 ماي 2026، بالإضافة إلى 73.30 فرنك سويسري كتكلفة التحصيل. خاصك تخلص المبلغ كاملًا أو تعترض على الدين في ظرف 10 أيام من تاريخ تسلمك للأمر.
- شنو خاصك تدير؟
خاصك تخلص مبلغ 2'300.00 فرنك سويسري مع الفائدة و73.30 فرنك سويسري كتكلفة التحصيل، أو إذا كنتي ما موافقش على الدين، خاصك تقدم اعتراض رسمي (opposition) في ظرف 10 أيام من تاريخ تسلمك للأمر.
- آخر أجل:
10 أيام من تاريخ تسلمك للأمر بالأداء.
- المصدر: المادة 69 و74 من قانون تحصيل الديون والإفلاس السويسري (SchKG).
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل بهيئة تحصيل الديون (Office des poursuites) اللي صيفرات لك الرسالة.

_check.py: ECHEC ['delai : 20'] | arabe 90% | source citée: 1 | non soutenus: -_

### baseline

- Ce que dit le courrier : C'est un commandement de payer. Tu dois payer CHF 2'300.00 avec des intérêts à 5 % dès le 1er mai 2026, plus CHF 73.30 de frais de poursuite, dans les vingt jours. Si tu contestes la dette, tu dois faire opposition dans les dix jours.
- Ce que tu dois faire : Tu dois payer le montant demandé ou contester la dette.
- Avant quand : Tu dois agir dans les vingt jours à partir de la date de notification (2 octobre 2026).
- Source : Courrier reçu le 2 octobre 2026, Office des poursuites de Montclair, poursuite n° 2026/7731.
- Dernière phrase : En cas de doute, contacte directement l'Office des poursuites de Montclair.

_check.py: ECHEC ['delai : 20'] | arabe 0% | source citée: 0 | non soutenus: -_


## t08 (assurance_maladie, fr)

Extraction : `{"type_document": "sommation", "delai": "9 novembre 2026", "montant": "CHF 1'267.50", "action_demandee": "payer CHF 1'267.50 d'ici le 9 novembre 2026"}`  
Passages : kvg_art64a, kvg_art65, kvg_art64 (meilleur score 0.7108)

### full

شنو كاتقول الرسالة؟
شركة التأمين الصحي ما توصلاتش بواجبات التأمين الصحي ديالك ديال شهور يوليو، غشت، سبتمبر 2026، اللي هو 1'237.50 فرنك سويسري. زائد مصاريف التذكير اللي هي 30.00 فرنك سويسري. مجموع المبلغ اللي خاصك تخلصو هو 1'267.50 فرنك سويسري. خاصك تخلصو قبل 9 نونبر 2026، وإلا غادي يبداو إجراءات قانونية لتحصيل الدين.
شنو خاصك تدير؟
خاصك تخلص المبلغ الكلي 1'267.50 فرنك سويسري قبل أو فآخر أجل المحدد.
آخر أجل:
9 نونبر 2026.
المصدر: المادة 64a من قانون التأمين الصحي السويسري (KVG).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بشركة التأمين الصحي Exemple SA اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 97% | source citée: 1 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
الشركة ديال التأمين (Assurance Santé Exemple SA) كاتقول أن واجبات التأمين ديالك من يوليو إلى سبتمبر 2026 ما تم دفعهمش، واللي هو 1'237.50 فرنك سويسري، مع إضافة 30 فرنك سويسري كتكاليف تذكير. مجموع المبلغ المطلوب هو 1'267.50 فرنك سويسري. خاصك تدفع هاد المبلغ قبل 9 نونبر 2026، وإلا يمكن للشركة تبدأ إجراءات قانونية.
- شنو خاصك تدير؟
خاصك تدفع مبلغ 1'267.50 فرنك سويسري للشركة قبل أو في تاريخ 9 نونبر 2026.
- آخر أجل:
9 نونبر 2026.
- المصدر: الرسالة الأصلية الصادرة عن Assurance Santé Exemple SA.
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل مباشرة بشركة التأمين الصحة اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 89% | source citée: 0 | non soutenus: -_

### baseline

- Ce que dit le courrier : Les primes de juillet à septembre 2026 ne sont pas payées. Il faut payer CHF 1'267.50 (CHF 1'237.50 de primes + CHF 30.00 de frais) avant le 9 novembre 2026. Sinon, ils engageront une poursuite.
- Ce que tu dois faire : Tu dois payer CHF 1'267.50 avant le 9 novembre 2026.
- Avant quand : Avant le 9 novembre 2026.
- Source : Courrier de "Assurance Santé Exemple SA" (sommation de payer)
- Dernière phrase : En cas de doute, contacte directement "Assurance Santé Exemple SA".

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_


## t09 (assurance_maladie, de)

Extraction : `{"type_document": "Avis de mise en conformité", "delai": "15. Oktober 2026", "montant": null, "action_demandee": "Souscrire une assurance maladie de base et confirmer l'affiliation à l'office cantonal de l'assurance maladie avant le 15 octobre 2026"}`  
Passages : kvg_art3_de, kvg_art64a, lei_art12 (meilleur score 0.7662)

### full

شنو كاتقول الرسالة؟
انت سكنت فالمقاطعة ديالنا نهار 15 يوليوز 2026، ولكن حسب المعلومات ديالنا، ما عندكش تأمين صحي أساسي. كل شخص ساكن فسويسرا لازم يتأمّن خلال ثلاثة أشهر من الإقامة. خاصك تاخذ تأمين أساسي قبل أو فآخر أجل 15 أكتوبر 2026 وتخبرنا بذلك. وإلا، غادي نعين لك شركة تأمين.
شنو خاصك تدير؟
خاصك تاخذ تأمين صحي أساسي (assurance de base) قبل أو فآخر أجل 15 أكتوبر 2026، وتخبر المكتب ديال التأمين الصحي (Amt für Krankenversicherung) بالانتساب ديالك.
آخر أجل:
15 أكتوبر 2026.
المصدر: المادة 3 من قانون التأمين الصحي السويسري (KVG).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بالمكتب ديال التأمين الصحي (Amt für Krankenversicherung) اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 86% | source citée: 1 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
ما عندكش تأمين مرضى رغم أنك ساكن في الكانتون من 15 يوليوز 2026. كل شخص ساكن في سويسرا لازم يتأمّن في ظرف 3 أشهر. خاصك تاخذ تأمين أساسي قبل 15 أكتوبر 2026 وتخبرنا بذلك.
- شنو خاصك تدير؟
خاصك تاخذ تأمين مرضى أساسي (Grundversicherung) قبل 15 أكتوبر 2026 وتثبت ذلك للهيئة.
- آخر أجل:
15 أكتوبر 2026.
- المصدر: المادة 3 من قانون التأمين الصحي السويسري (KVG).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل ب "Amt für Krankenversicherung Musterkanton".

_check.py: OK | arabe 83% | source citée: 1 | non soutenus: -_

### baseline

- Ce que dit le courrier : Tu as pris résidence dans le canton le 15 juillet 2026 et tu n'es pas assuré. Tu dois souscrire une assurance maladie de base avant le 15 octobre 2026, sinon le canton te désignera un assureur.
- Ce que tu dois faire : Souscrire une assurance maladie de base et confirmer ton affiliation à l'office cantonal de l'assurance maladie avant le 15 octobre 2026.
- Avant quand : Avant le 15 octobre 2026.
- Source : Amt für Krankenversicherung Musterkanton, courrier "Betrifft: fehlende Krankenversicherung"
- Dernière phrase : En cas de doute, contacte directement l'Amt für Krankenversicherung du canton.

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_


## t10 (assurance_maladie, fr)

Extraction : `{"type_document": "décompte de prestations", "delai": "5 novembre 2026", "montant": "455.00", "action_demandee": "payer le montant de CHF 455.00 jusqu'au 5 novembre 2026"}`  
Passages : kvg_art64, kvg_art65, kvg_art64a (meilleur score 0.5856)

### full

شنو كاتقول الرسالة؟
الشركة ديال التأمين (Assurance Santé Exemple SA) كاتقول أن عليك تسديد مبلغ 455.00 فرنك سويسري، وهو النسبة ديالك (quote-part) من مصاريف العلاج بعد خصم المبلغ الثابت (franchise). خاصك تخلص هاد المبلغ حدّ 5 نونبر 2026.
شنو خاصك تدير؟
خاصك تخلص مبلغ 455.00 فرنك سويسري حدّ 5 نونبر 2026، أو تستعمل ورقة الأداء (bulletin de versement) اللي كتكون مع الرسالة.
آخر أجل:
5 نونبر 2026.
المصدر: النص الرئيسي ديال الرسالة (décompte de prestations n° 88213).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بشركة التأمين الصحي (Assurance Santé Exemple SA) اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 75% | source citée: 0 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
الشركة ديال التأمين (Assurance Santé Exemple SA) كاتطلب منك تدفع مبلغ 455.00 فرنك سويسري، اللي هو التزامك في التكاليف (participation aux coûts) على العلاجات اللي تلقيتيها. خاصك تخلص هاد المبلغ حتى تاريخ 5 نونبر 2026.
- شنو خاصك تدير؟
خاصك تخلص مبلغ 455.00 فرنك سويسري للشركة (Assurance Santé Exemple SA) قبل أو في تاريخ 5 نونبر 2026.
- آخر أجل:
5 نونبر 2026.
- المصدر: محتوى الرسالة (Décompte de prestations n° 88213).
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل مباشرة بالشركة (Assurance Santé Exemple SA) اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 72% | source citée: 0 | non soutenus: -_

### baseline

- Ce que dit le courrier : Le courrier est un décompte de prestations de l'Assurance Santé Exemple SA. Il indique que tu dois payer CHF 455.00 pour ta participation aux coûts des traitements, jusqu'au 5 novembre 2026.
- Ce que tu dois faire : Tu dois payer le montant de CHF 455.00 à l'Assurance Santé Exemple SA avant le 5 novembre 2026.
- Avant quand : Avant le 5 novembre 2026.
- Source : Courrier de l'Assurance Santé Exemple SA, décompte de prestations n° 88213.
- Dernière phrase : En cas de doute, contacte directement l'Assurance Santé Exemple SA.

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_


## t11 (assurance_maladie, de)

Extraction : `{"type_document": "Prämienverbilligung", "delai": "30. November 2026", "montant": "CHF 1'440.00", "action_demandee": "Einreichen des beiliegenden Antragsformulars samt Steuerunterlagen"}`  
Passages : kvg_art65_de, schkg_art74_de, kvg_art64a_de (meilleur score 0.684)

### full

شنو كاتقول الرسالة؟
لديك احتمال أنك تستحق تخفيض واجبات التأمين الصحي بقيمة 1'440.00 فرنك سويسري في السنة. باش نقدر نحقق المطالبة ديالك، خاصك ترسل الاستمارة المرفقة مع وثائق الضرائب قبل 30 نونبر 2026.
شنو خاصك تدير؟
خاصك ترسل الاستمارة المرفقة مع جميع الوثائق المطلوبة (وثائق الضرائب) قبل 30 نونبر 2026.
آخر أجل:
30 نونبر 2026.
المصدر: المادة 64a من قانون التأمين الصحي السويسري (KVG).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بمديرية التأمين الاجتماعي (Sozialversicherungsamt) اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 93% | source citée: 1 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
الشركة ديال التأمين الاجتماعية (Sozialversicherungsamt) تقول ليك أنك عندك احتمال تستاهل تخفيض في واجب التأمين الصحي بقيمة 1'440.00 فرنك سويسري للسنة. خاصك تقدم الطلب مع الوثائق الضريبية قبل 30 نونبر 2026.
- شنو خاصك تدير؟
خاصك ترسل الطلب المرفق مع جميع الوثائق الضريبية المطلوبة قبل 30 نونبر 2026.
- آخر أجل:
30 نونبر 2026.
- المصدر: المادة 64a من قانون التأمين الصحي السويسري (KVG).
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل بالشركة ديال التأمين الاجتماعي اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 93% | source citée: 1 | non soutenus: -_

### baseline

- Ce que dit le courrier : Tes primes d'assurance maladie peuvent être réduites de CHF 1'440.00 par an. Tu dois envoyer le formulaire de demande avec tes documents fiscaux avant le 30. November 2026.
- Ce que tu dois faire : Envoie le formulaire (Prämienverbilligung) avec tes documents fiscaux (Steuerunterlagen) avant la date indiquée.
- Avant quand : Avant le 30. November 2026.
- Source : Courrier du Sozialversicherungsamt Musterkanton.
- Dernière phrase : En cas de doute, contacte directement le Sozialversicherungsamt Musterkanton.

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_


## t12 (sejour, fr)

Extraction : `{"type_document": "demande de renouvellement d'autorisation de séjour", "delai": "6 novembre 2026", "montant": "CHF 140.00", "action_demandee": "retourner le formulaire ci-joint, une copie de votre passeport valable et une attestation de votre employeur"}`  
Passages : lei_art33, lei_art34, lei_art62 (meilleur score 0.732)

### full

شنو كاتقول الرسالة؟
رخصة الإقامة ديالك غادي تسالي نهار 31 دجنبر 2026. باش تطلب تجديدها، خاصك ترسل الاستمارة المرفقة، نسخة من جواز السفر ديالك الساري، وشهادة من صاحب العمل ديالك قبل أو فآخر أجل هو 6 نونبر 2026. مبلغ 140.00 فرنك سويسري خاص يتخلص كتكلفة لمعالجة الطلب. التأخر قد يؤدي إلى إجراءات إضافية.
شنو خاصك تدير؟
خاصك تجمع الوثائق التالية: الاستمارة المرفقة، نسخة من جواز السفر الساري، وشهادة من صاحب العمل. ثم ترسلها كلها لخدمة السكان قبل أو فآخر أجل 6 نونبر 2026. كما خاصك تخلص مبلغ 140.00 فرنك سويسري.
آخر أجل:
6 نونبر 2026.
المصدر: الرسالة الرسمية الصادرة عن Service de la population.
إلا ما فهميتش شي حاجة أو عندك شك، تاصل مباشرة بService de la population اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 92% | source citée: 0 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
رخصة الإقامة ديالك غادي تسالي نهار 31 دجنبر 2026. باش تطلب تجديدها، خاصك ترسل للخدمة ديال السكان النموذج المرفق، نسخة من جواز السفر ديالك الصالحة، وشهادة من صاحب العمل ديالك، كل ذلك قبل 6 نونبر 2026. كاين رسم إداري بقيمة 140.00 فرنك سويسري، و التأخير قد يؤدي إلى إجراءات إضافية.
- شنو خاصك تدير؟
خاصك تجمع الوثائق المطلوبة (النموذج، جواز السفر، شهادة العمل) وتعيدها في ظرف 6 نونبر 2026، مع دفع مبلغ 140.00 فرنك سويسري.
- آخر أجل:
6 نونبر 2026.
- المصدر: الرسالة الرسمية الصادرة عن Service de la population.
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل بالService de la population اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 91% | source citée: 0 | non soutenus: -_

### baseline

- Ce que dit le courrier : تطلب منك الجهة المختصة تجديد تصريح الإقامة الخاص بك، ويجب عليك إرسال النموذج المرفق مع نسخة من جواز السفر الصالح وشهادة من صاحب العمل قبل 6 نوفمبر 2026، مع دفع مبلغ 140 فرنك سويسري.
- Ce que tu dois faire : أرسل النموذج المرفق، نسخة من جواز السفر الصالح، وشهادة من صاحب العمل إلى الجهة المختصة قبل 6 نوفمبر 2026، ودفع مبلغ 140 فرنك سويسري.
- Avant quand : قبل 6 نوفمبر 2026
- Source : Service de la population - courrier
- Dernière phrase : في حالة الشك، اتصل مباشرة بالجهة التي أرسلت لك هذا الخطاب.

_check.py: OK | arabe 76% | source citée: 0 | non soutenus: -_


## t13 (sejour, de)

Extraction : `{"type_document": "Anmeldung Aufforderung", "delai": "15. Oktober 2026", "montant": null, "action_demandee": "Persönliche Anmeldung bis zum 15. Oktober 2026 mit Pass und Mietvertrag"}`  
Passages : lei_art12_de, lei_art34, kvg_art3_de (meilleur score 0.7456)

### full

شنو كاتقول الرسالة؟
الشركة ديال مراقبة السكان في مدينة عينة (Musterstadt) كاتقول أنك دخلتي لسويسرا نهار 1 أكتوبر 2026، ولكن ما لازالش مسجلة عندهم. ككل أجنبي، خاصك تـتسجل عند السلطة المختصة في مكان إقامتك. خاصك تـتسجل شخصيا قبل 15 أكتوبر 2026، وتجيب معك جواز السفر و عقد الكراء.
شنو خاصك تدير؟
خاصك تـتسجل شخصيا عند السلطة المختصة في مكان إقامتك (Einwohnerkontrolle) قبل 15 أكتوبر 2026، وتجيب معك جواز السفر و عقد الكراء.
آخر أجل:
15 أكتوبر 2026.
المصدر: المادة 12 من قانون الأجانب والاندماج السويسري (LEI).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بالجماعة أو السلطة المختصة في مكان إقامتك.

_check.py: OK | arabe 93% | source citée: 1 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
الجماعة ديالك ما تلقاتش إشعار الإقامة ديالك. خاصك تعلن عن إقامتك قبل 15 أكتوبر 2026 وتجيب معك جواز السفر و عقد الكراء.
- شنو خاصك تدير؟
خاصك تروح للجماعة ديالك قبل 15 أكتوبر 2026 وتقدم طلب إشعار الإقامة، مع جواز السفر و عقد الكراء.
- آخر أجل:
15 أكتوبر 2026.
- المصدر: المادة 12 من قانون الأجانب والاندماج السويسري (LEI).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بالجماعة ديالك (Einwohnerkontrolle Musterstadt).

_check.py: OK | arabe 90% | source citée: 1 | non soutenus: -_

### baseline

- Ce que dit le courrier : Tu as besoin de te présenter en personne à l'Einwohnerkontrolle de ta ville avant le 15 octobre 2026. Tu dois apporter ton passeport et ton contrat de location.
- Ce que tu dois faire : Tu dois te rendre à l'Einwohnerkontrolle de ta commune avant le 15 octobre 2026. Apporte ton passeport et ton contrat de bail.
- Avant quand : Avant le 15 octobre 2026.
- Source : Courrier de l'Einwohnerkontrolle Musterstadt.
- Dernière phrase : En cas de doute, contacte directement l'Einwohnerkontrolle de ta ville.

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_


## t14 (sejour, fr)

Extraction : `{"type_document": "droit d'être entendu", "delai": "22 octobre 2026", "montant": null, "action_demandee": "se déterminer par écrit et transmettre les pièces justificatives"}`  
Passages : lei_art33, lei_art34, lei_art62 (meilleur score 0.6422)

### full

شنو كاتقول الرسالة؟
الجهة المختصة (Service de la population) تفكر في إلغاء رخصة الإقامة ديالك، لأنهم ما بقاوش مطمئنين على أنك تفي بشروط الحصول عليها. قبل ما يتخذوا قرار، عندك الحق تعطيهم جواب مكتوب وتقدم لهم الوثائق ديالك.
شنو خاصك تدير؟
خاصك ترسل جواب مكتوب للجهة المختصة وتوجد وتقدم جميع الوثائق اللي كتثبت أنك لازلت تفي بالشروط، كل هذا قبل تاريخ 22 أكتوبر 2026.
آخر أجل:
22 أكتوبر 2026.
المصدر: الرسالة الرسمية المقدمة.
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بالService de la population اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 89% | source citée: 0 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
الجهة المسؤولة تدرس سحب رخصة الإقامة ديالك لأنها تقول أنك ما كتفيش بالشروط ديال منحها. قبل ما يتخذوا قرار، عندك فرصة تعبر بالكتابة وتقدم الوثائق ديالك حتى تاريخ 22 أكتوبر 2026.
- شنو خاصك تدير؟
خاصك ترسل رسالة مكتوبة للجهة المسؤولة وتقدم جميع الوثائق التي تدعم موقفك، وذلك قبل تاريخ 22 أكتوبر 2026.
- آخر أجل:
22 أكتوبر 2026.
- المصدر: الرسالة الرسمية الصادرة عن Service de la population.
إلا ما فهميتش شي حاجة أو عندك شك، تاصل مباشرة بالService de la population اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 89% | source citée: 0 | non soutenus: -_

### baseline

- Ce que dit le courrier : Le Service de la population veut peut-être annuler ton autorisation de séjour. Tu as le droit de donner ton avis par écrit et de donner des documents jusqu'au 22 octobre 2026. Si tu ne réponds pas, ils prendront une décision sans ton point de vue.
- Ce que tu dois faire : Tu dois écrire une lettre pour donner ton point de vue et envoyer tous les documents qui prouvent que tu remplis les conditions de ton autorisation de séjour.
- Avant quand : Tu dois le faire avant le 22 octobre 2026.
- Source : Courrier du Service de la population (objet : droit d'être entendu avant décision)
- Dernière phrase : En cas de doute, contacte directement le Service de la population qui t'a envoyé ce courrier.

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_


## t15 (sejour, de)

Extraction : `{"type_document": "Gesuch um Niederlassungsbewilligung", "delai": "2. November 2026", "montant": "CHF 150.00", "action_demandee": "Einreichen eines Nachweises der Sprachkenntnisse und Bezahlung der Gebühr von CHF 150.00 bis zum 2. November 2026"}`  
Passages : lei_art34_de, lei_art12_de, schkg_art74_de (meilleur score 0.6396)

### full

شنو كاتقول الرسالة؟
طلب الإقامة الدائمة ديالك وصلنا. باش نقدر نحلّو، خاصك تقدم وثيقة تثبت معرفتك للغات حتى تاريخ 2 نونبر 2026. كما خاصك تخلص واجب التأمين الصحي أو الرسم بقيمة 150.00 فرنك سويسري لنفس التاريخ. إلا ما قدمتيش الوثيقة، ما يمكنش متابعة طلبك.
شنو خاصك تدير؟
خاصك تجمع وثيقة إثبات معرفتك للغات وتخلص مبلغ 150.00 فرنك سويسري.
آخر أجل:
2 نونبر 2026.
المصدر: الرسالة الرسمية من Migrationsamt (مكتب الهجرة).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بمكتب الهجرة اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 96% | source citée: 0 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
طلب الإقامة الدائمة ديالك وصلنا. خاصك تقدم دليل على معرفتك للغات حتى تاريخ 2 نونبر 2026، وكذلك تخلص رسم الطلب اللي هو 150.00 فرنك سويسري. إلا ما قدمتيش الوثائق، ما يمكنش متابعة الطلب ديالك.
- شنو خاصك تدير؟
خاصك تجمع وثيقة إثبات معرفتك للغات وتقدمها، وكذلك تخلص مبلغ 150.00 فرنك سويسري، كل ذلك قبل أو في تاريخ 2 نونبر 2026.
- آخر أجل:
2 نونبر 2026.
- المصدر: الرسالة الرسمية الصادرة عن Migrationsamt (مكتب الهجرة).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بمكتب الهجرة اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 96% | source citée: 0 | non soutenus: -_

### baseline

- Ce que dit le courrier : Il faut fournir une preuve de ses connaissances linguistiques et payer une taxe de CHF 150.00 avant le 2 novembre 2026. Sans ces documents, la demande ne sera pas traitée.
- Ce que tu dois faire : Tu dois présenter un certificat de langue et payer CHF 150.00 avant le 2 novembre 2026.
- Avant quand : Avant le 2 novembre 2026.
- Source : Courrier du Migrationsamt Musterkanton.
- Dernière phrase : En cas de doute, contacte directement le Migrationsamt Musterkanton.

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_


## t16 (autre, fr)

Extraction : `{"type_document": "Facture", "delai": "9 novembre 2026", "montant": "CHF 335.00", "action_demandee": "Payer le montant de CHF 335.00 jusqu'au 9 novembre 2026"}`  
Passages : aucun (règle sans source) (meilleur score 0.532)

### full

شنو كاتقول الرسالة؟
الهيئة المسؤولة على تحصيل رسوم التلفزة والإذاعة بعثت فاتورة سنوية ديال عام 2026 بقيمة 335.00 فرنك سويسري، وتطلب منك تخلصها قبل 9 نونبر 2026.
شنو خاصك تدير؟
خاصك تخلص مبلغ 335.00 فرنك سويسري قبل أو فآخر أجل 9 نونبر 2026.
آخر أجل:
9 نونبر 2026.
المصدر: الفاتورة المرسلة من طرف Organe de perception de la redevance radio et télévision.
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بالهيئة المسؤولة على تحصيل الرسوم (Organe de perception de la redevance radio et télévision).

_check.py: OK | arabe 73% | source citée: None | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
  وصلتك فاتورة سنوية لرسوم التلفزة والراديو لسنة 2026 بقيمة 335.00 فرنك سويسري، خاصك تخلصها حتى تاريخ 9 نونبر 2026.
- شنو خاصك تدير؟
  خاصك تخلص مبلغ 335.00 فرنك سويسري ل organe de perception de la redevance حتى تاريخ 9 نونبر 2026.
- آخر أجل:
  9 نونبر 2026.
- المصدر:
  الرسالة الأصلية من organe de perception de la redevance.
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل مباشرة ب organe de perception de la redevance اللي صيفطات ليك الفاتورة.

_check.py: OK | arabe 71% | source citée: None | non soutenus: -_

### baseline

- Ce que dit le courrier : C'est une facture pour la redevance radio et télévision de l'année 2026. Il faut payer CHF 335.00 avant le 9 novembre 2026.
- Ce que tu dois faire : Tu dois payer la somme de CHF 335.00 avant le 9 novembre 2026.
- Avant quand : Avant le 9 novembre 2026.
- Source : Organe de perception de la redevance, Facture annuelle de la redevance radio et télévision 2026
- Dernière phrase : En cas de doute, contacte directement l'organisme qui a envoyé le courrier.

_check.py: OK | arabe 0% | source citée: None | non soutenus: -_


## t17 (autre, de)

Extraction : `{"type_document": "Ordnungsbusse", "delai": "9. November 2026", "montant": "CHF 40.00", "action_demandee": "Bezahlen Sie den Betrag mit dem beiliegenden Einzahlungsschein"}`  
Passages : aucun (règle sans source) (meilleur score 0.4632)

### full

شنو كاتقول الرسالة؟
الشرطة البلدية ديال مدينة عينة غرّمتك مبلغ 40.00 فرنك سويسري لأنك وقفت فالمنطقة اللي ممنوعة الوقوف، نهار 2 أكتوبر 2026. خاصك تخلص هاد المبلغ.
شنو خاصك تدير؟
خاصك تخلص مبلغ 40.00 فرنك سويسري، باستخدام ورقة الأداء (Einzahlungsschein) اللي مع الرسالة.
آخر أجل:
9 نونبر 2026.
المصدر: الرسالة من الشرطة البلدية (Stadtpolizei Musterstadt).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بالشرطة البلدية ديال المدينة اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 88% | source citée: None | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
تم تغريمك بمبلغ 40.00 فرنك سويسري لأنك وقفت في منطقة ممنوعة في Bahnhofstrasse نهار 2 أكتوبر 2026. خاصك تخلص المبلغ مع وصل الدفع المرفق.
- شنو خاصك تدير؟
خاصك تخلص مبلغ 40.00 فرنك سويسري قبل أو في تاريخ 9 نونبر 2026، باستخدام وصل الدفع المرفق مع الرسالة.
- آخر أجل:
9 نونبر 2026.
- المصدر: الرسالة من الشرطة البلدية (Stadtpolizei Musterstadt).
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بالشرطة البلدية (Stadtpolizei Musterstadt).

_check.py: OK | arabe 82% | source citée: None | non soutenus: -_

### baseline

- Ce que dit le courrier : تم توقيفك لوقوفك في منطقة ممنوعة يوم 2 أكتوبر 2026 في Bahnhofstrasse. عليك دفع غرامة قدرها CHF 40.00 قبل 9 نوفمبر 2026 باستخدام وصل الدفع المرفق.
- Ce que tu dois faire : ادفع مبلغ CHF 40.00 قبل تاريخ 9 نوفمبر 2026 باستخدام وصل الدفع المرفق مع الرسالة.
- Avant quand : قبل 9 نوفمبر 2026.
- Source : Stadtpolizei Musterstadt, Ordnungsbusse.
- Dernière phrase : في حالة الشك، اتصل مباشرة بالجهة التي أرسلت لك الرسالة (Stadtpolizei Musterstadt).

_check.py: OK | arabe 57% | source citée: None | non soutenus: -_


## t18 (autre, de)

Extraction : `{"type_document": "Rechnung", "delai": "28. Oktober 2026", "montant": "CHF 89.90", "action_demandee": "Zahlung bis zum 28. Oktober 2026"}`  
Passages : aucun (règle sans source) (meilleur score 0.5054)

### full

شنو كاتقول الرسالة؟
شركة Beispiel Telecom AG كاتطلب منك تخلص فاتورة أكتوبر 2026، اللي فيها مبلغ إجمالي قدره 89.90 فرنك سويسري.
شنو خاصك تدير؟
خاصك تخلص مبلغ 89.90 فرنك سويسري قبل أو فآخر أجل المحدد.
آخر أجل:
28 أكتوبر 2026.
المصدر: الفاتورة الصادرة عن شركة Beispiel Telecom AG.
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بشركة Beispiel Telecom AG.

_check.py: OK | arabe 80% | source citée: None | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
شركة Beispiel Telecom AG كاتطلب منك تدفع فاتورة أكتوبر 2026، اللي هي 89.90 فرنك سويسري، قبل تاريخ 28 أكتوبر 2026.
- شنو خاصك تدير؟
خاصك تخلص المبلغ 89.90 فرنك سويسري قبل أو في تاريخ 28 أكتوبر 2026.
- آخر أجل:
28 أكتوبر 2026.
- المصدر: الرسالة الأصلية من Beispiel Telecom AG.
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل بشركة Beispiel Telecom AG.

_check.py: OK | arabe 79% | source citée: None | non soutenus: -_

### baseline

- Ce que dit le courrier : C'est une facture de la société Beispiel Telecom AG pour le mois d'octobre 2026. Elle comprend le prix de l'abonnement mobile (CHF 59.90) et une option supplémentaire pour l'international (CHF 30.00). Le total à payer est de CHF 89.90 et il faut le régler avant le 28 octobre 2026.
- Ce que tu dois faire : Tu dois payer la somme de CHF 89.90 avant le 28 octobre 2026.
- Avant quand : Avant le 28 octobre 2026.
- Source : Courrier de Beispiel Telecom AG, section "Rechnung für Oktober 2026" et "Zahlbar bis zum 28. Oktober 2026".
- Dernière phrase : En cas de doute, contacte directement Beispiel Telecom AG.

_check.py: OK | arabe 0% | source citée: None | non soutenus: -_


## t19 (autre, fr)

Extraction : `{"type_document": "Invitation à payer", "delai": "16 novembre 2026", "montant": "CHF 180.00", "action_demandee": "Retourner le talon d'inscription signé et verser le montant"}`  
Passages : aucun (règle sans source) (meilleur score 0.4839)

### full

شنو كاتقول الرسالة؟
المدرسة الابتدائية ديال Montclair تدعو الأطفال لحضور مخيم التزلج من 18 إلى 22 يناير 2027. المبلغ المطلوب من كل عائلة هو 180.00 فرنك سويسري.
شنو خاصك تدير؟
خاصك ترسل الورقة المرفقة (talon d'inscription) موقعة، وتخلص المبلغ 180.00 فرنك سويسري.
آخر أجل:
16 نونبر 2026.
المصدر: الرسالة الصادرة عن المدرسة الابتدائية ديال Montclair.
إلا ما فهميتش شي حاجة أو عندك شك، تاصل بالمدرسة الابتدائية ديال Montclair.

_check.py: OK | arabe 86% | source citée: None | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
  المدرسة الابتدائية ديال Montclair دعاتكم لحضور المخيم ديال التزلج من 18 إلى 22 يناير 2027. الثمن لكل عائلة هو 180.00 فرنك سويسري. خاصكم ترسلو التيلون الموقّع وتخلصوا المبلغ حتى 16 نونبر 2026.
- شنو خاصك تدير؟
  خاصك ترسل التيلون الموقّع وتخلص مبلغ 180.00 فرنك سويسري، كل هذا قبل 16 نونبر 2026.
- آخر أجل:
  16 نونبر 2026.
- المصدر:
  الرسالة من المدرسة الابتدائية ديال Montclair.
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل مباشرة بالمدرسة الابتدائية ديال Montclair.

_check.py: OK | arabe 92% | source citée: None | non soutenus: -_

### baseline

- Ce que dit le courrier : Il faut payer CHF 180.00 pour le camp de ski de l'école primaire de Montclair qui aura lieu en janvier 2027. Il faut aussi renvoyer le talon d'inscription signé.
- Ce que tu dois faire : Tu dois renvoyer le talon d'inscription signé et payer CHF 180.00.
- Avant quand : Avant le 16 novembre 2026.
- Source : École primaire de Montclair, courrier "Camp de ski 2027"
- Dernière phrase : En cas de doute, contacte directement l'école primaire de Montclair.

_check.py: OK | arabe 0% | source citée: None | non soutenus: -_


## t20 (rappel_poursuite, de)

Extraction : `{"type_document": "Mahnung", "delai": "22. Oktober 2026", "montant": "CHF 422.30", "action_demandee": "Überweisung des Betrags bis zum 22. Oktober 2026"}`  
Passages : kvg_art64a_de, schkg_art74_de, schkg_art69 (meilleur score 0.5638)

### full

شنو كاتقول الرسالة؟
الجماعة ديال Musterstadt كاتطلب منك تخلص فاتورة ديال الكهرباء أو الماء رقم 774120 اللي هي 412.30 فرنك سويسري، مع مصاريف التذكير اللي هي 10 فرنك سويسري، مجموعها 422.30 فرنك سويسري. خاصك تخلص المبلغ قبل 22 أكتوبر 2026، وإلا غادي يبداو إجراءات تحصيل الدين.
شنو خاصك تدير؟
خاصك تخلص المبلغ الكلي 422.30 فرنك سويسري قبل أو فآخر أجل 22 أكتوبر 2026. تقدر تخلص بالبريد أو عبر البنك أو بأي وسيلة أخرى مع ذكر رقم الفاتورة.
آخر أجل:
22 أكتوبر 2026.
المصدر: الفقرة الأولى من المادة 64a من قانون التأمين الصحي السويسري (KVG) المتعلقة بالتذكير بالخلاص.
إلا ما فهميتش شي حاجة أو عندك مشكل فالخلاص، تاصل مباشرة بالجماعة ديال Musterstadt (Stadtwerke Musterstadt).

_check.py: OK | arabe 90% | source citée: 1 | non soutenus: -_

### no_glossary

- شنو كاتقول الرسالة؟
الشركة ديال الماء والكهرباء (Stadtwerke) كاتطلب منك تدفع فاتورة بقيمة 422.30 فرنك سويسري، بما فيها رسوم تذكير بقيمة 10 فرنك سويسري، قبل تاريخ 22 أكتوبر 2026. وإلا ما تدفعتيش، غادي يبداو إجراءات قانونية لتحصيل الدين.
- شنو خاصك تدير؟
خاصك تخلص المبلغ الكلي 422.30 فرنك سويسري قبل أو في تاريخ 22 أكتوبر 2026.
- آخر أجل:
22 أكتوبر 2026.
- المصدر: الرسالة الرسمية (Mahnung) الصادرة عن Stadtwerke Musterstadt.
- إلا ما فهميتش شي حاجة أو عندك شك، تاصل مباشرة بشركة Stadtwerke Musterstadt اللي صيفطات ليك الرسالة.

_check.py: OK | arabe 85% | source citée: 0 | non soutenus: -_

### baseline

- Ce que dit le courrier : C'est un avertissement (Mahnung) pour une facture impayée. Il faut payer CHF 422.30 avant le 22 octobre 2026, sinon ils lanceront une procédure de recouvrement (Betreibung).
- Ce que tu dois faire : Tu dois payer la somme de CHF 422.30 avant le 22 octobre 2026.
- Avant quand : Avant le 22 octobre 2026.
- Source : Courrier reçu de Stadtwerke Musterstadt.
- Dernière phrase : En cas de doute, contacte directement Stadtwerke Musterstadt.

_check.py: OK | arabe 0% | source citée: 0 | non soutenus: -_
