# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 16:03:55 2023

@author: ranaf
"""

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from gradio_client import Client
from PIL import Image
import io


app = Flask(__name__)

import sys
print(sys.executable)

client = Client("https://asalhi85-diyaa.hf.space/--replicas/ie5al/")
apiKey = "AIzaSyBbdYBQywqEKWMCPkdktiu06xsT2I1Nlck"
genai.configure(api_key = apiKey)
model = genai.GenerativeModel('gemini-pro')
model_img = genai.GenerativeModel('gemini-pro-vision')


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
    pass

@app.route('/process_image', methods=['POST'])
def process_image():
    
    if 'image' in request.files:
        img = request.files['image']
        if img.filename != '':
            img = Image.open(io.BytesIO(img.read()))
            response_img = get_response_gemini_img(img,0.7,40,0.95,2048)
            response_img.resolve()
            response_key_words = get_response_gemini_extract_key_words(response_img.text,0.7,40,0.95,2048)
            response = get_response_gemini(response_key_words.text,0.7,40,0.95,2048)

    return jsonify({'response': response.text})

def get_response_gemini_img(img,temperature,top_k,top_p,max_output_tokens):
  prompt= "اكتب لي وصف عن الصورة المرفقة "
  response = model_img.generate_content(
        [prompt, img],
        generation_config=genai.types.GenerationConfig(temperature=temperature, top_k=top_k, top_p=top_p,
            max_output_tokens=max_output_tokens),stream=True, safety_settings = [
    {
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
    },])

  return response

def get_response_gemini(text,temperature,top_k,top_p,max_output_tokens):
    prompt= "اذكر لي آية من القرآن الكريم تتحدث عن :"+ text + ". و اشرح لي الآيه حسب تفسير تقدر تختار تفسير بن سعدي وارجوا ان لا تترجم اي نص الى لغة اخرى غير العربية عند الشرح"
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=temperature, top_k=top_k, top_p=top_p,
            max_output_tokens=max_output_tokens), safety_settings = [
    {
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
    },])

    return response


def get_response_gemini_extract_key_words(text,temperature,top_k,top_p,max_output_tokens):
    prompt= "استخرج كلمات مفتاحية من النص التالي: "+text
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=temperature, top_k=top_k, top_p=top_p,
            max_output_tokens=max_output_tokens), safety_settings = [
    {
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
    },])

    return response

    
if __name__ == "__main__":
    app.run(debug=True)