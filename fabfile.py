
from fabric.api import run, cd, sudo
from fabric.contrib.project import upload_project

def upload():
    run('mkdir -p ~/PycharmProjects')
    upload_project('../s_cities', '~/PycharmProjects')


def start():
    with cd('~/PycharmProjects/s_cities'):
        run('pip install -r requirements.txt')
        # sudo('nohup python run.py >& /dev/null < /dev/null &')

def stop():
    run("ps aux| grep python | awk '{print $2}'| xargs kill -9")

def restart():
    upload()
    with cd('~/PycharmProjects/s_cities'):
        run('docker-compose down')
        run('docker-compose up -d')

def r():
    upload()
    start()

if __name__ == '__main__':
    pass