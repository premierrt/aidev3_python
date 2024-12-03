import os
from openai import OpenAI


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



if __name__ == "__main__":
    katalog_path = "/home/rafal/Pobrane/pliki_z_fabryki/"
    pliki = get_files_by_extension( katalog_path , "mp3")
    for plik_nazwa in pliki:
        plik_sciezka =  f"{katalog_path}{plik_nazwa}"
        print(plik_sciezka)
    slownik = {}
  #  transkrypacja = process_mp3_file(testowy_mp3)
    
  #  slownik[testowy_mp3] = str_to_bool(aiFindInformation())