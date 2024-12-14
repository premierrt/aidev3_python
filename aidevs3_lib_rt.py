import json
import os
from openai import OpenAI
import requests


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


def ask_gpt_json_format(system_prompt, question):
    print ("============================================")
    print (question)
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        response_format={ "type": "json_object" },
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


def send_answer(object_data, task_name):
    answer_url = "https://centrala.ag3nts.org/report"
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
           # print (filename)
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


def load_files_to_dictionary(directory_path: str, file_list: list) -> dict:
    """
    Wczytuje zawartość plików tekstowych do słownika.
    
    Args:
        directory_path (str): Ścieżka do katalogu z plikami
        file_list (list): Lista nazw plików do wczytania
        
    Returns:
        dict: Słownik gdzie kluczem jest nazwa pliku, a wartością jego zawartość jako string
    """
    files_dictionary = {}
    
    try:
        for filename in file_list:
            full_path = os.path.join(directory_path, filename)
            try:
                with open(full_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    files_dictionary[filename] = content
            except FileNotFoundError:
                print(f"Nie znaleziono pliku: {filename}")
            except Exception as e:
                print(f"Błąd podczas wczytywania pliku {filename}: {e}")
                
        return files_dictionary
    
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return {}


def remove_extension(filename: str, extension: str) -> str:
    """
    Usuwa rozszerzenie z nazwy pliku.
    
    Args:
        filename (str): Nazwa pliku
        extension (str): Rozszerzenie do usunięcia (np. '.txt')
        
    Returns:
        str: Nazwa pliku bez rozszerzenia
    """
    # Upewnij się, że rozszerzenie zaczyna się od kropki
    if not extension.startswith('.'):
        extension = '.' + extension
        
    # Jeśli nazwa pliku kończy się danym rozszerzeniem, usuń je
    if filename.lower().endswith(extension.lower()):
        return filename[:-len(extension)]
    
    return filename



def do_embedding(text : str):
    client = OpenAI()
    result =client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        encoding_format="float"
    )
    return result