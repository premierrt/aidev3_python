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
    

def extract_raw_data_from_response(responsejson : str):
    reply = responsejson.get('reply', [])
    tabele=[]
    for element in reply:
        for key, value in element.items():
            tabele.append(value)
    return tabele

def send_requests_for_dc_ids(api_key, dc_ids, query2):
    results = []
    for dc_id in dc_ids:
        query = f"{query2}{dc_id}"  # Łączenie query2 z dc_id
        result = send_api_request(api_key, query)  # Wywołanie metody send_api_request
        raw = extract_raw_data_from_response(result)
        results.append(raw)  # Dodanie wyniku do listy
    return results

# Przykład użycia
if __name__ == "__main__":
    api_key = "c39a5c87-ce98-4292-8db1-8c3af9c1d566"
    query1 = "show tables"
    query_desc_table = "show create table "
    result = send_api_request(api_key,query1)
    print (result)
    table_names= extract_raw_data_from_response(result) 
    

    query2 = "show create table "  # Przykładowe zapytanie
    tables_descriptions = send_requests_for_dc_ids(api_key, table_names, query2)
    print(tables_descriptions)  # Wyświetlenie wyników

    systemPrompt = """ ###Context:
The user has to prepare sql select statement for data in database where tables structer  are descibed as follows:
[['connections', 'CREATE TABLE `connections` (\n  `user1_id` int(11) NOT NULL,\n  `user2_id` int(11) NOT NULL,\n  PRIMARY KEY (`user1_id`,`user2_id`)\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci'], ['correct_order', 'CREATE TABLE `correct_order` (\n  `base_id` int(11) DEFAULT NULL,\n  `letter` char(1) DEFAULT NULL,\n  `weight` int(11) DEFAULT 0\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci'], ['datacenters', 'CREATE TABLE `datacenters` (\n  `dc_id` int(11) DEFAULT NULL,\n  `location` varchar(30) NOT NULL,\n  `manager` int(11) NOT NULL DEFAULT 31,\n  `is_active` int(11) DEFAULT 0\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci'], ['users', "CREATE TABLE `users` (\n  `id` int(11) NOT NULL AUTO_INCREMENT,\n  `username` varchar(20) DEFAULT NULL,\n  `access_level` varchar(20) DEFAULT 'user',\n  `is_active` int(11) DEFAULT 1,\n  `lastlog` date DEFAULT NULL,\n  PRIMARY KEY (`id`)\n) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"]]

### Goal:
Given description of a table, prepare sql select which answer for the question: Which active data centers (DC_ID) are managed by employees who are on leave (is_active=0)?"""


    tools = [{ 
    "type": "function",
    "function" :{
        "name": "generate_sql_query",
        "description": "Generates a SQL SELECT query based on input conditions",
        "parameters": {
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "The name of the table to query"
                },
                "columns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "The list of columns to select"
                },
                "conditions": {
                    "type": "string",
                    "description": "The WHERE clause conditions"
                }
            },
            "required": ["table_name", "columns"]
        }
    }
    }
    ]

    function_call = ask_gpt_function_calling(systemPrompt, "",tools)
    arguments = json.loads(function_call.function.arguments)
    print (arguments)
    select_statement = "select " + ", ".join(arguments.get("columns")) + " from " + arguments.get("table_name") + " where " + arguments.get("conditions")
    print(select_statement)
    result = send_api_request(api_key,select_statement)
    print(result)
    dc_ids = [int(item['dc_id']) for item in result['reply']]
    send_answer(dc_ids, "database")

