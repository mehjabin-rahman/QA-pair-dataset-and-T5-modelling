import csv
import difflib

from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# Load the CSV data
with open('updated_dataset.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Define home page
@app.route('/')
def home():
    return render_template('index.html')

# Define function to generate answer to user question
def generate_answer(question, context):
    # Find matching row based on context and question
    match_rows = []
    for row in data:
        if context.lower() in row['context'].lower() and difflib.SequenceMatcher(None, question.lower(), row['question'].lower()).ratio() > 0.8:
            match_rows.append(row)

    # Return the answer(s)
    if match_rows:
        return [row['answer'] for row in match_rows], []
    else:
        return None, []

# Define answer endpoint
@app.route('/answer', methods=['POST'])
def answer():
    question = request.form['question']
    context = request.form['context']
    answer, top_5_sentences = generate_answer(question, context)
    return render_template('templates/index.html', answer=answer, top_5_sentences=top_5_sentences)

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
