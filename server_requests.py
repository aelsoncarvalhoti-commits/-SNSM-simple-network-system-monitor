import requests

# função responsável por mandar os dados para o servidor
def post_registers(system_infor: dict, log_file: dict, system_conf: dict) -> bool:
    data = {
        'system_infor': system_infor,
        'log': log_file,
        'conf': system_conf
    }

    print(data)

    try:
        response = requests.post(f'http://{system_conf['server_ip']}/api/post_informations', json=data)
        return True
    except(requests.exceptions.ConnectionError) as err:
        return False

def get_commands()-> bool:
    pass