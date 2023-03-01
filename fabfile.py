from fabric import task, Connection


@task
def deploy(c: Connection):
    with c.cd('~/project/decohogar-backend/'):
        with c.prefix('source env/bin/activate'):
            c.run('git pull')
            with c.cd('..'):
                c.run('pip install -r requirements.txt')
