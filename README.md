# Smart Irrigation Digital Twin: ROI-Driven Proactive Edge Optimization

## Team
- Libotean Cosmin
- Haidu Eduard


## IoT Scenario
**Sistemul fizic simulat:** O parcelă agricolă monitorizată de noduri IoT și coordonată de un Geamăn Digital (Digital Twin) avansat, găzduit pe un server Edge (Raspberry Pi 5)[cite: 1]. Proiectul se concentrează pe luarea deciziilor autonome, proaktive, bazate pe o funcție de optimizare a profitului net (ROI). Sistemul nu se limitează la reacții simple bazate pe praguri statice, ci rulează simulări predictive continue corelând datele de umiditate din sol, microclimatul aerului (BME280), prognoza meteo și costul dinamic al resurselor (apă/energie) cu valoarea estimată a recoltei la momentul recoltării.

**Senzori utilizați:**
*   **Fizici (Machetă hardware-in-the-loop pe ESP32):** Senzor capacitiv de umiditate a solului v1.2, senzor meteo BME280 (temperatură și umiditate aer) și un modul releu (3.3V) pentru acționarea fizică a pompei.
*   **Simulați (În Python):** Debitmetru de apă (pentru cuantificarea litrilor consumați și a costului operațional) și un flux de date Meteo & Piață (prognoza precipitațiilor pe 24h și prețul apei/recoltei).

**Anomalii și scenarii critice modelate:**
*   *Valul de caniculă extremă:* Creșterea rapidă a ratei de evapotranspirație care necesită ajustarea proactivă a dozajului de apă înainte ca planta să intre în stadiul de ofilire permanentă.
*   *Restricții și fluctuații economice:* Variații bruște ale costului resurselor de irigare corelate cu fluctuațiile de preț ale pieței agricole, testând robustețea deciziei autonome a Geamănului Digital.

## Architecture
`ESP32 Node (Senzor Sol + BME280)` + `Weather/Market Simulator` $\rightarrow$ `MQTT Broker` $\rightarrow$ `Raspberry Pi 5 (AI Digital Twin & ROI Engine)` $\rightarrow$ `InfluxDB / CSV` $\rightarrow$ `Streamlit Edge Dashboard`

## Research Question
**RQ:** În ce măsură un motor de decizie bazat pe un Digital Twin cu Machine Learning și optimizare ROI pe nodul Edge poate maximiza profitul net al unei culturi agricole în scenarii climatice și economice dinamice, comparativ cu automatizările tradiționale bazate pe reguli reactive?

## Hypothesis
**H1:** Un sistem autonom bazat pe un Geamăn Digital inteligent, care anticipează curba de umiditate a solului pe 24h prin modele de regresie ML și evaluează rentabilitatea economică înainte de fiecare acțiune, poate reduce consumul de resurse și crește marja de profit net a exploatației cu cel puțin $15\%$, adaptându-se fluid la șocurile de preț și la condițiile meteo neprevăzute.

## Baseline (Mențiune de referință)
*Notă metodologică:* Deși sistemul de bază tradițional folosește un control simplu de tip prag reactiv (`if-else`) strict pentru calibrarea inițială, accentul absolut al acestei cercetări cade pe **arhitectura inteligentă de optimizare proactivă** descrisă mai jos.

## Proposed Approach (Sistemul Inteligent de Optimizare - Digital Twin)
Abordarea propusă implementează un **Motor de Decizie Inteligent în 3 Pași** pe Raspberry Pi 5[cite: 1]:

1.  **Predicția Avansată a Evapotranspirației (Machine Learning):** Un model de regresie (ex. Random Forest / Linear Regression) antrenat pe fluxul de date de la senzorul BME280 și istoricul solului prezice cu precizie evoluția umidității pentru următoarele 24 de ore: $\hat{U}(t + 24\text{h})$.
2.  **Simulare „What-If” în Timp Real:** Geamănul Digital rulează simulări paralele pentru a evalua impactul biologic și financiar al amânării sau executării irigării, luând în calcul șansele de precipitații gratuite oferite de fluxul meteo extern.
3.  **Optimizarea Financiară Bazată pe ROI:** Comanda de pornire a pompei este emisă **doar după** validarea matematică a rentabilității economice:
    $$\text{ROI} = (\text{Biomasă}_{\text{salvată}} \times \text{Preț}_{\text{recoltă}}) - (\text{Litri}_{\text{apă}} \times \text{Cost}_{\text{litru}})$$
    Dacă $\text{ROI} \le 0$ sau condițiile meteo indică o ploaie iminentă, sistemul inteligent blochează sau ajustează autonom volumul pompat, protejând randamentul financiar al fermierului.

## Experimental Plan
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
    4.  **Latența de Decizie pe Edge ($ms$):** Timpul de răspuns al scriptului de pe Raspberry Pi 5[cite: 1].

## Technology Stack
*   **Sensor Simulation & Physical Node:** Python (generator date) + ESP32 fizic cu senzor sol capacitiv, BME280 și releu 3.3V.
*   **Edge Server:** Raspberry Pi 5 (8GB RAM)[cite: 1] + SSD NVMe Western Digital 256GB[cite: 2] în carcasă Argon NEO 5[cite: 1].
*   **Communication:** MQTT (Mosquitto Broker local).
*   **Database:** InfluxDB / CSV pentru stocarea metricilor inteligente.
*   **Frontend:** Streamlit (Python) – panou de control dedicat vizualizării stării Geamănului Digital și a simulărilor financiare.
*   **ML / AI:** Python (`scikit-learn`, `pandas`, `numpy`).

## How to Run
1.  Clonați proiectul pe Raspberry Pi 5[cite: 1] și instalați bibliotecile necesare: `pip install scikit-learn streamlit paho-mqtt pandas`.
2.  Inițializați modelul de Machine Learning pentru predicția pe Edge: `python3 train_ml_model.py`.
3.  Porniți interfața grafică a Geamănului Digital: `streamlit run digital_twin_app.py`.
4.  Rulați simularea inteligentă de 60 de zile și urmăriți evoluția deciziilor autonome bazate pe ROI.
5.  *(Demo Hardware)* Conectați nodul ESP32 pentru a testa bucla de acțiune în timp real declanșată de motorul inteligent de pe Edge.

## Results
*(Secțiune rezervată pentru reprezentări grafice și interpretări analitice)*
*   **Grafice (Plots):** Curbe de evoluție în timp real a umidității reale vs. umiditatea prezisă de AI, corelate cu momentele în care motorul de optimizare ROI a aprobat sau a respins acționarea sistemului de irigare.

## Limitations
*   **Acuratețea Prognozei Externe:** Performanța proactivă depinde de acuratețea datelor furnizate de API-ul meteo extern; deviațiile majore pot influența marja de profit estimată.
*   **Ipoteza de omogenitate:** Modelul presupune un comportament hidrologic uniform în zona senzorului fizic de referință.