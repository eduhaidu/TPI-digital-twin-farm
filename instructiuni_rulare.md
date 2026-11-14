# Rularea proiectului pe Windows

Comenzile sunt pentru CMD. Pastreaza deschise terminalele proceselor pornite.

## La fiecare pornire

### 1. Porneste InfluxDB 3

Porneste serverul folosind instalarea sau containerul configurat pe calculator.
Adresa serverului folosita de backend este `http://localhost:8181`.
Portul `8888` este pentru interfata InfluxDB Explorer, nu pentru conexiunea backendului.

### 2. Porneste Mosquitto

Daca serviciul Mosquitto ruleaza deja, nu mai porni o a doua instanta.
Altfel, intr-un terminal separat:

```bat
cd /d "C:\Program Files\mosquitto"
mosquitto.exe -v -c mosquitto.conf
```

### 3. Porneste backendul

Intr-un terminal nou:

```bat
cd /d "C:\Users\User\Desktop\Proiecte vs code\iot\TPI\TPI-digital-twin-farm"
.venv\Scripts\fastapi.exe dev app.py
```

Asteapta `Application startup complete`.

- Backend: http://127.0.0.1:8000
- Testare API: http://127.0.0.1:8000/docs

### 4. Porneste gatewayul

Intr-un terminal nou:

```bat
cd /d "C:\Users\User\Desktop\Proiecte vs code\iot\TPI\TPI-digital-twin-farm"
.venv\Scripts\python.exe gateway.py
```

Asteapta confirmarea conectarii la broker si abonarea la `senzor/umiditate`.

### 5. Porneste senzorul

Intr-un terminal nou, dupa pornirea gatewayului:

```bat
cd /d "C:\Users\User\Desktop\Proiecte vs code\iot\TPI\TPI-digital-twin-farm"
.venv\Scripts\python.exe senzor_umiditate.py 1
```

ID-ul poate fi intre `0` si `4`. Al doilea argument optional este intervalul dintre mesaje, in secunde:

```bat
.venv\Scripts\python.exe senzor_umiditate.py 1 5
```

Pentru mai multi senzori, deschide cate un terminal si schimba ID-ul.
Ruleaza din folderul proiectului, pentru ca senzorul sa gaseasca `datasets/plant_vase1.CSV`.

### Verificare si oprire

Gatewayul trebuie sa afiseze `Data sent to backend successfully`, iar backendul `POST /readings ... 200`.
Mesajele sunt salvate si in `date_umiditate.json`.
Backendul mapeaza `sensor_id` la coloana `id` si `moisture` la `humidity` in tabela `readings`.
Citirile cu acelasi senzor si timestamp sunt omise ca duplicate.

`GET /readings/{sensor_id}` cauta doar ultima ora: datele istorice din CSV pot fi salvate corect fara sa apara in acest rezultat.

Opreste cu `Ctrl+C` senzorii, apoi gatewayul si backendul.
Opreste Mosquitto doar daca l-ai pornit manual si nu mai ai nevoie de el.

## Configurare initiala (o singura data)

Ai nevoie de Python, Mosquitto si un server InfluxDB 3 configurat.

### Python si dependente

```bat
cd /d "C:\Users\User\Desktop\Proiecte vs code\iot\TPI\TPI-digital-twin-farm"
py -m venv .venv
.venv\Scripts\python.exe -m pip install "fastapi[standard]" influxdb3-python python-dotenv pandas numpy paho-mqtt requests
```

Daca mediul si dependentele exista deja, nu repeta instalarea.
Comenzile folosesc direct executabilele din `.venv`; nu trebuie sa activezi mediul.

### Fisierul .env

Daca nu exista `.env`, copiaza `.env.example` in `.env` si completeaza valorile reale:

```dotenv
INFLUXDB_HOST=http://localhost:8181
INFLUXDB_TOKEN=tokenul_tau
INFLUXDB_DATABASE=numele_bazei_tale
BACKEND_URL=http://localhost:8000
```

Nu suprascrie un `.env` deja configurat si nu publica tokenul.
Repornește backendul dupa schimbarea `.env`.
Gatewayul nu incarca `.env`; foloseste implicit `http://localhost:8000`.
Pentru alta adresa, seteaza variabila in terminalul gatewayului inainte de pornire:

```bat
set BACKEND_URL=http://localhost:8000
```

### Mosquitto

Instaleaza de la https://mosquitto.org/download/.
Poti selecta instalarea ca serviciu pentru rulare in fundal.
Pentru testare locala, configureaza in `C:\Program Files\mosquitto\mosquitto.conf`:

```conf
listener 1883 127.0.0.1
allow_anonymous true
```

Salvarea configuratiei sau pornirea serviciului poate necesita drepturi de administrator.

## Erori frecvente

- `fastapi is not recognized`: foloseste `.venv\Scripts\fastapi.exe dev app.py` din folderul proiectului.
- `ModuleNotFoundError`: instaleaza dependentele cu `.venv\Scripts\python.exe -m pip` folosind comanda de mai sus.
- Flight / gRPC cu HTTP 404: verifica `INFLUXDB_HOST`; serverul este pe `8181`, Explorer pe `8888`.
- `No field named sensor_id`: foloseste codul corectat pentru schema `id`, `humidity`, `time`.
- Conexiune MQTT refuzata: verifica daca Mosquitto ruleaza pe portul `1883`.
- Port ocupat: verifica terminalele sau serviciile existente inainte sa pornesti alta instanta.
- HTTP 500: citeste ultimele linii ale erorii din terminalul backendului; gatewayul arata doar rezultatul cererii HTTP.
