import base64
from openai import OpenAI
from PIL import Image
import io
from pathlib import Path


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
                         "text": "Obraz przedstawi fragment mapy miasta. Zwróc uwagę na nazwy ulicy, przystanki komunikacji miejskiej ich lokalizację, linie kolejowe, stacje kolejowe, obiekty architektury miejskiej, skrzyżowania dróg. Opisz co widzisz na tym obrazie uwzględniając moje wskazówki dotyczące obrazu."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}" 
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Wystąpił błąd: {str(e)}"


def find_png_files(directory_path):
    """
    Funkcja znajduje wszystkie pliki PNG w podanym katalogu
    
    Args:
        directory_path (str): Ścieżka do przeszukiwanego katalogu
    
    Returns:
        list: Lista ścieżek do znalezionych plików PNG
    """
    try:
        # Konwertujemy ścieżkę na obiekt Path
        directory = Path(directory_path)
        
        # Znajdujemy wszystkie pliki .png i konwertujemy je na stringi
        png_files = [str(file) for file in directory.glob("**/*.png")]
        
        return png_files
        
    except Exception as e:
        print(f"Wystąpił błąd: {str(e)}")
        return []


def save_list_to_file(string_list: list[str], file_path: str) -> None:
    """
    Zapisuje listę stringów do pliku tekstowego.
    
    Args:
        string_list (list[str]): Lista stringów do zapisania
        file_path (str): Ścieżka do pliku wyjściowego
        
    Raises:
        IOError: Gdy wystąpi błąd podczas zapisywania pliku
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            # Zapisuje każdy string w nowej linii
            for line in string_list:
                file.write(f"{line}\n")
    except IOError as e:
        raise IOError(f"Błąd podczas zapisywania pliku: {str(e)}")


def analyze_all_images_in_directory(directory_path: str) -> list[str]:
    """
    Analizuje wszystkie pliki PNG w podanym katalogu i zwraca listę opisów.
    
    Args:
        directory_path (str): Ścieżka do katalogu z plikami PNG
        
    Returns:
        list[str]: Lista opisów obrazów zwróconych przez OpenAI
    """
    # Znajdź wszystkie pliki PNG
    lista_plikow = find_png_files(directory_path)
    
    # Lista na odpowiedzi AI
    ai_responses_opis_rysunkow = []
    
    # Analizuj każdy plik
    for plik in lista_plikow:
        print(f"Analizuję plik: {plik}")
        ai_responses_opis_rysunkow.append(analyze_image(plik))
    
    return ai_responses_opis_rysunkow


def ask_gpt(system_prompt, question):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.1,
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


def read_file_to_string(file_path: str) -> str:
    """
    Wczytuje zawartość pliku tekstowego do stringa.
    
    Args:
        file_path (str): Ścieżka do pliku wejściowego
        
    Returns:
        str: Zawartość pliku jako string
        
    Raises:
        IOError: Gdy wystąpi błąd podczas odczytu pliku
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Błąd podczas odczytu pliku: {str(e)}")

# Przykład użycia:
if __name__ == "__main__":
    output_file = "opisy_obrazow.txt"
    should_analyze = True

    # Sprawdź czy plik istnieje
    try:
        if Path(output_file).exists():
            # Sprawdź czy plik jest pusty
            if Path(output_file).stat().st_size > 0:
                should_analyze = False
                print(f"Plik {output_file} już istnieje i nie jest pusty.")
    except Exception as e:
        print(f"Błąd podczas sprawdzania pliku: {str(e)}")

    # Wykonaj analizę tylko jeśli plik nie istnieje lub jest pusty
    if should_analyze:
        image_path = "/home/rafal/Pulpit/vision_ai"
        opisy = analyze_all_images_in_directory(image_path)
        save_list_to_file(opisy, output_file)
        print(f"Zapisano opisy do pliku {output_file}")
    else:
        conxtext = read_file_to_string(output_file)
        print(conxtext)
        system_prompt_intro = "Poniżej znajdziesz opis czterech fragmentów map miasta."
        combined_prompt = f"{system_prompt_intro}\n\n{conxtext}"

        question = """ 
        
        Podaj nazwę miasta w polsce w którym występują te ulice, skrzyżowani i inne obiekty z danych? W tym mieście występują też spichlerze i twierdze.

        """
        print(ask_gpt(combined_prompt, question))

