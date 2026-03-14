"""
European Countries Currency Comparison Module
Compares: USD → INR vs EuropeanCurrency → INR
Shows which currency is stronger relative to INR
"""

import requests
import json
from datetime import datetime

EUROPEAN_COUNTRIES = [
    {"country": "Germany", "currency": "Euro", "code": "EUR", "capital": "Berlin", "language": "German", "english_friendly": True},
    {"country": "France", "currency": "Euro", "code": "EUR", "capital": "Paris", "language": "French", "english_friendly": False},
    {"country": "Netherlands", "currency": "Euro", "code": "EUR", "capital": "Amsterdam", "language": "Dutch", "english_friendly": True},
    {"country": "Switzerland", "currency": "Swiss Franc", "code": "CHF", "capital": "Bern", "language": "German/French/Italian", "english_friendly": True},
    {"country": "United Kingdom", "currency": "British Pound", "code": "GBP", "capital": "London", "language": "English", "english_friendly": True},
    {"country": "Sweden", "currency": "Swedish Krona", "code": "SEK", "capital": "Stockholm", "language": "Swedish", "english_friendly": True},
    {"country": "Denmark", "currency": "Danish Krone", "code": "DKK", "capital": "Copenhagen", "language": "Danish", "english_friendly": True},
    {"country": "Norway", "currency": "Norwegian Krone", "code": "NOK", "capital": "Oslo", "language": "Norwegian", "english_friendly": True},
    {"country": "Finland", "currency": "Euro", "code": "EUR", "capital": "Helsinki", "language": "Finnish", "english_friendly": True},
    {"country": "Ireland", "currency": "Euro", "code": "EUR", "capital": "Dublin", "language": "English", "english_friendly": True},
    {"country": "Austria", "currency": "Euro", "code": "EUR", "capital": "Vienna", "language": "German", "english_friendly": True},
    {"country": "Belgium", "currency": "Euro", "code": "EUR", "capital": "Brussels", "language": "Dutch/French/German", "english_friendly": True},
    {"country": "Luxembourg", "currency": "Euro", "code": "EUR", "capital": "Luxembourg City", "language": "French/German/Luxembourgish", "english_friendly": True},
    {"country": "Spain", "currency": "Euro", "code": "EUR", "capital": "Madrid", "language": "Spanish", "english_friendly": False},
    {"country": "Portugal", "currency": "Euro", "code": "EUR", "capital": "Lisbon", "language": "Portuguese", "english_friendly": False},
    {"country": "Italy", "currency": "Euro", "code": "EUR", "capital": "Rome", "language": "Italian", "english_friendly": False},
    {"country": "Greece", "currency": "Euro", "code": "EUR", "capital": "Athens", "language": "Greek", "english_friendly": False},
    {"country": "Poland", "currency": "Polish Zloty", "code": "PLN", "capital": "Warsaw", "language": "Polish", "english_friendly": False},
    {"country": "Czech Republic", "currency": "Czech Koruna", "code": "CZK", "capital": "Prague", "language": "Czech", "english_friendly": False},
    {"country": "Hungary", "currency": "Hungarian Forint", "code": "HUF", "capital": "Budapest", "language": "Hungarian", "english_friendly": False},
    {"country": "Romania", "currency": "Romanian Leu", "code": "RON", "capital": "Bucharest", "language": "Romanian", "english_friendly": False},
    {"country": "Bulgaria", "currency": "Bulgarian Lev", "code": "BGN", "capital": "Sofia", "language": "Bulgarian", "english_friendly": False},
    {"country": "Croatia", "currency": "Euro", "code": "EUR", "capital": "Zagreb", "language": "Croatian", "english_friendly": False},
    {"country": "Slovakia", "currency": "Euro", "code": "EUR", "capital": "Bratislava", "language": "Slovak", "english_friendly": False},
    {"country": "Slovenia", "currency": "Euro", "code": "EUR", "capital": "Ljubljana", "language": "Slovenian", "english_friendly": False},
    {"country": "Estonia", "currency": "Euro", "code": "EUR", "capital": "Tallinn", "language": "Estonian", "english_friendly": True},
    {"country": "Latvia", "currency": "Euro", "code": "EUR", "capital": "Riga", "language": "Latvian", "english_friendly": False},
    {"country": "Lithuania", "currency": "Euro", "code": "EUR", "capital": "Vilnius", "language": "Lithuanian", "english_friendly": False},
    {"country": "Malta", "currency": "Euro", "code": "EUR", "capital": "Valletta", "language": "Maltese/English", "english_friendly": True},
    {"country": "Cyprus", "currency": "Euro", "code": "EUR", "capital": "Nicosia", "language": "Greek/Turkish", "english_friendly": True},
    {"country": "Iceland", "currency": "Icelandic Krona", "code": "ISK", "capital": "Reykjavik", "language": "Icelandic", "english_friendly": True},
    {"country": "Serbia", "currency": "Serbian Dinar", "code": "RSD", "capital": "Belgrade", "language": "Serbian", "english_friendly": False},
    {"country": "Albania", "currency": "Albanian Lek", "code": "ALL", "capital": "Tirana", "language": "Albanian", "english_friendly": False},
    {"country": "North Macedonia", "currency": "Macedonian Denar", "code": "MKD", "capital": "Skopje", "language": "Macedonian", "english_friendly": False},
    {"country": "Montenegro", "currency": "Euro", "code": "EUR", "capital": "Podgorica", "language": "Montenegrin", "english_friendly": False},
    {"country": "Bosnia and Herzegovina", "currency": "Convertible Mark", "code": "BAM", "capital": "Sarajevo", "language": "Bosnian/Croatian/Serbian", "english_friendly": False},
    {"country": "Moldova", "currency": "Moldovan Leu", "code": "MDL", "capital": "Chisinau", "language": "Romanian", "english_friendly": False},
    {"country": "Ukraine", "currency": "Ukrainian Hryvnia", "code": "UAH", "capital": "Kyiv", "language": "Ukrainian", "english_friendly": False},
    {"country": "Belarus", "currency": "Belarusian Ruble", "code": "BYN", "capital": "Minsk", "language": "Belarusian/Russian", "english_friendly": False},
]


