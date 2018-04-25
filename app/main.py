from flask import Flask
from . import char_rnn
import random
app = Flask(__name__)

import os
import sys

import twitter
api = twitter.Api(consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
                  consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
                  access_token_key=os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
                  access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

@app.route('/')
def hello_world():
    tp = os.path.dirname(os.path.realpath(__file__))
    with open(tp + '/trump.txt', 'r') as fp:
        txt = fp.read()
    with open(tp + '/speech.txt') as f:
        htxt = f.read()
    total = len(htxt.split("."))
    r_num = random.randrange(0, total)
    # refer to the model downloaded from the Dockerfile
    cnn = "".join(char_rnn.infer(txt, ckpt_name=tp+'/trump.ckpt', n_iterations=100))
    h = htxt.split(".")[r_num].strip('\n') 
    result = (h[0:3]+ " " + cnn.lstrip() + h[3::])[0:130] + ' #CADL'
    try:
      api.PostUpdate(result)
    except:
       result = 'TWEET IS RATE LIMITED: ' + result
    return result
if __name__ == '__main__':
    app.run()
