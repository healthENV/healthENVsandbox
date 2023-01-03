cp /usr/local/lib/python3.8/dist-packages/mkdocs/commands/gh_deploy.py /project/docs

cp /project/docs/gh_deploy.py /usr/local/lib/python3.8/dist-packages/mkdocs/commands


try:
    ghp_import.ghp_import(
        config.site_dir = /project/docs/site
        message = Deployed 5bb2d8d with MkDocs version: 1.4.2
        remote_name = origin
        remote_branch = gh-pages
        push=True
        force= True
        shell = False
        no_history= False
        nojekyll=True


cp /usr/local/lib/python3.8/dist-packages/ghp_import.py /project/docs