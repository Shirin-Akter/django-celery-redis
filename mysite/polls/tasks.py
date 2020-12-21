
from celery import shared_task
from django.conf import settings
from io import BytesIO
from PIL import Image
import os
from django.core.files import File
import string
import json
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

@shared_task
def adding_task(x, y):
    return x + y

@shared_task
def img_upload(data):
    data = json.dumps(data)
    json_object = json.loads(data)
    url = json_object['digital_ocean_url']
    name, extn = os.path.splitext(os.path.basename(url))
    # initialising bad_chars list
    bad_chars = ['"',' ','!', ':', '*','}','{']
    # # using replace() to
    # # remove bad_chars
    for i in bad_chars:
        extn = extn.replace(i, '')

    if extn in ['.jpg', '.jpeg', '.tif', '.gif']:
        data1 = name + '.png'
        return data1
    elif extn in ['.avi','.mov','.mkv','.flv', '.webm']:
        data1 = name + '.mp4'
        return data1
    else:
        return data


@shared_task
def tts():
    url = "https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/b85a7740-98a7-430b-a122-208a75c00cd7"
    apikey = "kkMD8MeGj8_EkNdbfrnwYCH9A6N6PtrQlT5ebEes3W3M"
    auth = IAMAuthenticator(apikey)
    tts = TextToSpeechV1(authenticator=auth)
    tts.set_service_url(url)
    with open('C:/Dev/speechV1.mp3', 'wb') as audiofile:
        res = tts.synthesize('Experience learning takes its cue from games as well as traditional education and can be non-linear and self-managed by the student. Deliver learning experiences via the cloud across all devices, from VR headsets to mobile phone apps, wherever your learners are.', accept='audio/mp3', voice='en-US_AllisonV3Voice').get_result()
        audiofile.write(res.content)
    return url