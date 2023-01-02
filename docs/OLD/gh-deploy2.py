#!/usr/bin/python3

"""Push pages to GitHub via 'mkdocs gh-deloy --force'

"""

import pexpect
import time as t

def pushToGH():
    child = pexpect.spawn ('mkdocs gh-deploy --force')
    t.sleep(5)
    #child.expect ("Username for 'https://github.com':\r")
    #print(child.before)
    child.sendline ('Cotswoldsmaker')
    #child.expect ("Password for 'https://Cotswoldsmaker@github.com':\r")
    #print(child.before)
    t.sleep(2)
    child.sendline ('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')
    #print('Password sent')
    #print(child.after)
    #print(child.before)

    return

if __name__ == '__main__':
	pushToGH()