def fetch_currency_rates():
    """Fetch live currency rates using free API (exchangerate-api.com)"""
    try:
        # Free tier - no API key needed for this endpoint
        response = requests.get(
            "https://open.er-api.com/v6/latest/USD",
            timeout=10
        )
        data = response.json()
        if data.get("result") == "success":
            return data["rates"]
    except Exception as e:
        print(f"Live API failed: {e}, using fallback rates")

    # Fallback rates (approximate as of early 2026)
    return {
        "INR": 83.5, "EUR": 0.92, "GBP": 0.79, "CHF": 0.88,
        "SEK": 10.5, "DKK": 6.87, "NOK": 10.7, "PLN": 4.05,
        "CZK": 23.2, "HUF": 365.0, "RON": 4.58, "BGN": 1.80,
        "ISK": 137.0, "RSD": 108.0, "ALL": 96.0, "MKD": 56.5,
        "BAM": 1.80, "MDL": 17.8, "UAH": 41.5, "BYN": 3.27,
        "USD": 1.0,
    }


def compare_currencies():
    """
    Compare USD→INR vs each European currency→INR
    Returns structured data for the frontend
    """
    rates = fetch_currency_rates()
    inr_per_usd = rates.get("INR", 83.5)

    results = []
    for country in EUROPEAN_COUNTRIES:
        code = country["code"]
        rate_to_usd = rates.get(code, None)

        if rate_to_usd is None:
            continue

        # How many INR does 1 unit of this currency buy?
        inr_per_unit = inr_per_usd / rate_to_usd

        # Compare: if inr_per_unit > inr_per_usd, that currency is stronger than USD
        # if inr_per_unit < inr_per_usd, USD is stronger
        if inr_per_unit > inr_per_usd:
            stronger = country["currency"]
            strength_ratio = inr_per_unit / inr_per_usd
        else:
            stronger = "US Dollar"
            strength_ratio = inr_per_usd / inr_per_unit

        results.append({
            "country": country["country"],
            "capital": country["capital"],
            "currency_name": country["currency"],
            "currency_code": code,
            "language": country["language"],
            "english_friendly": country["english_friendly"],
            "usd_to_inr": round(inr_per_usd, 2),
            "currency_to_inr": round(inr_per_unit, 2),
            "stronger_currency": stronger,
            "strength_ratio": round(strength_ratio, 2),
        })

    return {
        "timestamp": datetime.now().isoformat(),
        "base_usd_to_inr": round(inr_per_usd, 2),
        "countries": sorted(results, key=lambda x: x["currency_to_inr"], reverse=True),
    }


if __name__ == "__main__":
    data = compare_currencies()
    print(json.dumps(data, indent=2))
