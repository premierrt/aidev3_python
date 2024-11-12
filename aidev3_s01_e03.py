import json
import re
import requests
from openai import OpenAI


def read_and_process_json():
    # Read the content of the json.json file
    with open('json.json', 'r') as file:
        content = file.read()  
        
        
    
    # Parse the JSON content
    # json.loads() to convert JSON-formatted strings into Python objects, such as dictionaries.
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    data['apikey'] ="c39a5c87-ce98-4292-8db1-8c3af9c1d566"
    # Ensure 'test-data' is in the parsed JSON data
    if 'test-data' not in data:
        print("No 'test-data' key found in JSON.")
        return
    
    # Iterate through each object in 'test-data'
    test_data = data['test-data']
    if isinstance(test_data, list):
        for item in test_data:
            if 'question' in item:
                question = item['question']
                correct_sum = evaluate_sum(question)
                item['answer'] = correct_sum
                print ("poprawna suma to ", correct_sum)
            else:
                print("No 'question' key found in item.")
            if 'test' in item:
                test_value = item['test']
                # Print the test dictionary
                print(f"Found 'test' with value: {test_value}")

                # Check if 'a' key is in the 'test' object and update it
                if isinstance(test_value, dict) and 'a' in test_value:
                    test_value['a'] = call_ai(test_value['q'])
                    print(f"Updated 'a' to: {test_value['a']}")             
    else:
        print("'test-data' is not a list")
    send_answer(data)    
    

def evaluate_sum(question):
    print(f"Question: {question}")
    # Use regular expressions to extract numbers and calculate the sum
    numbers = list(map(int, re.findall(r'\d+', question)))
    if len(numbers) >= 2: # Checking if there are at least two numbers to add
        result = sum(numbers)
        print(f"Calculated sum: {result}")
        return result
    else:
        print("Not enough numbers found for addition.")    

def call_ai(question ):
    print ("********** to jest pytanie do ai", question)
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
        {"role": "system", "content": preparePrompt()},
            {
                "role": "user",
                "content": question
            }
        ]
    )
    answer = completion.choices[0].message.content
    print (answer)
    return answer
    
def preparePrompt():
    content ="You are a helpful assistant. Answer given question. Be strict. Don't return nothing more than exact answer"
    content+= "\'\'\' example:"
    content+= "user: when first war world started? "
    content+= "assistant: 1939"
    return content


def send_answer(object_data):
    answer_url = "https://centrala.ag3nts.org/report"
    task_name = "JSON"
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

    


# Call the function
read_and_process_json()