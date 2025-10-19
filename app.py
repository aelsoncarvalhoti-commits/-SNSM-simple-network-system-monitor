import psutil
import platform
import json
import os
from time import sleep

on_off = True

t_wait = 15

partitions = {}

for p in psutil.disk_partitions(all=False):
    partitions[p.mountpoint] = f'{psutil.disk_usage(p.mountpoint).total/(1024**3):.2f}'

with open('system_infor.json', 'w') as system_infor:
    system_infor.writelines(
        json.dumps({
            'Sistem': f'Sistem: {platform.system()} {platform.release()}',
            'Arquitecture': f'{platform.machine()}',
            'Total of cores': f'{psutil.cpu_count(logical=False)}',
            'Total of threads': f'{psutil.cpu_count(logical=True)}',
            'Memory total': f'{psutil.virtual_memory().total / (1024**3):.2f}GB', 
            'Discs': partitions      
                    })
    )

while on_off:
    with open('log_file.txt', '+a') as log_file:
        log_file.writelines('teste')
    #cpu usage
    print(f'CPU usage porcentage: {psutil.cpu_percent(interval=1)}% ')
    print(f'Memory total: {psutil.virtual_memory().total / (1024**3):.2f}GB')
    #memory usage
    print(f'Memory usage porcentage: {psutil.virtual_memory().percent}%')

    print(f'Memory used: {psutil.virtual_memory().used / (1024**3):.2f}GB')

    print(f"Sistem: {platform.system()} {platform.release()}")
    print(f"Arquitetura: {platform.machine()}")
    print(f"Total of cores: {psutil.cpu_count(logical=False)}")
    print(f"Total of threads: {psutil.cpu_count(logical=True)}")

    print(f'{psutil.disk_usage('/').total/(1024**3):.2f}')

    net = psutil.net_io_counters()
    print(f"Bytes enviados: {net.bytes_sent}, Bytes recebidos: {net.bytes_recv}")
    sleep(t_wait)