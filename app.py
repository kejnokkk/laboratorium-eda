import streamlit as st
import pandas as pd
from analiza import (
    wczytaj_dane,
    wyczysc_dane,
    podsumowanie,
    sprzedaz_wg_kanalu
)

# Konfiguracja strony Streamlit
st.set_page_config(
    page_title="Analiza sprzedazy",
    layout="wide"
)

st.title("Analiza danych sprzedazowych")

# Wczytanie i oczyszczenie danych za pomocą modułu analiza.py
df = wczytaj_dane("data/sprzedaz.csv")
df = wyczysc_dane(df)

# Panel boczny z filtrami
st.sidebar.header("Filtry")
kanaly = sorted(df["kanal"].dropna().unique())

wybrane = st.sidebar.multiselect(
    "Kanal sprzedazy",
    kanaly,
    default=kanaly
)

# Filtrowanie danych na podstawie wyboru użytkownika
df_filtr = df[df["kanal"].isin(wybrane)]

# Obliczenie statystyk dla przefiltrowanych danych
wyniki = podsumowanie(df_filtr)

# Wyświetlenie głównych wskaźników (Metryk)
c1, c2, c3 = st.columns(3)
c1.metric(
    "Liczba zamowien",
    wyniki["liczba"]
)
c2.metric(
    "Suma sprzedazy",
    f"{wyniki['suma']:.2f} zl"
)
c3.metric(
    "Srednia wartosc",
    f"{wyniki['srednia']:.2f} zl"
)

# Sekcja wykresu i podsumowania tabelarycznego
st.subheader("Sprzedaz wedlug kanalu")
tabela = sprzedaz_wg_kanalu(df_filtr)
st.dataframe(tabela)

# Generowanie wykresu, jeśli dane nie są puste
if not tabela.empty:
    st.bar_chart(
        tabela.set_index("kanal")["suma_sprzedazy"]
    )

# Wyświetlenie pełnej tabeli źródłowej po filtrowaniu
st.subheader("Dane po filtrowaniu")
st.dataframe(df_filtr)

# Przygotowanie i wyświetlenie przycisku pobierania plików CSV
csv = df_filtr.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Pobierz CSV",
    data=csv,
    file_name="wyniki.csv",
    mime="text/csv"
)
