# Sistem IoT de Irigare Inteligentă: Optimizarea Randamentului Recoltei și a Costului de Apă prin Machine Learning

## Membrii echipei
- Libotean Cosmin
- Haidu Eduard

--- 

## Scenariul IoT
Proiectul dezvoltă și simulează un sistem IoT de irigare inteligentă destinat unei culturi agricole, având ca scop optimizarea consumului de apă și maximizarea șanselor de a obține o recoltă bogată. Spre deosebire de sistemele clasice care udă solul mecanic la scăderea umidității sub un prag fix, acest sistem utilizează un model de Machine Learning pentru a lua decizii proactive pe baza evoluției solului și a prognozei meteo.

Sistemul este complet simulat software (fără componente fizice precum ESP32 sau relee de acționare a pompelor) și evaluează eficiența irigării prin două direcții: procentul de creștere a șanselor unei recolte mai bune (%) și costul total al apei consumate, calculat pe baza unui preț fix al apei stabilit la începutul simulării.

**Senzori utilizați:**
Nu se utilizează hardware fizic; toate nodurile senzoriale sunt simulate în Python, generând fluxuri de date în timp real pentru următoarele mărimi:

* *2 × Senzori capacitivi de umiditate a solului*: Măsoară umiditatea volumetrică a solului (%) în două puncte ale parcelei pentru a determina nivelul actual de hidratare a rădăcinilor (date extrase din Soil Moisture Dataset).

* *1 × Senzor meteo local (simulare BME280 + API Meteo)*: Măsoară temperatura aerului (°C), umiditatea relativă a aerului (%) și preia prognoza de precipitații (mm/h) pe următoarele 24 de ore prin intermediul OpenMeteo API.

* *1 × Debitmetru de apă virtual*: Cuantifică volumul de apă consumat (Litri) în timpul sesiunilor de irigare recomandate de sistem, valoare folosită direct pentru calculul costului pe baza tarifului fix.

**Date utilizate și Modelul de Machine Learning**
* *Date de intrare*: Istoricul umidității solului de la cei 2 senzori, temperatura aerului, umiditatea aerului și precipitațiile prognozate.

* *Parametru configurabil*: Prețul fix pe litru/metru cub de apă (setat la inițializarea sistemului).

* *Modelul ML (Random Forest Regressor)*: Antrenat pe datele senzorilor și istoricul climatic, modelul prezice evoluția umidității solului pe următoarele 24 de ore (rata de evapotranspirație) și estimează procentul de succes/sănătate a recoltei (%) în funcție de stresul hidric evitat.

**Anomalii și scenarii critice modelate:**
*   *Diferențe mari de temperatură în intervale scurte:* Variații bruște de temperatură de la o oră la alta pentru a testa capacitatea sistemului de a filtra erorile de citire față de valurile reale de căldură.
*   *Ploi iminente după scăderea umidității:* Situații în care solul este uscat, dar urmează să plouă în câteva ore sunt un scenariu cheie în care sistemul inteligent amână irigarea și economisește apă comparativ cu metoda clasică.

---

## Obiective
- [ ] Simularea celor 2 senzori de umiditate a solului (extragerea și transmiterea datelor din Soil Moisture Dataset).   
- [ ] Simularea senzorului meteo și a prognozei pe 24h (integrarea cu OpenMeteo API).   
- [ ] Implementarea fluxului de date prin MQTT către Backend și stocarea în baza de date Time-Series (InfluxDB).   
- [ ] Antrenarea modelului de Machine Learning pentru predicția umidității solului și estimarea procentului de îmbunătățire a recoltei.   
- [ ] Crearea unui Dashboard în Streamlit pentru compararea metodei propuse cu metoda clasică (cost apă vs. șanse de producție).   

## Arhitectură și fluxul de date
Fluxul de date urmează arhitectura standard IoT, structurată pe 5 niveluri:

`Senzori simulați`$\rightarrow$ `MQTT Broker` $\rightarrow$ `Backend (Python + ML Engine)` $\rightarrow$ `Bază de date Time-Series (InfluxDB)` $\rightarrow$ `Streamlit Dashboard`

1. *Senzori (Generator Python)*: Scripturile simulează cei 2 senzori de sol, senzorul meteo și debitmetrul, împachetând măsurătorile în mesaje JSON.   
2. *Gateway (Mosquitto MQTT Broker)*: Preia mesajele publicate de senzori pe topicuri dedicate (ex: iot/sol/umiditate, iot/meteo/stare) și le rutează asincron către backend.   

3. *Backend (Serviciu Python & ML Inference)*: Abonat la Gateway, acest modul validează datele, rulează modelul de Machine Learning pentru a prezice umiditatea și procentul de randament al recoltei, decide cantitatea optimă de apă necesară și calculează costul aferent (la preț fix).

4. *Bază de date Time-Series (InfluxDB)*: Stochează cu marcaj temporal (timestamp) toate valorile brute de la senzori, predicțiile ML, volumul de apă consumat și costurile cumulate, atât pentru metoda inteligentă, cât și pentru metoda clasică.   

5. *Dashboard (Streamlit)*: Interfață grafică conectată la InfluxDB care afișează în timp real graficele de umiditate, starea vremii, procentul estimat de succes al recoltei și economia financiară realizată din reducerea consumului de apă.   

---

## Întrebare de cercetare
În ce măsură poate un sistem IoT de irigare bazat pe predicții Machine Learning să reducă volumul și costul apei consumate (la tarif fix), menținând un procent de succes al recoltei cel puțin egal sau superior față de un sistem clasic bazat pe praguri fixe (if-else)?

---

