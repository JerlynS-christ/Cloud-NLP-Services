# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.




from flask import Flask, render_template, request,url_for
from flask_cors import cross_origin
import boto3

import google.auth
from google.cloud import translate

app = Flask(__name__)

SOURCE, TARGET = ('en', 'English'), ('es', 'Spanish')

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/sound", methods = ["GET", "POST"])
@cross_origin()
def sound():
    if request.method == "POST":
        text = request.form['texttotranslate']  
        sourcelanguage = request.form['sourcelanguage']
        targetlanguage = request.form['targetlanguage']
        translate = boto3.client(service_name='translate',region_name='us-east-1') 

        result = translate.translate_text(Text=text, SourceLanguageCode=sourcelanguage,TargetLanguageCode=targetlanguage)

        #translated = open("translated.txt","w+")
        #translated.write(str(result["TranslatedText"]))
        text = result['TranslatedText']
        polly = boto3.client(service_name='polly',region_name='us-east-1')  
        response = polly.synthesize_speech(OutputFormat='mp3', VoiceId='Brian',Text=text)
        file = open('static/speech.mp3', 'wb')
        file.write(response['AudioStream'].read())
        file.close()
        audiospeech=True

    return render_template("index.html",conversion=result['TranslatedText'],audiospeech=audiospeech)

@app.route("/sound1", methods = ["GET", "POST"])
@cross_origin()
def sound1():
    if request.method == "POST":
        
        # sourcelanguage = request.form['en']
        # targetlanguage = request.form['en']

        #translated = open("translated.txt","w+")
        #translated.write(str(result["TranslatedText"]))
        text = request.form['texttotranslate']  
        polly = boto3.client(service_name='polly',region_name='us-east-1')  
        response = polly.synthesize_speech(OutputFormat='mp3', VoiceId='Brian',Text=text)
        file = open('static/speech.mp3', 'wb')
        file.write(response['AudioStream'].read())
        file.close()
        audiospeech=True

    return render_template("index3.html",audiospeech=audiospeech)


@app.route("/sentiment", methods = ["GET", "POST"])
@cross_origin()
def sentiment():
    if request.method == "POST":
        text = request.form['sentimenttext']  
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

        result = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        return render_template("index2.html",result=result['Sentiment'])
    else:
        return render_template("index2.html")


@app.route('/index', methods=['GET', 'POST'])
def translate(gcf_request=None):
    """
    main handler - show form and possibly previous translation
    """

    # Flask Request object passed in for Cloud Functions
    # (use gcf_request for GCF but flask.request otherwise)
    local_request = gcf_request if gcf_request else request

    # reset all variables (GET)
    text = translated = None

    # form submission and if there is data to process (POST)
    if local_request.method == 'POST':
        text = local_request.form['text'].strip()
        if text:
            data = {
                'contents': [text],
                'parent': PARENT,
                'target_language_code': TARGET[0],
            }
            # handle older call for backwards-compatibility
            try:
                rsp = TRANSLATE.translate_text(request=data)
            except TypeError:
                rsp = TRANSLATE.translate_text(**data)
            translated = rsp.translations[0].translated_text

    # create context & render template
    context = {
        'orig':  {'text': text, 'lc': SOURCE},
        'trans': {'text': translated, 'lc': TARGET},
    }
    return render_template('index.html', **context)


@app.route('/index2', methods=['GET', 'POST'])
def index2(gcf_request=None):
    """
    main handler - show form and possibly previous translation
    """

    # Flask Request object passed in for Cloud Functions
    # (use gcf_request for GCF but flask.request otherwise)
    local_request = gcf_request if gcf_request else request

    # reset all variables (GET)
    text = translated = None

    # form submission and if there is data to process (POST)
    if local_request.method == 'POST':
        text = local_request.form['text'].strip()
        if text:
            data = {
                'contents': [text],
                'parent': PARENT,
                'target_language_code': TARGET[0],
            }
            # handle older call for backwards-compatibility
            try:
                rsp = TRANSLATE.translate_text(request=data)
            except TypeError:
                rsp = TRANSLATE.translate_text(**data)
            translated = rsp.translations[0].translated_text

    # create context & render template
    context = {
        'orig':  {'text': text, 'lc': SOURCE},
        'trans': {'text': translated, 'lc': TARGET},
    }
    return render_template('index2.html', **context)

@app.route('/index3', methods=['GET', 'POST'])
def index3(gcf_request=None):
    """
    main handler - show form and possibly previous translation
    """

    # Flask Request object passed in for Cloud Functions
    # (use gcf_request for GCF but flask.request otherwise)
    local_request = gcf_request if gcf_request else request

    # reset all variables (GET)
    text = translated = None

    # form submission and if there is data to process (POST)
    if local_request.method == 'POST':
        text = local_request.form['text'].strip()
        if text:
            data = {
                'contents': [text],
                'parent': PARENT,
                'target_language_code': TARGET[0],
            }
            # handle older call for backwards-compatibility
            try:
                rsp = TRANSLATE.translate_text(request=data)
            except TypeError:
                rsp = TRANSLATE.translate_text(**data)
            translated = rsp.translations[0].translated_text

    # create context & render template
    context = {
        'orig':  {'text': text, 'lc': SOURCE},
        'trans': {'text': translated, 'lc': TARGET},
    }
    return render_template('index3.html', **context)

@app.route("/services")
def services():
    return render_template('services.html')

if __name__ == '__main__':
    import os
    app.run(debug=True, threaded=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))


