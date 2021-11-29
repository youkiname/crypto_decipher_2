from flask import Flask, request, jsonify, abort
from decipher import calculate_key_length, calculate_offsets, decipher, get_matrix, ALPH
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def web_controller(text: str, custom_key: str) -> dict:
    key_length, indices_of_coincidence = calculate_key_length(text)
    matrix = get_matrix(text, key_length)
    offsets = calculate_offsets(text, key_length)
    presumptive_key = "".join([top_char for top_char, offset in offsets])
    key = custom_key or presumptive_key
    decipher_text = decipher(text, key)
    return {
        "decipherText": decipher_text,
        "presumptiveKey": presumptive_key,
        "usedKey": key,
        "presumptiveOffsets": offsets,
        "indicesOfCoincidence": indices_of_coincidence,
        "matrix": matrix
    }


@app.route("/c2/api/")
def api():
    text = request.args.get("text", default="")
    key = request.args.get("key", default=None)
    if not text:
        abort(400, "text is required param.")
    return jsonify(web_controller(text, key))


@app.route("/c2/form/", methods=['POST', "GET"])
def home():
    decipher_text = ""
    text = ""
    used_key = ""
    if request.method == 'POST':
        text = request.form.get('text', default="")
        key = request.form.get('key', default=None)
        result = web_controller(text, key)
        decipher_text = result['decipherText']
        used_key = result['usedKey']
    return f"<form method='POST'><textarea name='text' value='{text}'>{text}</textarea><br><input name='key'></input><button type='submit'>Submit</button></form><p>{decipher_text}</p><p>{used_key}</p>"


if __name__ == "__main__":
    app.run("localhost", port=8779)
