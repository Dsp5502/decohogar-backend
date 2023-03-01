from fabric import task, Connection


@task
def deploy(c: Connection):
    with c.cd('~/project/decohogar-backend/'):
        c.run('git pull')
