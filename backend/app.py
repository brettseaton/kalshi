from flask import Flask, jsonify
from kalshi_markets import runthis
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/get-markets": {"origins": "http://localhost:3000"}})

@app.route('/get-markets', methods=['GET'])
def get_markets():
    data = runthis()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)


