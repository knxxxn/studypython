import psutil

cpu = psutil.cpu_freq() #cpu속도 출력
print(cpu)

cpu_core = psutil.cpu_count(logical=False) #cpu의 물리코어 수 출력
print(cpu_core)

memory = psutil.virtual_memory() #메모리의 정보 출력
print(memory)

disk = psutil.disk_partitions() #디스크 정보 출력
print(disk)

net = psutil.net_io_counters() #네트워크를 통해 보내고 받은 데이터량 출력
print(net)

