from flask import Flask, request, jsonify
from flask_cors import CORS
from TodoAgent import TodoAgent

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to allow React frontend to communicate

@app.route('/', methods=['GET'])
def home():
    return "nothing to see here, move along"

@app.route('/call-agent', methods=['POST'])
def call_agent():
    try:
        # Get the JSON data from the request
        data = request.get_json()


        # Extract the 'msg' variable from the request
        msg = data.get('msg', '')
        if not msg:
            return jsonify({"error": "No message provided"}), 400
        else:

            agent = TodoAgent()
            response = agent.run(msg)
            # Return JSON response with 'response' key and 'hello' value
            return jsonify({
                "response": response
            })

    except Exception as e:
        # Handle any errors and return error response
        return jsonify({
            "error": "Invalid request",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
