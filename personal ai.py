import speech_recognition as SR
import os
import win32com.client
import webbrowser
import sys
import pygame
import random
import fnmatch
from threading import Thread
import datetime 
import google.generativeai as genai
from config import apikey, apikey2
import requests

# --- Initialize Speaker with Personality ---
speaker = win32com.client.Dispatch("SAPI.SpVoice")
pygame.mixer.init()

# Voice Configuration
voices = speaker.GetVoices()
female_voice_index = 1  # Change based on your system
speaker.Voice = voices.Item(female_voice_index)
speaker.Rate = 1.5  # Default slightly faster pace
speaker.Volume = 90   # Softer but clear

# Personality Settings
greetings = [
    "Hey there, superstar! ✨", 
    "Anya at your service, lovely human! 💖",
    "Ready to rock and roll? Let's go! 🚀"
]

goodbyes = [
    "Catch you on the flip side! 🌙",
    "Anya out! *mic drop* 🎤", 
    "Byeeeee! Sending virtual hugs! 🤗"
]

jokes = [
    "Why don’t AIs like fast food? Too many bytes! 🍔",
    "Why was the computer cold? It left its Windows open! ❄️"
]

# Emotional Voice System

def say(text, emotion="neutral"):
    emotions = {
        "happy": {"rate": 2, "volume": 95},
        "sad": {"rate": 0.5, "volume": 80},
        "excited": {"rate": 2.5, "volume": 100},
        "default": {"rate": 1.5, "volume": 90}
    }
    style = emotions.get(emotion, emotions["default"])
    
    speaker.Rate = style["rate"]
    speaker.Volume = style["volume"]
    speaker.Speak(text)
    # Reset to default
    speaker.Rate = 1.5
    speaker.Volume = 90

def listen():
    r = SR.Recognizer()
    with SR.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-IN")
            print(f"User said {query}")
            return query
        except Exception as e:
            say("Sorry, I didn't catch that. Can you repeat?", "sad")
            return " "

def get_website_url(site_name):
    """Map common site names to their actual URLs"""
    site_name = site_name.lower().strip()
    
    # Special cases mapping
    url_map = {
        "deep seek": "https://www.deepseek.ai",
        "chat gpt": "https://chat.openai.com",
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://twitter.com",
        "reddit": "https://www.reddit.com",
        "github": "https://github.com",
        "wikipedia": "https://en.wikipedia.org",
        "amazon": "https://www.amazon.com",
        "whatsapp": "https://web.whatsapp.com",
        "gmail": "https://mail.google.com",
        "outlook": "https://outlook.live.com",
        "linkedin": "https://www.linkedin.com",
        "netflix": "https://www.netflix.com",
        "spotify": "https://www.spotify.com",
        "discord": "https://discord.com",
        "zoom": "https://zoom.us",
        "jupyter": "http://localhost:8888",
        # Add more mappings as needed
    }
    
    # Check if it's a mapped site
    if site_name in url_map:
        return url_map[site_name]
    
    # Try common domain extensions
    common_domains = ['.com', '.org', '.net', '.ai', '.io']
    for domain in common_domains:
        url = f"https://www.{site_name}{domain}"
        try:
            if webbrowser.open(url):
                return url
        except:
            continue
    
    # Fallback to Google search
    return f"https://www.google.com/search?q={site_name}"

# Then modify your website opening code:

def play_music_non_blocking(file_path):
    """Play music without blocking main thread"""
    def play():
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            say(f"Could not play music. Error: {str(e)}")
    
    Thread(target=play).start()

def search_file(filename, search_path="C:\\"):
    """Search for file recursively across the system"""
    matches = []
    filename_lower = filename.lower()
    
    # Search common locations first
    common_locations = [
        os.path.expanduser("~\\Desktop"),
        os.path.expanduser("~\\Downloads"),
        os.path.expanduser("~\\Documents"),
        "C:\\"
    ]
    
    for location in common_locations:
        for root, dirs, files in os.walk(location):
            for file in files:
                if fnmatch.fnmatch(file.lower(), f"*{filename_lower}*"):
                    matches.append(os.path.join(root, file))
                    if len(matches) >= 3:  # Limit results for speed
                        return matches
    return matches

