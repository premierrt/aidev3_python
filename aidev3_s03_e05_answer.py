
import json

import requests
from aidev3_s03_e05 import *


def send_answer(object_data):
    answer_url = "https://centrala.ag3nts.org/report"
    task_name = "connections"
    api_key= "c39a5c87-ce98-4292-8db1-8c3af9c1d566"
    payload = {
        "task": task_name,
        "apikey": api_key,
        "answer": object_data
    }
    print ( json.dumps(payload))
    headers = {'Content-Type': 'application/json'}  # Set the content type to application/json
    response = requests.post(answer_url, headers=headers, data=json.dumps(payload), verify=False)
    # Print the response from the server
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)





shortest_path = ['28', '3', '77', '39']
result_names =[]
users = load_json_from_file ("users.json")

for id in shortest_path:
    result_names.append (find_by_id(users, id))

print(result_names)
result_names_string = ', '.join(result_names)

print(result_names_string)

send_answer(result_names_string)