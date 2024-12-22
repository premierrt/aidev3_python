import requests
import json
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
    
    # Zapisz dane do pliku w formacie JSON
    with open(f"{table_name}.json", "w") as file:
        json.dump(resp, file)  # Użyj json.dump() do zapisu w formacie JSON
    print(f"Dane zapisane do pliku: {table_name}.json")


def find_name(users, name) :
    for user in users:
        if user["username"] == name :
            return user["id"]

# Przykład użycia
if __name__ == "__main__":
    api_key = "c39a5c87-ce98-4292-8db1-8c3af9c1d566"
    
    # Wczytanie danych do plików
    # fetch_and_save_table_data(api_key, "users")   
    # fetch_and_save_table_data(api_key, "connections")

    users = load_json_from_file ("users.json")
    print (users)

    connections = load_json_from_file ("connections.json")

    rafal_id = find_name(users, "Rafał")
    barbara_id = find_name(users, "Barbara")

    print(rafal_id, barbara_id)

    

