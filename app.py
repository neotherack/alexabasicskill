from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/")

def get_headlines(sep):
  user_pass_dict = {'user': 'USERNAME',
                    'passwd': 'PASSWORD',
                    'api_type': 'json'}

  sess = requests.Session()
  sess.headers.update({'User-Agent': 'Alexa test'})
  sess.post('https://www.reddit.com/api/login', data=user_pass_dict)
  time.sleep(2)

  url = 'https://reddit.com/r/worldnews/.json?limit=4'
  html = sess.get(url)
  data = json.loads(html.content.decode('utf-8'))
  titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
  titles = sep.join([i for i in titles])
  return titles


@app.route("/")
def homepage():
  return get_headlines('\n')

@ask.launch
def start_skill():
  hi = 'Hola! dime si o no?'
  return question(hi)


@ask.intent("YesIntent")
def share_headlines():
  headlines = get_headlines('... ')
  headline_msg = 'Estas son las lineas {}'.format(headlines)
  return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
  bye_text = 'hasta luego moreno!'
  return statement(bye_text)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5443)
