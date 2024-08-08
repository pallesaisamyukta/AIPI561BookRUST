from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/test", methods=['POST'])
def test():
    print("Received request at /test endpoint")
    return jsonify({"response": "Hello from /test endpoint"})

@app.route('/summarize', methods=['POST'])
def summarize():
    """
    API endpoint to summarize PDF text.
    Expects JSON input with 'pdf_path' as the path to the PDF file.
    Returns a JSON response with the 'summary'.
    """
    print("Received request at /summarize endpoint")
    data = request.get_json()
    pdf_path = data.get('pdf_path')
    print(f"Received request to summarize PDF: {pdf_path}")

    rust_server_url = 'http://bart_openai:3030/summarize'  # Adjust if Rust server is running on a different port or IP

    try:
        print("making req")
        # Make a request to the Rust server
        rust_response = requests.post(rust_server_url, json={'pdf_path': pdf_path})
        print("rust rep")
        if rust_response.status_code == 200:
            summary = rust_response.json().get('summary', '')
            formatted_summary = summary.replace('<|eot_id|>', '').replace('. ', '.\n').strip()
            print(f"Generated summary for {pdf_path}:\n{formatted_summary}")
            return jsonify({'summary': formatted_summary})
        else:
            error_message = rust_response.json().get('error', 'Unknown error')
            print(f"Error from Rust server: {error_message}")
            return jsonify({'error': error_message}), rust_response.status_code
    except Exception as e:
        print(f"Error during communication with Rust server: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
