import speech_recognition as SR
import os
import win32com.client
import webbrowser
import sys
import pygame
import fnmatch  # For pattern matching
from threading import Thread  # For non-blocking music playback
import datetime 
import openai

# Initialize speaker and pygame mixer
speaker = win32com.client.Dispatch("SAPI.SpVoice")
pygame.mixer.init()
voices = speaker.GetVoices()
print("Available Voices:")
for i, voice in enumerate(voices):
    print(f"{i}: {voice.GetDescription()}")

# Select a female voice (check your system for available options)
female_voice_index = 1  # Typically 1 is female voice
speaker.Voice = speaker.GetVoices().Item(female_voice_index)

# Adjust speech settings
speaker.Rate = 1  # Speech rate (-10 to 10)
speaker.Volume = 100  # Volume (0-100)

def say(text):
    speaker.Speak(text)

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
            return "Some Error Occurred. Sorry From Anya"



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



if __name__ == "__main__":
    say("Hello, I am Anya A I.")
    while True:
        print("Listening...")
        query = listen().lower()
        
        # Exit command
        
        if any(phrase in query for phrase in ["go to sleep", "sleep", "stop", "exit", "bye"]):
            pygame.mixer.music.stop()
            say("Goodbye! Going to sleep now.")
            sys.exit()
        
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
        
        # Default response
        else:
            say("I didn't understand that command. Please try again.")


        if "time" in query or "date" in query:  # More flexible trigger
            date = datetime.datetime.now().strftime("%B %d, %Y")
            time = datetime.datetime.now().strftime("%I:%M %p")
            say(f"Sir, today is {date} and the current time is {time}")