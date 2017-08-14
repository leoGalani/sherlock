import yaml

def prod_db():
    with open("docker-compose.yml", 'r') as ymlfile:
        docker_config = yaml.load(ymlfile)

    mysql_container = docker_config['services']['mysql']['container_name']
    base_pass = docker_config['services']['mysql']['environment']['MYSQL_ROOT_PASSWORD']
    base = docker_config['services']['mysql']['environment']['MYSQL_DATABASE']

    return 'root:{}@{}/{}'.format(base_pass,mysql_container, base)
