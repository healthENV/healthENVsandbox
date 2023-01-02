#!/usr/bin/expect

set timeout 20
set GH_user test
set GH_token test

proc check_host {} {
    global GH_user GH_token

    spawn mkdocs gh-deploy --force
    expect "Username for 'https://github.com':\r"
    send "$GH_user\r"
    expect "Password for 'https://$GH_user@github.com':\r"                ;# adjust to suit the prompt accordingly
    send "$GH_token\r"
    expect eof
}

set fp [open ../.env r]
while {[gets $fp line] != -1} {
    check_host $line
}
close $fp