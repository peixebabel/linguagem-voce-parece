# -*- coding: utf-8 -*-
"""github-stereotype-public.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tiDBoKgM65dsZaGauCSpInohoVOUDSqX

#### Imports
"""

import urllib.request
import re, pickle, os, json, sys
import numpy as np

from PIL import Image
import requests
from skimage import io

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
#from django.core.management import execute_from_command_line
#execute_from_command_line(sys.argv)

"""#### Code"""

KEY = os.environ['FACE_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['FACE_ENDPOINT']
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def dict_face(detected_faces, url):
  att_dict = {'face': True}
  for face in detected_faces: 
    att_dict['url'] = str(url)
    att_dict['age'] = int(face.face_attributes.age)
    att_dict['gender'] = str(face.face_attributes.gender).split('.')[-1]
    att_dict['smile'] = float(face.face_attributes.smile)
    att_dict['facial_hair'] = face.face_attributes.facial_hair.__dict__
    att_dict['glasses'] = str(face.face_attributes.glasses).split('.')[-1]
    att_dict['emotion'] = face.face_attributes.emotion.__dict__
    att_dict['bald'] = float(face.face_attributes.hair.bald)
    att_dict['hair_color'] = [(str(hair.color).split('.')[-1], float(hair.confidence)) for hair in face.face_attributes.hair.hair_color] 
    att_dict['makeup'] = face.face_attributes.makeup.__dict__

  return att_dict

def get_face(url):
	single_image_name = os.path.basename(url)
	face_attributes = ['age', 'gender', 'smile', 'facialHair', 'glasses', 'emotion', 'hair', 'makeup']
	try:
		detected_faces = face_client.face.detect_with_url(url=url, return_face_attributes=face_attributes)
		if not detected_faces:
			return {'face': False}
			# raise Exception('No face detected from image {}'.format(single_image_name))
	except:
		return {'face': False}
	
	return dict_face(detected_faces, url)

emocoes = {'anger': 'Raiva', 'contempt': 'Desprezo', 'disgust': 'Nojo', 'fear': 'Medo',
           'happiness': 'Felicidade', 'neutral': 'Neutro', 'sadness': 'Tristeza', 'surprise': 'Surpresa'}

gender = {'male':0, 'female':1}
glasses = {'no_glasses': 0, 'reading_glasses':1, 'sunglasses': 2, 'swimming_goggles':3}
emotions = {'Desprezo': 7,'Felicidade': 1,'Medo': 6,'Neutro': 2,'Raiva': 4,'Surpresa': 3,'Tristeza': 5,np.nan: 0}
color = {'brown':0, 'black':1, 'blond':2, 'gray':3, 'other':4, 'red':5}

def att2feat(att):
  row = {}

  row['Idade'] = att['age']
  row['Gênero'] = gender[att['gender']]
  row['Sorriso'] = att['smile']

  bigode, barba, costeleta = att['facial_hair']['moustache'], att['facial_hair']['beard'], att['facial_hair']['sideburns'] 
  row['Pêlos Faciais'] = (bigode + barba + costeleta)/3.0
  row['Bigode'] = (bigode)
  row['Barba'] = (barba)
  row['Costeleta'] = (costeleta)

  row['Óculos'] = glasses[att['glasses']]
  keys, values = list(att['emotion'].keys())[1:], list(att['emotion'].values())[1:]
  emotion = keys[np.argmax(values)] 
  row['Emoção'] = emotions[emocoes[emotion]] 

  row['Careca'] = att['bald']
  if len(att['hair_color']) > 0:
    row['Cor de cabelo'] = color[max(att['hair_color'],key=lambda item:item[1])[0]]
  else: row['Cor de cabelo'] = 0
  
  row['Maquiagem'] = (att['makeup']['eye_makeup'] + att['makeup']['lip_makeup'])/2.0

  row = pd.Series(row)
  return np.array(row.values)

import anvil.server
anvil.server.connect(os.environ['ANVIL_KEY'])

with open('bayes_model.pkl', 'rb') as fp:
  clf = pickle.load(fp)

with open('linguagens.txt', 'r') as fp:
  linguagens = json.loads(fp.read())

@anvil.server.callable
def run(url):
  face = get_face(url)
  img = io.imread(url)

  if face['face'] == False:
    return img, face, None
  
  feat = att2feat(face)

  probs  = clf.predict_proba( feat[np.newaxis,:] )
  best_n = np.argsort(probs, axis=1)[:,-5:]
  topk   = [linguagens[str(n)] for n in best_n[0]]

  return img, face, topk

while True:
  pass
