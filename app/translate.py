"""
    Translatation of webpages functionality
"""
import json
import sys
from urllib import request, parse
import pickle
import os.path
import re
import os
import subprocess
import pexpect

mainDirectory: str = os.getcwd()
#print(mainDirectory)
url: str = 'http://0.0.0.0:5006/'
dictLocation: str = './dictionaryMultilingual.pi'
rootdir: str = './templates'
dictionaryMultilingual = {}
name: str = 'Hello'
name = 100



if os.path.exists(dictLocation):
    file = open(dictLocation, 'rb')
    dictionaryMultilingual = pickle.load(file)
    file.close()


#print(dictionaryMultilingual)
#sys.exit()

DEFINEDLANGUAGES = ['en','fr', 'fi', 'sv', 'it']

def findSentensesToTranslate():
    """Searches templates folder to find trans['someSentenseToTranslate']
    
    """

    global dictionaryMultilingual

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".html"):
                f = open(filepath, "r")
                fileContents = f.read()
                f.close()
                result = re.findall('trans\[\'(.*)\'\]', fileContents)
                #print(result)
                for sentence in result:
                    if sentence not in dictionaryMultilingual:
                        dictionaryMultilingual[sentence] = {}
                        #print(sentence)
    
    #print(dictionaryMultilingual)
    updateDictionary()

    return



def updateDictionary():
    """Updates from LibreTranslate container (still in building phase)

    """

    global dictionaryMultilingual, DEFINEDLANGUAGES

    lt = LibreTranslateAPI(url)

    # Check if LibreTranslate installed


    # Check if docker container running (if not start it)
    
    #os.chdir(mainDirectory)
    #os.chdir("..")

    # Check if running well 

    # Send translation queries

    
    for key1, value1 in dictionaryMultilingual.items():
        if not value1:
            for lang in DEFINEDLANGUAGES:
                try:
                    translation = lt.translate(key1, "en", lang)
                except:
                    print("Error translating")
                else:
                    dictionaryMultilingual[key1][lang]= translation
    
    file = open('dictionaryMultilingual.pi', 'wb')
    pickle.dump(dictionaryMultilingual, file)
    file.close()
    return




def translatedWords(language):
    """ Translate words to diffent languages
        :param str language: message to log
        :returns: None
        :rtype: None
    """
    #print(dictionaryMultilingual)
    #print('****')
    if language not in DEFINEDLANGUAGES:
        raise Exception(f"Provided language '{ language }' is not defined")
        return

    dictionarySingleLanguage = {}
    for key1, value1 in dictionaryMultilingual.items():
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
    #print(translatedWords('fr'))
    #findSentensesToTranslate()
    
