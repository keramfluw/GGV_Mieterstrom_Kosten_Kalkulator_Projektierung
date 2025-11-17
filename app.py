
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mieterstrom & GGV – BW Zählerkonzept", layout="wide")

st.markdown(
    """
    <style>
    * { font-family: "Times New Roman", serif !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Mieterstrom / GGV – Zähler- und Messkonzept (Baden-Württemberg)")
st.write(
    "Dieses Tool liefert auf Basis vordefinierter Szenarien (10 / 20 / 40 / 80 WE) "
    "eine Empfehlung für Messkonzept, Zählerschrank-Auslegung und grobe Kostenschätzung "
    "für Objekte in Baden-Württemberg."
)

SCENARIOS = [
    {
        "we_bucket": 10,
        "modell": "klassischer Mieterstrom",
        "messkonzept": "Zwei-Sammelschienen (physischer Summenzähler)",
        "beschreibung": "Mieterstromteilnehmer und Nichtteilnehmer auf getrennten Sammelschienen, physischer Summenzähler zur bilanziellen Trennung.",
        "wohnungszaehler": 10,
        "allgemeinstrom": 1,
        "pv_zaehler": 1,
        "summenzaehler_physisch": 1,
        "summenzaehler_virtuell": False,
        "smart_meter_pflicht": "Empfohlen (mind. PV-Erzeugung + Summenzähler)",
        "zaehlerschrank_typ": "Standzählerschrank mit eHZ-Technik, 2-Sammelschienen, APZ, ca. 14 Direktmessplätze",
        "direkte_zaehlerplaetze": 12,
        "sonderfelder": "2 Sonderzählerfelder (PV+Summen)",
        "kosten_material": 3000,
        "kosten_montage": 7000,
        "kosten_planung": 3000,
        "kosten_nb_msb": 1500,
        "kosten_sonstige": 2500,
    },
    {
        "we_bucket": 10,
        "modell": "GGV",
        "messkonzept": "Summenzählermodell mit iMSys",
        "beschreibung": "Zentrale Erzeugungsmessung, alle Teilnehmer mit Smart Meter, Aufteilung der PV-Mengen über iMSys/Backend.",
        "wohnungszaehler": 10,
        "allgemeinstrom": 1,
        "pv_zaehler": 1,
        "summenzaehler_physisch": 0,
        "summenzaehler_virtuell": True,
        "smart_meter_pflicht": "Ja, für alle Teilnehmer und PV-Anlage",
        "zaehlerschrank_typ": "Standzählerschrank mit eHZ, APZ, vorbereitet für Smart-Meter-Gateways, ca. 12 Direktmessplätze",
        "direkte_zaehlerplaetze": 12,
        "sonderfelder": "1 Feld für Erzeugung, APZ erweitert",
        "kosten_material": 3500,
        "kosten_montage": 8000,
        "kosten_planung": 4000,
        "kosten_nb_msb": 2000,
        "kosten_sonstige": 4000,
    },
    {
        "we_bucket": 20,
        "modell": "klassischer Mieterstrom",
        "messkonzept": "Zwei-Sammelschienen (physischer Summenzähler)",
        "beschreibung": "Teilnehmer/Nichtteilnehmer je Sammelschiene, physischer Summenzähler, ggf. mehrere Allgemeinstromkreise.",
        "wohnungszaehler": 20,
        "allgemeinstrom": 1,
        "pv_zaehler": 1,
        "summenzaehler_physisch": 1,
        "summenzaehler_virtuell": False,
        "smart_meter_pflicht": "Empfohlen",
        "zaehlerschrank_typ": "Große Zähleranlage mit 2-Sammelschienen, eHZ, APZ, Reserve für spätere Zählpunkte",
        "direkte_zaehlerplaetze": 24,
        "sonderfelder": "2–3 Sonderzählerfelder",
        "kosten_material": 5000,
        "kosten_montage": 12000,
        "kosten_planung": 4000,
        "kosten_nb_msb": 2500,
        "kosten_sonstige": 5000,
    },
    {
        "we_bucket": 20,
        "modell": "GGV",
        "messkonzept": "Summenzählermodell mit iMSys",
        "beschreibung": "Summenzählerfunktion über Smart Meter und Backend, alle WE mit iMSys, PV-Erzeugung separat.",
        "wohnungszaehler": 20,
        "allgemeinstrom": 1,
        "pv_zaehler": 1,
        "summenzaehler_physisch": 0,
        "summenzaehler_virtuell": True,
        "smart_meter_pflicht": "Ja",
        "zaehlerschrank_typ": "Mehrfeld-Zähleranlage mit ausreichenden eHZ-Plätzen, APZ, Kommunikationsreserve",
        "direkte_zaehlerplaetze": 24,
        "sonderfelder": "Felder für PV, Gateway, Reserve",
        "kosten_material": 6000,
        "kosten_montage": 13000,
        "kosten_planung": 6000,
        "kosten_nb_msb": 3000,
        "kosten_sonstige": 7000,
    },
    {
        "we_bucket": 40,
        "modell": "klassischer Mieterstrom",
        "messkonzept": "Zwei-Sammelschienen + ggf. Unterverteilungen",
        "beschreibung": "Mehrere Sammelschienen/Unterverteilungen, physische Summenzähler pro Strang oder Gesamtanlage.",
        "wohnungszaehler": 40,
        "allgemeinstrom": 2,
        "pv_zaehler": 1,
        "summenzaehler_physisch": 1,
        "summenzaehler_virtuell": False,
        "smart_meter_pflicht": "Empfohlen",
        "zaehlerschrank_typ": "Modulare Zählerfeldanlage mit mehreren Standschränken, teils Wandlermessung",
        "direkte_zaehlerplaetze": 44,
        "sonderfelder": "3–4 Sonderzähler/Wandlerfelder",
        "kosten_material": 8000,
        "kosten_montage": 20000,
        "kosten_planung": 7000,
        "kosten_nb_msb": 4000,
        "kosten_sonstige": 8000,
    },
    {
        "we_bucket": 40,
        "modell": "GGV",
        "messkonzept": "Summenzählermodell mit iMSys/virtuellem Summenzähler",
        "beschreibung": "Virtuelle Summierung über Backend, alle WE mit iMSys, flexible Teilnehmerverwaltung.",
        "wohnungszaehler": 40,
        "allgemeinstrom": 2,
        "pv_zaehler": 1,
        "summenzaehler_physisch": 0,
        "summenzaehler_virtuell": True,
        "smart_meter_pflicht": "Ja",
        "zaehlerschrank_typ": "Mehrere Zählerschränke mit iMSys-Vorbereitung, zentrale Gateway- und IT-Infrastruktur",
        "direkte_zaehlerplaetze": 44,
        "sonderfelder": "Felder für mehrere Gateways und Kommunikation",
        "kosten_material": 9500,
        "kosten_montage": 22000,
        "kosten_planung": 9000,
        "kosten_nb_msb": 5000,
        "kosten_sonstige": 12000,
    },
    {
        "we_bucket": 80,
        "modell": "klassischer Mieterstrom",
        "messkonzept": "Individuelles Konzept (Mehrfach-Sammelschienen, Teilnetze)",
        "beschreibung": "Typisch mehrere Zähleranlagen/Stränge mit eigenen Summenzählern, teils Kombination mit BHKW/Speicher.",
        "wohnungszaehler": 80,
        "allgemeinstrom": 3,
        "pv_zaehler": 1,
        "summenzaehler_physisch": 1,
        "summenzaehler_virtuell": False,
        "smart_meter_pflicht": "Empfohlen",
        "zaehlerschrank_typ": "Projektierte Groß-Zähleranlage mit mehreren Schrankreihen, Wandlermessung, hoher Planungsaufwand",
        "direkte_zaehlerplaetze": 88,
        "sonderfelder": "Mehrere Sonderzähler/Wandlerfelder",
        "kosten_material": 14000,
        "kosten_montage": 35000,
        "kosten_planung": 12000,
        "kosten_nb_msb": 7000,
        "kosten_sonstige": 15000,
    },
    {
        "we_bucket": 80,
        "modell": "GGV",
        "messkonzept": "Summenzählermodell iMSys/virtuelle Zählschiene",
        "beschreibung": "Alle WE und PV mit iMSys, flexible Verteilung über 15-Minuten-Werte, mehrere Gateways/Backendsysteme.",
        "wohnungszaehler": 80,
        "allgemeinstrom": 3,
        "pv_zaehler": 1,
        "summenzaehler_physisch": 0,
        "summenzaehler_virtuell": True,
        "smart_meter_pflicht": "Ja, zwingend",
        "zaehlerschrank_typ": "Großanlage mit verteilten Zählerschränken, Gateways, IT-/Netzwerkinfrastruktur",
        "direkte_zaehlerplaetze": 88,
        "sonderfelder": "Zusätzliche Felder für Kommunikation/IT",
        "kosten_material": 16000,
        "kosten_montage": 38000,
        "kosten_planung": 15000,
        "kosten_nb_msb": 9000,
        "kosten_sonstige": 20000,
    },
]

def choose_bucket(we: int) -> int:
    if we <= 10:
        return 10
    elif we <= 20:
        return 20
    elif we <= 40:
        return 40
    else:
        return 80

def get_scenario(we: int, modell: str):
    bucket = choose_bucket(we)
    for s in SCENARIOS:
        if s["we_bucket"] == bucket and s["modell"] == modell:
            factor = max(1.0, we / bucket)
            s_scaled = s.copy()
            for k in ["kosten_material", "kosten_montage", "kosten_planung", "kosten_nb_msb", "kosten_sonstige"]:
                s_scaled[k] = round(s[k] * factor, 0)
            s_scaled["we_effektiv"] = we
            s_scaled["we_bucket"] = bucket
            return s_scaled
    return None

st.sidebar.header("Eingaben")

netzbetreiber = st.sidebar.selectbox(
    "Netzbetreiber (vereinfachte Auswahl)",
    ["Netze BW", "Stuttgart Netze", "Regionale Stadtwerke"],
)

we = st.sidebar.number_input("Anzahl Wohneinheiten (WE)", min_value=1, max_value=500, value=20, step=1)

modell = st.sidebar.selectbox(
    "Modell",
    ["klassischer Mieterstrom", "GGV"],
)

show_detailkosten = st.sidebar.checkbox("Detailkosten anzeigen", value=True)

scenario = get_scenario(we, modell)

if scenario is None:
    st.error("Für diese Kombination liegt kein Szenario vor.")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Mess- & Zählerkonzept")
        st.markdown(f"**Gebäudegröße (eingeben):** {scenario['we_effektiv']} WE (abgebildet auf Bucket {scenario['we_bucket']} WE)")
        st.markdown(f"**Modell:** {modell}")
        st.markdown(f"**Messkonzept:** {scenario['messkonzept']}")
        st.markdown(f"**Kurzbeschreibung:** {scenario['beschreibung']}")
        st.markdown(f"**Netzbetreiber (vereinfacht):** {netzbetreiber}")
        st.markdown(f"**Smart-Meter-Pflicht:** {scenario['smart_meter_pflicht']}")

        st.markdown("**Zähleranzahl (Richtwerte):**")
        st.write(f"- Wohnungszähler: {scenario['wohnungszaehler']}")
        st.write(f"- Allgemeinstrom-Zähler: {scenario['allgemeinstrom']}")
        st.write(f"- PV-Erzeugungszähler: {scenario['pv_zaehler']}")
        st.write(f"- Physischer Summenzähler: {scenario['summenzaehler_physisch']}")
        st.write(f"- Virtueller Summenzähler/Backend: {'Ja' if scenario['summenzaehler_virtuell'] else 'Nein'}")

    with col2:
        st.subheader("Zählerschrank & Kosten (Schätzung)")
        st.markdown(f"**Empfohlener Zählerschrank-Typ:** {scenario['zaehlerschrank_typ']}")
        st.markdown(f"**Direkte Zählerplätze (Richtwert):** {scenario['direkte_zaehlerplaetze']}")
        st.markdown(f"**Zusatzfelder/Sonderzähler:** {scenario['sonderfelder']}")

        gesamt = (
            scenario["kosten_material"]
            + scenario["kosten_montage"]
            + scenario["kosten_planung"]
            + scenario["kosten_nb_msb"]
            + scenario["kosten_sonstige"]
        )

        st.metric("Gesamtkosten Zähleranlage (geschätzt)", f"{gesamt:,.0f} €".replace(",", "."))

        if show_detailkosten:
            df_cost = pd.DataFrame(
                [
                    ["Material Zählerschrank", scenario["kosten_material"]],
                    ["Montage / Elektroarbeiten", scenario["kosten_montage"]],
                    ["Planung / Engineering", scenario["kosten_planung"]],
                    ["Netzbetreiber / MSB initial", scenario["kosten_nb_msb"]],
                    ["Sonstige Kosten (Bau/IT/Backend)", scenario["kosten_sonstige"]],
                ],
                columns=["Kostenart", "Betrag (€)"],
            )
            st.table(df_cost)

    st.subheader("Export")
    df_export = pd.DataFrame([scenario])
    csv = df_export.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Aktuelles Szenario als CSV herunterladen",
        data=csv,
        file_name="mieterstrom_ggv_bw_szenario.csv",
        mime="text/csv",
    )

    st.info(
        "Hinweis: Alle Werte sind Richtwerte auf Basis typischer Annahmen "
        "für Baden-Württemberg (Netze BW / Stuttgart / Stadtwerke). "
        "Für konkrete Projekte sind TAB, Messkonzept-Formblätter und Angebote verbindlich zu prüfen."
    )
