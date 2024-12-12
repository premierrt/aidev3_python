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
Analyze following text and generate keywords to be used as meta-data for searching purpeses in other search and indexing tools. 
Please generate keyword in Polish. """ 


raporty_path = "/home/rafal/Pobrane/pliki_z_fabryki_2/"
fakty_path = raporty_path+"/fakty/"
raporty_keywords_path = raporty_path +"/raporty_keywords/"
fakty_keyword_path = fakty_path +"/fakty_keywords/"


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
        
        with open(filename, 'w', encoding='utf-8') as file:
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
  


if __name__ == "__main__" : 
    processTextFiles(raporty_path, raporty_keywords_path, prompt)
  #  processTextFiles(fakty_path, fakty_keyword_path)

