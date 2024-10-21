import pandas as pd
import csv
from datetime import datetime

# Eingabedatei und Ausgabedatei festlegen
input_file = "input3.csv"
output_file = "output.csv"

# CSV-Datei einlesen und überspringen der ersten beiden Zeilen
df = pd.read_csv(input_file, skiprows=3)
# Liste für das neue Datenformat
transformed_data = []


# Funktion zum Berechnen des Wechselkurses
def calculate_exchange_rate(amount1, amount2):
    try:
        return float(amount1) / float(amount2) if float(amount2) != 0 else 0
    except ValueError:
        return 0


# Funktion, um den Transaktionstyp zu mappen
def map_transaction_type(transaction_type):
    if transaction_type == "Buy":
        return "Kauf"
    elif transaction_type == "Sell":
        return "Verkauf"
    elif transaction_type == "Deposit":
        return "Einzahlung"
    elif transaction_type == "Withdraw":
        return "Auszahlung"
    elif transaction_type == "Staking Income":
        return "Dividende"
    elif transaction_type == "Learning Reward":
        return "Einbuchung"
    elif transaction_type == "Receive":
        return "Einbuchung"
    elif transaction_type == "Send":
        return "Ausbuchung"
    elif transaction_type == "Convert":
        return "Convert"
    else:
        return transaction_type  # Fallback auf den Originaltyp, wenn keiner passt


# Funktion zum Umwandeln des Dezimalpunkts in ein Komma
def convert_decimal(value):
    if isinstance(value, float):
        value = f"{value:.12f}".rstrip("0").rstrip(
            "."
        )  # Konvertiert Float in normale Dezimalzahl ohne wissenschaftliche Notation
    return str(value).replace(".", ",")


