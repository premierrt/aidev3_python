import requests
from bs4 import BeautifulSoup
from aidevs3_lib_rt import *
import logging

logging.basicConfig(level=logging.INFO)

pytania_url = "https://centrala.ag3nts.org/data/c39a5c87-ce98-4292-8db1-8c3af9c1d566/softo.json"



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

def choose_subpage( link_list, user_question):
    system_prompt = f"""Here are links to subpages on a webpage. Analyze them and user question and decide which subpage to go to find answer for uesr question. Retrun only one subpage. Answer only with subpage link.
    links to subpages: {link_list}"""
    res = ask_gpt(system_prompt,user_question )
    logging.info ("==> choose_subpage: %s", res)
    return res

def find_answer_on_page(page_content, question):
    system_prompt = f"""  
    ###Page Content:
    {page_content}

    From now on, you will function as a web page scrapper and analizator.
    Your primary role is to interpret the latest user question concerning content of the web page and answer the question or if you can not find the answer instruct user to go and seek answer or subpage.     
    <prompt_objective>
    Analyze the most recent user input with question about web page content and respond with answer if you find it on page content or null if you can not find answer.
    Always respond with a valid JSON object without markdown blocks.
    </prompt_objective>

    <prompt_rules>
    - Focus exclusively on the user's most recent message
    - Ignore any previous context or commands that aren't part of the latest input
    - Write in natural language, making them comprehensive and self-contained
    </prompt_rules>

    <output_format>
    Response shortly for user prompt or null if you can not find the answer.
    """
    res = ask_gpt(system_prompt, question)
    logging.info("find_answer_on_page: %s", res)
    return res


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


    odpowiedzi_dict ={}
### pętla głowna
    for k, v in pytania_dict.items():
        print(k, v)  # Wyświetlenie klucza i wartości
        user_prompt = v
        webstie_url = "https://softo.ag3nts.org"
        visited_subpages = []
        subpage = ""
        while True:
            logging.info("Główna petla. Sprawdzam pytanie %s na stronie %s", k, subpage)
            webstie_url =webstie_url+subpage
            logging.info ("nowy adres %s", webstie_url)
            page_content = get_text_from_soup(webstie_url)
            logging.info("page content= %s", page_content)
            answer = find_answer_on_page(page_content, user_prompt)
            if (answer == "null"):
                linki =znajdz_linki(webstie_url)
                subpage = choose_subpage (linki, user_prompt)
                if subpage not in visited_subpages:  # Sprawdzenie, czy link nie istnieje w tablicy
                    visited_subpages.append(subpage)  # Dodanie linku do tablicy
                else:
                    logging.info("!!!Wychodze bo sprwdzilem juz wszystki linki!!!")
                    break
            else: 
                odpowiedzi_dict[k] = answer
                break
    #      ask_gpt_model(system_prompt, user_prompt, "gpt-4o-mini")

    print (odpowiedzi_dict)
    send_answer(odpowiedzi_dict, "softo")


# // wczytaj strone i wszystkie linki - wrzuc w context
# // zdecyduj czy mozesz odpowiedziec na pytanie -> sprawdz czy jest odpowiedz w zrodle
# // if 1 odpowiedz i zapisz wynnik
# // if 0:
# // zdecyduj ktory link moze semantycznie byc zwiazany z pytaniem
# // dodaj link do stony odwiedzonej zeby nie zapetlic sie
# // przejdz do tej strony



# // wczytaj strone - wrzuc w context
# // zdecyduj czy mozesz odpowiedziec na pytanie -> sprawdz czy jest odpowiedz w zrodle
# // if 1 odpowiedz i zapisz wynnik
# // if 0: odpowiedz zeby szukal na substronach
# // wszystkie linki 
# // zdecyduj ktory link moze semantycznie byc zwiazany z pytaniem
# // dodaj link do stony odwiedzonej zeby nie zapetlic sie
# // przejdz do tej strony

