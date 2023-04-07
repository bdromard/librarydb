import requests as req
import json

try:
    response = req.get("https://openlibrary.org/isbn/9780140328721.json")
    response.raise_for_status()
    response_as_json = response.json()
    # Méthode de la librairie json pour mettre en forme le fichier JSON ; type => string.
    pretty_json = json.dumps(response_as_json, sort_keys=True, indent=4)
except Exception as err:
    print(f'An Exception has occurred: {err}')
else:
    with open("response.txt", "w") as data:
        data.write(f"{response_as_json['title']}")
        data.write(pretty_json)
        data.write(f"{response_as_json['authors']}")