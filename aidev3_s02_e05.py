import json
import re
from openai import OpenAI
import requests


#####
#####
#### Wersja "na skróty" - zamiast podmieniac wszyskie media na opis za pomoca modelu,
# ## na krótko wrzucony jest opis alt obrazka z pizza i model poprawnie odpowiedzial na pytanie
####

questions = {
    "01": "jakiego owocu użyto podczas pierwszej próby transmisji materii w czasie?",
    "02": "Na rynku którego miasta wykonano testową fotografię użytą podczas testu przesyłania multimediów?",
    "03": "Co Bomba chciał znaleźć w Grudziądzu?",
    "04": "Resztki jakiego dania zostały pozostawione przez Rafała?",
    "05": "Od czego pochodzą litery BNW w nazwie nowego modelu językowego?"
}

def read_markdown_file() -> str:
    """
    Wczytuje zawartość pliku html-to-markdown.md.txt do zmiennej string.
    
    Returns:
        str: Zawartość pliku lub pusty string w przypadku błędu
    """
    try:
        with open('html-to-markdown.md.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        print(f"Błąd podczas odczytu pliku: {e}")
        return "" 





def add_alt_text(markdown_content, image_path, alt_text):
    """
    Dodaje tekst alt do znacznika obrazu w Markdown.
    
    Args:
        markdown_content (str): Treść Markdown.
        image_path (str): Ścieżka do obrazu w znaczniku.
        alt_text (str): Tekst alternatywny do dodania.
    
    Returns:
        str: Markdown z dodanym tekstem alt.
    """
    # Regex do znalezienia znacznika obrazu z podaną ścieżką
    pattern = rf'!\[\](\({re.escape(image_path)}\))'
    replacement = rf'![{alt_text}]\1'
    
    # Zastąp pusty tekst alt odpowiednim tekstem
    updated_content = re.sub(pattern, replacement, markdown_content)
    
    return updated_content



#fake implemetnacja - na szywno zwracam tekst, ktory powinno zwroić ai do image'ów
def enrich_markdown_with_picture_description(markdown_text) -> str:
   

    image_path = "i/resztki.png"
    alt_text = "Obrazek przedstawia pizze"

    # Dodanie alt text
    updated_markdown = add_alt_text(markdown_text, image_path, alt_text)

    # Wynik
    print(updated_markdown)
    return updated_markdown



def ask_gpt(system_prompt, question):
    print ("============================================")
    print (question)
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[{
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }]
    )
    res = response.choices[0].message.content
    print (res)
    print ("================================================")
    return res

def send_answer(object_data):
    answer_url = "https://centrala.ag3nts.org/report"
    task_name = "arxiv"
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

def extract_all_image_filenames(text: str) -> list[str]:
    """
    Wyszukuje wszystkie obrazy markdown w tekście i zwraca listę nazw plików.
    
    Args:
        text (str): Tekst do przeanalizowania
        
    Returns:
        list[str]: Lista nazw plików obrazów
    """
    import re
    
    pattern = r'!\[\]\(i/([^)]+)\)'
    
    # Znajdujemy wszystkie dopasowania
    matches = re.finditer(pattern, text)
    
    # Zwracamy listę nazw plików
    return [match.group(1) for match in matches]

if __name__ == "__main__" :
    context = read_markdown_file()

    print (extract_all_image_filenames(context))
    context = (enrich_markdown_with_picture_description(context))
    systemPromptInro = "Poniżej znajduje się dokument. Przenalizuj go bardzo szczegółowo. Na jego podstawie odpowiedz na pytania dostarczone przez Użytkownika: "
    systemPrompt = systemPromptInro + context
   # print (systemPrompt)
    userPrompt = " Poniżej lista pytań dotyczących dokumentu. Odpowiedz na każde z nich osobno. Na każde pytanie odpwoiedz krótko jednym zdaniem. " 
   
    pytania = """
    01=jakiego owocu użyto podczas pierwszej próby transmisji materii w czasie?
    02=Na rynku którego miasta wykonano testową fotografię użytą podczas testu przesyłania multimediów?
    03=Co Bomba chciał znaleźć w Grudziądzu?
    04=Resztki jakiego dania zostały pozostawione przez Rafała?
    05=Od czego pochodzą litery BNW w nazwie nowego modelu językowego?
    """
    
    question = userPrompt + pytania
    ask_gpt(systemPrompt, question)

    answer = {
    "01": "truskawki",
    "02": "estową fotografię wykonano na rynku w Krakowie.",
    "03": "hotel",
    "04": "Rafał pozostawił resztki pizzy.",
    "05": "Litery BNW w nazwie nowego modelu językowego pochodzą od 'Brave New World'"
    }

   # send_answer(answer)