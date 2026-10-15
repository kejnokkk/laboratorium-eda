import pandas as pd

def wczytaj_dane(sciezka):
    """Wczytuje dane z pliku CSV z separatorem ';'."""
    return pd.read_csv(sciezka, sep=";")

def wyczysc_dane(df):
    """Ujednolica kolumnę 'kanal': usuwa spacje i zamienia na małe litery."""
    wynik = df.copy()
    wynik["kanal"] = wynik["kanal"].str.strip().str.lower()
    return wynik

def podsumowanie(df):
    """
    Zwraca słownik zawierający ogólne statystyki dla całego zbioru:
    liczbę zamówień, sumę sprzedaży, średnią wartość i medianę.
    """
    statystyki = {
        "liczba": int(df.shape[0]),
        "suma": float(df["wartosc"].sum()),
        "srednia": float(df["wartosc"].mean()),
        "mediana": float(df["wartosc"].median())
    }
    return statystyki


def sprzedaz_wg_kanalu(df):
    """
    Zwraca DataFrame z sumą sprzedaży pogrupowaną według kanału.
    Zwracany obiekt ma kolumny: 'kanal' oraz 'suma_sprzedazy'.
    """
    # Grupowanie i sumowanie wartości
    wynik = df.groupby("kanal")["wartosc"].sum().reset_index()
    
    # Zmiana nazw kolumn na wymagane w specyfikacji zadania
    wynik.columns = ["kanal", "suma_sprzedazy"]
    return wynik

if __name__ == "__main__":
    # Testowe uruchomienie modułu w konsoli (pomaga sprawdzić działanie przed wdrożeniem)
    try:
        df_raw = wczytaj_dane("data/sprzedaz.csv")
        df_clean = wyczysc_dane(df_raw)
        
        print("--- TEST PODSUMOWANIA (SŁOWNIK) ---")
        print(podsumowanie(df_clean))
        
        print("\n--- TEST SPRZEDAŻY WG KANAŁU (DATAFRAME) ---")
        print(sprzedaz_wg_kanalu(df_clean))
    except FileNotFoundError:
        print("Nie znaleziono pliku data/sprzedaz.csv. Uruchom skrypt z głównego folderu projektu.")
