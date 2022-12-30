import json
import requests

paramsN = {
	'q': "fine",
	'source': "en",
	'target': "fr",
	'format': "text",
	'api_key': ""
}


params = {
	'body' : json.dumps(paramsN, separators=(',', ':')),
}

headers = { "Content-Type": "application/json" }

response = requests.post("http://0.0.0.0:4000/translate", json=json.dumps(paramsN), headers=headers)

print(response)



{'args': {},
 'data': '{"key": "value"}',
 'files': {},
 'form': {},
 'headers': {'Accept': '*/*',
             'Accept-Encoding': 'gzip, deflate',
             'Connection': 'close',
             'Content-Length': '16',
             'Content-Type': 'application/json',
             'Host': 'httpbin.org',
             'User-Agent': 'python-requests/2.4.3 CPython/3.4.0',
             'X-Request-Id': 'xx-xx-xx'},
 'json': {'key': 'value'},
 'origin': 'x.x.x.x',
 'url': 'http://httpbin.org/post'}

"""import fetch

const res = await fetch("https://libretranslate.com/translate", {
        method: "POST", 
        body: JSON.stringify({
		q: "Hello!",
		source: "en",
		target: "es"
	}),
	headers: { "Content-Type": "application/json" }
});

console.log(await res.json());
"""