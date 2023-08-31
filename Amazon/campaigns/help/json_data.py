import json

def is_json(text):
    try:
        content = json.loads(text)
        return content
    except:

        return False