import os
from aidevs3_lib_rt import ask_gpt


###
##Wystarczy odpytać LLM o słowa kluczowe dla każdego faktu (jeden raz i zapisać). 
##Później dla każdego raportu (jeden raz i zapisać). 
# Później zapytać kogo wymienia dany raport (jaką osobę) i jeśli mamy takie fakty to połączyć słowa z faktów ze słowami z raportu i mamy pełną listę słów kluczowych.
###
### Do tego zadania spokojnie starcza “tani” model typu gpt-4o-mini

# A jeśli w raporcie jest mowa o Kowalskim, 
#to wszystkie słowa kluczowe z faktów o Kowalskim są tutaj oczekiwane
#indexowac nazwy plikow

#a to zrobiłem tak, że dla każdego faktu mam listę osób które tam występują (wygenerowaną przez model) i po nich łączę. 
#Dzięki temu mogę to wykorzystać gdziekolwiek później, by
#
# kwestia jak łączysz fakty z raportami. 
# Wydobywasz słowa kluczowe osobno dla faktów i później dołączasz je do słów z raportu jeśli osoba pasuje? 
#
# może warto spróbować napisać prompt po angielsku i użyć “keywords” - mam wrażenie że wtedy LLM lepiej wie co wyciągać. No i warto dodać informację po co te słowa kluczowe - tak jak w zadaniu → “Metadane powinny ułatwić centrali wyszukiwanie tych raportów za pomocą własnych technologii”
#Wtedy też model wyciąga inne/więcej słów kluczowych niż tylko poproszony “po prostu” o słowa kluczowe. 

prompt = """
''' Objective:
Analyze following text and generate keywords to be used as meta-data for searching purpeses in other search and indexing tools. 
''' Rules:
Please generate keywords in Polish. 
Time should be returned in time format, for example 21:44
You should not start new line with - sign
""" 


raporty_path = "/home/rafal/Pobrane/pliki_z_fabryki_2/"
fakty_path = raporty_path+"facts/"
raporty_keywords_path = raporty_path +"/raporty_keywords/"
fakty_keyword_path = fakty_path +"fakty_keywords/"


find_name_prompt = """
''' Objective: Analyze text and find name and surname of a person and sector name

''' Rules: 
Return data in JSON format
If you can't find any name and surname then in JSON response set name = null


'''Example 1:
{"name" : "Adam Michnik",
"sector": "sektor D"
}

'''Example 2:
{"name" : null,
"sector": "sektor D"
}


"""


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
    

def save_to_file(content: str, filename: str) -> bool:
    """
    Zapisuje podany tekst do pliku. Tworzy katalogi w ścieżce, jeśli nie istnieją.
    
    Args:
        content (str): Treść do zapisania
        filename (str): Nazwa pliku docelowego
    
    Returns:
        bool: True jeśli zapis się powiódł, False w przypadku błędu
    """
    try:
        # Utworzenie katalogu (i katalogów nadrzędnych), jeśli nie istnieją
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(content)
        return True
        
    except IOError as e:
        print(f"Błąd podczas zapisu do pliku: {e}")
        return False
# Przykład użycia:
# text = "Przykładowa treść do zapisania"
# success = save_to_file(text, "output.txt")
# if success:
#     print("Zapisano pomyślnie")
    

def processTextFiles(path: str, output_path: str, prompt: str):
    fileNames = get_files_by_extension(path, ".txt")
    for file in fileNames:
        print(file)
        with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
            content = f.read()
            keywords = ask_gpt(prompt, content)
            output_file = os.path.join(output_path, file.replace('.txt', '_keywords.txt'))
            save_to_file(keywords, output_file)
  

def appendMetaDataFromFileName(path: str, output_path: str):
    filelist = get_files_by_extension(path, ".txt")
    print(path)
    for filename in filelist:
        print(filename)
        # Rozdzielamy najpierw na podstawie pierwszego podkreślnika
        date, rest = filename.split('_', 1)
        
        # Z pozostałej części wyodrębniamy numer raportu i sektor
        report_part, sector_part = rest.rsplit('-sektor_', 1)
        
        # Wyciągamy numer raportu
        report_number = report_part.replace('report-', '')
        
        # Usuwamy rozszerzenie .txt z sektora
        sector = sector_part.replace('.txt', '')
        
        # Formatujemy końcowy string
        additional_keywords = f" , {date}, raport {report_number}, sektor {sector}"
        print(additional_keywords)
        output_file = os.path.join(output_path, filename.replace('.txt', '_keywords.txt'))
        save_to_file(additional_keywords, output_file)

