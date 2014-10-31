from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'git@github.com:lennyk/cso.git'
REPO_NAME = 'cso'
GIT_KEY = 'cso_rsa'


def deploy(target):
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    ssh_key = '/home/%s/.ssh/%s' % (env.user, GIT_KEY)
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder, ssh_key)
    _update_settings(source_folder, env.host, target)
    _update_virtualenv(source_folder)
    _install_node_tools(site_folder)
    _install_bower_components(source_folder)
    _update_static_files(source_folder, target)
    _update_database(source_folder, target)
    _deploy_fixtures(source_folder, target)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source', 'media', 'logs'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder, ssh_key):
    if exists(source_folder + '/.git'):
        run('cd %s && eval $(ssh-agent) && ssh-add %s && git fetch' % (source_folder, ssh_key))
        # run('cd %s && git fetch' % (source_folder,))
    else:
        run('eval $(ssh-agent) && ssh-add %s && git clone %s %s' % (ssh_key, REPO_URL, source_folder))
        # run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name, target):
    instance_settings_file = source_folder + '/instance_settings.py'

    if not exists(instance_settings_file):
        append(instance_settings_file, '\nALLOWED_HOSTS = ["%s"]' % (site_name,))
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(instance_settings_file, "\nSECRET_KEY = '%s'" % (key,))


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, source_folder
        ))


def _install_node_tools(site_folder):
    # TODO: use shrinkwrap to manage dependencies
    run('cd %s && npm install bower yuglify' % site_folder)


def _install_bower_components(source_folder):
    run('cd %s && ../node_modules/bower/bin/bower install' % source_folder)


def _update_static_files(source_folder, target):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput --settings=%s.settings --configuration=%s'
        % (source_folder, REPO_NAME, target.capitalize()))


def _update_database(source_folder, target):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput --settings=%s.settings --configuration=%s'
        % (source_folder, REPO_NAME, target.capitalize()))


def _deploy_fixtures(source_folder, target):
    run('cd %s && ../virtualenv/bin/python3 manage.py loaddata --settings=%s.settings --configuration=%s fixtures/initial_data-common.json fixtures/initial_data-%s.json' % (
        source_folder, REPO_NAME, target.capitalize(), target
        ))
