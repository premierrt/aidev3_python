import requests
from bs4 import BeautifulSoup
from aidevs3_lib_rt import *
import logging

pytania_url = "https://centrala.ag3nts.org/data/c39a5c87-ce98-4292-8db1-8c3af9c1d566/softo.json"
webstie_url = "https://softo.ag3nts.org"


def pobierz_pytania(pytania_url):
    try:
        res = requests.get(pytania_url)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Wyspil wyjatek: {e} ")
        return ""
    

def znajdz_linki(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Wyszukiwanie wszystkich linków 
    links = []
    for a_tag in soup.find_all('a', href=True):  # Znajdź wszystkie tagi <a> z atrybutem href
        href = a_tag['href']
        if href != "/":
            links.append(href)
    # Usunięcie duplikatów
    links = list(set(links))
    return links

def plan():
    return ""

def execute():
    return ""

def get_text_from_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    """Zwraca sam tekst z obiektu soup."""
    return soup.get_text(separator=" ", strip=True)  # Usuwa białe znaki na początku i końcu

if __name__ == "__main__":
    
    pytania_dict = pobierz_pytania(pytania_url)
    
    
    # links = znajdz_linki()# Wyświetlenie znalezionych linków
    # for link in links:
    #     print(link)

    # ile =num_tokens_from_string("dupa srala i piredziala")
    # print (ile)


### pętla głowna
    for k, v in pytania_dict.items():
        print(k, v)  # Wyświetlenie klucza i wartości
        user_prompt = v
    #      ask_gpt_model(system_prompt, user_prompt, "gpt-4o-mini")
    print( get_text_from_soup(webstie_url+"/kontakt") )

# // wczytaj strone i wszystkie linki - wrzuc w context
# // zdecyduj czy mozesz odpowiedziec na pytanie -> sprawdz czy jest odpowiedz w zrodle
# // if 1 odpowiedz i zapisz wynnik
# // if 0:
# // zdecyduj ktory link moze semantycznie byc zwiazany z pytaniem
# // dodaj link do stony odwiedzonej zeby nie zapetlic sie
# // przejdz do tej strony


