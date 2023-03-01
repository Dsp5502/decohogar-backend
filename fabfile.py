from fabric import task, Connection


@task
def deploy(c: Connection):
    with c.cd('~/project/'):
        with c.prefix('source env/bin/activate'):
            with c.cd('decohogar-backend/'):
                c.run('git pull')
                c.run('pip install -r requirements.txt')
