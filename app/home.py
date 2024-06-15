from flask import Flask, Response
from flask import request
from app import app
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json
import os
import requests 
import google.generativeai as genai
import sqlite3

def read_prompt(prompt):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, prompt)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file or directory: '{file_path}'")

    # Read the contents of the file
    with open(file_path, 'r') as file:
        prompt = file.read()
    return prompt

def save_chat(bot_name, chat_id, username, name, message, request, response):
    try:
        print("Starting save_chat function.")
        
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__))
        print(f"Current directory: {current_directory}")
        
        # Construct the path to the database file
        file_path = os.path.join(current_directory, 'chat_data.db')
        print(f"Database file path: {file_path}")
        
        # Connect to the SQLite database
        print("Connecting to the database...")
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        print("Connected to the database.")
        
        # Create table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS chat_messages
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           bot_name TEXT NULL,
                           chat_id TEXT NOT NULL,
                           username TEXT NULL,
                           name TEXT NULL,
                           message TEXT NOT NULL,
                           request TEXT NULL,
                           response TEXT NOT NULL)''')
        conn.commit()
        print("Table created or verified successfully.")
        
        # Insert the chat data
        cursor.execute("INSERT INTO chat_messages (bot_name, chat_id, username, name, message, request, response) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       (bot_name, chat_id, username, name, message, request, response))
        conn.commit()
        print("Data inserted successfully.")
        
        # Close the connection
        conn.close()
        print("Database connection closed.")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/', methods=['GET'])
def hoem():
    return Response('Welcome Home')

@app.route('/pka', methods=['POST'])
def pka_chat():
    bot_token = "7145127367:AAFvT3dwg9KbizIs41azfcSATluatEEYrgg"
    if request.method == 'POST':
        # Access POST data from the request
        msg = request.get_json()  
        print("Message: ",msg)

        # Trying to parse message
        try:
            chat_id = msg['message']['chat']['id']
            text = msg['message']['text']


            genai.configure(api_key='AIzaSyC6Cct7fUm291DRjHS83KC7gkOU-Mokt5Y')
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }

            # prompt = requests.get(f"https://docs.google.com/document/d/1g1d8TA56cbKfHwB0Cg0gf8LXWdZTYGK-sCIvWtl5B0U/export?format=txt").text
            # dataset = read_prompt('dataset.csv')
            # prompt = prompt.replace("[DATASET]", dataset)
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                },
                system_instruction=read_prompt('prompt.txt'),
                # system_instruction=read_prompt(prompt),
            )
            chat_session = model.start_chat(history=[])

            response = chat_session.send_message(text)            
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'            
            payload = {
                'chat_id': chat_id,
                'text': response.text
            }
            r = requests.post(url, json=payload)

            if r.status_code == 200:
                return Response('ok', status=200)
            else: 
                return Response('Failed to send message to Telegram', status=500)
        except Exception as e:
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'            
            payload = {
                'chat_id': chat_id,
                'text': "Maaf kak aku ga bisa jawab untuk itu.\n{e}"
            }
            r = requests.post(url, json=payload)
            print(f"An unexpected error occurred: {e}")

        return Response('ok', status=200)
    

@app.route('/bctajg', methods=['POST'])
def bctajg_chat():
    bot_token = "6855102088:AAG1njb9dsWSOsAiQoS6sQi_8dQu_cL2hAg"
    if request.method == 'POST':
        # Access POST data from the request
        msg = request.get_json()  
        print("Message: ",msg)

        # Trying to parse message
        try:
            chat_id = msg['message']['chat']['id']
            username = msg['message']['from']['username']
            name = msg['message']['from']['first_name']
            text = msg['message']['text']

            genai.configure(api_key='AIzaSyC6Cct7fUm291DRjHS83KC7gkOU-Mokt5Y')
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }

            prompt = requests.get(f"https://docs.google.com/document/d/1uszRK5wmXYJ7K9u1VoP1Ex50wtxr1BrNs6f3nE1wKF0/export?format=txt").text
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                },
                # system_instruction=read_prompt('bctajg_prompt.txt'),
                system_instruction=prompt,
            )
            chat_session = model.start_chat(history=[])

            response = chat_session.send_message(text)            
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'            
            payload = {
                'chat_id': chat_id,
                'text': response.text
            }
            r = requests.post(url, json=payload)

            if r.status_code == 200:
                save_chat('bctajg_bot', chat_id, username, name, text, json.dumps(msg), response.text)
                return Response('ok', status=200)
            else: 
                return Response('Failed to send message to Telegram', status=500)
        except Exception as e:
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'            
            payload = {
                'chat_id': chat_id,
                'text': "Lo ngomong apa sih ga jelas amat cok jancokk!!"
            }
            r = requests.post(url, json=payload)
            print(f"An unexpected error occurred: {e}")

        return Response('ok', status=200)
    