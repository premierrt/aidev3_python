

import json

import requests


def send_answer(object_data):
    answer_url = "https://centrala.ag3nts.org/report"
    task_name = "notes"
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


if __name__ == '__main__':
    
    
    dane =    {
        "01":"2019",
        "02":"Adam",
        "03":"jaskinia skalna",
        "04":"2024-11-12",
        "05":"Lubawa"
        }
    resp =send_answer(dane)

    print(resp)

#{{FLG:DEATHNOTE}}