# Zeilen der ursprünglichen Daten durchlaufen und die Daten konvertieren
for index, row in df.iterrows():
    try:
        datum = datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S %Z").strftime(
            "%d.%m.%Y"
        )
    except ValueError:
        continue

    # Transaktionsart abbilden
    transaktions_typ = row["Transaction Type"]
    mapped_transaction = map_transaction_type(transaktions_typ)

    if transaktions_typ == "Convert":
        # Informationen aus der Notes-Spalte extrahieren
        convert_notes = row["Notes"]
        old_amount = float(row["Quantity Transacted"])
        new_amount = float(convert_notes.split(" to ")[-1].split()[0])
        new_asset = convert_notes.split(" to ")[-1].split()[1]
        original_asset = row["Asset"]

        # Verkauf der alten Währung
        verkauf_preis = float(
            row["Price at Transaction"].replace("€", "").replace(",", "")
        )
        subtotal = float(row["Subtotal"].replace("€", "").replace(",", ""))
        total_incl_fees = float(
            row["Total (inclusive of fees and/or spread)"]
            .replace("€", "")
            .replace(",", "")
        )
        fees = (
            float(row["Fees and/or Spread"].replace("€", "").replace(",", ""))
            if pd.notnull(row["Fees and/or Spread"])
            else 0.0
        )

        # Wechselkurs berechnen von alter Währung zu EUR
        wechselkurs_alt_eur = subtotal / old_amount

        # Verkaufseintrag für die alte Währung hinzufügen
        verkauf_row = [
            datum,  # Datum
            original_asset,  # ISIN (hier der Asset-Name)
            original_asset,  # Name
            "Fremdwährung",  # Typ
            "Verkauf",  # Transaktion
            convert_decimal(verkauf_preis),  # Preis mit Komma statt Punkt
            convert_decimal(old_amount),  # Anzahl mit Komma
            convert_decimal(fees),  # Gebühren mit Komma
            "0",  # Steuern (immer 0)
            "EUR",  # Währung
            "1",
            # convert_decimal(wechselkurs_alt_eur),  # Wechselkurs mit Komma
        ]
        transformed_data.append(verkauf_row)

        # Kauf der neuen Währung
        kauf_preis = subtotal  # Preis ohne Gebühren
        wechselkurs_eur_neu = calculate_exchange_rate(kauf_preis, new_amount)

        # Kauf der neuen Währung in EUR berechnen
        kauf_row = [
            datum,  # Datum
            new_asset,  # ISIN (hier der neue Asset-Name)
            new_asset,  # Name
            "Fremdwährung",  # Typ
            "Kauf",  # Transaktion
            convert_decimal(kauf_preis / new_amount),  # Preis mit Komma
            convert_decimal(new_amount),  # Anzahl mit Komma
            "0",  # Gebühren (bereits beim Verkauf berücksichtigt)
            "0",  # Steuern
            "EUR",  # Währung
            "1",
            # convert_decimal(wechselkurs_eur_neu),  # Wechselkurs mit Komma
        ]
        transformed_data.append(kauf_row)
    elif transaktions_typ == "Staking Income":
        asset_name = row["Asset"].replace("ETH2", "ETH")
        preis = float(row["Price at Transaction"].replace("€", "").replace(",", ""))
        menge = row["Quantity Transacted"]
        total_incl_fees = float(
            row["Total (inclusive of fees and/or spread)"]
            .replace("€", "")
            .replace(",", "")
        )
        gebühren = (
            float(row["Fees and/or Spread"].replace("€", "").replace(",", ""))
            if pd.notnull(row["Fees and/or Spread"])
            else 0.0
        )
        wechselkurs = 1.00  # Standardmäßig auf 1.00 setzen, wenn nicht anders angegeben
        transaktion = map_transaction_type(transaktions_typ)

        # Zu transformierende Daten
        transformed_row = [
            datum,  # Datum
            asset_name,  # ISIN / Währungsname (hier verwenden wir den Asset-Namen)
            asset_name,  # Name der Währung/Aktie
            (
                "Fremdwährung"
                # if asset_name in ["BTC", "ETH", "AKT", "ETH2"]
                # else "Aktie"
            ),  # Typ
            transaktion,  # Transaktion (gemappter Typ)
            convert_decimal(total_incl_fees),  # Preis mit Komma
            "1",  # Anzahl mit Komma
            "",  # Gebühren mit Komma
            "",  # Steuern
            "EUR",  # Währung (annehmen, dass es immer EUR ist)
            convert_decimal(wechselkurs),  # Wechselkurs mit Komma
        ]

        transformed_data.append(transformed_row)
        # Kauf der neuen Währung
        kauf_preis = total_incl_fees  # Preis ohne Gebühren

        # Kauf der neuen Währung in EUR berechnen
        kauf_row = [
            datum,  # Datum
            asset_name,  # ISIN (hier der neue Asset-Name)
            asset_name,  # Name
            "Fremdwährung",  # Typ
            "Kauf",  # Transaktion
            convert_decimal(preis),  # Preis mit Komma
            convert_decimal(menge),  # Anzahl mit Komma
            "0",  # Gebühren (bereits beim Verkauf berücksichtigt)
            "0",  # Steuern
            "EUR",  # Währung
            "1",
            # convert_decimal(wechselkurs_eur_neu),  # Wechselkurs mit Komma
        ]
        transformed_data.append(kauf_row)

    else:
        asset_name = row["Asset"].replace("ETH2", "ETH")
        preis = float(row["Price at Transaction"].replace("€", "").replace(",", ""))
        menge = row["Quantity Transacted"]
        gebühren = (
            float(row["Fees and/or Spread"].replace("€", "").replace(",", ""))
            if pd.notnull(row["Fees and/or Spread"])
            else 0.0
        )
        wechselkurs = 1.00  # Standardmäßig auf 1.00 setzen, wenn nicht anders angegeben
        transaktion = map_transaction_type(transaktions_typ)

        # Zu transformierende Daten
        transformed_row = [
            datum,  # Datum
            asset_name,  # ISIN / Währungsname (hier verwenden wir den Asset-Namen)
            asset_name,  # Name der Währung/Aktie
            (
                "Fremdwährung"
                # if asset_name in ["BTC", "ETH", "AKT", "ETH2"]
                # else "Aktie"
            ),  # Typ
            transaktion,  # Transaktion (gemappter Typ)
            convert_decimal(preis),  # Preis mit Komma
            convert_decimal(menge),  # Anzahl mit Komma
            convert_decimal(gebühren),  # Gebühren mit Komma
            "0",  # Steuern
            "EUR",  # Währung (annehmen, dass es immer EUR ist)
            convert_decimal(wechselkurs),  # Wechselkurs mit Komma
        ]

        transformed_data.append(transformed_row)

# In die neue CSV-Datei schreiben
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    # Header hinzufügen
    writer.writerow(
        [
            "Datum",
            "ISIN",
            "Name",
            "Typ",
            "Transaktion",
            "Preis",
            "Anzahl",
            "Gebühren",
            "Steuern",
            "Währung",
            "Wechselkurs",
        ]
    )
    # Zeilen schreiben
    writer.writerows(transformed_data)

print(
    "Die Umwandlung der CSV-Datei ist abgeschlossen. Die Ausgabe wurde in der Datei 'umgewandelte_datei.csv' gespeichert."
)
