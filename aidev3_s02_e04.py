import base64
import io
import json
import os
from openai import OpenAI
from PIL import Image
import requests



def get_files_by_extension(directory_path: str, extension: str) -> list:
    """
    Returns a list of files with the specified extension from the given directory.
    
    Args:
        directory_path (str): Path to the directory to search in
        extension (str): File extension to filter (e.g., '.txt', '.mp3')
    
    Returns:
        list: List of filenames with the specified extension
    """
    # Ensure extension starts with a dot
    if not extension.startswith('.'):
        extension = '.' + extension
    
    # List to store matching files
    matching_files = []
    
    try:
        # Iterate through files in the directory
        for filename in os.listdir(directory_path):
            print (filename)
            # Check if the file ends with the specified extension
            if filename.lower().endswith(extension.lower()):
                matching_files.append(filename)
                
        return matching_files
    
    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
        return []
    except PermissionError:
        print(f"Permission denied to access directory: {directory_path}")
        return []


def process_mp3_file(filePath):
    client = OpenAI()
    audio_file= open(filePath, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcription.text

def aiFindInformation(system_prompt, prompt):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        messages=[{
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": prompt
        }]
    )
    return response.choices[0].message.content

def str_to_bool(text: str) -> bool:
    """
    Konwertuje tekst 'true' lub 'false' na wartość logiczną.
    Rzuca ValueError dla nieprawidłowych wartości.
    """
    text = text.lower()
    if text == 'true':
        return True
    elif text == 'false':
        return False
    else:
        raise ValueError(f"Nieprawidłowa wartość: '{text}'. Dozwolone wartości to 'true' lub 'false'")

def append_to_file(file_path: str, text: str) -> None:
    """
    Dopisuje tekst na końcu pliku.
    
    Args:
        file_path (str): Ścieżka do pliku
        text (str): Tekst do dopisania
    """
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(text + '\n')
    except IOError as e:
        print(f"Błąd podczas zapisywania do pliku {file_path}: {e}")


def analyze_image(image_path):
    """
    Funkcja wczytuje obraz PNG i wysyła go do OpenAI w celu analizy
    
    Args:
        image_path (str): Ścieżka do pliku PNG
        api_key (str): Klucz API OpenAI
    
    Returns:
        str: Opis obrazu zwrócony przez OpenAI
    """
    # Inicjalizacja klienta OpenAI
    client = OpenAI()
    
    # Wczytanie obrazu
    try:
        # Otwieramy obraz za pomocą PIL
        image = Image.open(image_path)
        
        # Konwertujemy obraz do formatu bajtowego
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        
        # Kodowanie obrazu do base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Wysłanie zapytania do API OpenAI
        response = client.chat.completions.create(
            model="gpt-4o",  
            temperature=0.1,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", 
                         "text": "Spójrz dokładnie na text na obrazie. Jest to notatka. Zwróć tekst tej notatki. "},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}" 
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Wystąpił błąd: {str(e)}"

def save_text_transcription_to_file(katalog_path: str, wyniki_path: str) -> None:
    """
    Processes all MP3 files in a directory and saves their transcriptions to a file.
    
    Args:
        katalog_path (str): Path to the directory containing MP3 files
        wynik_transkrypcji_path (str): Path to the output file where transcriptions will be saved
    """
    pliki = get_files_by_extension(katalog_path, "mp3")
    for plik_nazwa in pliki:
        plik_sciezka = f"{katalog_path}{plik_nazwa}"
        print(plik_sciezka)
        transkrypacja = process_mp3_file(plik_sciezka)
        print(transkrypacja)
        new_file_extension = add_txt_extension(plik_nazwa)
        nowa_sciezka =  f"{wyniki_path}{new_file_extension}"
        append_to_file(nowa_sciezka, transkrypacja)


def add_txt_extension(filename: str) -> str:
    """
    Dodaje rozszerzenie .txt do nazwy pliku.
    
    Args:
        filename (str): Nazwa pliku
        
    Returns:
        str: Nazwa pliku z dodanym rozszerzeniem .txt
    """
    return f"{filename}.txt"


