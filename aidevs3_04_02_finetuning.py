import json
import logging
from aidevs3_lib_rt import *


# Ustawienie poziomu logowania na INFO
logging.basicConfig(level=logging.INFO)

def convert_data_to_ml(data_string, classifcation_result):
    # Tworzenie struktury danych
    data = {
        "messages": [
            {"role": "system", "content": "Classify data"},
            {"role": "user", "content": data_string},
            {"role": "assistant", "content": classifcation_result}
        ]
    }
  #  logging.info("####convert_data_to_json: %s", data)  # Użycie %s do formatowania
    return json.dumps(data)


def przerob_plik(file_name, file_name_output, classifcation_result):
    correct_file = read_file_content_line(file_name)
    with open(file_name_output, 'w') as output_file:  # Otwórz plik do zapisu
        for line in correct_file:
            line = line.strip()  # Usunięcie znaku nowej linii i białych znaków
            logging.info("linia: %s", line)
            linia_json = convert_data_to_ml(line, classifcation_result)
            output_file.write(linia_json + '\n')  # Zapisz linia_json do pliku




if __name__ == "__main__":

    # przerob_plik ("correct.txt", "correct_ml.txt", "1")
    # przerob_plik ("incorrect.txt", "incorrect_ml.txt", "0")

    dane_testowe = read_file_content_line("verify.txt")
    result = {}
    for linia in dane_testowe:
        linia = linia.strip()
        key, value = linia.split("=")
        result[key] =value

    print (result)

    system_prompt = "Classify data "
    model= "moj_model_fine_tuned"

    corect_dasta = []
    for key, value in result.items():
        print (key, value)
        res = ask_gpt_json_format_model(system_prompt, value,model)
        print (res)
        if (res == "1"):
            corect_dasta.append(key)

    send_answer(corect_dasta, "research")