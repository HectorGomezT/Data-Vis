"""Normaliza los nombres de país de Lahman y de la MLB Stats API a ISO3 + nombre en español."""
import pandas as pd

# iso3 -> (nombre en español, continente, región)
COUNTRIES = {
    "USA": ("Estados Unidos", "América", "Norteamérica"),
    "CAN": ("Canadá", "América", "Norteamérica"),
    "MEX": ("México", "América", "Norteamérica"),
    "DOM": ("República Dominicana", "América", "Caribe"),
    "PRI": ("Puerto Rico", "América", "Caribe"),
    "CUB": ("Cuba", "América", "Caribe"),
    "CUW": ("Curaçao", "América", "Caribe"),
    "ABW": ("Aruba", "América", "Caribe"),
    "BHS": ("Bahamas", "América", "Caribe"),
    "JAM": ("Jamaica", "América", "Caribe"),
    "VIR": ("Islas Vírgenes (EE.UU.)", "América", "Caribe"),
    "PAN": ("Panamá", "América", "Centroamérica"),
    "NIC": ("Nicaragua", "América", "Centroamérica"),
    "HND": ("Honduras", "América", "Centroamérica"),
    "BLZ": ("Belice", "América", "Centroamérica"),
    "VEN": ("Venezuela", "América", "Sudamérica"),
    "COL": ("Colombia", "América", "Sudamérica"),
    "PER": ("Perú", "América", "Sudamérica"),
    "BRA": ("Brasil", "América", "Sudamérica"),
    "JPN": ("Japón", "Asia", "Asia Oriental"),
    "KOR": ("Corea del Sur", "Asia", "Asia Oriental"),
    "TWN": ("Taiwán", "Asia", "Asia Oriental"),
    "CHN": ("China", "Asia", "Asia Oriental"),
    "PHL": ("Filipinas", "Asia", "Sudeste Asiático"),
    "IDN": ("Indonesia", "Asia", "Sudeste Asiático"),
    "SGP": ("Singapur", "Asia", "Sudeste Asiático"),
    "VNM": ("Vietnam", "Asia", "Sudeste Asiático"),
    "SAU": ("Arabia Saudita", "Asia", "Medio Oriente"),
    "AFG": ("Afganistán", "Asia", "Medio Oriente"),
    "AUS": ("Australia", "Oceanía", "Oceanía"),
    "ASM": ("Samoa Americana", "Oceanía", "Oceanía"),
    "GUM": ("Guam", "Oceanía", "Oceanía"),
    "ZAF": ("Sudáfrica", "África", "África"),
    "GBR": ("Reino Unido", "Europa", "Europa"),
    "IRL": ("Irlanda", "Europa", "Europa"),
    "DEU": ("Alemania", "Europa", "Europa"),
    "NLD": ("Países Bajos", "Europa", "Europa"),
    "ITA": ("Italia", "Europa", "Europa"),
    "ESP": ("España", "Europa", "Europa"),
    "FRA": ("Francia", "Europa", "Europa"),
    "PRT": ("Portugal", "Europa", "Europa"),
    "AUT": ("Austria", "Europa", "Europa"),
    "BEL": ("Bélgica", "Europa", "Europa"),
    "CZE": ("Chequia", "Europa", "Europa"),
    "SVK": ("Eslovaquia", "Europa", "Europa"),
    "DNK": ("Dinamarca", "Europa", "Europa"),
    "FIN": ("Finlandia", "Europa", "Europa"),
    "GRC": ("Grecia", "Europa", "Europa"),
    "LVA": ("Letonia", "Europa", "Europa"),
    "LTU": ("Lituania", "Europa", "Europa"),
    "NOR": ("Noruega", "Europa", "Europa"),
    "POL": ("Polonia", "Europa", "Europa"),
    "RUS": ("Rusia", "Europa", "Europa"),
    "SWE": ("Suecia", "Europa", "Europa"),
    "CHE": ("Suiza", "Europa", "Europa"),
}

# Nombre crudo (Lahman / Stats API / CSV curados en inglés) -> iso3.
# Los países históricos se asignan a su sucesor actual.
ALIASES = {
    "USA": "USA", "United States": "USA",
    "CAN": "CAN", "Canada": "CAN",
    "México": "MEX", "Mexico": "MEX",
    "D.R.": "DOM", "Dominican Republic": "DOM",
    "P.R.": "PRI", "Puerto Rico": "PRI",
    "Cuba": "CUB",
    "Curaçao": "CUW", "Curacao": "CUW",
    "Aruba": "ABW", "Bahamas": "BHS", "Jamaica": "JAM",
    "U.S. Virgin Islands": "VIR",
    "Panama": "PAN", "Nicaragua": "NIC", "Honduras": "HND", "British Honduras": "BLZ",
    "Venezuela": "VEN", "VEN": "VEN", "Colombia": "COL", "Peru": "PER", "Brazil": "BRA",
    "Japan": "JPN", "South Korea": "KOR", "Republic of Korea": "KOR", "Korea": "KOR",
    "Taiwan": "TWN", "Chinese Taipei": "TWN", "China": "CHN",
    "Philippines": "PHL", "Indonesia": "IDN", "Singapore": "SGP", "South Vietnam": "VNM",
    "Saudi Arabia": "SAU", "Afghanistan": "AFG",
    "Australia": "AUS", "American Samoa": "ASM", "Guam": "GUM",
    "South Africa": "ZAF",
    "England": "GBR", "Scotland": "GBR", "Wales": "GBR", "Northern Ireland": "GBR",
    "United Kingdom": "GBR", "Great Britain": "GBR",
    "Ireland": "IRL",
    "Germany": "DEU", "West Germany": "DEU", "Prussia": "DEU",
    "Netherlands": "NLD", "Kingdom of the Netherlands": "NLD",
    "Italy": "ITA", "Spain": "ESP", "France": "FRA", "Portugal": "PRT",
    "Austria": "AUT", "Austria-Hungary": "AUT", "Belgium": "BEL",
    "Czechoslovakia": "CZE", "Bohemia": "CZE", "Czech Republic": "CZE", "Czechia": "CZE",
    "Slovakia": "SVK", "Denmark": "DNK", "Finland": "FIN", "Greece": "GRC",
    "Latvia": "LVA", "Lithuania": "LTU", "Norway": "NOR", "Poland": "POL",
    "Russia": "RUS", "Soviet Union": "RUS", "Sweden": "SWE", "Switzerland": "CHE",
}


def to_iso3(names: pd.Series) -> pd.Series:
    """Devuelve el ISO3; los valores sin mapeo (p. ej. 'At Sea') quedan como NaN."""
    return names.map(ALIASES)


def table() -> pd.DataFrame:
    return pd.DataFrame(
        [(iso, *v) for iso, v in COUNTRIES.items()],
        columns=["iso3", "country", "continent", "region"],
    )
