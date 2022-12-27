#!/usr/bin/python

import requests as req

resp = req.get("http://hub:80")

print(resp.text)