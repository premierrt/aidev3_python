import openai
from pathlib import Path

def get_mp3_files(directory_path: str) -> list[str]:
    """
    Zwraca listę ścieżek do plików MP3 w podanym katalogu.
    
    Args:
        directory_path (str): Ścieżka do katalogu
        
    Returns:
        list[str]: Lista ścieżek do plików MP3
        
    Raises:
        NotADirectoryError: Gdy podana ścieżka nie jest katalogiem
    """
    directory = Path(directory_path)
    
    # Sprawdzenie czy katalog istnieje
    if not directory.is_dir():
        raise NotADirectoryError(f"Ścieżka {directory_path} nie jest katalogiem")
    
    # Znalezienie wszystkich plików MP3 i zwrócenie ich ścieżek jako lista stringów
    return [str(file) for file in directory.glob("*.m4a")]

def transcribe_audio_file(file_path: str) -> str:
    """
    Dokonuje transkrypcji pliku audio przy użyciu OpenAI API.
    
    Args:
        file_path (str): Ścieżka do pliku audio
        
    Returns:
        str: Tekst transkrypcji
        
    Raises:
        FileNotFoundError: Gdy plik nie istnieje
        Exception: Gdy wystąpi błąd podczas transkrypcji
    """
    
    # Sprawdzenie czy plik istnieje
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"Plik {file_path} nie istnieje")
    
    try:
        # Otwarcie pliku audio
        with open(file_path, "rb") as audio_file:
            # Wywołanie API OpenAI do transkrypcji
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            
            # Zwrócenie tekstu transkrypcji
            return transcript.text
            
            
    except Exception as e:
        raise Exception(f"Wystąpił błąd podczas transkrypcji: {str(e)}")    

# poprawić zeby zmienilo rozszerzenie na .txt    
def save_text_to_file(file_path: str, text: str) -> None:
    """
    Zapisuje tekst do pliku.
    
    Args:
        file_path (str): Ścieżka do pliku wyjściowego
        text (str): Tekst do zapisania
        
    Raises:
        IOError: Gdy wystąpi błąd podczas zapisywania pliku
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
    except IOError as e:
        raise IOError(f"Błąd podczas zapisywania pliku: {str(e)}")


def save_all_texts_to_files(directory_path: str) -> None:
    mp3_files = get_mp3_files(directory_path)
    for file in mp3_files:
        print(file)
        text = transcribe_audio_file(file)
        print(text)
        save_text_to_file(file, text)

def read_txt_files(directory_path: str) -> str:
    """
    Wczytuje i łączy zawartość wszystkich plików .txt z podanego katalogu.
    
    Args:
        directory_path (str): Ścieżka do katalogu
        
    Returns:
        str: Połączona zawartość wszystkich plików .txt
        
    Raises:
        NotADirectoryError: Gdy podana ścieżka nie jest katalogiem
        IOError: Gdy wystąpi błąd podczas odczytu pliku
    """
    directory = Path(directory_path)
    
    # Sprawdzenie czy katalog istnieje
    if not directory.is_dir():
        raise NotADirectoryError(f"Ścieżka {directory_path} nie jest katalogiem")
    
    combined_text = []
    # Wczytanie wszystkich plików .txt
    for file_path in directory.glob("*.txt"):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                combined_text.append(content)
        except IOError as e:
            print(f"Błąd podczas odczytu pliku {file_path.name}: {str(e)}")
            continue
            
    # Łączenie tekstów z podwójnym znakiem nowej linii jako separator
    return "\n\n".join(combined_text)

def count_total_characters(text: str) -> int:
    """
    Sumuje wszystkie znaki w tekście.
    
    Args:
        text (str): Tekst do przeanalizowania
        
    Returns:
        int: Całkowita liczba znaków
    """
    return len(text)

def ask_gpt(system_prompt, question):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.5,
        messages=[{
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
#    save_all_texts_to_files("/home/rafal/Pobrane/przesluchania/")
    system_prompt_intro = "Poniżej dane dotyczące profesora Maja. Przenalizuj je dokładnie."
    zeznania = read_txt_files("/home/rafal/Pobrane/przesluchania/")
    combined_prompt = f"{system_prompt_intro}\n\n{zeznania}"
    question = "Podaj nazwę ulicy, na której znajduje się instytut, gdzie wykłada profesor Maj. Przejdź przez proces myślowy krok po kroku. Wykorzystaj swoją wiedzę, żeby znaleść odpowiedź jeśli nie jest ona jawnie podana. Okrśl najpierw miasto, poźniej uczelnie, poźniej instytu, a na konńcu ulicę na której znajduje się ten instutyt"

    print(ask_gpt(combined_prompt, question))
