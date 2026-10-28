# Cum se ruleaza proiectul (gateway + senzori)?

1. Instaleaza mosquitto: https://mosquitto.org/download/
    - La instalare bifeaza optiunea "Service" pentru a rula brokerul in fundal
2. Intra in C:\Program Files\mosquitto si deschide fisierul *mosquitto.conf*
3. Completeaza/editeaza fisierul cu urmatoarele:
    ```
    listener 1883
    allow_anonymous true

    ```

4. Deschide CMD sau Powershell ca admin si ruleaza urmatoarele comenzi:
    ```
    cd "C:\Program Files\mosquitto"
    mosquitto.exe -v -c mosquitto.conf

    ```

5. In proiect ruleaza serverul gateway folosind comanda:
    ```
    pyton gateway.py
    ```

6. Deschide un nou terminal si ruleaza scriptul pentru senzor si pune-i un id de la 0 la 4 pentru a trimite valori diferite. De exemplu:
    ```
    python senzor_umiditate.py 1
    ```