def remove_txt_extension(filename: str) -> str:
    """
    Usuwa rozszerzenie .txt z nazwy pliku.
    
    Args:
        filename (str): Nazwa pliku z rozszerzeniem .txt
        
    Returns:
        str: Nazwa pliku bez rozszerzenia .txt
    """
    if filename.endswith('.txt'):
        return filename[:-4]
    return filename


def save_ocr_to_file(katalog_path, wyniki_path):
    pliki = get_files_by_extension(katalog_path, "png")
    for plik_nazwa in pliki:
        plik_sciezka = f"{katalog_path}{plik_nazwa}"
        print(plik_sciezka)
        ocr = analyze_image(plik_sciezka)
        print(ocr)
        new_file_extension = add_txt_extension(plik_nazwa)
        nowa_sciezka =  f"{wyniki_path}{new_file_extension}"
        append_to_file(nowa_sciezka, ocr)
        
        
        ##########



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


def read_file(file_path: str) -> str:
    """
    Wczytuje zawartość pliku tekstowego.
    
    Args:
        file_path (str): Ścieżka do pliku
        
    Returns:
        str: Zawartość pliku
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        print(f"Błąd podczas odczytu pliku {file_path}: {e}")
        return ""


def process_files_with_gpt(katalog_path: str, system_prompt: str) -> dict:
    """
    Przetwarza wszystkie pliki txt w katalogu przez ask_gpt i zapisuje wyniki w słowniku.
    
    Args:
        katalog_path (str): Ścieżka do katalogu z plikami
        system_prompt (str): Prompt systemowy dla GPT
        
    Returns:
        dict: Słownik z wynikami, gdzie kluczem jest nazwa pliku
    """
    slownik = {}
    pliki = get_files_by_extension(katalog_path, "txt")
    
    for plik_nazwa in pliki:
        plik_sciezka = f"{katalog_path}{plik_nazwa}"
        tresc = read_file(plik_sciezka)
        wynik = ask_gpt(system_prompt, tresc)
        if wynik != "null":
            slownik[ remove_txt_extension (plik_nazwa)] = wynik
        
    return slownik


def send_answer(object_data):
    answer_url = "https://centrala.ag3nts.org/report"
    task_name = "kategorie"
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


def reverse_dictionary(slownik: dict) -> dict:
     # Tworzymy nowy słownik z kluczami 'people' i 'hardware'
    transformed_dict = {"people": [], "hardware": []}
    
    # Iterujemy przez podany słownik
    for key, value in dict.items():
        if value in transformed_dict:
            # Dodajemy klucz do odpowiedniej kategorii
            transformed_dict[value].append(key)
    
    return transformed_dict


if __name__ == "__main__":
    wynik_transkrypcji_path = "/home/rafal/Pobrane/pliki_z_fabryki/wyniki_rafal/"
    katalog_path = "/home/rafal/Pobrane/pliki_z_fabryki/"
   # save_text_transcription_to_file(katalog_path, wynik_transkrypcji_path)
   # save_ocr_to_file(katalog_path, wynik_transkrypcji_path)
    system_prompt= """
###Objective
Proszę przeanalizować poniższy tekst. 
Odpowiadaj tylko wartościami people, hardware, null.

###Rules
Jeśli w tekście znajdują się w nim informacje o schwytanych ludziach lub śladach ich obecności wykrytych w trakcie patrolu, zwróć słowo "people". 
Jeżeli w tekście znajdują się informacje o naprawionych usterkach sprzętowych (hardware), zwróć słowo "hardware".  Jeśli tekst dotyczy software zwracaj null.
W przypadku, gdy żaden z tych tematów nie występuje, odpowiedz null. Oto tekst do analizy:    """

    dict = process_files_with_gpt(wynik_transkrypcji_path, system_prompt)
    for klucz in dict:
        print(f"{klucz}: {dict[klucz]}")
    object_json = reverse_dictionary(dict)

    print(object_json)
    send_answer(object_json)    
   # print (get_files_by_extension(wynik_transkrypcji_path, "txt") )
