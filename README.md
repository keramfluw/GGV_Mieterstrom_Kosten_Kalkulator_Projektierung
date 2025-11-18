
# Mieterstrom / GGV BW – Zähler- und Messkonzept-App (v2)

Diese Streamlit-App bildet typische Szenarien für Mieterstrom- und GGV-Modelle
in Mehrfamilienhäusern in Baden-Württemberg ab (10 / 20 / 40 / 80 WE) und liefert:

- Empfehlung für Messkonzept
- Anzahl der relevanten Zähler (Wohnungen, Allgemeinstrom, PV, Summenzähler)
- Grobe Empfehlung für den Zählerschrank-Typ
- **Differenzierte Kostenschätzung** für die Zähleranlage:
  - Material
  - Montage / Elektro
  - Planung / Engineering
  - NB Netzdienstleistungen (Netzauskunft, Schalt-/Inbetriebnahmetermine etc.)
  - MSB (Zählersetzung, iMSys-Einrichtung)
  - Backend / IT (insb. GGV)
  - Sonstige Projektkosten

Die Kostenwerte sind **Richtwerte** und müssen für reale Projekte anhand von Angeboten,
TAB des Netzbetreibers und Messkonzept-Vorgaben überprüft und angepasst werden.

## Installation

```bash
pip install -r requirements.txt
```

## Start der App

```bash
streamlit run app.py
```

Die App läuft dann im Browser unter der von Streamlit ausgegebenen URL (i.d.R. http://localhost:8501).
