from flask import Flask, request

app = Flask(__name__)

@app.route('/reverse', methods=['POST'])
def reverse_string():
    data = request.get_json()
    input_str = data['string']
    reversed_str = input_str[::-1]
    return {'reversed_string': reversed_str}


if __name__ == '__main__':
    app.run(debug=True)
