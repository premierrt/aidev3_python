import requests
from aidevs3_lib_rt import *

def send_api_request(api_key, query):
    url = "https://centrala.ag3nts.org/apidb"
    
    # Treść zapytania JSON
    payload = {
        "task": "database",
        "apikey": api_key,
        "query": query
    }
    
    try:
        # Wysyłanie POST z zapytaniem JSON
        response = requests.post(url, json=payload)
        
        # Sprawdzenie statusu odpowiedzi
        if response.status_code == 200:
            # Zwrócenie odpowiedzi w formacie JSON
            return response.json()
        else:
            return {
                "error": f"Request failed with status code {response.status_code}",
                "details": response.text
            }
    except requests.RequestException as e:
        return {
            "error": "Request failed",
            "details": str(e)
        }
    

def fetch_and_save_table_data(api_key, table_name):
    select_statement = f"select * from {table_name}"
    print(select_statement)
    result = send_api_request(api_key, select_statement)
    resp = result.get("reply")
    
    # Zapisz dane do pliku
    with open(f"{table_name}.txt", "w") as file:
        file.write(str(resp))  # Zapisz odpowiedź jako tekst
    print(f"Dane zapisane do pliku: {table_name}.txt")

# Przykład użycia
if __name__ == "__main__":
    api_key = "c39a5c87-ce98-4292-8db1-8c3af9c1d566"
    
    # Wywołanie nowej funkcji
    fetch_and_save_table_data(api_key, "users")   
    fetch_and_save_table_data(api_key, "connections")


 
