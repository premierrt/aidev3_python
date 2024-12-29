import requests



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
    

pytania_dict = pobierz_pytania(pytania_url)
print(pytania_dict.get("01"))