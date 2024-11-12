from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "W podanym zdaniu zamień każde wystąpienie słów imię + nazwisko, nazwę ulicy + numer, miasto, wiek osoby na słowo CENZURA.\nNie możesz zmieniać składni, interpunkcji, białych znaków.\nPrzykład:\nZdanie:\nOsoba podejrzana to Andrzej Mazur. Adres: Gdańsk, ul. Długa 8. Wiek: 29 lat.\nZamień na:\nOsoba podejrzana to CENZURA. Adres: CENZURA, ul. CENZURA. Wiek: CENZURA lat."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "\nDane osoby podejrzanej: Paweł Zieliński. Zamieszkały w Warszawie na ulicy Pięknej 5. Ma 28 lat.\n"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "Dane osoby podejrzanej: CENZURA. Zamieszkały w CENZURA na ulicy CENZURA CENZURA. Ma CENZURA lat."
        }
      ]
    }
  ],
  temperature=1,
  max_tokens=2048,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  response_format={
    "type": "text"
  }
)