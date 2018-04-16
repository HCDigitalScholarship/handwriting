from myscript_keys import *
import hmac
import hashlib
import base64

import json
import requests
import time
from json import dumps

#message = bytes(application_key).encode('utf-8')
#secret = bytes(HMAC_key).encode('utf-8')

#myscript_url = 'https://webdemoapi.myscript.com/api/v3.0/recognition/rest/text/languages.json?'
myscript_url = 'https://webdemoapi.myscript.com/api/v3.0/recognition/rest/text/doSimpleRecognition.json?'
#myscript_url = 'https://webdemoapi.myscript.com/api/v3.0/recognition/ws/text'
#myscript_url = 'https://webdemoapi.myscript.com//api/v3.0/recognition/rest/text/contenttypes.json?'

#signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
#print(signature)
#
# Download Tweets from a user profile
#
def myscript():

    # api_url  = myscript_url +'applicationKey=%s&inputMode=CURSIVE' % (application_key)
    #api_url = myscript_url +'applicationKey=%s' % (application_key)
    api_url = myscript_url
    print (api_url)
    textInput = {
        "textParameter":{
            "language":"en_US",
           "textInputMode":"CURSIVE"
          },
        "inputUnits":[
           {
               "textInputType":"MULTI_LINE_TEXT",
              "components":[
                 {
                     "type":"stroke",
                     
                    "x":[375.0, 375.0, 42.6, 42.64, 41.98, 41.03, 40.32, 39.85, 0.0, 252.9, 254.82, 257.19, 257.66, 258.86],
                   "y":[0.0, 88.0, 88.0, 87.23, 86.59, 86.62, 87.08, 88.0, 88.0, 21.22, 21.62, 23.01, 25.06, 31.29]
                 }
                   
                   ]
                 }             
             ]
              
           }


    obj = {
       'applicationKey': application_key,
       'hmac': HMAC_key,
       'textInput': json.dumps(textInput)
   }

    # send request to Twitter
    #print json.dumps(textInput)
    response = requests.post(api_url, params=obj)
    print(response.status_code)
    print(response.url)

    if response.status_code == 200:

        content = json.loads(response.content)
        #print "HERE"
        #print content
        return content

    return None


# get a list of Tweets
results = myscript()

if results is not None:
    print("results is not NONE")
    print(json.dumps(results, indent=4, sort_keys=True))
    # loop over each Tweet and print the date and text
    #for line in results:

    #{"result":{ "textSegmentResult":{"selectedCandidateIdx":0,"candidates":[{"label":"a","normalizedScore":1.0,"resemblanceScore":0.9970794,"children":[]}},"instanceId":"9232b0ea-16d5-41fb-93e0-50fe99c0b70a"


else:
    
    print('[*] Error.')