from aidevs3_lib_rt import *


# 1. Wysyłam do LLM message z api w celu wyciągnięcia nazw fotek.
# 2. Wysyłam fotki do LLM w celu zdefiniowania jaka operacja ma być na nich wykonana (jedna z 3 lub nic jeżeli fota jest dobra).
# 3. Wykonuje odpowiednie operacje na fotkach z wykorzystaniem API. Dodatkowo wyciągam nowe nazwy fotek z wykorzystaniem prompta z punktu 1.
# 3. Powtarzam punkt 2 oraz 3, aż wszystkie fotki są ok.
# 4. Przesyłam poprawione fotki do LLM w celu stworzenia rysopisu.

# y na tym etapie powinniśmy wchodzić w interakcję z agentem i nim “sterować” w obrębie dostarczonych mu narzędzi
# i ich wykorzystania na podstawie odpowiedzi, które od niego otrzymujemy, 
# czy raczej wszystkie kroki powinny odbywać się autonomicznie i być zdefiniowane przez nas w algorytmie oczekując,
# że “zrobi za nas wszystko” i na końcu wypluje odpowiedź?
# możesz spokojnie rozbić na etapy. W tym zadaniu główny nacisk jest na to żeby stworzyć odpowiednie narzędzia 
# i żeby LLM się tymi narzedziami posłużył. Ale możesz spokojnie mieć dwa etapy na przykład:
# poprawianie zdjęć
# opisywanie zdjęć


def get_file_urls() :
    response = send_answer ("START", "photos")
    resp_message = response['message']

    get_file_urls_system_prompt = """ Jesteś asystentem który analizuje dane podane przez użytkownika i zwraca odpowiedź w postaci JSON. Stosuje  się do następujących wskazówek.

    ### Goal
    Przeanalizuje dane podane przez użytkownika i zwróć  listę adresów url do plików PNG. 

    ###Rules
    Odpowiedź może zawierać tylko JSON z danymi. Nie wchodź w interakcje z użytkownikiem.

    ### Response Format
    {
    "urls": [
    {"file_name":"name of the file 1", "file_url": "url of file 1"},
    {"file_name":"name of the file 2", "file_url": "url of file 2"},
    ]
    }


    ###Example
    input: Jakis tekst https://adres.obrazka/ a nazwa obrazka jest dalej IMG_666.PNG
    output: [ {"file_name": "IMG_666.PNG" ,file_url" : "https://adres.obrazka/IMG_666.PNG"} ] """

    ask_gpt_json_format(get_file_urls_system_prompt, resp_message)


def get_file_url_mock():
    mock_resp ="""{
    "urls": [
        {"file_name": "IMG_559.PNG", "file_url": "https://centrala.ag3nts.org/dane/barbara/IMG_559.PNG"},
        {"file_name": "IMG_1410.PNG", "file_url": "https://centrala.ag3nts.org/dane/barbara/IMG_1410.PNG"},
        {"file_name": "IMG_1443.PNG", "file_url": "https://centrala.ag3nts.org/dane/barbara/IMG_1443.PNG"},
        {"file_name": "IMG_1444.PNG", "file_url": "https://centrala.ag3nts.org/dane/barbara/IMG_1444.PNG"}
    ]
    }"""
    return json.loads(mock_resp)

if __name__ == "__main__":
    url_tab = get_file_url_mock()
    print (url_tab)
    