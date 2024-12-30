from flask import Flask, request, jsonify

app = Flask(__name__)
def where_am_i (instruction ):
    description = "to jest jakis opis z LLM"
    return description


@app.route('/where_am_i', methods=['POST'])
def api_where_am_i():
    data = request.get_json()  # Odbierz dane JSON z żądania
    instruction = data.get('instruction')

    if instruction is None:
        return jsonify({"error": "Instruction must be provided"}), 400

    description = where_am_i(instruction)
    return jsonify({"description": description})

if __name__ == '__main__':
        app.run(debug=True, port=8080)  # Zmiana portu na 8080

# curl -X POST http://127.0.0.1:8080/where_am_i -H "Content-Type: application/json" -d '{"instruction": "tutaj instrukcja gdzie poleciał dron"}'