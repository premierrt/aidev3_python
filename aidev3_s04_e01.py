from aidevs3_lib_rt import *
import re

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


def ocen_obrazek_w_gpt( picture_name) :
    static_url= "https://centrala.ag3nts.org/dane/barbara/"
    image_url = static_url +"/"+picture_name
    user_promtp_to_eval_picture = f"""Jesteś asystentem AI, który analizuje jakość obrazów przesłanych przez użytkownika i zwraca odpowiedź, opisującą jaką operację na obrazie należy wykonać. Stosuj  się do następujących wskazówek.

    ### Goal
    Przeanalizuje dokładnie jakość przesłanego przez użytkownika obrazu i zdecyduj która operację na obrazie należy wykonać, aby poprawić jego jakość. Jedyne możliwe opcje to:
    rozjaśnienie, przyciemnienie albo naprawa szumów/glitch'y

    ### Response Format
    Odpowiadaj zwięźle jaką operacją na zdjęciu należy wykonać. 
    Załączaj w treści odpowiedzi nawzę obrazka = {picture_name}
    """
    resp = analyze_image_url( image_url,user_promtp_to_eval_picture)
    return resp


def znajdz_nazwe_pliku_re(text ):
    print ("!!!!szukam w text pliku png ", text)
    # Wyrażenie regularne
    pattern = r'\b\w+\.PNG\b'

    # Wyszukiwanie nazwy pliku
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        print(f"Znaleziono nazwę pliku: {match.group()}")
        return match.group()
    else:
        print("Nie znaleziono pliku .PNG")
        return ""
    
def zmodyfikuj_foto_w_centrali(uesr_prmompt):
    system_prompt=""" 
    Jesteś analizatorem treści przesłanej przez użytkownika.
    ###Goal
    Zdecyduj jaką operację na zdjęciu potrzebuje użytkownik. Możesz wybrać jedną wartość z pośród :  REPAIR, DARKEN ,BRIGHTEN 

    ###Rules
    Jeśli obraz wymaga usuniecia szumów/glitche zwróć REPAIR 
    Jeśli obraz wymaga rozjaśnienia zwróć BRIGHTEN
    Jeśli obraz wymaga przyciemnienia zwróć DARKEN
    Jeśli nie wiesz co odpowiedzieć, odpowiedź ERROR.

    ### Response Format
    Odpowiadaj zawsze tylko 1 słowem.

    """
    resp = ask_gpt(system_prompt,uesr_prmompt)
    print ("funkcja zmodyfikuj_foto_w_centali zwrócila ", resp)
    resp_z_centrali =modyfikuj_foto (resp)
    return resp_z_centrali

def modyfikuj_foto(operacja, picture_name):
    payload = operacja + picture_name
    answer = send_answer(payload, "photos")
    print ("funkcja modyfikuj_foto z parametrami zwrócila ", operacja, payload, answer)
    return answer


def plan(userPrompt):
    understaning_prompt_system_message = """
       From now on, you will function as a Task Query Analyzer and Splitter, focusing exclusively on the user's most recent message. 
    Your primary role is to interpret the latest user request about pictures and divide it into comprehensive subquery choosing one of following actions:  modify, evaluate or save picture.    
    <prompt_objective>
    Analyze the most recent user input about tasks and split it into detailed subquery for modifying, evaluating quality, or saving the picture, preserving all relevant information from this specific query. Provide thorough reasoning in the "_thinking" field.
    Always respond with a valid JSON object without markdown blocks.
    </prompt_objective>

    <prompt_rules>
    - Always answer with one next best action
    - Choose save option only when user explictly says the job is done
    - Focus exclusively on the user's most recent message
    - Ignore any previous context or commands that aren't part of the latest input
    - Analyze the entire latest user input to extract all task-related information
    - Split the input into separate queries for modifying or evaluating the picture
    - Ensure each subquery contains ALL necessary details from the latest input to perform the action
    - Write subqueries in natural language, making them comprehensive and self-contained
    - Include all relevant details such as picture name and picture url or any other mentioned attributes
    - Preserve the original wording and intent of the user's latest message as much as possible in the subqueries
    - In the "_thinking" field:
    - Explain your reasoning for splitting the query in detail
    - Consider and discuss different options for interpreting the user's latest request
    - Justify your choices for how you've split the queries
    - Mention any assumptions made and why they were necessary
    - Highlight any ambiguities in the latest query and how you resolved them
    - Explain how you ensured all information from the latest query is preserved
    - If the latest input is ambiguous or lacks crucial information, explicitly state this in the "_thinking" field and explain how you proceeded
    - Do not add any information or details that were not present or implied in the latest query
    </prompt_rules>

    <output_format>
    Always respond with this JSON structure:
    {
    "_thinking": "Detailed explanation of your interpretation process, consideration of options, reasoning for decisions, and any assumptions made",
    "modify": "(string) Comprehensive query for pricture that need to be modyfied, or None if not applicable",
    "evaluate": "(string) Comprehensive query for pricture to be quality evaluated, or None if not applicable",
    "save": "(string) Comprehensive query for pricture to be saved when user says the picure is ok and the job is done, or None if not applicable",
    "
    }
    </output_format>
    
    """
    response =ask_gpt_json_format("gpt-4o",understaning_prompt_system_message, userPrompt)
    print("######====",response)
    return response

def zapisz_obraz(nazwa_pliku,lista):
    list.append (  nazwa_pliku)
    return lista


def execute (planned_acction):
    nazwa_pliku = znajdz_nazwe_pliku_re(json.dumps(planned_acction))
    if planned_acction.get("modify") is not None:
        resp =zmodyfikuj_foto_w_centrali(nazwa_pliku)
    elif planned_acction.get("evaluate") is not None:
        resp =ocen_obrazek_w_gpt(nazwa_pliku)
    elif planned_acction.get("save") is not None:
        zapisz_obraz(nazwa_pliku)
        resp="DONE"
    return resp


        


if __name__ == "__main__":
    url_tab = get_file_url_mock()
    print (url_tab)

    
    pierwszy_obraz = url_tab.get('urls')[0].get("file_name")
    print (pierwszy_obraz  )
#     res = ocen_obrazek_w_gpt(pierwszy_obraz["file_url"])
#     print(res)
    # answer = send_answer("REPAIR IMG_559.PNG", "photos")
    # resp_message = answer['message']
    # print (resp_message)
    # print (znajdz_nazwe_pliku_re (resp_message) )

    #resp_message = ocen_obrazek_w_gpt ("https://centrala.ag3nts.org/dane/barbara/IMG_559_FGR4.PNG")
    #print (resp_message)
    

    init_prompt =f"Oto zdjęcie {pierwszy_obraz}. Sprawdź czy wymaga poprawienia "
    action_response =init_prompt

    while action_response != "DONE":
        action =plan(action_response)
        action_response =execute(action)


 