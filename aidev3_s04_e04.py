from flask import Flask, request, jsonify
import logging
from aidevs3_lib_rt import *

# Ustawienie poziomu logowania na INFO
logging.basicConfig(level=logging.INFO)

system_prompt ="""
Simulate the movement of a drone across a two-dimensional 4x4 map based on user commands in natural language, determining the final position of the drone.

The initial position of the drone is at row 1, column 1, located at the upper left corner of the map. Translate user commands into movements on this grid and calculate the final landing position of the drone.

# Steps

1. Start from position [1,1].
2. Translate each user command from natural language into a directional move on the grid (e.g., "move up", "go down two spaces").
3. Apply each movement to the current position, ensuring movers stay within the bounds of the map.
4. Determine the final position of the drone.

# Output Format

Provide the final position as a coordinate pair [ column, raw]. 
Answer only with pair of coorinate pair [column, raw]


# Example

**Input:** "Move twice to the right, then down one."

**Output:** [3, 2]
"""



opis_pol_na_mapie = """
***Gol
Zamień wartość podaną przez użytkonika na opis zgodnie z poniższym mapowaniem. 
Zwróć tylko opis.

[1, 1] = znacznik
[2, 1] = trawa
[3, 1] = drzewo
[4, 1] = dom
[1, 2] = trawa
[2, 2] = wiatrak
[3, 2] = trawa
[4, 2] = trawa
[1, 3] = trawa
[2, 3] = trawa
[3, 3] = skały
[4, 3] = drzewa
[1, 4] = góry
[2, 4] = góry
[3, 4] = samochód
[4, 4] = jaskinia

Przykład:
***input: [4, 4]
***output:  jaskinia
"""


app = Flask(__name__)
def where_am_i (instruction ):
    resp_position = ask_gpt_model(system_prompt, instruction, "gpt-4o")
    logging.info("where_am_i llm odpowiedzial: %s", resp_position)

    description = ask_gpt (opis_pol_na_mapie, resp_position)
    logging.info ("Opis zwrócony przez LLM: %s", description)
    return description


@app.route('/where_am_i', methods=['POST'])
def api_where_am_i():
    data = request.get_json()  # Odbierz dane JSON z żądania
    instruction = data.get('instruction')

    if instruction is None:
        return jsonify({"error": "Instruction must be provided"}), 400

    logging.info("API _where_am_i : %s", instruction)
    description = where_am_i(instruction)
    return jsonify({"description": description})







if __name__ == '__main__':
        app.run(debug=True, port=51131)  # Zmiana portu na 8080

# curl -X POST http://127.0.0.1:51131/where_am_i -H "Content-Type: application/json" -d '{"instruction": "tutaj instrukcja gdzie poleciał dron"}'
# curl -X POST https://azyl-51131.ag3nts.org/where_am_i -H "Content-Type: application/json" -d '{"instruction": "tutaj instrukcja gdzie poleciał dron"}'


# https://azyl-51131.ag3nts.org/where_am_i
# ssh -R 51131:localhost:51131 agent11131@azyl.ag3nts.org -p 5022