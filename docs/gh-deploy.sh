#!/usr/bin/expect -f

set timeout 5

spawn mkdocs gh-deploy --force

expect "Username for 'https://github.com':\r"
send -- "$env(GH_user)\r"

expect "Password for 'https://Cotswoldsmaker@github.com':\r"
send -- "$env(GH_token)\r"

expect eof