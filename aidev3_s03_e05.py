import requests
import json
from aidevs3_lib_rt import *
from collections import defaultdict, deque


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
        


def find_shortest_path(json_data, start_id, end_id):
    # Budowanie grafu z danych JSON
    graph = defaultdict(list)
    for edge in json_data:
        user1 = edge["user1_id"]
        user2 = edge["user2_id"]
        graph[user1].append(user2)
        graph[user2].append(user1)  # Zakładamy graf nieskierowany
    
    # BFS do znalezienia najkrótszej ścieżki
    queue = deque([(start_id, [start_id])])  # Kolejka BFS, przechowuje (węzeł, ścieżka)
    visited = set()  # Zbiór odwiedzonych węzłów

    while queue:
        current_node, path = queue.popleft()
        
        if current_node == end_id:  # Znaleziono ścieżkę
            return path

        if current_node not in visited:
            visited.add(current_node)
            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    
    return None  # Jeśli brak ścieżki

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

    # Wywołanie funkcji
    start_node = rafal_id
    end_node = barbara_id
    shortest_path = find_shortest_path(connections, start_node, end_node)

    if shortest_path:
        print(f"Najkrótsza ścieżka od {start_node} do {end_node}: {shortest_path}")
    else:
        print(f"Brak ścieżki od {start_node} do {end_node}")

        