def open_file_systemwide(filename):
    """Try to open file from desktop first, then search entire system"""
    # First try desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    desktop_file = os.path.join(desktop_path, filename)
    
    if os.path.exists(desktop_file):
        return desktop_file
    
    # If not on desktop, search system
    say(f"Searching for {filename}...")
    found_files = search_file(filename)
    
    if not found_files:
        say(f"Sorry, I couldn't find {filename} anywhere.")
        return None
    elif len(found_files) == 1:
        return found_files[0]
    else:
        say(f"I found {len(found_files)} matches. Opening the first one.")
        return found_files[0]

def handle_file_open(filename):
    """Handle opening any file type"""
    file_path = open_file_systemwide(filename)
    if not file_path:
        return
    
    if file_path.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
        say(f"Playing {os.path.basename(file_path)}")
        play_music_non_blocking(file_path)
    else:
        os.startfile(file_path)
        say(f"Opening {os.path.basename(file_path)}")

def open_application(app_name):
    """Handle opening applications"""
    app_name = app_name.lower().strip()
    app_paths = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
        "jupyter": "jupyter-notebook.exe",
        "whatsapp":""
        # Add more application paths as needed
    }
    
    if app_name in app_paths:
        try:
            os.startfile(app_paths[app_name])
            say(f"Opening {app_name}")
        except Exception as e:
            say(f"Sorry, I couldn't open {app_name}. Error: {str(e)}")
    else:
        say(f"I don't know how to open {app_name}. Please teach me the path.")

def ai(prompt):
    try:
        genai.configure(api_key=apikey)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=500
            )
        )
        
        ai_response = response.text
        print("\n🔵 Anya:", ai_response)
        
        # Speak in chunks if long
        max_chunk = 300
        for i in range(0, len(ai_response), max_chunk):
            say(ai_response[i:i+max_chunk])
        
        # Save with timestamp
        if not os.path.exists("Anya_Memories"):
            os.mkdir("Anya_Memories")
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Anya_Memories/{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"💬 User: {prompt}\n\n")
            f.write(f"🤖 Anya: {ai_response}\n")
        
        say(f"Saved to our memory bank!", "happy")
        
    except Exception as e:
        error_msg = f"Oopsie! {str(e)}"
        say(error_msg, "sad")

def tell_joke():
    joke = random.choice(jokes)
    say(joke, "happy")
    return joke

def chat_with_anya():
    say(random.choice(greetings), "happy")
    conversation_history = []
    
    while True:
        user_input = listen()
        
        if not user_input:
            if len(conversation_history) > 0:
                say("Are you still there?", "thoughtful")
                time.sleep(2)
                continue
            else:
                say("I'll be here when you're ready to chat!", "happy")
                break
        
        if any(phrase in user_input for phrase in ["exit chat", "good bye", "stop talking"]):
            say("It was wonderful chatting with you! Let's talk again soon.", "happy")
            break
            
        conversation_history.append(f"User: {user_input}")
        
        try:
            # Build the prompt using conversation history
            context = "\n".join(conversation_history[-3:])
            prompt = f"""Continue this conversation naturally as helpful AI assistant Anya:
            {context}
            Anya:"""
            
            # Prepare the OpenRouter API request
            headers = {
                "Authorization": f"Bearer {apikey2}",  # Your OpenRouter API key
                "Content-Type": "application/json",
                "HTTP-Referer": "https://example.com",  # Change to your app URL
                "X-Title": "Anya Chat"                # Your app name
            }
            
            payload = {
                "model": "mistralai/mistral-small-3.2-24b-instruct:free",  # Free model
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.9,  # Matching your Gemini settings
                "max_tokens": 150     # Matching your Gemini settings
            }
            
            # Make the API call
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            # Get the AI response
            ai_response = response.json()['choices'][0]['message']['content'].strip()
            print(f"\nAnya: {ai_response}")
            
            # Emotional response logic (same as before)
            emotion = "thoughtful"
            if "!" in ai_response or "great" in ai_response.lower():
                emotion = "happy"
            elif "?" in ai_response:
                emotion = "thoughtful"
                
            say(ai_response, emotion)
            conversation_history.append(f"Anya: {ai_response}")
            
            # Auto-save conversation (same as before)
            if len(conversation_history) % 4 == 0:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(f"Anya_Chat_{timestamp}.txt", "w") as f:
                    f.write("\n".join(conversation_history))
            
        except Exception as e:
            error_msg = f"Oops! My circuits glitched: {str(e)}"
            say(error_msg, "sad")
            print("Error:", error_msg)

