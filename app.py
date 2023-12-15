# let's import the flask
from flask import Flask, render_template, request, redirect, url_for
import os # importing operating system module
import re
import nltk
import json
from nltk.corpus import stopwords
from collections import Counter
from nltk.tokenize import word_tokenize

app = Flask(__name__)
# to stop caching static file
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


nltk.download('punkt')
nltk.download('stopwords')


def calculate_lexical_density(words):
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]

    total_words = len(words)
    lexical_words = sum(1 for word in filtered_words if word.isalpha())

    if total_words == 0:
        return 0
    lexical_density = (lexical_words / total_words) * 100
    return f"{lexical_density:.2f}"


@app.route('/') # this decorator create the home route
def home ():
    techs = ['HTML', 'CSS', 'Flask', 'Python']
    name = '30 Days Of Python Programming'
    return render_template('home.html', techs=techs, name = name, title = 'Home')

@app.route('/about')
def about():
    name = '30 Days Of Python Programming'
    return render_template('about.html', name = name, title = 'About Us')

@app.route('/result')
def result():
    counted_words = request.args.get('counted_words')
    words_list = json.loads(counted_words)
    return render_template('result.html', counted_words=words_list)

@app.route('/post', methods= ['GET','POST'])
def post():
    name = 'Text Analyzer'
    if request.method == 'GET':
         return render_template('post.html', name = name, title = name)
    if request.method =='POST':
        content = request.form['content']
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '',content)
        words = word_tokenize(cleaned_text)
        chars = ''.join(words)
        counted_words = Counter(words)
        tuple_words = [(key, value) for key, value in counted_words.items()]
        data = {
            'lexical_density': calculate_lexical_density(words),
            'counted_words': json.dumps(tuple_words),
            'most_frequent_word': counted_words.most_common(1)[0][0],
            'num_of_words': len(words),
            'num_of_char': len(chars)
        }
        return redirect(url_for('result', **data))