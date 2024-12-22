from aidevs3_lib_rt import *
import requests
import sys  # Dodaj import sys na początku pliku
import json  # Upewnij się, że importujesz json na początku pliku

# Tutaj w sumie niewiele trzeba użyć LLMa, wystarczy na starcie wyciągnąć miejsca i imiona a później w pętli iterować 
# (druga iteracja) po API. Czy coś pominąłem? Chyba nie.. bo flaga zdobyta

def ask_place(query):
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
            response_json = response.json()
            if 'message' in response_json:
                if response_json['message'] == '[**RESTRICTED DATA**]':
                    return ["RESTRICTED"]  # Zwraca słowo RESTRICTED
              #  if response_json['message'] != "RESTRICTED":
                return response_json['message'].split()  # Zwraca listę miejsc
            return []  # Zwraca pustą listę, jeśli 'message' nie istnieje
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

def ask_people(query):
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
            response_json = response.json()
            if 'message' in response_json:
                if response_json['message'] == '[**RESTRICTED DATA**]':
                    return ["RESTRICTED"]  # Zwraca słowo RESTRICTED
                return response_json['message'].split()  # Zwraca listę miejsc
            return []  # Zwraca pustą listę, jeśli 'message' nie istnieje
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

def extract_people_from_response(response_json):
    """Zwraca listę miejsc z odpowiedzi JSON."""
    people = []
    if 'people' in response_json:
        people = response_json['people']
    return people


def gpt_decide_if_people_or_place(item):
    response_str = ask_gpt(system_prompt_decide_people_place, item)
    response_json = json.loads(response_str)  # Zdeserializuj odpowiedź JSON
    # Parse the JSON response to extract user_input and classified_type
    user_input = response_json.get("user_input")
    classified_type = response_json.get("classfied_type")
    return (user_input, classified_type)  # Return as a tuple

# jako parametr lista
def pytaj_dalej(items): 
    global circut_breaker  # Deklaracja zmiennej globalnej
    if circut_breaker > circut_breaker_limit:  # Sprawdzenie wartości circuit_breaker
        sys.exit()  # Zakończ działanie programu
    for item in items:
        print(f"Current item: '{item}'")  # Debugging line
        if item.lower() == "restricted" or item.lower() == "barbara" or item.lower() == "glitch":
            print("Restricted")
            continue
        if item in itemy_odpytane:  # Sprawdzenie, czy item jest już na liście itemy_odpytane
            continue  # Jeśli tak, przejdź do następnego item
        else:
            print(f"{item} nie było jeszcze odwiedzone.")
            what_is_item = gpt_decide_if_people_or_place(item)
            if what_is_item[1] == "people":
                resp = ask_people(what_is_item[0])
            elif what_is_item[1] == "place":
                resp = ask_place(what_is_item[0])
            else:
                raise ValueError(f"{what_is_item[0]} blad danych ani place ani people.")

            itemy_odpytane.append(what_is_item[0])
            wyniki_przesukiwania[what_is_item[0]] = resp
            print ("**************Procesuje : " +what_is_item[0] + " *******"+ str(circut_breaker)  )
            print (wyniki_przesukiwania)  
            circut_breaker += 1
            pytaj_dalej(resp)    
            
  


if __name__ == "__main__":
    api_key = "c39a5c87-ce98-4292-8db1-8c3af9c1d566"
    file_path = "/home/rafal/Pobrane/barbara.txt"
    file_content = read_file_content(file_path)
    print(file_content)

    system_prompt = "###Document " + file_content + """ \n  ###Goal
    Find all peopele first names and city names in the document


    ###Output Format
    Response with JSON object with two list. One list with people  first names and the other one with places.
    \n If place is not in polish translate it to polish 
    \n You must not use polish letters in response \n """


    itemy_odpytane =[]
    wyniki_przesukiwania = {}
    circut_breaker =0
    circut_breaker_limit =20


    system_prompt_decide_people_place = """###Goal
Analazy user input and find if the word is place or first name. 

###Rules
If user input is place then classfied type "type" = "place".  if user input is first name then classfied type= "people". If user input can not be classified answer with "error".
AZAZEL is first name.

###Output Format
Response with json containg user_input and found classfied_type. You must not use polish letters in response.

###Example
Example 1
input: Warszawa
output: {"user_input":"WARSZAWA", "classfied_type": "place"}

Example 2
input: Rafał
output: output: {"user_input":"RAFAL", "classfied_type": "people"}
"""

    response_json =json.loads (ask_gpt_json_format(system_prompt, ""))
   # miasta = extract_places_from_response(response_json)
    people = extract_people_from_response (response_json)
    pytaj_dalej(people)
    # for miasto in miasta:
    #     print("#### pytam o miasto: ", miasto)
    #     resp =ask_for_place(miasto)
    #     print (resp)

   # print( ask_for_people("BARBARA") )
   # {'code': 0, 'message': '[**RESTRICTED DATA**]'}
    #  wez osobe 
  #      sprawdz gdzie byla
  #          dla kazdej osoby spraw

 