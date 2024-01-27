# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 16:03:55 2023

@author: ranaf
"""

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from pytube import YouTube
from moviepy.editor import *
import speech_recognition as sr
import stanza

app = Flask(__name__)

import sys
print(sys.executable)

apiKey = "AIzaSyBbdYBQywqEKWMCPkdktiu06xsT2I1Nlck"
genai.configure(api_key = apiKey)
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/process_text', methods= ['POST'])
def process_text():
    text = request.form['text']
    # Process the text_prompt...
    prompt= "اذكر لي آية من القرآن الكريم تتحدث عن :"+ text + ". و اشرح لي الآيه حسب تفسير تقدر تختار تفسير بن سعدي وارجوا ان لا تترجم اي نص الى لغة اخرى غير العربية عند الشرح"
    response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.9, top_k=40, top_p=0.95,
                max_output_tokens=2048), safety_settings=[{
            
                    "category": "HARM_CATEGORY_DANGEROUS",        
                    "threshold": "BLOCK_NONE",    
                },   
                {       
                    "category": "HARM_CATEGORY_HARASSMENT",       
                    "threshold": "BLOCK_NONE",   
                },    
                {       
                    "category": "HARM_CATEGORY_HATE_SPEECH",       
                    "threshold": "BLOCK_NONE", 
                },   
                {       
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",       
                    "threshold": "BLOCK_NONE",    
                },  
                {       
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",       
                    "threshold": "BLOCK_NONE",   
                }])
    
    text_response = response.text
    return jsonify({'response': text_response})


@app.route('/process_video', methods= ['POST'])
def process_video():
    vid_url = request.form['text']
    
    vid_text = extract_text_from(vid_url)
    response_key_words = get_response_gemini_extract_key_words(vid_text,0.7,40,0.95,2048)
    response = get_response_gemini(response_key_words.text,0.7,40,0.95,2048)

    text_response = response.text
    return jsonify({'response': text_response})
    
def get_response_gemini(text,temperature,top_k,top_p,max_output_tokens):

    prompt = "أذكر لي آية من القران الكريم تتحدث عن أحد هذه المواضيع او اكثر: "+ text + " واشرح الآيه وفسرها باللغة العربية."
    response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=temperature, top_k=top_k, top_p=top_p,
                max_output_tokens=max_output_tokens), safety_settings=[{
            
                    "category": "HARM_CATEGORY_DANGEROUS",        
                    "threshold": "BLOCK_NONE",    
                },   
                {       
                    "category": "HARM_CATEGORY_HARASSMENT",       
                    "threshold": "BLOCK_NONE",   
                },    
                {       
                    "category": "HARM_CATEGORY_HATE_SPEECH",       
                    "threshold": "BLOCK_NONE", 
                },   
                {       
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",       
                    "threshold": "BLOCK_NONE",    
                },  
                {       
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",       
                    "threshold": "BLOCK_NONE",   
                }])
    
    return response

def get_response_gemini_extract_key_words(text,temperature,top_k,top_p,max_output_tokens):
  prompt= "استخرج كلمات مفتاحية من النص التالي: "+text
  response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=temperature, top_k=top_k, top_p=top_p,
               max_output_tokens=max_output_tokens), safety_settings=[{
           
                   "category": "HARM_CATEGORY_DANGEROUS",        
                   "threshold": "BLOCK_NONE",    
               },   
               {       
                   "category": "HARM_CATEGORY_HARASSMENT",       
                   "threshold": "BLOCK_NONE",   
               },    
               {       
                   "category": "HARM_CATEGORY_HATE_SPEECH",       
                   "threshold": "BLOCK_NONE", 
               },   
               {       
                   "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",       
                   "threshold": "BLOCK_NONE",    
               },  
               {       
                   "category": "HARM_CATEGORY_DANGEROUS_CONTENT",       
                   "threshold": "BLOCK_NONE",   
               }])

  return response

def extract_text_from(vid_link):
    yt = YouTube(vid_link)
    text = ""
    audio_stream = yt.streams.get_audio_only()
    audio_stream.download(filename='tmp.mp4')
    audio_clip = AudioFileClip('tmp.mp4')
    audio_clip.write_audiofile('tmp.wav')
    r = sr.Recognizer()
    with sr.AudioFile('tmp.wav') as source:
      audio_data = r.record(source)
      try:
          text = r.recognize_google(audio_data,  language='ar')
      except sr.UnknownValueError:
          print("Google Speech Recognition could not understand audio")
      except sr.RequestError as e:
          print("Could not request results from Google Speech Recognition service; {0}".format(e))
      return text

if __name__ == "__main__":
    app.run(debug=True)