from fabric import task, Connection


@task
def deploy(c: Connection):
    with c.cd('~/project/decohogar-backend/'):
        c.run('git pull')

    with c.cd('~/project/'):
        c.prefix('source env/bin/activate')

    with c.cd('~/project/decohogar-backend/'):
        c.run('pip install -r requirements.txt')

    c.sudo('systemctl restart decohogar-backend')
    c.sudo('systemctl restart nginx')

    c.sudo('systemctl status decohogar-backend')
    print('Deployed!')
