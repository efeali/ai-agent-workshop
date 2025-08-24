from quart import Quart, request, jsonify
import mcp_client
import direct_ollama_call
import sys

app = Quart(__name__)

ollama_host = ""
model = ""

# Enable CORS manually
@app.after_request
async def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/', methods=['GET'])
def home():
    return "nothing to see here, move along"

@app.route('/call-agent', methods=['POST'])
async def call_agent():
    try:
        # Get the JSON data from the request
        data = await request.get_json()


        # Extract the 'msg' variable from the request
        msg = data.get('msg', '')
        if not msg:
            return jsonify({"error": "No message provided"}), 400
        else:

            client_agent = await mcp_client.main( ollama_host, model)
            #client_agent = await direct_ollama_call.main(ollama_host, model)

            response = await client_agent.run(msg) # This line is for client with ReActAgent


            print(f"Response from agent: {response}")
            # Return JSON response with 'response' key and 'hello' value
            return jsonify({
            "response": str(response)
            })

    except Exception as e:
        # Handle any errors and return error response
        return jsonify({
            "error": "Invalid request",
            "message": str(e)
        }), 400

if __name__ == '__main__':


    if len(sys.argv) < 2:
        print("Usage: python main.py [ollama_host] [ollama_model]")
        print("Example: python main.py http://10.10.1.1:11434 llama3.2")
        sys.exit(1)

    ollama_host = sys.argv[1]
    model = sys.argv[2]

    app.run(debug=True, host='0.0.0.0', port=5000)

