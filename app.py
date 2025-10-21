import psutil
import platform
import json
import os
from time import sleep
import datetime
from server_requests import *

config_load = {}

try:
    with open('system_conf.json', 'r') as system_conf:
        config_load = json.load(system_conf)
except(json.JSONDecodeError, FileNotFoundError) as err_json:
    with open('erro_log.txt', 'a') as erro_log:
        erro_log.writelines(f'{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}: Error in open system config file {str(erro_log)} \n')

## Configurações do sistema 
on_off = True
system_name = config_load['system_name']
t_wait = config_load['monitor_timing']
server = config_load['server']

'''
    Parte responsável por gerar log de informação do sistema.
    por padrão ela so irá executar uma vez quando o app é executado
'''
partitions = {}
system_data = {
                'system': f'{platform.system()} {platform.release()}', # Sistema operacional e sua versão
                'arquitecture': f'{platform.machine()}', # Arquitetura do sistema
                'total_of_cores': f'{psutil.cpu_count(logical=False)}', # numero de núcleos físicos do processador
                'total_of_threads': f'{psutil.cpu_count(logical=True)}', # Numero de threads do processador
                'total_of_memory': f'{psutil.virtual_memory().total / (1024**3):.2f}GB', # Quantidade total de memória do sistema
                'discs': partitions # pega a variavel partitions e salva os discos     
                }

# Pega as unidades de disco e salva na variável partition
for p in psutil.disk_partitions(all=False):
    partitions[p.mountpoint] = f'{psutil.disk_usage(p.mountpoint).total/(1024**3):.2f}GB Total | {psutil.disk_usage(p.mountpoint).used/(1024**3):.2f}GB'

# Gera o arquivo de informação do sistema

try:
    with open('system_infor.json', 'w') as system_infor:
        system_infor.writelines(
            json.dumps(system_data)
        )
except(json.JSONDecodeError, FileNotFoundError) as err_json:
    with open('erro_log.txt', 'w') as erro_log:
        erro_log.writelines(f'{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}: Error in save log file {str(erro_log)} \n')

while on_off:
    net = psutil.net_io_counters()

    data = {
                'date_time': datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                'cpu_usage_porcentage': f'{psutil.cpu_percent(interval=1)}%',
                'memory_usage_porcentage': f'{psutil.virtual_memory().percent}%',
                'total_of_memory_used': f'{psutil.virtual_memory().used / (1024**3):.2f}GB',
                'internet_bytes_enviados': net.bytes_sent,
                'internet_bytes_recebidos': net.bytes_recv
            }
    
    try:
        with open('log_file.json', 'r') as log_file:
            logs = json.load(log_file)
    except(json.JSONDecodeError, FileNotFoundError):
        logs = []

    logs.append(data)

    with open('log_file.json', 'w') as log_file:
        json.dump(logs, log_file, indent=4)

    if(server == True):
        post_status = post_registers(system_data, data, config_load)
        commands = get_commands()
    
    sleep(t_wait)