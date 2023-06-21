import json

#COMMENT FOR YOU, IT MIGHT BE PRUDENT TO ADD ABSOLUT PATHS TO ALL OF YOUR CODE SO WE DONT HAVE ISSUES

global current_language
global text

def set_language(lang):
    global text
    global current_language

    current_language = lang

    # Load the text for the new current language from a JSON file in the json_files folder
    with open(f"Assets/Json/{current_language}.json", "r", encoding='utf-8') as f:
        text = json.load(f)

def switch_language(config):

    # Switch the current language
    if current_language == "english":
        lang = "arabic"
    else:
        lang = "english"

    config.set("Settings", "current_language", lang)
    with open("config.ini", "w") as f:
        config.write(f)
    
    set_language(lang)

def get_text(section, key):
    
    return text[section][key]