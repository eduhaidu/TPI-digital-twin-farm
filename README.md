# Smart Irrigation Digital Twin: ROI-Driven Proactive Edge Optimization

## Team
- Libotean Cosmin
- Haidu Eduard

--- 

## IoT Scenario
Proiectul propus simulează o parcelă agricolă monitorizată de noduri IoT și coordonată de un Geamăn Digital (Digital Twin) avansat, găzduit pe un server Edge (Raspberry Pi 5). Proiectul se concentrează pe luarea deciziilor autonome, proactive, bazate pe o funcție de optimizare a profitului net (ROI). Sistemul rulează simulări predictive continue corelând datele de umiditate din sol, microclimatul aerului (BME280), prognoza meteo și costul dinamic al resurselor (apă/energie) cu valoarea estimată a recoltei la momentul recoltării.

**Senzori utilizați:**
*   **Fizici (Machetă hardware-in-the-loop pe ESP32):** Senzor capacitiv de umiditate a solului v1.2, senzor meteo BME280 (temperatură și umiditate aer) și un modul releu (3.3V) pentru acționarea fizică a pompei.
*   **Simulați (În Python):** Debitmetru de apă (pentru cuantificarea litrilor consumați și a costului operațional) și un flux de date Meteo & Piață (prognoza precipitațiilor pe 24h și prețul apei/recoltei).

**Anomalii și scenarii critice modelate:**
*   *Valul de caniculă extremă:* Creșterea rapidă a ratei de evapotranspirație care necesită ajustarea proactivă a dozajului de apă înainte ca planta să intre în stadiul de ofilire permanentă.
*   *Restricții și fluctuații economice:* Variații bruște ale costului resurselor de irigare corelate cu fluctuațiile de preț ale pieței agricole, testând robustețea deciziei autonome a Geamănului Digital.

---

## Arhitectură
`ESP32 Node (Senzor Sol + BME280)` + `Weather/Market Simulator` $\rightarrow$ `MQTT Broker` $\rightarrow$ `Raspberry Pi 5 (AI Digital Twin & ROI Engine)` $\rightarrow$ `InfluxDB (Time-Series)` $\rightarrow$ `Streamlit Edge Dashboard`

---

## Întrebare de cercetare
În ce măsură un motor de decizie bazat pe un Digital Twin cu Machine Learning și optimizare ROI pe nodul Edge poate maximiza profitul net al unei culturi agricole în scenarii climatice și economice dinamice, comparativ cu automatizările tradiționale bazate pe reguli reactive?

---

## Ipoteză inițială
Un sistem autonom bazat pe un Geamăn Digital inteligent, care anticipează curba de umiditate a solului pe 24h prin modele de regresie ML și evaluează rentabilitatea economică înainte de fiecare acțiune, poate reduce consumul de resurse și crește marja de profit net a exploatației cu cel puțin $15\%$, adaptându-se fluid la șocurile de preț și la condițiile meteo neprevăzute.

---

## Baseline
Sistemul de bază tradițional folosește un control simplu de tip prag reactiv (`if-else`). Astfel, când sistemul detectează că pragul necesar de umiditate a fost atins sau depășit, sistemul trimite o comandă către releuri pentru a activa sau dezactiva sistemul de irigare.

---

## Abordarea propusă (Sistemul Inteligent de Optimizare - Digital Twin)
Abordarea propusă implementează un **Motor de Decizie Inteligent în 3 Pași** pe Raspberry Pi 5:

1.  **Predicția Avansată a Evapotranspirației (Machine Learning):** Un model de regresie (ex. Random Forest / Linear Regression) antrenat pe fluxul de date de la senzorul BME280 și istoricul solului prezice cu precizie evoluția umidității pentru următoarele 24 de ore:
2.  **Simulare „What-If” în Timp Real:** Geamănul Digital rulează simulări paralele pentru a evalua impactul biologic și financiar al amânării sau executării irigării, luând în calcul șansele de precipitații gratuite oferite de fluxul meteo extern.
3.  **Optimizarea Financiară Bazată pe ROI:** Comanda de pornire a pompei este emisă **doar după** validarea matematică a rentabilității economice:
   > **ROI** = (**Biomasă**<sub>salvată</sub> × **Preț**<sub>recoltă</sub>) − (**Litri**<sub>apă</sub> × **Cost**<sub>litru</sub>)
    Dacă $\text{ROI} \le 0$ sau condițiile meteo indică o ploaie iminentă, sistemul inteligent blochează sau ajustează autonom volumul pompat, protejând randamentul financiar al fermierului.

---

## Plan experimental
*   **Dataset / Date generate:** Simulator Python care generează serii de timp de înaltă fidelitate pentru 60 de zile de ciclu agricol (variabila meteo, dinamica umidității, costuri variabile), utilizate pentru antrenarea și testarea modelului inteligent.
*   **Scenariul de test (Experimente):**
    *   *Scenariul 1 (Adaptabilitate Climatică):* Comportamentul sistemului inteligent în fața fluctuațiilor bruște de temperatură și a episoadelor de secetă.
    *   *Scenariul 2 (Optimizare Economică):* Testarea răspunsului Geamănului Digital la creșteri abrupte ale costului apei sau scăderi ale prețului de piață al recoltei.
    *   *Scenariul 3 (Acuratețea Predicției ML):* Evaluarea erorilor de estimare a umidității solului de către modelele de pe Edge ($RMSE$, $MAE$).
*   **Variabile controlate:** Pragul de stres hidric al culturii, profilul termic zilnic, tarifele resurselor.
*   **Metrici de evaluare:**
    1.  **Eroarea de Predicție a Modelului ML ($RMSE$):** Cât de bine anticipează AI-ul dinamica solului.
    2.  **Eficiența Hidrică Globală ($L$):** Volumul total de apă administrat inteligent.
    3.  **Profitul Net Optimizat ($\text{RON}$):** Valoarea finală a recoltei minus costurile calculate de motorul ROI.
    4.  **Latența de Decizie pe Edge ($ms$):** Timpul de răspuns al scriptului de pe Raspberry Pi 5.
 
---

## Tehnologii propuse
*   **Sensor Simulation & Physical Node:** Python (generator date) + ESP32 fizic cu senzor sol capacitiv, BME280 și releu 3.3V.
*   **Edge Server:** Raspberry Pi 5 (8GB RAM) + SSD NVMe Western Digital 256GB.
*   **Communication:** MQTT (Mosquitto Broker local).
*   **Database:** InfluxDB / CSV pentru stocarea metricilor inteligente.
*   **Frontend:** Streamlit (Python) – panou de control dedicat vizualizării stării Geamănului Digital și a simulărilor financiare.
*   **ML / AI:** Python (`scikit-learn`, `pandas`, `numpy`).

---

## Cum se rulează proiectul
*(de completat după implementare)*

 ---
 
## Results
*(de completat după rularea simulărilor)*

---

## Limitări
*   **Acuratețea Prognozei Externe:** Performanța proactivă depinde de acuratețea datelor furnizate de API-ul meteo extern; deviațiile majore pot influența marja de profit estimată.
*   **Ipoteza de omogenitate:** Modelul presupune un comportament hidrologic uniform în zona senzorului fizic de referință.
