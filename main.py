import requests
from bs4 import BeautifulSoup
import spacy

from flask import Flask, request
import json


nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def main():
  if request.method == 'POST':
    try:
      url  = request.json['url']
      page = requests.get(url=url)
      soup = BeautifulSoup(page.content, "html")

      for script in soup(["script", "style"]):
        script.decompose()    # rip it out

      text  = soup.get_text()

      doc   = nlp(text)

      lines = [token.lemma_.lower()
                 for token in doc 
                 if token.is_alpha is True 
                 and token.is_stop is not True 
                 and token.is_digit is not True]

      return json.dumps(len(lines))
    except:
      return json.dumps({'trace': traceback.format_exc()})

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)