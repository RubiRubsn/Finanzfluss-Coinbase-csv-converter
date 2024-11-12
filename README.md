# Finanzfluss Copilot - Coinbase CSV Import Converter

Dieses kleine Skript bereitet eine Coinbase-CSV-Datei so auf, dass sie in den Finanzfluss Copilot importiert werden kann. Dieses Projekt steht in keinerlei Verbindung zur Finflow GmbH oder Coinbase Germany GmbH. Ich übernehme keine Haftung für die Sicherheit oder Genauigkeit der Daten. Die Nutzung dieses Skripts erfolgt auf eigene Verantwortung.

# Bekannte Fehler

- Die umgerechneten Beträge können leichte Abweichungen im Cent- oder niedrigen Euro-Bereich aufweisen, da bei der Umwandlung Rundungen auftreten.

# Anleitung

## 1. Coinbase-Daten exportieren

### Schritt 1:
Oben rechts auf das Account-Symbol klicken.

![Schritt 1](/img/1.png)

### Schritt 2:
Auf den Namen klicken.

![Schritt 2](/img/2.png)

### Schritt 3:
Auf “Abrechnungen” klicken.

![Schritt 3](/img/3.png)

### Schritt 4:
Bei “Datum” den Punkt “Bisheriger Jahresverlauf” auswählen und dann auf “Benutzerdefiniert” klicken.

![Schritt 4](/img/4.png)

### Schritt 5:
Zeitraum auswählen. Für einen Erstimport sollte der Zeitraum ab Kontoerstellung gewählt werden. Bei einer Aktualisierung kann ein kürzerer Zeitraum genügen. Wichtig: CSV als Format auswählen und dann auf “Erzeugen” klicken.

![Schritt 5](/img/5.png)

## Skripte ausführen

### Schritt 6:
Auf dieser Seite (github) main.py anklicken.

![Schritt 6](/img/6.png)

### Schritt 7:

Auf “Copy raw” klicken.

![Schritt 7](/img/7.png)

### Schritt 8:
Einen Online-Python-Compiler öffnen, z. B. [dieser](https://www.onlinegdb.com/online_python_compiler#), und ein neues Dokument anlegen.

![Schritt 8](/img/8.png)

### Schritt 9:
Das neue Dokument output.csv benennen.

![Schritt 9](/img/9.png)

### Schritt 10:
Den in GitHub kopierten Code in die main.py einfügen.

![Schritt 10](/img/10.png)

### Schritt 11:
Auf “Upload file” klicken und die Coinbase-CSV-Datei hochladen.

![Schritt 11](/img/11.png)

### Schritt 12:
Im Kontextmenü “Rename” auswählen.

![Schritt 12](/img/12.png)

### Schritt 13:
Die Datei in input.csv umbenennen.

![Schritt 13](/img/13.png)

### Schritt 14:
main.py auswählen und auf “Run” klicken.

![Schritt 14](/img/14.png)

### Schritt 15:
Die Datei output.csv auswählen und auf “Download Current File” klicken.

![Schritt 15](/img/15.png)

## 3. CSV in Finanzfluss Copilot importieren

Die heruntergeladene CSV-Datei kann jetzt in Finanzfluss Copilot importiert werden.

Viel Spaß!