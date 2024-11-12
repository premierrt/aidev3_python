import json
import requests
from openai import OpenAI


# Stała przechowująca klucz API
aidev3_api_key = "c39a5c87-ce98-4292-8db1-8c3af9c1d566"

system_prompt = "W podanym zdaniu zamień każde wystąpienie słów imię + nazwisko, nazwę ulicy + numer, miasto, wiek osoby na słowo CENZURA.\nNie możesz zmieniać składni, interpunkcji, białych znaków.\nPrzykład:\nZdanie:\nOsoba podejrzana to Andrzej Mazur. Adres: Gdańsk, ul. Długa 8. Wiek: 29 lat.\nZamień na:\nOsoba podejrzana to CENZURA. Adres: CENZURA, ul. CENZURA. Wiek: CENZURA lat."




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



def ask_gpt(system_prompt, question):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }]
    )
    return response.choices[0].message.content



def send_answer(object_data):
    answer_url = "https://centrala.ag3nts.org/report"
    task_name = "CENZURA"
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


# Pobranie i wyświetlenie danych
data = get_suspect_data(aidev3_api_key)
if data:
    print(data)
    result = ask_gpt(system_prompt, data)
    print(result)
    send_answer(result) 

