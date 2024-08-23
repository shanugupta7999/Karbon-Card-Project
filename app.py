from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from model import process  # Import the process function from model.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        # Load the JSON data from the uploaded file
        data = json.load(file)
        
        # Process the data using the model's process function
        result = process(data["data"])
        
        # Convert result to a JSON string to pass it via URL
        result_json = json.dumps(result)
        
        return redirect(url_for('result', result=result_json))

@app.route('/result')
def result():
    result = request.args.get('result', '{}')
    result_dict = json.loads(result)
    return render_template('result.html', result=result_dict)

if __name__ == '__main__':
    app.run(debug=True)
