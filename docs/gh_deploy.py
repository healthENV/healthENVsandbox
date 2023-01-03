from __future__ import annotations

import logging
import os
import re
import subprocess
from typing import Optional, Tuple, Union

import ghp_import
from packaging import version

import mkdocs
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import Abort

log = logging.getLogger(__name__)

default_message = """Deployed {sha} with MkDocs version: {version}"""


def _is_cwd_git_repo() -> bool:
    try:
        proc = subprocess.Popen(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        log.error("Could not find git - is it installed and on your path?")
        raise Abort('Deployment Aborted!')
    proc.communicate()
    return proc.wait() == 0


def _get_current_sha(repo_path) -> str:
    proc = subprocess.Popen(
        ['git', 'rev-parse', '--short', 'HEAD'],
        cwd=repo_path or None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, _ = proc.communicate()
    sha = stdout.decode('utf-8').strip()
    return sha


def _get_remote_url(remote_name: str) -> Union[Tuple[str, str], Tuple[None, None]]:
    # No CNAME found.  We will use the origin URL to determine the GitHub
    # pages location.
    remote = f"remote.{remote_name}.url"
    proc = subprocess.Popen(
        ["git", "config", "--get", remote],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, _ = proc.communicate()
    url = stdout.decode('utf-8').strip()

    if 'github.com/' in url:
        host, path = url.split('github.com/', 1)
    elif 'github.com:' in url:
        host, path = url.split('github.com:', 1)
    else:
        return None, None
    return host, path


def _check_version(branch: str) -> None:
    proc = subprocess.Popen(
        ['git', 'show', '-s', '--format=%s', f'refs/heads/{branch}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, _ = proc.communicate()
    msg = stdout.decode('utf-8').strip()
    m = re.search(r'\d+(\.\d+)+((a|b|rc)\d+)?(\.post\d+)?(\.dev\d+)?', msg, re.X | re.I)
    previousv = version.parse(m.group()) if m else None
    currentv = version.parse(mkdocs.__version__)
    if not previousv:
        log.warning('Version check skipped: No version specified in previous deployment.')
    elif currentv > previousv:
        log.info(
            f'Previous deployment was done with MkDocs version {previousv}; '
            f'you are deploying with a newer version ({currentv})'
        )
    elif currentv < previousv:
        log.error(
            f'Deployment terminated: Previous deployment was made with MkDocs version {previousv}; '
            f'you are attempting to deploy with an older version ({currentv}). Use --ignore-version '
            'to deploy anyway.'
        )
        raise Abort('Deployment Aborted!')


def gh_deploy(
    config: MkDocsConfig,
    message: Optional[str] = None,
    force=False,
    no_history=False,
    ignore_version=False,
    shell=False,
) -> None:

    if not _is_cwd_git_repo():
        log.error('Cannot deploy - this directory does not appear to be a git repository')

    remote_branch = config.remote_branch
    remote_name = config.remote_name

    if not ignore_version:
        _check_version(remote_branch)

    if message is None:
        message = default_message
    sha = _get_current_sha(os.path.dirname(config.config_file_path))
    message = message.format(version=mkdocs.__version__, sha=sha)

    log.info(
        "Copying '%s' to '%s' branch and pushing to GitHub.",
        config.site_dir,
        config.remote_branch,
    )

    print(f'config.site_dir = { config.site_dir }')
    print(f'message = { message }')
    print(f'remote_name = { remote_name }')
    print(f'remote_branch = { remote_branch }')
    print(f'push=True')
    print(f'force= { force }')
    print(f'shell = { shell }')
    print(f'no_history= { no_history }')
    print(f'nojekyll=True')

    try:
        ghp_import.ghp_import(
            config.site_dir,
            mesg=message,
            remote=remote_name,
            branch=remote_branch,
            push=True,
            force=force,
            use_shell=shell,
            no_history=no_history,
            nojekyll=True,
        )
    except ghp_import.GhpError as e:
        log.error(f"Failed to deploy to GitHub with error: \n{e.message}")
        raise Abort('Deployment Aborted!')

    cname_file = os.path.join(config.site_dir, 'CNAME')
    # Does this repository have a CNAME set for GitHub pages?
    if os.path.isfile(cname_file):
        # This GitHub pages repository has a CNAME configured.
        with open(cname_file) as f:
            cname_host = f.read().strip()
        log.info(
            f'Based on your CNAME file, your documentation should be '
            f'available shortly at: http://{cname_host}'
        )
        log.info(
            'NOTE: Your DNS records must be configured appropriately for your CNAME URL to work.'
        )
        return

    host, path = _get_remote_url(remote_name)

    if host is None or path is None:
        # This could be a GitHub Enterprise deployment.
        log.info('Your documentation should be available shortly.')
    else:
        username, repo = path.split('/', 1)
        if repo.endswith('.git'):
            repo = repo[: -len('.git')]
        url = f'https://{username}.github.io/{repo}/'
        log.info(f"Your documentation should shortly be available at: {url}")
