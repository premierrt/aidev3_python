import requests

def get_suspect_data(api_key):
    # Bazowy URL
    base_url = "https://centrala.ag3nts.org/data"
    
    # Pełny URL z kluczem API
    url = f"{base_url}/{api_key}/cenzura.txt"
    
    try:
        # Pobieranie danych
        response = requests.get(url)
        response.raise_for_status()  # Sprawdzenie czy nie było błędu
        
        # Zwracanie zawartości pliku
        return response.text
        
    except requests.exceptions.RequestException as e:
        print(f"Wystąpił błąd podczas pobierania danych: {e}")
        return None

# Stała przechowująca klucz API
aidev3_api_key = "c39a5c87-ce98-4292-8db1-8c3af9c1d566"

# Pobranie i wyświetlenie danych
data = get_suspect_data(aidev3_api_key)
if data:
    print(data)    