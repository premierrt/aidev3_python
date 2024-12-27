from aidevs3_lib_rt import *


if __name__ =="__main__":
    foty = ['IMG_559_NRR7.PNG', 'IMG_1410_FXER.PNG', 'IMG_1443_FT12.PNG']
    url = 'https://centrala.ag3nts.org/dane/barbara/'
    foty_url = [url + file for file in foty]

    print(foty_url)
#    Przeanlizuj przesłane zdjęcia dokładnie. Zwróć uwagę na szczegóły osoby na zdjęciu. Na jej wygląd, cechy wyglądu, ubioru, znaki szczególne.

    user_prompt="""
    Sporządź rysopis osób na zdjęciach. 
    
    """

    rysopis= analyze_image_list_url(foty_url, user_prompt)
    print(rysopis)

    send_answer(rysopis, "photos")

    