def load_keywords_from_raport_file(file_path: str) -> dict:
    """
    Wczytuje dane z pliku tekstowego do słownika.
    
    Args:
        file_path (str): Ścieżka do pliku wejściowego
        
    Returns:
        dict: Słownik gdzie kluczem jest nazwa pliku, a wartością lista danych
    """
    keywords_dict = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            filename = os.path.basename(file_path)
            new_filename = filename.replace('_keywords', '')
         
            for line in file:
                parts = line.strip().split(',')
                data = [item.strip() for item in parts]
                keywords_dict[new_filename] = data
                
        return keywords_dict
    
    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {file_path}")
        return {}
    except Exception as e:
        print(f"Wystąpił błąd podczas wczytywania pliku: {e}")
        return {}

# Przykład użycia:
# keywords = load_keywords_from_file("sciezka/do/pliku.txt")
# print(keywords)


def load_keywords_from_fact_file(file_path: str) -> dict:
    """
    Wczytuje dane z pliku tekstowego do słownika.
    Każda linia pliku powinna zawierać nazwę pliku i dane rozdzielone przecinkami.
    
    Args:
        file_path (str): Ścieżka do pliku wejściowego
        
    Returns:
        dict: Słownik gdzie kluczem jest nazwa pliku, a wartością lista danych
    """
    keywords_dict = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Dzielimy linię na części
                parts = line.strip().split(',')
                
                # Pierwszy element to nazwa pliku
                filename = parts[0].strip()
                
                # Pozostałe elementy to dane
                data = [item.strip() for item in parts]
                
                # Dodajemy do słownika
                keywords_dict[filename] = data
                
        return keywords_dict
    
    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {file_path}")
        return {}
    except Exception as e:
        print(f"Wystąpił błąd podczas wczytywania pliku: {e}")
        return {}

def load_keywords_raport_files (path):
    i=0
    dane = []
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        print(full_path)
        dane.append(load_keywords_from_raport_file(full_path))
        i += 1
    return dane    


def load_keywords_fact_files (path):
    i=0
    dane = []
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        print(full_path)
        dane.append(load_keywords_from_fact_file(full_path))
        i += 1
    return dane   

def print_keywords_data(keywords_data: list):
    """
    Prints keywords data from reports in a readable format.
    
    Args:
        keywords_data (list): List of dictionaries containing keywords data
    """
    for report_dict in keywords_data:
        for filename, keywords in report_dict.items():
            print(f"\key: {filename}")
            print("values:", ", ".join(keywords))

if __name__ == "__main__":
    ### zrzucenie keywords do plików
   # processTextFiles(raporty_path, raporty_keywords_path, prompt)
   # processTextFiles(fakty_path, fakty_keyword_path, prompt)
   # appendMetaDataFromFileName(raporty_path, raporty_keywords_path)
   #dane= load_keywords_from_raport_file("/home/rafal/Pobrane/pliki_z_fabryki_2/raporty_keywords/2024-11-12_report-00-sektor_C4_keywords.txt")
   #print(dane)
   #fakty = load_keywords_from_fact_file("/home/rafal/Pobrane/pliki_z_fabryki_2/facts/fakty_keywords/f01_keywords.txt")
   #print(fakty)
   raporty = load_keywords_raport_files(raporty_keywords_path)
   print_keywords_data(raporty)

   fakty = load_keywords_fact_files (fakty_keyword_path)
   print_keywords_data(fakty)

   #dla kazdego elmentu tablicy z raportami wywolaj gpt zeby zwrocil jsona z naziwskiem i imieniem
   #przeiteruj przez wszystkie elementy z tablicy z faktami i zajrzyj do klucza czy jest taki. 
   #jesli jest to zwroc fakty i doklej do wyniku...