## Ipoteză inițială
Utilizarea unui model de regresie Machine Learning care corelează umiditatea solului cu prognoza meteo pe 24h permite anticiparea precipitațiilor și evitarea udărilor inutile. Astfel:   
    1. În condiții de randament egal al recoltei (%) între metoda clasică și cea propusă, metoda noastră câștigă prin reducerea costului de irigare cu cel puțin 15–20%.
    2. Pentru același buget de apă consumat, metoda propusă crește procentul de șanse pentru o recoltă mai bună (%) prin evitarea perioadelor de stres hidric sever sau supra-udare.

---

## Baseline
Sistemul de referință folosește o logică reactivă simplă de tip prag (`if-else`). Când media celor 2 senzori de umiditate a solului scade sub un prag fix (ex: 30%), sistemul comandă administrarea unei cantități fixe de apă, indiferent dacă urmează să plouă în următoarele ore sau dacă temperatura exterioară este scăzută. Nu se iau în calcul prognoza meteo sau rata de evaporare.

---

## Abordarea propusă (Sistemul Inteligent de Irigare)
Abordarea propusă implementează un **Motor de Decizie Inteligent în 3 Pași**:

1.  **Predicția Umidității Solului (Machine Learning):** Modelul Random Forest Regressor analizează datele de la cei 2 senzori de sol și senzorul meteo pentru a prezice curba de umiditate pe următoarele 24 de ore.
2.  **Estimarea Șanselor de Producție (%):** Pe baza timpului petrecut de cultură în zona optimă de umiditate (fără stres hidric sau băltire), sistemul calculează procentul de potențial al recoltei (ex: menținerea umidității în intervalul optim 40%–60% asigură o creștere cu X% a șanselor unei recolte maxime față de expunerea la secetă).
3.  **Logica de Optimizare a Costului (La Preț Fix al Apei):** 
   > **Cost Irigare** = **Volum Apă** (Litri) × **Preț Fix**<sub>litru</sub>
    Dacă modelul ML prezice că o ploaie iminentă va readuce umiditatea în parametri optimi fără a afecta procentul de producție al recoltei, irigarea este anulată sau redusă. Regula de validare: Dacă Procent Producție ML >= Procent Producție clasic și Cost Irigare ML < Cost Irigare clasic, algoritmul inteligent este declarat superior

---

## Plan experimental
*   **Dataset / Date generate:** Simulator Python care rulează un ciclu agricol de 60 de zile, combinând datele din Soil Moisture Dataset cu istoricul meteo din OpenMeteo API.
*   **Scenariul de test (Experimente):**
    *   *Scenariul 1 (Ploaie după secetă):* Umiditatea scade sub pragul critic cu 3 ore înainte de o ploaie prognozată. Metoda clasică udă inutil; metoda ML așteaptă ploaia, obținând același procent de recoltă la un cost de apă mai mic.
    *   *Scenariul 2 (Caniculă și evapotranspirație accelerată):* Temperaturi ridicate și anomalii termice bruște. Evaluarea modului în care modelul ML dozează preventiv apa pentru a crește cu X% șansele unei recolte sănătoase.
    *   *Scenariul 3 (Acuratețea Predicției ML):* Evaluarea erorilor de estimare a umidității solului ($RMSE$, $MAE$).
*   **Variabile controlate:** Prețul fix al apei (RON/Litru), pragul de stres hidric al culturii (%), durata simulării.
*   **Metrici de evaluare:**
    1.  **Procentul estimat de succes al recoltei (%):** Calculat pe baza orelor de hidratare optimă a plantei (Metoda ML vs. Clasic).
    2.  **Volumul total de apă consumat ($L$) și Costul Total ($RON$):** Calculat direct din litrii administrați înmulțiți cu prețul fix stabilit.
    3.  **Eroarea de Predicție a Modelului ML (RMSE / MAE):** curatețea cu care modelul anticipează umiditatea solului.
 
---

## Tehnologii propuse
*   **Simulare senzori:** Python (requests, paho-mqtt, scripturi de citire și extragere a datelor din dataset)
*   **Gateway:** MQTT (Mosquitto Broker local).
*   **Backend & Machine Learning:** Python (scikit-learn, pandas, numpy).
*   **Bază de date Time-Series:** InfluxDB
*   **Frontend:** Streamlit (vizualizare metrici în timp real și grafice comparative)

---

## Cum se rulează proiectul
*(de completat după implementare)*

 ---
 
## Results
*(de completat după rularea simulărilor)*

---

## Limitări
*   **Acuratețea Prognozei Meteo:** Performanța proactivă depinde de acuratețea datelor furnizate de API-ul meteo extern.
*   **Simulare Software:** Neutilizând senzori fizici și supape reale, sistemul nu ia în calcul pierderile mecanice de pe conducte sau întârzierile de infiltrare a apei în straturile profunde ale solului.

---

## Resurse utilizate / referințe
* [OpenMeteo API](https://open-meteo.com/en/docs)
* [Soil Moisture Dataset](https://www.kaggle.com/datasets/amirmohammdjalili/soil-moisture-dataset)
* [Chinadrip](https://www.chinadrip.com/drip-irrigation_c2?gad_source=1&gad_campaignid=23120891475&gbraid=0AAAAADhI9utvrrOYY9eqNfQaf_bryS0IZ&gclid=Cj0KCQjw6ObWBhDDARIsAFdfcUhneYcWzLi8FbmZrNdmNHRnKJVMisevDfT2T5LrOsjwdQcSzaZG7gEaAhm2EALw_wcB)
* [Automating My Vegetable Garden Irrigation with Home Assistant - Rudy Mens](https://lazyadmin.nl/smart-home/home-assistant-garden-irrigation-automation/)


 
