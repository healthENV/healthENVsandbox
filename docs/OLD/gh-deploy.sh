#!/usr/bin/expect -f

source ../.env_gh-deploy

set timeout 2

spawn mkdocs gh-deploy --force

expect "Username for 'https://github.com':\r"
send -- "$GH_user\r"

expect "Password for 'https://Cotswoldsmaker@github.com':\r"
send -- "$GH_token\r"

expect eof