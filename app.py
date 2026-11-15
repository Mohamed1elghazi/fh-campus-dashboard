import streamlit as st
import requests
from datetime import datetime
from urllib.parse import quote

st.set_page_config(
    page_title="FH Campus Dashboard",
    page_icon="🎓",
    layout="wide"
)

MENSA = "https://mensa-st.bburke.de/"
EVENTS = "https://www.steinfurt.de/Veranstaltungen.htm"
TRANSPORT = "https://www.bus-und-bahn-im-muensterland.de/"
FH = "https://www.fh-muenster.de/"
MYFH = "https://myfh.fh-muenster.de/"

LAT = 52.15
LON = 7.33

st.markdown("""
<style>
.stApp {
    background: #F5F7FA;
    color: #18344D;
}
[data-testid="stSidebar"] {
    background: #FFFFFF;
}
h1,h2,h3 {
    color: #18344D;
}
[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #E5EBF0;
}
.stButton button {
    background: #167A70;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=1800)
def get_weather():
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": LAT,
                "longitude": LON,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "wind_speed_10m,"
                    "weather_code"
                ),
                "timezone": "Europe/Berlin"
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()["current"]
    except Exception:
        return None


def header(title, subtitle):
    st.title(title)
    st.caption(subtitle)


with st.sidebar:
    st.markdown("# 🎓 FH CAMPUS")
    st.caption("STEINFURT · MÜNSTER")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Mensa",
            "Zug & Bus",
            "Veranstaltungen",
            "Wetter",
            "FH Münster",
            "Über das Projekt"
        ]
    )

    st.divider()
    st.caption("Version 2.0")


if page == "Dashboard":

    header(
        "Guten Tag! 👋",
        "Dein digitaler Campus-Assistent."
    )

    st.caption(datetime.now().strftime("%d.%m.%Y %H:%M"))

    weather = get_weather()

    if weather:
        c1, c2, c3 = st.columns(3)
        c1.metric("🌡️ Temperatur", f'{weather["temperature_2m"]} °C')
        c2.metric("💧 Luftfeuchtigkeit", f'{weather["relative_humidity_2m"]}%')
        c3.metric("💨 Wind", f'{weather["wind_speed_10m"]} km/h')
    else:
        st.info("Wetterdaten aktuell nicht verfügbar.")

    st.divider()
    st.subheader("Dein Campus")

    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            st.subheader("🍽️ Mensa")
            st.write("Speiseplan Steinfurt")
            st.link_button("Öffnen", MENSA)

    with c2:
        with st.container(border=True):
            st.subheader("🚆 Mobilität")
            st.write("Verbindungen nach Münster")
            st.link_button("Fahrplan", TRANSPORT)

    with c3:
        with st.container(border=True):
            st.subheader("📅 Events")
            st.write("Veranstaltungen Steinfurt")
            st.link_button("Entdecken", EVENTS)

    st.divider()
    st.subheader("🍴 Mensa Steinfurt")

    st.link_button("Speiseplan öffnen", MENSA)

    st.components.v1.iframe(
        MENSA,
        height=500,
        scrolling=True
    )

    st.divider()
    st.subheader("🎓 Hochschulportale")

    a, b, c = st.columns(3)

    a.link_button("FH Münster", FH)
    b.link_button("myFH", MYFH)
    c.link_button(
        "Studierendenwerk",
        "https://www.stw-muenster.de/"
    )


elif page == "Mensa":

    header("🍽️ Mensa Steinfurt", "Aktueller Speiseplan.")

    st.link_button("Mensa öffnen", MENSA)

    st.components.v1.iframe(
        MENSA,
        height=750,
        scrolling=True
    )

    st.link_button(
        "Offizielle Informationen",
        "https://www.stw-muenster.de/"
    )


elif page == "Zug & Bus":

    header("🚆 Mobilität", "Steinfurt nach Münster")

    start = st.text_input(
        "Start",
        "Steinfurt-Burgsteinfurt"
    )

    destination = st.text_input(
        "Ziel",
        "Münster (Westf) Hbf"
    )

    if st.button("Verbindung suchen"):

        if start.strip() and destination.strip():

            url = (
                "https://www.google.com/maps/dir/?api=1"
                f"&origin={quote(start)}"
                f"&destination={quote(destination)}"
                "&travelmode=transit"
            )

            st.link_button("Fahrplan öffnen", url)

        else:
            st.warning("Bitte Start und Ziel eingeben.")

    st.divider()

    st.link_button("Bus und Bahn Münsterland", TRANSPORT)
    st.link_button("Deutsche Bahn", "https://www.bahn.de/")


elif page == "Veranstaltungen":

    header(
        "📅 Veranstaltungen",
        "Entdecke Steinfurt und Münster."
    )

    st.link_button(
        "Stadt Steinfurt",
        EVENTS
    )

    st.link_button(
        "FH Münster",
        FH
    )

    st.link_button(
        "Stadt Münster",
        "https://www.stadt-muenster.de/"
    )


elif page == "Wetter":

    header(
        "🌤️ Wetter Steinfurt",
        "Aktuelle Wetterinformationen."
    )

    weather = get_weather()

    if weather:
        st.metric(
            "Temperatur",
            f'{weather["temperature_2m"]} °C'
        )

        st.metric(
            "Luftfeuchtigkeit",
            f'{weather["relative_humidity_2m"]}%'
        )

        st.metric(
            "Wind",
            f'{weather["wind_speed_10m"]} km/h'
        )
    else:
        st.error("Wetterdaten nicht verfügbar.")

    st.link_button("Deutscher Wetterdienst", "https://www.dwd.de/")


elif page == "FH Münster":

    header(
        "🎓 FH Münster",
        "Deine Hochschulportale."
    )

    portals = [
        ("FH Münster", FH),
        ("myFH", MYFH),
        ("Bibliothek", "https://www.fh-muenster.de/bibliothek/"),
        ("Studierendenwerk", "https://www.stw-muenster.de/"),
        ("Hochschulsport", "https://www.uni-muenster.de/Hochschulsport/")
    ]

    for name, url in portals:
        with st.container(border=True):
            st.subheader(name)
            st.link_button("Öffnen", url)


elif page == "Über das Projekt":

    header(
        "Über das Projekt",
        "FH Campus Dashboard 2.0"
    )

    st.markdown("""
    ### Technologien
    - Python
    - Streamlit
    - Open-Meteo
    - Requests

    ### Datenschutz
    - Keine Speicherung von FH-Passwörtern.
    - Keine persönlichen Studentendaten.
    - Öffentliche Informationsquellen.

    ### Server
    Dein eigener Windows-11-PC.
    """)

    st.link_button(
        "Open-Meteo",
        "https://open-meteo.com/"
    )


st.divider()

st.caption(
    "FH CAMPUS DASHBOARD 2.0 | Python & Streamlit"
)
