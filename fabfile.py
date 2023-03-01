from fabric import task, Connection


@task
def deploy(c: Connection):
    with c.cd('~/project/decohogar-backend/'):
        c.run('git pull')
        with c.lcd('..'):
            with c.prefix('source env/bin/activate'):
                c.run('pip install -r requirements.txt')
