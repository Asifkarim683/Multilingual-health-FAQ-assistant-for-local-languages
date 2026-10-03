"""Curated repository of official public health source texts across all 8 required topics in English, Hindi, and Odia."""
from typing import List, Dict, Any

OFFICIAL_HEALTH_DOCUMENTS: List[Dict[str, Any]] = [
    # 1. Vector-borne diseases (Dengue, Malaria)
    {
        "doc_id": "SRC-01",
        "title": "Dengue Fever and Vector Control Guidelines",
        "language": "en",
        "topic": "Vector-borne diseases",
        "url": "https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue",
        "section": "Symptoms, Transmission, and Prevention",
        "text": """
Dengue is a viral infection transmitted to humans through the bite of infected Aedes mosquitoes, primarily Aedes aegypti. The mosquitoes thrive in urban environments and breed in clean, stagnant water containers such as discarded tires, flower pots, overhead tanks, and plastic vessels.

Common symptoms of dengue include sudden high fever (40°C/104°F), severe headache, pain behind the eyes, joint and muscle pain, fatigue, nausea, vomiting, and skin rash. Symptoms typically begin 4 to 10 days after infection and last for 2 to 7 days. Most patients recover within 1-2 weeks.

Warning signs of severe dengue (dengue hemorrhagic fever) appear after the initial fever drops (usually 3 to 7 days after illness onset). Warning signs include severe abdominal pain, persistent vomiting, mucosal bleeding (gums or nose), rapid breathing, fatigue, restlessness, and blood in vomit or stool. If any warning signs appear, immediate hospitalization is critical for fluid replacement.

Prevention focuses on mosquito bite prevention: wearing long-sleeved clothing, using mosquito nets and repellents, and eliminating standing water weekly (Dry Day practice) to disrupt larval breeding cycles.
"""
    },
    {
        "doc_id": "SRC-01-HI",
        "title": "डेंगू बुखार के लक्षण, बचाव एवं नियंत्रण",
        "language": "hi",
        "topic": "Vector-borne diseases",
        "url": "https://nvbdcp.gov.in/index4.php?lang=1&level=0&linkid=431&lid=3685",
        "section": "लक्षण और बचाव",
        "text": """
डेंगू एडीज मच्छर के काटने से फैलने वाली एक विषाणु जनित (वायरल) बीमारी है। एडीज मच्छर दिन के समय काटता है और साफ, ठहरे हुए पानी जैसे कूलरों, टंकियों, गमलों और पुराने टायरों में पनपता है।

डेंगू के मुख्य लक्षण: तेज बुखार, सिरदर्द, आंखों के पीछे दर्द, जोड़ों और मांसपेशियों में तेज दर्द, जी मिचलाना, उल्टी और त्वचा पर लाल चकत्ते। यह लक्षण मच्छर के काटने के 4 से 10 दिनों में दिखाई देते हैं।

गंभीर डेंगू के खतरे के लक्षण: पेट में लगातार तेज दर्द, बार-बार उल्टी होना, नाक या मसूड़ों से खून आना, अत्यधिक थकान, बेचैनी और सांस लेने में कठिनाई। ऐसे लक्षण दिखने पर रोगी को बिना देर किए तुरंत अस्पताल ले जाना चाहिए।

बचाव के उपाय: घर के आसपास पानी जमा न होने दें। हर सप्ताह कूलर और पानी के बर्तनों को सुखाकर साफ करें। पूरे शरीर को ढकने वाले कपड़े पहनें और मच्छरदानी या मच्छर भगाने वाली दवाओं का प्रयोग करें।
"""
    },
    {
        "doc_id": "SRC-01-OR",
        "title": "ଡେଙ୍ଗୁ ଜ୍ୱରର ଲକ୍ଷଣ, ନିରାକରଣ ଓ ପ୍ରତିକାର",
        "language": "or",
        "topic": "Vector-borne diseases",
        "url": "http://www.nrhmorissa.gov.in/dengue-guidelines",
        "section": "ଲକ୍ଷଣ ଏବଂ ସତର୍କତା",
        "text": """
ଡେଙ୍ଗୁ ଏକ ଭୂତାଣୁଜନିତ ରୋଗ ଯାହା ଏଡିସ୍ ମଶା କାମୁଡ଼ିବା ଦ୍ୱାରା ବ୍ୟାପିଥାଏ। ଏହି ମଶା ସାଧାରଣତଃ ଦିନବେଳା କାମୁଡ଼ିଥାଏ ଏବଂ ଘର ଭିତରେ ବା ପାଖରେ ଥିବା ସଫା ଜମା ପାଣି, କୁଲର, ଫୁଲକୁଣ୍ଡ ଏବଂ ଟାୟାରରେ ବଂଶବୃଦ୍ଧି କରେ।

ଡେଙ୍ଗୁର ପ୍ରମୁଖ ଲକ୍ଷଣ: ହଠାତ୍ ପ୍ରବଳ ଜ୍ୱର, ମୁଣ୍ଡବିନ୍ଧା, ଆଖି ପଛପଟେ ଯନ୍ତ୍ରଣା, ଗଣ୍ଠି ଓ ମାଂସପେଶୀ ବିନ୍ଧା, ବାନ୍ତି ଏବଂ ଶରୀରରେ ଲାଲ ଦାଗ। ଏହି ଲକ୍ଷଣଗୁଡ଼ିକ ୨ ରୁ ୭ ଦିନ ପର୍ଯ୍ୟନ୍ତ ରହିପାରେ।

ବିପଦପୂର୍ଣ୍ଣ ଲକ୍ଷଣ: ପ୍ରବଳ ପେଟ ଯନ୍ତ୍ରଣା, ଲଗାତାର ବାନ୍ତି, ନାକ କିମ୍ବା ମାଢ଼ିରୁ ରକ୍ତସ୍ରାବ, ଦୁର୍ବଳତା ଏବଂ ନିଶ୍ୱାସ ନେବାରେ କଷ୍ଟ। ଏପରି ଲକ୍ଷଣ ଦେଖାଦେଲେ ତୁରନ୍ତ ନିକଟସ୍ଥ ଡାକ୍ତରଖାନାରେ ଭର୍ତ୍ତି କରନ୍ତୁ।

ପ୍ରତିରୋଧ: ପ୍ରତି ସପ୍ତାହରେ ଘର ଚାରିପାଖରେ ଥିବା ଜମା ପାଣି ସଫା କରନ୍ତୁ (ଡ୍ରାଏ ଡେ ପାଳନ କରନ୍ତୁ), ସମ୍ପୂର୍ଣ୍ଣ ଶରୀର ଘୋଡ଼ାଇ ହେଉଥିବା ପୋଷାକ ପିନ୍ଧନ୍ତୁ ଏବଂ ମଶାରୀ ବ୍ୟବହାର କରନ୍ତୁ।
"""
    },

    # 2. Diabetes basics and lifestyle
    {
        "doc_id": "SRC-04",
        "title": "Type 2 Diabetes Prevention and Management",
        "language": "en",
        "topic": "Diabetes basics and lifestyle",
        "url": "https://www.who.int/news-room/fact-sheets/detail/diabetes",
        "section": "Lifestyle, Nutrition, and Screening",
        "text": """
Diabetes is a chronic metabolic disorder characterized by elevated levels of blood glucose. In Type 2 diabetes, the body either resists the effects of insulin or does not produce enough insulin. It accounts for over 95% of diabetes cases and is closely linked to excess body weight, physical inactivity, and dietary factors.

Common symptoms include frequent urination (polyuria), excessive thirst (polydipsia), persistent hunger, unexplained weight loss, blurred vision, extreme fatigue, and slow-healing sores or frequent infections. Many people with Type 2 diabetes have no symptoms for years until complications develop.

Lifestyle measures to prevent or manage Type 2 diabetes include:
1. Achieving and maintaining healthy body weight.
2. At least 30 minutes of moderate-intensity physical activity (e.g. brisk walking) at least 5 days a week.
3. Eating a balanced diet rich in dietary fiber, whole grains, lentils, legumes, vegetables, and fresh fruits while avoiding refined sugars, sugary beverages, and saturated fats.
4. Avoiding tobacco use and limiting alcohol.
5. Routine monitoring of fasting blood sugar and HbA1c to detect complications early.
"""
    },
    {
        "doc_id": "SRC-04-HI",
        "title": "मधुमेह (डायबिटीज) के लक्षण, आहार एवं जीवनशैली",
        "language": "hi",
        "topic": "Diabetes basics and lifestyle",
        "url": "https://www.icmr.gov.in/guidelines-diabetes",
        "section": "जीवनशैली और आहार",
        "text": """
मधुमेह एक दीर्घकालिक उपापचयी रोग है जिसमें रक्त में ग्लूकोज (शर्करा) का स्तर सामान्य से अधिक हो जाता है। टाइप-2 मधुमेह सबसे आम है जो मुख्य रूप से अस्वस्थ खानपान, मोटापे और शारीरिक निष्क्रियता के कारण होता है।

मधुमेह के प्रमुख लक्षण: बार-बार पेशाब लगना, बहुत अधिक प्यास लगना, बिना कारण वजन घटना, लगातार भूख लगना, आंखों में धुंधलापन, अत्यधिक थकान और घाव या चोट का देर से भरना।

मधुमेह नियंत्रण एवं रोकथाम के नियम:
1. प्रतिदिन कम से कम 30 से 45 मिनट तेज चाल से टहलना या योग/व्यायाम करना।
2. आहार में साबुत अनाज, दालें, हरी पत्तेदार सब्जियां और सलाद का सेवन बढ़ाएं।
3. चीनी, मिठाई, मीठे पेय, मैदा और तले हुए भोजन से पूरी तरह परहेज करें।
4. तंबाकू और धूम्रपान का सेवन बंद करें।
5. खाली पेट और भोजन के बाद रक्त शर्करा (ब्लड शुगर) की नियमित जांच कराएं।
"""
    },
    {
        "doc_id": "SRC-04-OR",
        "title": "ମଧୁମେହ (ଡାଇବେଟିସ୍) ରୋକିବା ଓ ଜୀବନଶୈଳୀ ପରିଚାଳନା",
        "language": "or",
        "topic": "Diabetes basics and lifestyle",
        "url": "http://www.nrhmorissa.gov.in/ncd-diabetes",
        "section": "ଖାଦ୍ୟପେୟ ଏବଂ ବ୍ୟାୟାମ",
        "text": """
ମଧୁମେହ ହେଉଛି ଏକ ଦୀର୍ଘକାଳୀନ ରୋଗ ଯେଉଁଥିରେ ରକ୍ତରେ ଶର୍କରାର ମାତ୍ରା ବୃଦ୍ଧି ପାଏ। ଉପଯୁକ୍ତ ବ୍ୟାୟାମର ଅଭାବ, ମୋଟାପଣ ଏବଂ ଅସ୍ୱାସ୍ଥ୍ୟକର ଖାଦ୍ୟାଭ୍ୟାସ ଯୋଗୁଁ ଟାଇପ୍-୨ ମଧୁମେହ ହୋଇଥାଏ।

ମୁଖ୍ୟ ଲକ୍ଷଣଗୁଡ଼ିକ: ବାରମ୍ବାର ପରିସ୍ରା ଲାଗିବା, ଅତ୍ୟଧିକ ଶୋଷ ଏବଂ ଭୋକ ଲାଗିବା, ଶରୀରର ଓଜନ ହଠାତ୍ କମିବା, ଆଖିକୁ ଝାପ୍ସା ଦେଖାଯିବା, ଦୁର୍ବଳତା ଏବଂ କୌଣସି କ୍ଷତ ବା ଘାଆ ଶୀଘ୍ର ନ ଶୁଖିବା।

ଜୀବନଶୈଳୀ ପରିବର୍ତ୍ତନ:
୧. ପ୍ରତିଦିନ ଅତି କମରେ ୩୦ ମିନିଟ୍ ଦ୍ରୁତ ପଦଯାତ୍ରା କିମ୍ବା ବ୍ୟାୟାମ କରନ୍ତୁ।
୨. ଖାଦ୍ୟରେ ଫାଇବର ଯୁକ୍ତ ପନିପରିବା, ଶାଗ, ଡାଲି ଏବଂ ଶସ୍ୟ ସାମିଲ କରନ୍ତୁ।
୩. ମିଠା, ଚିନି, କୋଲ୍ଡ ଡ୍ରିଙ୍କ୍ସ, ଏବଂ ଅତ୍ୟଧିକ ତେଲଯୁକ୍ତ ଖାଦ୍ୟଠାରୁ ଦୂରେଇ ରୁହନ୍ତୁ।
୪. ଧୂମପାନ ଓ ତମାଖୁ ସେବନ ବନ୍ଦ କରନ୍ତୁ ଏବଂ ନିୟମିତ ବ୍ୟବଧାନରେ ରକ୍ତ ପରୀକ୍ଷା କରନ୍ତୁ।
"""
    },

    # 3. Hypertension basics and lifestyle
    {
        "doc_id": "SRC-05",
        "title": "Hypertension Diagnosis and Lifestyle Guidelines",
        "language": "en",
        "topic": "Hypertension basics and lifestyle",
        "url": "https://www.who.int/news-room/fact-sheets/detail/hypertension",
        "section": "Blood Pressure Targets and Salt Reduction",
        "text": """
Hypertension (high blood pressure) occurs when blood pressure in the arteries is persistently elevated (systolic pressure >= 140 mmHg or diastolic pressure >= 90 mmHg on two separate days). Often called a "silent killer," hypertension usually presents no noticeable symptoms until severe damage to the heart, brain, or kidneys has already occurred.

When symptoms do occur, they can include early morning headaches, nosebleeds, irregular heart rhythms, vision changes, and buzzing in the ears. Severe hypertension can cause fatigue, nausea, vomiting, confusion, anxiety, chest pain, and muscle tremors.

Key non-pharmacological management recommendations:
1. Reduce dietary salt consumption to less than 5 grams per day (equivalent to under 1 level teaspoon).
2. Follow the DASH (Dietary Approaches to Stop Hypertension) pattern: eat more fruits, vegetables, low-fat dairy, and reduce saturated fats.
3. Engage in regular physical aerobic exercise (150 minutes of moderate activity per week).
4. Maintain a healthy Body Mass Index (BMI between 18.5 and 24.9 kg/m2).
5. Stop smoking and limit alcohol intake.
6. Manage psychological stress with adequate sleep and relaxation techniques.
"""
    },
    {
        "doc_id": "SRC-05-HI",
        "title": "उच्च रक्तचाप (हाई ब्लड प्रेशर) नियंत्रण एवं जीवनशैली",
        "language": "hi",
        "topic": "Hypertension basics and lifestyle",
        "url": "https://www.ihci.in/guidelines-hypertension",
        "section": "नमक में कमी और दैनिक नियम",
        "text": """
उच्च रक्तचाप (हाइपरटेंशन) तब माना जाता है जब रक्तचाप लगातार 140/90 mmHg या इससे अधिक रहता है। इसे अक्सर 'साइलेंट किलर' कहा जाता है क्योंकि शुरुआती दौर में इसके कोई स्पष्ट लक्षण दिखाई नहीं देते।

लक्षण: सिर के पिछले हिस्से में सुबह दर्द होना, चक्कर आना, घबराहट, सीने में भारीपन, सांस फूलना या नाक से खून आना।

जीवनशैली में जरूरी बदलाव:
1. भोजन में नमक की मात्रा कम करें - प्रतिदिन 5 ग्राम (एक छोटा चम्मच) से कम नमक खाएं। पापड़, अचार, नमकीन और डिब्बाबंद खाद्य पदार्थों से बचें।
2. ताजे फल, सब्जियां, सलाद और कम वसा वाले दुग्ध उत्पादों का सेवन करें।
3. प्रतिदिन 30 मिनट टहलें और वजन को नियंत्रित रखें।
4. बीड़ी, सिगरेट और तंबाकू का सेवन पूरी तरह छोड़ दें।
5. हर महीने अपने नजदीकी स्वास्थ्य केंद्र पर जाकर रक्तचाप की जांच कराएं।
"""
    },
    {
        "doc_id": "SRC-05-OR",
        "title": "ଉଚ୍ଚ ରକ୍ତଚାପ (ହାଇ ବିପି) ନିୟନ୍ତ୍ରଣ ଓ ସ୍ୱାସ୍ଥ୍ୟକର ଜୀବନଶୈଳୀ",
        "language": "or",
        "topic": "Hypertension basics and lifestyle",
        "url": "http://www.nrhmorissa.gov.in/ncd-hypertension",
        "section": "ଲୁଣ ନିୟନ୍ତ୍ରଣ ଏବଂ ପରାମର୍ଶ",
        "text": """
ଉଚ୍ଚ ରକ୍ତଚାପ (ହାଇପରଟେନସନ) ସେତେବେଳେ କୁହାଯାଏ ଯେତେବେଳେ ରକ୍ତଚାପ ଲଗାତାର ୧୪୦/୯୦ mmHg ବା ତା’ଠାରୁ ଅଧିକ ରହିଥାଏ। ଏହାର କୌଣସି ସ୍ପଷ୍ଟ ବାହ୍ୟ ଲକ୍ଷଣ ନ ଥାଇ ମଧ୍ୟ ଏହା ହୃଦଘାତ ବା ଷ୍ଟ୍ରୋକ୍ କରାଇପାରେ।

କେତେକ କ୍ଷେତ୍ରରେ ମୁଣ୍ଡ ବୁଲାଇବା, ମୁଣ୍ଡବିନ୍ଧା, ଛାତି ଧଡ଼ଧଡ଼ ହେବା କିମ୍ବା ନାକରୁ ରକ୍ତ ପଡ଼ିବା ଭଳି ଲକ୍ଷଣ ଦେଖାଦିଏ।

ନିୟନ୍ତ୍ରଣ ପାଇଁ ମୁଖ୍ୟ ଉପାୟ:
୧. ଦୈନିକ ଖାଦ୍ୟରେ ଲୁଣର ପରିମାଣ କମାନ୍ତୁ - ଦିନକୁ ୫ ଗ୍ରାମ (ଗୋଟିଏ ଛୋଟ ଚାମଚ)ରୁ କମ୍ ଲୁଣ ଖାଆନ୍ତୁ। ଆଚାର, ପାମ୍ପଡ଼ ଏବଂ ଚିପ୍ସ ବର୍ଜନ କରନ୍ତୁ।
୨. ଖାଦ୍ୟରେ ସବୁଜ ପନିପରିବା ଏବଂ ତାଜା ଫଳ ଅଧିକ ଖାଆନ୍ତୁ।
୩. ପ୍ରତିଦିନ ସକାଳେ ଅତି କମରେ ଅଧଘଣ୍ଟା ଚାଲିବା ଅଭ୍ୟାସ କରନ୍ତୁ।
୪. ଧୂମପାନ ଓ ମଦ୍ୟପାନ ସମ୍ପୂର୍ଣ୍ଣ ବନ୍ଦ କରନ୍ତୁ।
୫. ପ୍ରତି ମାସରେ ସ୍ୱାସ୍ଥ୍ୟକେନ୍ଦ୍ରରେ ରକ୍ତଚାପ ପରୀକ୍ଷା କରାନ୍ତୁ।
"""
    },

    # 4. Child immunization schedule
    {
        "doc_id": "SRC-03",
        "title": "National Immunization Schedule (NIS) of India",
        "language": "en",
        "topic": "Child immunization schedule",
        "url": "https://main.mohfw.gov.in/sites/default/files/National_Immunization_Schedule.pdf",
        "section": "Infant and Child Vaccine Timetable",
        "text": """
The Universal Immunization Programme (UIP) in India protects children against 12 life-threatening vaccine-preventable diseases.

Vaccination Schedule for Infants and Children:
- At Birth: BCG (Tuberculosis), Oral Polio Vaccine (OPV birth dose), and Hepatitis B (birth dose within 24 hours of birth).
- At 6 Weeks: OPV-1, Pentavalent-1 (Diphtheria, Pertussis, Tetanus, Hepatitis B, Hib), Rotavirus Vaccine-1 (RVV), Fractional Inactivated Poliovirus Vaccine-1 (fIPV-1), and Pneumococcal Conjugate Vaccine-1 (PCV-1).
- At 10 Weeks: OPV-2, Pentavalent-2, and RVV-2.
- At 14 Weeks: OPV-3, Pentavalent-3, RVV-3, fIPV-2, and PCV-2.
- At 9 to 12 Months: Measles-Rubella-1 (MR-1), PCV Booster, Japanese Encephalitis-1 (in endemic districts), and Vitamin A 1st dose (1 lakh IU).
- At 16 to 24 Months: MR-2, DPT Booster-1, OPV Booster, JE-2, and Vitamin A 2nd dose (2 lakh IU).
- At 5 to 6 Years: DPT Booster-2.
- At 10 and 16 Years: Td (Tetanus and adult Diphtheria) vaccine.

All government health sub-centers, Primary Health Centers (PHCs), and Anganwadi centers administer these vaccines free of cost on designated Village Health and Nutrition Days (VHND).
"""
    },
    {
        "doc_id": "SRC-03-HI",
        "title": "राष्ट्रीय टीकाकरण सारणी (भारत सरकार)",
        "language": "hi",
        "topic": "Child immunization schedule",
        "url": "https://main.mohfw.gov.in/national-immunization-schedule",
        "section": "शिशुओं और बच्चों का टीकाकरण",
        "text": """
भारत के सार्वभौमिक टीकाकरण कार्यक्रम (UIP) के अंतर्गत बच्चों को 12 जानलेवा बीमारियों से बचाने के लिए निःशुल्क टीके लगाए जाते हैं।

टीकाकरण का समय:
- जन्म के समय: बीसीजी (टीबी से बचाव), पोलियो की जीरो खुराक (OPV-0), और हेपेटाइटिस बी जन्म खुराक (24 घंटे के अंदर)।
- 6 सप्ताह पर: पेंटावेलेंट-1 (गलघोंटू, काली खांसी, टिटनेस, हेपेटाइटिस बी, हिब), पोलियो-1 (OPV-1), रोटावायरस-1, fIPV-1, और न्यूमोकोकल (PCV-1)।
- 10 सप्ताह पर: पेंटावेलेंट-2, पोलियो-2, रोटावायरस-2।
- 14 सप्ताह पर: पेंटावेलेंट-3, पोलियो-3, रोटावायरस-3, fIPV-2, और PCV-2।
- 9 से 12 महीने पर: खसरा-रूबेला (MR-1), पीसीवी बूस्टर, और विटामिन ए की पहली खुराक।
- 16 से 24 महीने पर: एमआर-2, डीपीटी बूस्टर-1, पोलियो बूस्टर, और विटामिन ए की दूसरी खुराक।
- 5 से 6 वर्ष पर: डीपीटी बूस्टर-2।
- 10 और 16 वर्ष की आयु में: टीडी (Td) का टीका।

यह सभी टीके सरकारी प्राथमिक स्वास्थ्य केंद्र (PHC), आंगनवाड़ी और उपकेंद्रों पर निःशुल्क उपलब्ध हैं।
"""
    },
    {
        "doc_id": "SRC-03-OR",
        "title": "ଜାତୀୟ ଟୀକାକରଣ କାର୍ଯ୍ୟସୂଚୀ (ଭାରତ ସରକାର)",
        "language": "or",
        "topic": "Child immunization schedule",
        "url": "http://www.nrhmorissa.gov.in/immunization-schedule",
        "section": "ଶିଶୁ ଟୀକାକରଣ ତାଲିକା",
        "text": """
ସାର୍ବଜନୀନ ଟୀକାକରଣ କାର୍ଯ୍ୟକ୍ରମ ଅଧୀନରେ ଶିଶୁମାନଙ୍କୁ ବିଭିନ୍ନ ମାରାତ୍ମକ ରୋଗରୁ ରକ୍ଷା କରିବା ପାଇଁ ମାଗଣାରେ ଟିକା ଦିଆଯାଏ।

ଟୀକାକରଣ ସମୟସୂଚୀ:
- ଜନ୍ମ ସମୟରେ: ବିସିଜି (BCG - ଯକ୍ଷ୍ମା ପାଇଁ), ପୋଲିଓ ଜିରୋ ଡୋଜ୍ (OPV-0), ଏବଂ ହେପାଟାଇଟିସ୍-ବି ଜନ୍ମ ଡୋଜ୍ (୨୪ ଘଣ୍ଟା ମଧ୍ୟରେ)।
- ୬ ସପ୍ତାହରେ: ପେଣ୍ଟାଭାଲେଣ୍ଟ-୧, ପୋଲିଓ-୧, ରୋଟାଭାଇରସ୍-୧, fIPV-୧, ଏବଂ ପିସିଭି-୧ (ନିମୋନିଆ ପାଇଁ)।
- ୧୦ ସପ୍ତାହରେ: ପେଣ୍ଟାଭାଲେଣ୍ଟ-୨, ପୋଲିଓ-୨, ରୋଟାଭାଇରସ୍-୨।
- ୧୪ ସପ୍ତାହରେ: ପେଣ୍ଟାଭାଲେଣ୍ଟ-୩, ପୋଲିଓ-୩, ରୋଟାଭାଇରସ୍-୩, fIPV-୨, ଏବଂ ପିସିଭି-୨।
- ୯ ରୁ ୧୨ ମାସରେ: ମିଜିଲ୍ସ-ରୁବେଲା (MR-1), ପିସିଭି ବୁଷ୍ଟର ଏବଂ ଭିଟାମିନ୍-ଏ ପ୍ରଥମ ମାତ୍ରା।
- ୧୬ ରୁ ୨୪ ମାସରେ: ଏମଆର-୨, ଡିପିଟି ବୁଷ୍ଟର-୧, ଏବଂ ପୋଲିଓ ବୁଷ୍ଟର।
- ୫ ରୁ ୬ ବର୍ଷରେ: ଡିପିଟି ବୁଷ୍ଟର-୨।

ନିକଟସ୍ଥ ଅଙ୍ଗନବାଡ଼ି କେନ୍ଦ୍ର କିମ୍ବା ପ୍ରାଥମିକ ସ୍ୱାସ୍ଥ୍ୟ କେନ୍ଦ୍ର (PHC) ରେ ଏହି ସମସ୍ତ ଟିକା ମାଗଣାରେ ମିଳିଥାଏ।
"""
    },

    # 5. Maternal health and pregnancy care basics
    {
        "doc_id": "SRC-06",
        "title": "Maternal and Antenatal Care (PMSMA Guidelines)",
        "language": "en",
        "topic": "Maternal health and pregnancy care basics",
        "url": "https://pmsma.nhp.gov.in/guidelines",
        "section": "Antenatal Checkups and Danger Signs",
        "text": """
Safe motherhood requires quality antenatal care (ANC) throughout pregnancy to ensure healthy outcomes for both mother and baby.

Key Components of Antenatal Care:
1. Minimum of 4 Antenatal Checkups: 1st visit within the first trimester (up to 12 weeks), 2nd visit between 14-26 weeks, 3rd visit at 28-34 weeks, and 4th visit between 36 weeks and term. Under the Pradhan Mantri Surakshit Matritva Abhiyan (PMSMA), comprehensive checkups by doctors are provided on the 9th of every month.
2. Tetanus and adult Diphtheria (Td) immunization: 2 doses given 4 weeks apart during early pregnancy, or a single booster if vaccinated in the last 3 years.
3. Micronutrient Supplementation: Daily Iron and Folic Acid (IFA) tablets (100 mg elemental iron and 500 mcg folic acid) for at least 180 days starting from the second trimester (after 14 weeks), alongside calcium supplementation (500 mg twice daily, taken separately from iron).
4. Danger Signs in Pregnancy: Vaginal bleeding, severe headache with blurred vision, convulsions/fits, severe swelling of face and hands, persistent abdominal pain, high fever, or reduced fetal movement. Any danger sign requires emergency hospital visit immediately.
"""
    },
    {
        "doc_id": "SRC-06-HI",
        "title": "मातृ स्वास्थ्य एवं गर्भावस्था की देखभाल (PMSMA)",
        "language": "hi",
        "topic": "Maternal health and pregnancy care basics",
        "url": "https://pmsma.nhp.gov.in/hi/guidelines",
        "section": "प्रसवपूर्व जांच एवं खतरे के लक्षण",
        "text": """
स्वस्थ प्रसव और सुरक्षित मातृत्व के लिए गर्भावस्था के दौरान नियमित प्रसवपूर्व जांच (ANC) अत्यंत आवश्यक है।

गर्भावस्था में देखभाल के मुख्य नियम:
1. कम से कम 4 प्रसवपूर्व जांचें: पहली जांच पहले 3 महीनों में, दूसरी 14 से 26 सप्ताह में, तीसरी 28 से 34 सप्ताह में और चौथी 36 सप्ताह के बाद। प्रधानमंत्री सुरक्षित मातृत्व अभियान के तहत हर महीने की 9 तारीख को सरकारी अस्पतालों में विशेषज्ञ डॉक्टरों द्वारा निःशुल्क जांच होती है।
2. टीडी (Td) का टीका: गर्भावस्था में टिटनेस और डिप्थीरिया से बचाव के लिए 4 सप्ताह के अंतर पर टीडी के 2 टीके लगवाएं।
3. आयरन और फोलिक एसिड (IFA) गोलियां: गर्भावस्था के चौथे महीने से प्रतिदिन 1 लाल गोली (IFA) कम से कम 180 दिनों तक लें, और कैल्शियम की गोली भी लें (आयरन और कैल्शियम की गोली एक साथ न खाएं)।
4. खतरे के लक्षण: योनि से रक्तस्राव, तेज सिरदर्द और धुंधला दिखना, हाथ-चेहरे पर अत्यधिक सूजन, तेज बुखार, पेट में असहनीय दर्द या गर्भस्थ शिशु की हलचल कम होना। ऐसा होने पर तुरंत अस्पताल पहुंचे।
"""
    },
    {
        "doc_id": "SRC-06-OR",
        "title": "ମାତୃ ସ୍ୱାସ୍ଥ୍ୟ ଏବଂ ଗର୍ଭାବସ୍ଥା ଯତ୍ନ ପରାମର୍ଶ",
        "language": "or",
        "topic": "Maternal health and pregnancy care basics",
        "url": "http://www.nrhmorissa.gov.in/maternal-health",
        "section": "ଗର୍ଭକାଳୀନ ଯାଞ୍ଚ ଓ ସତର୍କତା",
        "text": """
ନିରାପଦ ମାତୃତ୍ୱ ଏବଂ ନବଜାତ ଶିଶୁର ସୁରକ୍ଷା ପାଇଁ ଗର୍ଭାବସ୍ଥାରେ ନିୟମିତ ଗର୍ଭକାଳୀନ ପରୀକ୍ଷା (ANC) ନିହାତି ଜରୁରୀ।

ମୁଖ୍ୟ ପରାମର୍ଶ:
୧. ଅତି କମରେ ୪ ଥର ଗର୍ଭକାଳୀନ ଯାଞ୍ଚ କରାନ୍ତୁ। ପ୍ରଥମ ୩ ମାସ ଭିତରେ ନାମ ପଞ୍ଜୀକରଣ କରି ପ୍ରଥମ ଯାଞ୍ଚ କରନ୍ତୁ। ପ୍ରତି ମାସ ୯ ତାରିଖରେ ପ୍ରଧାନମନ୍ତ୍ରୀ ସୁରକ୍ଷିତ ମାତୃତ୍ୱ ଅଭିଯାନରେ ମାଗଣା ଡାକ୍ତରୀ ପରୀକ୍ଷା କରାଯାଏ।
୨. ଟିଡି (Td) ଟିକା: ଗର୍ଭାବସ୍ଥାରେ ୪ ସପ୍ତାହ ବ୍ୟବଧାନରେ ୨ଟି ଟିଡି ଟିକା ନିଶ୍ଚୟ ନିଅନ୍ତୁ।
୩. ଆଇରନ୍ ଓ ଫୋଲିକ୍ ଏସିଡ୍ (IFA) ବଟିକା: ଗର୍ଭାବସ୍ଥାର ଚତୁର୍ଥ ମାସରୁ ଦୈନିକ ଗୋଟିଏ ଲେଖାଏଁ ଆଇରନ୍ ବଟିକା ଅତି କମରେ ୧୮୦ ଦିନ ପର୍ଯ୍ୟନ୍ତ ଖାଆନ୍ତୁ। କ୍ୟାଲସିୟମ୍ ବଟିକା ମଧ୍ୟ ନିୟମିତ ସେବନ କରନ୍ତୁ।
୪. ବିପଦପୂର୍ଣ୍ଣ ଲକ୍ଷଣ: ଯୋନୀରୁ ରକ୍ତସ୍ରାବ, ପ୍ରବଳ ମୁଣ୍ଡବିନ୍ଧା ଓ ଆଖିକୁ ଝାପ୍ସା ଦେଖାଯିବା, ମୁହଁ ଓ ହାତ ଗୋଡ଼ ଫୁଲିଯିବା, ଗର୍ଭସ୍ଥ ଶିଶୁର ଚଳପ୍ରଚଳ କମିଯିବା। ଏଭଳି ଲକ୍ଷଣ ଦେଖାଦେଲେ ବିଳମ୍ବ ନକରି ଡାକ୍ତରଖାନାକୁ ଯାଆନ୍ତୁ।
"""
    },

    # 6. Nutrition and anemia
    {
        "doc_id": "SRC-07",
        "title": "Dietary Guidelines for Indians and Anemia Prevention",
        "language": "en",
        "topic": "Nutrition and anemia",
        "url": "https://www.nin.res.in/dietaryguidelines",
        "section": "Iron Deficiency Anemia and Balanced Nutrition",
        "text": """
Anemia is characterized by a reduced level of hemoglobin in the blood, impairing the oxygen-carrying capacity of red blood cells. In India, iron deficiency is the leading cause of anemia, affecting adolescent girls, pregnant women, and young children.

Common symptoms of anemia include chronic fatigue, pale skin and conjunctiva, weakness, shortness of breath on exertion, dizziness, cold hands and feet, brittle nails, and difficulty concentrating.

Dietary recommendations for combating anemia:
1. Increase intake of iron-rich foods: Green leafy vegetables (spinach, fenugreek, drumstick leaves), pulses, lentils, jaggery (gur), sesame seeds, and animal sources (eggs, poultry, lean meat where culturally accepted).
2. Enhance iron absorption: Consume Vitamin C-rich foods (amla, lemon, guava, oranges, tomatoes) alongside meals. Vitamin C dramatically improves non-heme iron absorption from plant foods.
3. Inhibit absorption factors: Avoid drinking tea or coffee immediately before, during, or after meals, as tannins and polyphenols bind iron and hinder absorption.
4. Deworming: Periodic deworming with Albendazole (every 6 months) under the Anemia Mukt Bharat program to prevent intestinal parasite-induced blood loss.
"""
    },
    {
        "doc_id": "SRC-07-HI",
        "title": "पोषण और एनीमिया (खून की कमी) की रोकथाम",
        "language": "hi",
        "topic": "Nutrition and anemia",
        "url": "https://anemiamuktbharat.info/guidelines",
        "section": "आयरन युक्त आहार और बचाव",
        "text": """
एनीमिया यानी शरीर में खून (हीमोग्लोबिन) की कमी होना। भारत में एनीमिया का मुख्य कारण आहार में आयरन और आवश्यक पोषक तत्वों की कमी है, जो विशेष रूप से बच्चों, किशोरियों और गर्भवती महिलाओं में पाया जाता है।

एनीमिया के लक्षण: लगातार थकान और कमजोरी महसूस होना, चेहरा व आंखें पीली दिखना, सांस फूलना, चक्कर आना, नाखूनों का सफेद व कमजोर होना और काम में मन न लगना।

बचाव एवं आहार संबंधी उपाय:
1. आयरन युक्त खाद्य पदार्थ खाएं: हरी पत्तेदार सब्जियां (पालक, मेथी, सहजन/मुनगा के पत्ते), चना, सोयाबीन, गुड़, काले तिल और अंकुरित अनाज।
2. विटामिन सी का उपयोग करें: भोजन के साथ आंवला, नींबू, अमरूद, संतरा जैसे खट्टे फल खाएं, जिससे भोजन का आयरन शरीर में आसानी से अवशोषित हो सके।
3. चाय और कॉफी से परहेज: खाना खाने के तुरंत पहले या बाद में चाय-कॉफी न पिएं, क्योंकि यह आयरन को सोखने से रोकती हैं।
4. कृमि मुक्ति (पेट के कीड़े मारने की दवा): साल में दो बार एल्बेंडाजोल (Albendazole) की गोली लें ताकि आंतों के कीड़ों से होने वाला खून का रिसाव रुक सके।
"""
    },
    {
        "doc_id": "SRC-07-OR",
        "title": "ପୁଷ୍ଟିକର ଖାଦ୍ୟ ଏବଂ ରକ୍ତହୀନତା (ଆନେମିଆ) ନିରାକରଣ",
        "language": "or",
        "topic": "Nutrition and anemia",
        "url": "http://www.nrhmorissa.gov.in/anemia-mukt-odisha",
        "section": "ଲୌହସାର ଯୁକ୍ତ ଖାଦ୍ୟ ଓ ସତର୍କତା",
        "text": """
ରକ୍ତରେ ହିମୋଗ୍ଲୋବିନର ମାତ୍ରା କମିଗଲେ ରକ୍ତହୀନତା ବା ଆନେମିଆ ହୁଏ। ଆମ ରାଜ୍ୟରେ ମହିଳା ଓ ଶିଶୁମାନଙ୍କ ମଧ୍ୟରେ ଲୌହସାର (ଆଇରନ୍) ର ଅଭାବ ଏହାର ପ୍ରଧାନ କାରଣ।

ରକ୍ତହୀନତାର ଲକ୍ଷଣ: ଶୀଘ୍ର ଥକିଯିବା, ଦୁର୍ବଳ ଲାଗିବା, ଚେହେରା ଓ ଆଖି ଧଳା ପଡ଼ିଯିବା, ସାମାନ୍ୟ ପରିଶ୍ରମରେ ନିଶ୍ୱାସ ଫୁଲିବା, ମୁଣ୍ଡ ବୁଲାଇବା ଏବଂ ନଖ ଭାଙ୍ଗିଯିବା।

ପ୍ରତିକାର ଓ ଉପଯୁକ୍ତ ଆହାର:
୧. ଲୌହସାର ଯୁକ୍ତ ଖାଦ୍ୟ ଖାଆନ୍ତୁ: ସବୁଜ ଶାଗ (ସଜନା ଶାଗ, ପାଳଙ୍ଗ ଶାଗ), ଡାଲି, କୋଳଥ, ଗୁଡ଼, କଳା ରାଶି ଏବଂ ଗଜା ମୁଗ।
୨. ଭିଟାମିନ୍-ସି ଯୁକ୍ତ ଖାଦ୍ୟ: ଖାଇବା ସହିତ ଅଁଳା, ଲେମ୍ବୁ, ପିଜୁଳି ଖାଆନ୍ତୁ, ଏହା ଶରୀରରେ ଆଇରନ୍ ଶୋଷଣ କରିବାରେ ସାହାଯ୍ୟ କରେ।
୩. ଖାଇବା ପରେ ପରେ ଚାହା କିମ୍ବା କଫି ପିଅନ୍ତୁ ନାହିଁ।
୪. ବର୍ଷକୁ ଦୁଇଥର କୃମି ନାଶକ ବଟିକା (ଆଲବେଣ୍ଡାଜୋଲ୍) ଖାଇ ପେଟ କୃମି ମୁକ୍ତ ରଖନ୍ତୁ।
"""
    },

    # 7. Hygiene, water safety, diarrhea and ORS
    {
        "doc_id": "SRC-08",
        "title": "Diarrhea Management, Dehydration, and ORS Preparation",
        "language": "en",
        "topic": "Hygiene, water safety, diarrhea and ORS",
        "url": "https://www.who.int/news-room/fact-sheets/detail/diarrhoeal-disease",
        "section": "ORS Preparation and Zinc Therapy",
        "text": """
Diarrhea is defined as the passage of three or more loose or liquid stools per day. It is a leading cause of malnutrition and death in young children, primarily driven by waterborne pathogens and poor sanitation. The greatest threat posed by diarrhea is dehydration (loss of water and essential electrolytes).

Standard Oral Rehydration Salts (ORS) Preparation:
1. Wash hands thoroughly with soap and running water before preparation.
2. Dissolve the entire content of one standard WHO-formula ORS packet into exactly 1 liter (1000 mL) of clean, boiled and cooled drinking water.
3. Stir well until the powder is fully dissolved.
4. Do not boil the prepared solution and do not mix with milk, juice, or soup.
5. The prepared solution must be covered and used within 24 hours. Discard any remaining solution after 24 hours and prepare fresh.

Zinc Supplementation: Children suffering from acute diarrhea should receive 20 mg of elemental zinc daily (10 mg for infants under 6 months) for 14 continuous days. Zinc reduces the duration and severity of the episode and prevents recurrence for months.

Danger Signs of Severe Dehydration: Extreme thirst, sunken eyes, skin that returns very slowly after pinching, lethargy or loss of consciousness, and inability to drink. Immediate emergency intravenous fluids are needed at a hospital.
"""
    },
    {
        "doc_id": "SRC-08-HI",
        "title": "दस्त रोग, निर्जलीकरण और ओआरएस (ORS) बनाने की विधि",
        "language": "hi",
        "topic": "Hygiene, water safety, diarrhea and ORS",
        "url": "https://nhm.gov.in/diarrhea-control-guidelines",
        "section": "ओआरएस घोल और जिंक की गोली",
        "text": """
दिन में तीन या अधिक बार पतला पानी जैसा शौच आना दस्त (डायरिया) कहलाता है। दस्त का सबसे बड़ा खतरा शरीर में पानी और लवणों की कमी (निर्जलीकरण/डिहाइड्रेशन) होना है।

ओआरएस (ORS) घोल बनाने की सही विधि:
1. घोल बनाने से पहले अपने हाथों को साबुन और साफ पानी से धोएं।
2. एक साफ बर्तन में पूरा 1 लीटर (1000 मिली) पीने का उबला और ठंडा किया हुआ पानी लें।
3. ओआरएस का पूरा पैकेट 1 लीटर पानी में डालकर अच्छी तरह घोलें।
4. इस घोल को दूध, सूप या दाल में न मिलाएं।
5. बना हुआ ओआरएस घोल केवल 24 घंटे तक ही प्रयोग करें। 24 घंटे के बाद बचा हुआ घोल फेंक दें और नया घोल बनाएं।

जिंक का सेवन: 2 महीने से बड़े बच्चों को दस्त शुरू होते ही 14 दिनों तक लगातार जिंक की एक गोली पानी या मां के दूध में घोलकर अवश्य दें। यह दस्त को जल्दी रोकता है।

गंभीर खतरे के लक्षण: अत्यधिक प्यास लगना, आंखें अंदर धंस जाना, त्वचा चुटकी काटने पर धीरे-धीरे लौटना, बच्चा सुस्त या बेहोश होना, कुछ भी न पी पाना। ऐसे में तुरंत अस्पताल जाएं।
"""
    },
    {
        "doc_id": "SRC-08-OR",
        "title": "ତରଳ ଝାଡ଼ା, ଜଳକ୍ଷୟ ଏବଂ ଓଆରଏସ୍ (ORS) ପ୍ରସ୍ତୁତି ପ୍ରଣାଳୀ",
        "language": "or",
        "topic": "Hygiene, water safety, diarrhea and ORS",
        "url": "http://www.nrhmorissa.gov.in/ors-zinc-guidelines",
        "section": "ଓଆରଏସ୍ ଦ୍ରବଣ ଏବଂ ଜିଙ୍କ୍ ଉପଚାର",
        "text": """
ଦିନରେ ୩ ଥର କିମ୍ବା ତା’ଠାରୁ ଅଧିକ ପାଣି ଭଳି ପତଳା ଝାଡ଼ା ହେଲେ ତାହାକୁ ତରଳ ଝାଡ଼ା କୁହାଯାଏ। ଏହାର ସବୁଠାରୁ ବଡ଼ ବିପଦ ହେଉଛି ଶରୀରରୁ ପାଣି ଓ ଲବଣ କମିଯିବା (ଜଳକ୍ଷୟ/ଡିହାଇଡ୍ରେସନ୍)।

ଓଆରଏସ୍ (ORS) ପ୍ରସ୍ତୁତି ନିୟମ:
୧. ପ୍ରସ୍ତୁତ କରିବା ପୂର୍ବରୁ ସାବୁନରେ ହାତ ଭଲଭାବେ ଧୁଅନ୍ତୁ।
୨. ଏକ ପରିଷ୍କାର ପାତ୍ରରେ ଠିକ୍ ୧ ଲିଟର ଫୁଟା ଥଣ୍ଡା ପିଇବା ପାଣି ନିଅନ୍ତୁ।
୩. ଓଆରଏସ୍ ପ୍ୟାକେଟ୍‌ର ସମସ୍ତ ଗୁଣ୍ଡ ସେହି ୧ ଲିଟର ପାଣିରେ ଢାଳି ଭଲଭାବେ ଗୋଳାନ୍ତୁ।
୪. ଏହି ଦ୍ରବଣକୁ ଗରମ କରନ୍ତୁ ନାହିଁ କିମ୍ବା କ୍ଷୀର/ଜୁସ୍ ସହିତ ମିଶାନ୍ତୁ ନାହିଁ।
୫. ପ୍ରସ୍ତୁତ ଓଆରଏସ୍ ପାଣିକୁ ଘୋଡ଼ାଇ ରଖନ୍ତୁ ଏବଂ ୨୪ ଘଣ୍ଟା ମଧ୍ୟରେ ବ୍ୟବହାର କରନ୍ତୁ। ୨୪ ଘଣ୍ଟା ପରେ ବଳକା ପାଣି ଫିଙ୍ଗି ନୂଆ ତିଆରି କରନ୍ତୁ।

ଜିଙ୍କ୍ ବଟିକା: ଝାଡ଼ା ହେଲେ ପିଲାଙ୍କୁ ଲଗାତାର ୧୪ ଦିନ ପର୍ଯ୍ୟନ୍ତ ଜିଙ୍କ୍ ବଟିକା ଦେବା ଜରୁରୀ।

ଗୁରୁତର ବିପଦ ଲକ୍ଷଣ: ଆଖି ଗାତରେ ପଶିଯିବା, ପ୍ରବଳ ଶୋଷ ହେବା, ପିଲା ଅଚେତ ବା ନିସ୍ତେଜ ହୋଇଯିବା। ଏଭଳି ହେଲେ ତୁରନ୍ତ ଡାକ୍ତରଖାନାରେ ଭର୍ତ୍ତି କରନ୍ତୁ।
"""
    },

    # 8. Seasonal illnesses (flu, fever when to seek care)
    {
        "doc_id": "SRC-09",
        "title": "Seasonal Influenza and Viral Fever Guidelines",
        "language": "en",
        "topic": "Seasonal illnesses (flu, fever when to seek care)",
        "url": "https://idsp.mohfw.gov.in/seasonal-influenza-advisory",
        "section": "Home Care and Red Flag Symptoms",
        "text": """
Seasonal influenza (flu) is an acute respiratory infection caused by influenza viruses circulating worldwide. Symptoms include abrupt onset of fever, cough (usually dry), headache, muscle and joint pain, severe malaise, sore throat, and runny nose. Most people recover within a week without requiring medical treatment.

General Home Management:
1. Adequate rest and plenty of fluids (water, soups, oral hydration) to prevent dehydration.
2. Maintain respiratory etiquette: cover mouth and nose with a handkerchief or elbow when coughing or sneezing, and wash hands frequently.
3. Avoid self-medicating with antibiotics; antibiotics are ineffective against viral infections like influenza.
4. Isolate at home to prevent spreading infection to high-risk individuals (the elderly, pregnant women, and people with chronic health conditions).

Red Flag Symptoms Requiring Immediate Medical Attention:
- Difficulty breathing or severe shortness of breath.
- Persistent pain or pressure in the chest or abdomen.
- Sudden dizziness, confusion, or inability to wake up.
- High fever that does not decrease after 3 days or fever that improves but returns with worsening cough.
- Bluish lips or face (indicating low oxygen).
"""
    },
    {
        "doc_id": "SRC-09-HI",
        "title": "मौसमी फ्लू एवं मौसमी बुखार: देखभाल और खतरे के संकेत",
        "language": "hi",
        "topic": "Seasonal illnesses (flu, fever when to seek care)",
        "url": "https://idsp.mohfw.gov.in/hi/influenza-advisory",
        "section": "घरेलू देखभाल और गंभीर लक्षण",
        "text": """
मौसमी फ्लू एक संक्रामक श्वसन संक्रमण है जो वायरस के कारण फैलता है। इसके मुख्य लक्षण हैं: अचानक तेज बुखार, सूखी खांसी, सिरदर्द, गले में खराश, बदन दर्द, नाक बहना और अत्यधिक कमजोरी। अधिकांश लोग पर्याप्त आराम और तरल पदार्थों के सेवन से 1 सप्ताह में ठीक हो जाते हैं।

घरेलू देखभाल के उपाय:
1. पर्याप्त आराम करें और खूब पानी, सूप, दाल का पानी या गुनगुना तरल पदार्थ पिएं।
2. खांसते या छींकते समय मुंह और नाक को रुमाल या कोहनी से ढकें।
3. बिना डॉक्टर की सलाह के एंटीबायोटिक दवाएं कभी न लें, क्योंकि फ्लू वायरस से होता है जिस पर एंटीबायोटिक काम नहीं करती।
4. परिवार के बुजुर्गों और बच्चों से दूरी बनाकर रखें ताकि संक्रमण न फैले।

खतरे के संकेत (तुरंत डॉक्टर को दिखाएं):
- सांस लेने में कठिनाई या छाती में तेज दर्द।
- लगातार 3 दिन से अधिक तेज बुखार रहना।
- अत्यधिक चक्कर आना, भ्रम या बेहोशी की स्थिति।
- होंठ या चेहरे का नीला पड़ना (ऑक्सीजन की कमी)।
"""
    },
    {
        "doc_id": "SRC-09-OR",
        "title": "ଋତୁକାଳୀନ ଫ୍ଲୁ ଏବଂ ଜ୍ୱର: ପ୍ରାଥମିକ ଯତ୍ନ ଓ ବିପଦ ସଙ୍କେତ",
        "language": "or",
        "topic": "Seasonal illnesses (flu, fever when to seek care)",
        "url": "http://www.nrhmorissa.gov.in/seasonal-flu-advisory",
        "section": "ଘରୋଇ ଯତ୍ନ ଏବଂ ଡାକ୍ତରୀ ପରାମର୍ଶ",
        "text": """
ଋତୁ ପରିବର୍ତ୍ତନ ସମୟରେ ଭୂତାଣୁ (ଭାଇରସ୍) ଜନିତ ଫ୍ଲୁ ଓ ଜ୍ୱର ସାଧାରଣତଃ ଦେଖାଦିଏ। ଏହାର ଲକ୍ଷଣ: ହଠାତ୍ ଜ୍ୱର, ଶୁଖିଲା କାଶ, ଗଳା ଦରଜ, ମୁଣ୍ଡବିନ୍ଧା, ଶରୀର ଯନ୍ତ୍ରଣା ଏବଂ ନାକରୁ ପାଣି ବୋହିବା। ପ୍ରାୟତଃ ଏକ ସପ୍ତାହ ମଧ୍ୟରେ ଏହା ଭଲ ହୋଇଯାଏ।

ଘରୋଇ ଯତ୍ନ:
୧. ସମ୍ପୂର୍ଣ୍ଣ ବିଶ୍ରାମ ନିଅନ୍ତୁ ଏବଂ ପ୍ରଚୁର ପରିମାଣରେ ଉଷୁମ ପାଣି, ସୁପ୍ ବା ତରଳ ପାନୀୟ ପିଅନ୍ତୁ।
୨. କାଶିବା ବା ଛିଙ୍କିବା ସମୟରେ ରୁମାଲ୍ ବ୍ୟବହାର କରନ୍ତୁ ଏବଂ ନିୟମିତ ହାତ ଧୁଅନ୍ତୁ।
୩. ଡାକ୍ତରଙ୍କ ବିନା ପରାମର୍ଶରେ ଆଣ୍ଟିବାୟୋଟିକ୍ ଖାଆନ୍ତୁ ନାହିଁ, କାରଣ ଏହା ଭୂତାଣୁ ଉପରେ କାମ କରେ ନାହିଁ।

ତୁରନ୍ତ ଡାକ୍ତରଖାନା ଯିବାର ବିପଦ ସଙ୍କେତ:
- ନିଶ୍ୱାସ ନେବାରେ କଷ୍ଟ କିମ୍ବା ଛାତିରେ ଅତ୍ୟଧିକ ଚାପ।
- ୩ ଦିନରୁ ଅଧିକ ସମୟ ଧରି ପ୍ରବଳ ଜ୍ୱର ରହିବା।
- ଅତ୍ୟଧିକ ଦୁର୍ବଳତା, ଅଚେତ ହୋଇଯିବା।
- ଓଠ କିମ୍ବା ମୁହଁ ନୀଳ ପଡ଼ିଯିବା।
"""
    }
]

# Onboarded Languages: Bengali (bn), Telugu (te), Tamil (ta)
try:
    from .sources_expansion import EXPANDED_HEALTH_DOCUMENTS
    OFFICIAL_HEALTH_DOCUMENTS.extend(EXPANDED_HEALTH_DOCUMENTS)
except ImportError:
    pass