if __name__ == "__main__":
    say(random.choice(greetings), "happy")
    while True:
        print("\n🎙️ Listening...")
        query = listen().lower()

        if not query:
            continue
        
        if "hi anya" in query or "hello anya" in query or "let's talk" in query:
            say("Yes, darling? 💖  Lets have a bauitful conversation !", "happy ")
            chat_with_anya()
        # Exit command
        
        if any(phrase in query for phrase in ["go to sleep", "sleep", "stop", "exit", "bye"]):
            pygame.mixer.music.stop()
            say(random.choice(goodbyes), "happy")
            sys.exit()
        
        elif "joke" in query:
            tell_joke()

        elif "sing" in query:
            say("🎵 Anya-bot, Anya-bot, does whatever you like~ 🎶", "excited")

        elif "i feel" in query:
            if "sad" in query:
                say("Oh no! *virtual hug* Let me brighten your day! 🌈", "sad")
            elif "happy" in query:
                say("YAY! Your happiness is contagious! ✨", "excited")
        # File opening command

        elif "open" in query and "file" in query:
            filename = query.replace("open", "").replace("file", "").strip()
            if filename:
                handle_file_open(filename)
            else:
                say("Please specify a file name.")
        
        # Website opening

        elif "open" in query or ("website" in query or "site" in query or "." in query):
            site_name = query.replace("open", "").replace("website", "").replace("site", "").strip()
            if site_name:
                say(f"Opening {site_name}...")
                url = get_website_url(site_name)
                webbrowser.open(url)
            else:
                say("Please specify which website to open.")
                
        # Direct website opening (without saying "website")

        elif "open" in query or any(web in query for web in [".com", ".org", ".net", ".ai", ".io"]):
            site_name = query.replace("open", "").strip()
            say(f"Opening {site_name}...")
            url = get_website_url(site_name)
            webbrowser.open(url)
        
        # Music control

        elif "stop music" in query:
            pygame.mixer.music.stop()
            say("Music stopped")
             
             #to open any app 

        elif "open" in query and "app" in query:
            app_name = query.replace("open", "").replace("app", "").strip()
            if app_name:
                open_application(app_name)
            else:
                say("Please specify which application to open.")


        elif "search" in query:
            search_query = query.replace("search", "").strip()
            if search_query:
                url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(url)
                say(f"Searching for {search_query} on Google")
            else:
                say("Please specify what you want to search for.")
        
        # In your main loop, fix the prompt extraction:
        elif "using gemini" in query or "using artificial intelligence" in query:
            prompt = query.replace("using gemini", "").replace("using artificial intelligence", "").strip()
            if prompt:
                say("Accessing the knowledge cosmos... 🌌", "happy")
                ai(prompt)
            else:
                say("Please tell me what you'd like me to ask Gemini.")

        # Default response
        else:
             say("Hmm, let me think... Nope, need clearer instructions! 🤔", "sad")

        if "time" in query or "date" in query:  # More flexible trigger
            date = datetime.datetime.now().strftime("%B %d, %Y")
            time = datetime.datetime.now().strftime("%I:%M %p")
            say(f"Sir, today is {date} and the current time is {time} ","happy")
    say("System standby... but I'll miss you! 💔", "sad")