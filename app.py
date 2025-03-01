from openai import OpenAI
from apikey import api_key

import os
import speech_recognition as sr 
import pyttsx3  
import webbrowser 

# OpenAI API Configuration
Model = "gpt-4o"
client = OpenAI(api_key=api_key)

def Reply(question):
    completion = client.chat.completions.create(
        model=Model,
        messages=[
            {'role': "system", "content": "You are a helpful assistant"},
            {'role': 'user', 'content': question}
        ],
        max_tokens=200
    )
    answer = completion.choices[0].message.content
    return answer 

# Text-to-Speech Engine Configuration
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # You can change index to 1 for a different voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source: 
        print('Listening...')
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        recognizer.pause_threshold = 1  # 1 sec before considering the end of a phrase
        audio = recognizer.listen(source)
    
    try: 
        print('Recognizing...')
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User Said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please repeat.")
        return "None"
    except sr.RequestError:
        print("Could not request results, check your internet connection.")
        return "None"
    
    return query.lower()

if __name__ == '__main__':
    speak("Hello! How can I assist you today?")
    
    while True: 
        query = takeCommand()
        if query == 'none':
            continue
        
        # Get AI Response
        ans = Reply(query)
        print(ans)
        speak(ans)
        
        # Specific Browser Related Tasks 
        if "open youtube" in query: 
            webbrowser.open('https://www.youtube.com')
        elif "open google" in query: 
            webbrowser.open('https://www.google.com')
        elif "bye" in query or "exit" in query:
            speak("Goodbye! Have a great day!")
            break
