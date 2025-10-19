import psutil
import platform
import json
import os
from time import sleep

on_off = True

t_wait = 15

'''
    Parte responsável por gerar log de informação do sistema.
    por padrão ela so irá executar uma vez quando o app é executado
'''
partitions = {}

# Pega as unidades de disco e salva na variável partition
for p in psutil.disk_partitions(all=False):
    partitions[p.mountpoint] = f'{psutil.disk_usage(p.mountpoint).total/(1024**3):.2f}GB Total | {psutil.disk_usage(p.mountpoint).used/(1024**3):.2f}GB'

# Gera o arquivo de informação do sistema
with open('system_infor.json', 'w') as system_infor:
    system_infor.writelines(
        json.dumps({
            'Sistem': f'Sistem: {platform.system()} {platform.release()}', # Sistema operacional e sua versão
            'Arquitecture': f'{platform.machine()}', # Arquitetura do sistema
            'Total of cores': f'{psutil.cpu_count(logical=False)}', # numero de núcleos físicos do processador
            'Total of threads': f'{psutil.cpu_count(logical=True)}', # Numero de threads do processador
            'Memory total': f'{psutil.virtual_memory().total / (1024**3):.2f}GB', # Quantidade total de memória do sistema
            'Discs': partitions # pega a variavel partitions e salva os discos     
                    })
    )

while on_off:
    net = psutil.net_io_counters()

    data = {
                'CPU usage porcentage': f'{psutil.cpu_percent(interval=1)}%',
                'Memory usage porcentage:': f'{psutil.virtual_memory().percent}%',
                'Total of memory used': f'{psutil.virtual_memory().used / (1024**3):.2f}GB',
                'Internet bytes enviados': net.bytes_sent,
                'Internet bytes recebidos': net.bytes_recv
            }
    
    try:
        with open('log_file.json', 'r') as log_file:
            logs = json.load(log_file)
    except(json.JSONDecodeError, FileNotFoundError):
        logs = []

    logs.append(data)

    with open('log_file.json', 'w') as log_file:
        json.dump(logs, log_file, indent=4)
    
    sleep(t_wait)