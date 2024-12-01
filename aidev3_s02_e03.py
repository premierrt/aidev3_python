import requests
import json
from openai import OpenAI

def pobierz_dane():
    url = "https://centrala.ag3nts.org/data/c39a5c87-ce98-4292-8db1-8c3af9c1d566/robotid.json"
    
    try:
        # Pobieranie danych z URL
        odpowiedz = requests.get(url)
        odpowiedz.raise_for_status()  # Sprawdzenie czy nie wystąpił błąd HTTP
        
        # Przetworzenie odpowiedzi na format JSON
        dane = odpowiedz.json()
        
        # Wyświetlenie zawartości
        print("Pobrane dane:")
        print(json.dumps(dane, indent=2, ensure_ascii=False))
        
        return dane
        
    except requests.exceptions.RequestException as e:
        print(f"Wystąpił błąd podczas pobierania danych: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Wystąpił błąd podczas przetwarzania JSON: {e}")
        return None

def get_description(json_data):
    try:
        # Sprawdzenie czy json_data nie jest None
        if json_data is None:
            raise ValueError("Otrzymano pusty obiekt JSON")
            
        # Próba pobrania wartości pola 'description'
        if 'description' in json_data:
            return json_data['description']
        else:
            raise KeyError("Nie znaleziono pola 'description' w obiekcie JSON")
            
    except (TypeError, KeyError) as e:
        print(f"Wystąpił błąd podczas przetwarzania JSON: {e}")
        return None

def send_answer(object_data):
    answer_url = "https://centrala.ag3nts.org/report"
    task_name = "robotid"
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


def generateImage(image_prompt):
    from openai import OpenAI
    client = OpenAI()   
    response = client.images.generate(
    model="dall-e-3",
    prompt=image_prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )
    image_url = response.data[0].url
    return image_url

if __name__ == "__main__":
   description = get_description( pobierz_dane()  )
   print ( description)
   url = generateImage(description)
   send_answer(url)
   print (url)

