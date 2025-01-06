from PyPDF2 import PdfReader
import fitz  # PyMuPDF
from aidevs3_lib_rt import * 
from io import BytesIO
from PIL import Image
import base64
import requests


pdf_file_name = "notatnik-rafala.pdf"

def  ocr_pdf ():
    reader = PdfReader(pdf_file_name)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    print(text)
    return text;


def get_image_from_pdf ():
    # Open the PDF file
    pdf_file = pdf_file_name
    doc = fitz.open(pdf_file)

    # Specify the page number (0-based index)
    page_number = 18  # For example, page 3
    page = doc[page_number]

    # Render the page as a pixmap (image representation)
    pix = page.get_pixmap()

    # Convert pixmap to an image using PIL
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Save image to a BytesIO buffer
    buffer = BytesIO()
    image.save(buffer, format="PNG")  # Save as PNG
    buffer.seek(0)

    # Convert image bytes to Base64
    image_bytes = buffer.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    #print("Base64 Representation of Entire Page:")
    #print(image_base64)

    doc.close()
    return image_base64


def zapisz_strone_jako_obraz(pdf_path, page_number, output_path="obraz.png"):
    """
    Renderuje całą stronę PDF jako obraz i zapisuje do pliku.

    :param pdf_path: Ścieżka do pliku PDF.
    :param page_number: Numer strony (0-based index).
    :param output_path: Ścieżka do zapisu obrazu (domyślnie 'obraz.png').
    """
    try:
        # Otwórz plik PDF
        doc = fitz.open(pdf_path)

        # Pobierz stronę
        page = doc[page_number]

        # Renderuj stronę jako pixmapę (obraz w pamięci)
        pix = page.get_pixmap()

        # Konwertuj pixmapę na obraz PIL
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Zapisz obraz do pliku
        image.save(output_path, format="PNG")
        print(f"Strona {page_number + 1} zapisana jako {output_path}")

        # Zamknij dokument PDF
        doc.close()

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

    



def fetch_json_from_url(url):
    try:
        response = requests.get(url)  # Wykonaj zapytanie GET
        response.raise_for_status()  # Sprawdź, czy wystąpił błąd HTTP
        return response.json()  # Zwróć odpowiedź jako obiekt JSON
    except requests.exceptions.RequestException as e:
        print(f"Wystąpił błąd: {e}")
        return None  # Zwróć None w przypadku błędu


if __name__ == "__main__":
    ocr = ocr_pdf()
    image_prompt = "Przeanalizuj dokładnie obraz. Opisz co na nim jest"
    b64_image = get_image_from_pdf()
  #  resp_image_note = analyze_image_base64(b64_image, image_prompt)
    resp_image_note =""
    print (resp_image_note)
   # zapisz_strone_jako_obraz(pdf_file_name, 18)
   # print (image_prompt)

#     # Przykład użycia
    url = "https://centrala.ag3nts.org/data/c39a5c87-ce98-4292-8db1-8c3af9c1d566/notes.json"
    json_data = fetch_json_from_url(url)


    content_string = "Context: "+ ocr + resp_image_note
    
    prompt = " /n Przeanalizuj dokładnie tekst: " + content_string + "Uwzględnij wszystkie fakty podane w tekście, w szczególnosci odwołania do wydarzeń.  Wykorzystaj wiedzę z tego tekstu oraz powiąż ją z ogólną wiedzą którą posiadasz, żeby odpowiedzieć na pytanie użytkownika. Jeśli pytania dotyczy daty przy szukaniu odpowiedzi uwzględnij względne odwołania do dat/ wydarzeń występujące w tekście.  "
    ##cache
    system_prompt=  content_string + prompt

    if json_data is not None:
        print(json_data)  # Wyświetli pobrany JSON

    for key, value in json_data.items():
         print(f'Klucz: {key}, Wartość: {value}')
         resp_gpt = ask_gpt_model(system_prompt, value, "gpt-4o")
         print (resp_gpt)