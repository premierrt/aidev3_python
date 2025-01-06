
import json

import requests


def send_answer(object_data):
    answer_url = "https://centrala.ag3nts.org/report"
    task_name = "webhook"
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
    resp =send_answer("https://azyl-51131.ag3nts.org/where_am_i")

    print(resp)

### {{FLG:DARKCAVE}}"
