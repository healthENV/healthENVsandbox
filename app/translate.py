"""
    Translatation of webpages functionality
"""
import json
import sys
from urllib import request, parse

url = "http://0.0.0.0:4000/"


dictionaryMultilingual = {
    'Build consistent, accessible user interfaces. Learn from the research and experience of other NHS digital teams.': {'fr': "Créez des interfaces utilisateur cohérentes et accessibles. Apprenez des recherches et de l'expérience d'autres équipes numériques du NHS."},
    'Command line': {'fr': 'ligne de commande'},
    'Environments': {'fr': 'Environnements'},
    'Network': {'fr': 'Réseau'},
    'Messages': {'fr': 'Messages'},
    'Portal': {'fr': 'Portail'},
    'Search': {'fr': 'Rechercher'},
    'Settings': {'fr': 'Réglages'},
    'Spin up an environment': {'fr': 'Faire tourner un environnement'},
    'Use the tools below to start up a new environment': {'fr': 'Utilisez les outils ci-dessous pour démarrer un nouvel environnement'},
    'Use the link below to start up a new command line': {'fr': 'Utilisez le lien ci-dessous pour démarrer une nouvelle ligne de commande'},
}

testWords = {'bike': '','chair': '', 'house': ''}


definedLanguages = ['en', 'fr', 'ge']


def updateDictionary():
    """
        Updates from LibreTranslate container (still in building phase)
    """
    global dictionaryMultilingual, definedLanguages

    lt = LibreTranslateAPI(url)

    for key1, value1 in dictionaryMultilingual.items():
        for key2, value2 in value1.items():
            for lang in definedLanguages:
                translation = lt.translate(key1, lang, key2)
                print(translation)
                dictionaryMultilingual[key1][lang]= translation
    #print(dictionaryMultilingual)
    return




def translatedWords(language):
    """ Translate words to diffent languages
        :param str language: message to log
        :returns: None
        :rtype: None
    """

    if language not in definedLanguages:
        raise Exception(f"Provided language '{ language }' is not defined")
        return

    dictionarySingleLanguage = {}
    for key1, value1 in dictionaryMultilingual.items():
        dictionarySingleLanguage[key1] = key1
        for key2, value2 in value1.items():
            if key2 == language:
                dictionarySingleLanguage[key1] = value2
                break
    return dictionarySingleLanguage


class LibreTranslateAPI:
    """Connect to the LibreTranslate API"""

    """Example usage:
    from libretranslatepy import LibreTranslateAPI

    lt = LibreTranslateAPI("https://translate.argosopentech.com/")

    print(lt.translate("LibreTranslate is awesome!", "en", "es"))
    # LibreTranslate es impresionante!

    print(lt.detect("Hello World"))
    # [{"confidence": 0.6, "language": "en"}]
    
    print(lt.languages())
    # [{"code":"en", "name":"English"}]
    """

    DEFAULT_URL = "https://translate.argosopentech.com/"

    def __init__(self, url=None, api_key=None):
        """Create a LibreTranslate API connection.

        Args:
            url (str): The url of the LibreTranslate endpoint.
            api_key (str): The API key.
        """
        self.url = LibreTranslateAPI.DEFAULT_URL if url is None else url
        self.api_key = api_key

        # Add trailing slash
        assert len(self.url) > 0
        if self.url[-1] != "/":
            self.url += "/"

    def translate(self, q, source="en", target="es"):
        """Translate string

        Args:
            q (str): The text to translate
            source (str): The source language code (ISO 639)
            target (str): The target language code (ISO 639)

        Returns:
            str: The translated text
        """
        url = self.url + "translate"
        params = {"q": q, "source": source, "target": target}
        if self.api_key is not None:
            params["api_key"] = self.api_key
        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode())
        response = request.urlopen(req)
        response_str = response.read().decode()
        return json.loads(response_str)["translatedText"]

    def detect(self, q):
        """Detect the language of a single text.

        Args:
            q (str): Text to detect

        Returns:
            The detected languages ex: [{"confidence": 0.6, "language": "en"}]
        """
        url = self.url + "detect"
        params = {"q": q}
        if self.api_key is not None:
            params["api_key"] = self.api_key
        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode())
        response = request.urlopen(req)
        response_str = response.read().decode()
        return json.loads(response_str)

    def languages(self):
        """Retrieve list of supported languages.

        Returns:
            A list of available languages ex: [{"code":"en", "name":"English"}]
        """
        url = self.url + "languages"
        params = dict()
        if self.api_key is not None:
            params["api_key"] = self.api_key
        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode(), method="GET")
        response = request.urlopen(req)
        response_str = response.read().decode()
        return json.loads(response_str)


if __name__ == '__main__':
    updateDictionary()
