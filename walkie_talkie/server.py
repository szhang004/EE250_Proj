from flask import Flask, request, jsonify
import openai

openai.api_key = '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'


app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def receive_data():
    # Check if the request contains JSON data
    if request.is_json:
        # Get JSON data from the request
        data = request.get_json()
        
        # Log the received data (or process it as needed)
        print(data)
        
        # Send a response back to the client
        return jsonify({"message": "Data received successfully"}), 200
    else:
        return jsonify({"message": "Request does not contain JSON data"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)