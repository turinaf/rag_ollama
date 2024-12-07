from flask import Flask, request, jsonify, render_template
from query import query  # Assuming your existing code is in query.py

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query_api():
    data = request.json
    query_text = data.get('query')
    if not query_text:
        return jsonify({'error': 'No query provided'}), 400
    
    response = query(query_text)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)