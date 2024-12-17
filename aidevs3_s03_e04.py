from aidevs3_lib_rt import *
import requests

# Tutaj w sumie niewiele trzeba użyć LLMa, wystarczy na starcie wyciągnąć miejsca i imiona a później w pętli iterować 
# (druga iteracja) po API. Czy coś pominąłem? Chyba nie.. bo flaga zdobyta

def ask_for_place(query):
    """Wysyła zapytanie do API w celu uzyskania informacji o osobach lub miejscach."""
    api_key = "TWÓJ KLUCZ"  # Zastąp swoim kluczem API
    url = "https://centrala.ag3nts.org/places"
    
    payload = {
        "apikey": api_key,
        "query": query
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()  # Zwraca odpowiedź w formacie JSON
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

def ask_for_people(query):
    """Wysyła zapytanie do API w celu uzyskania informacji o osobach."""
    api_key = "TWÓJ KLUCZ"  # Zastąp swoim kluczem API
    url = "https://centrala.ag3nts.org/people"
    
    payload = {
        "apikey": api_key,
        "query": query
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()  # Zwraca odpowiedź w formacie JSON
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

def extract_places_from_response(response_json):
    """Zwraca listę miejsc z odpowiedzi JSON."""
    places = []
    if 'places' in response_json:
        places = response_json['places']
    return places

if __name__ == "__main__":
    api_key = "c39a5c87-ce98-4292-8db1-8c3af9c1d566"
    file_path = "/home/rafal/Pobrane/barbara.txt"
    file_content = read_file_content(file_path)
    print(file_content)

    system_prompt = "###Document " + file_content + """ \n  ###Goal
    Find all  peopele names and places in the document


    ###Output Format
    Response with JSON object with two list. One list with people  names and the other one with places.
    \n You must not use polish letters in response"""

    response_json =json.loads (ask_gpt_json_format(system_prompt, ""))
    miasta = extract_places_from_response(response_json)
    for miasto in miasta:
        print("pytam o miasto: ", miasto)
        resp =ask_for_place(miasto)
        print (resp)