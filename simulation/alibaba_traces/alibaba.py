import csv
#import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
'''
### Calculate mean and median of batch tasks duration
job_task_duration = defaultdict(list)
infile = open('batch_task.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')
# For each machine, task running time is the params 6 - 5
for line in csv_reader:
    # Only consider termiinated tasks
    if line[4] != 'Terminated' or int(line[6]) < int(line[5]):
        continue
    task_duration = int(line[6]) - int(line[5])
    job_name = line[2]
    job_task_duration[job_name].append(task_duration)
infile.close()

job_mean  = []
for _, tasks_durations in job_task_duration.items():
    job_mean.append(sum(tasks_durations) / float(len(tasks_durations)))
#plt.plot(job_mean)
#plt.title('Mean task durations over jobs')
#plt.show()
job_mean.sort()
print "Mean task durations over all jobs is", np.mean(job_mean)," sec"
print "Median average task durations over jobs is", np.percentile(job_mean, 50), "sec"
print "90th and 99th percentile average task durations are ", np.percentile(job_mean, 90), "sec and ", np.percentile(job_mean, 99),"sec"
#plt.plot(job_median)
#plt.title('Median task durations over jobs')
#plt.show()
'''
'''

### Plot machines per failure domain
# There are 292 failue domains - 1 - 292
# There are 4034 machines in all
#failure_domain = {}
#for index in range(292):
#    failure_domain[index + 1] = 0
#infile = open('machine_meta.csv', 'r')
#csv_reader = csv.reader(infile, delimiter=',')
# For each machine, check if param 3 or 4 contain a particular failure domain
#for line in csv_reader:
#    if line[3] != '':
#        failure_domain[int(line[3])] += 1
#    if line[2] != '' and line[3] != '' and int(line[2]) != int(line[3]):
#        failure_domain[int(line[2])] += 1
#for domain in failure_domain:
#    if failure_domain[domain] > 0:
#        print "Domain ", domain, "has ", failure_domain[domain], "machines"
#x, y = zip(*(sorted(failure_domain.items())))
#plt.plot(x,y)
#plt.xlabel('Failure Domain ID') 
#plt.ylabel('Number of Machines')
#plt.title('Number of machines over failure domains')
#plt.show()
#infile.close()

### Calculate discrete values of CPUs and RAM
infile = open('machine_meta.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')
min_cpu = float('inf')
max_cpu = float('-inf')
min_ram = float('inf')
max_ram = float('-inf')
for line in csv_reader:
    cpu = int(line[4])
    ram = int(line[5])
    if cpu < min_cpu:
        min_cpu = cpu
    if cpu > max_cpu:
        max_cpu = cpu
    if ram < min_ram:
        min_ram = ram
    if ram > max_ram:
        max_ram = ram
print " Min cpu is ", min_cpu
print " Max cpu is ", max_cpu
print " Min ram is ", min_ram
print " Max ram is ", max_ram
infile.close()
### Plot CPU and RAM discrete values

### Stats on number of machines running containers, batch and co-located workload
all_machines = set()
infile = open('machine_meta.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')
for params in csv_reader:
    all_machines.add(params[0])
#4034    
print "Total number of machines (from machine_meta)", len(all_machines)    
infile.close()


containers = set()
machines_running_containers = set()
infile = open('container_meta.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')
for params in csv_reader:
    machines_running_containers.add(params[1])
    containers.add(params[0])
#4005
print "Total number of machines running containers (from container_meta)", len(machines_running_containers)    
infile.close()

machines_not_running_containers = set()
infile = open('machine_usage.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')
for params in csv_reader:
    machine = params[0]
    if machine not in machines_running_containers:
        machines_not_running_containers.add(machine)
#24        
print "Total number of machines not running containers", len(machines_not_running_containers)    
infile.close()

print "Total number of machines not running containers (from machine_usage - container_meta) 24"

infile = open('batch_machines', 'r')
machines_running_batch = set(infile.read().split(' '))
print "Total number of machines running batch instances (from batch_instances)", len(machines_running_batch) 

only_batch = machines_running_batch - machines_running_containers
print "Total number of machines running ONLY batch instances (from batch_instances - container_meta)", len(only_batch)
only_container = machines_running_containers - machines_running_batch
print "Total number of machines running ONLY container instances (from container_meta - batch_instances)", len(only_container)
only_colocated = machines_running_containers.intersection(machines_running_batch)
print "Total number of machines running BOTH container AND batch instances (from container_meta.intersection(batch_instances))", len(only_colocated)

no_mention_machines = all_machines - machines_running_batch - machines_running_containers
print "Machines in machine_meta but not in container or batch meta", no_mention_machines

### CPU utilization over time for machines hosting containers
cpu_containers_only = []
cpu_no_mention_machines_only = []
cpu_batch_only = []
cpu_colocated_machines_only = []
# File format - machine id, time stamp, cpu util
infile = open('machine_usage.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')

# For each machine, there are multiple data points
for line in csv_reader:
    machine = line[0]
    if line[2] == '':
        continue
    util = int(line[2])
    if machine in only_container:
        cpu_containers_only.append(util)
    if machine in only_batch:
        cpu_batch_only.append(util)
    if machine in only_colocated:
        cpu_colocated_machines_only.append(util)
    if machine in no_mention_machines:
        cpu_no_mention_machines_only.append(util)

cpu_containers_only.sort()
cpu_batch_only.sort()
cpu_colocated_machines_only.sort()
cpu_no_mention_machines_only.sort()

print "######### CPU Utilization Stats #######"
print "Mean CPU utilization for machines hosting containers only", np.mean(cpu_containers_only)
print "25th", np.percentile(cpu_containers_only, 25), "50th - ", np.percentile(cpu_containers_only, 50)
print "90th", np.percentile(cpu_containers_only, 90), "99th - ", np.percentile(cpu_containers_only, 99)
print "Mean CPU utilization for machines hosting batch only", np.mean(cpu_batch_only)
print "25th", np.percentile(cpu_batch_only, 25), "50th - ", np.percentile(cpu_batch_only, 50)
print "90th", np.percentile(cpu_batch_only, 90), "99th - ", np.percentile(cpu_batch_only, 99)
print "Mean CPU utilization for machines hosting both batch and container", np.mean(cpu_colocated_machines_only)
print "25th", np.percentile(cpu_colocated_machines_only, 25), "50th - ", np.percentile(cpu_colocated_machines_only, 50)
print "90th", np.percentile(cpu_colocated_machines_only, 90), "99th - ", np.percentile(cpu_colocated_machines_only, 99)
print "Mean CPU utilization for machines hosting neither batch or container", np.mean(cpu_no_mention_machines_only)
print "25th", np.percentile(cpu_no_mention_machines_only, 25), "50th - ", np.percentile(cpu_no_mention_machines_only, 50)
print "90th", np.percentile(cpu_no_mention_machines_only, 90), "99th - ", np.percentile(cpu_no_mention_machines_only, 99)
#cpu_file = open('cpu_utilization', 'a+')
#cpu_file.write("All CPU utilization figures\n")
#for item in cpu_containers_only:
#    cpu_file.write("%d " %item)
infile.close()
#cpu_file.close()
### CPU utilization over time for machines hosting containers
'''

### Co-location interference calculation
# Workaround. Bug in container_usage.csv where container_id is not visible
# So only considering container meta, and not container usage.
containers = set()
machines_running_containers = set()
machines_containers_mapping = {}
infile = open('container_meta.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')
for params in csv_reader:
    container = params[0]
    machine = params[1]
    timestamp = int(params[2])
    cpu_req = int(params[5])
    cpu_limit = int(params[6])
    machines_running_containers.add(machine)
    containers.add(container)
    # {machine:{timestamp:{container1:cpu, container2:cpu,...}, timestamp:{} ... }}
    if machine not in machines_containers_mapping.keys():
        machines_containers_mapping[machine] = {}
    if timestamp not in machines_containers_mapping[machine].keys():
        machines_containers_mapping[machine][timestamp] = {}
    machines_containers_mapping[machine][timestamp][container] = cpu_req
infile.close()

'''
# Filter out the dimension of cpu.
# Only consider the most common cpu request at that particular time instant.
# machine_ts_containers contains the cpu and list of containers that have requested for the same resources at the same time. 
# Then, cpu_util_percent from container_usage.csv can be applied to any of these containers.
machine_ts_containers = {}
for machine, value in machines_containers_mapping.items():
    if machine not in machine_ts_containers.keys():
        machine_ts_containers[machine] = {}
    for timestamp, cpu_container_value in value.items():
        cpu = sorted(cpu_container_value, key=lambda cpu: len(cpu_container_value[cpu]), reverse=True)[0]
        containers = cpu_container_value[cpu]
        assert(len(containers) > 0)
        machine_ts_containers[machine][timestamp] = [containers, cpu]
'''

# Now do the same for batch jobs for machines and timestamps - batch_instance
machines_batch_mapping = {}
infile = open('batch_instance.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')
for params in csv_reader:
    machine = params[7]
    # Only parse information if this machine is colocating batch with containers
    if machine not in machines_containers_mapping.keys():
       continue 
    instance_name = params[0]
    start_time = int(params[5])
    end_time = int(params[6])
    if params[10] != '':
        cpu_avg = float(params[10])
    if params[11] != '':
        cpu_max = float(params[11])
    if machine not in machines_batch_mapping.keys():
        machines_batch_mapping[machine] = []
    machines_batch_mapping[machine].append([instance_name, start_time, end_time, cpu_avg, cpu_max])   
infile.close()

# Now consolidate colocation information
# For this, obtain a machine - timestamp - {container:cpu,..., batch:cpu,..}
colocated_machines = {}
for machine in machines_batch_mapping.keys():
    batch_instances = machines_batch_mapping[machine]
    for timestamp in machines_containers_mapping[machine].keys():
        for instance_details in batch_instances:
            start_time = instance_details[1]
            end_time = instance_details[2]
            if timestamp <= end_time and timestamp >= start_time:
                #Colocated batch instance and container
                if machine not in colocated_machines.keys():
                    colocated_machines[machine] = {}
                if timestamp not in colocated_machines[machine].keys():
                    colocated_machines[machine][timestamp] = machines_containers_mapping[machine][timestamp].copy()
                batch_instance_name = instance_details[0]
                batch_cpu = instance_details[3]
                colocated_machines[machine][timestamp][batch_instance_name] = batch_cpu

### Calculate discrete values of CPUs and RAM
infile = open('machine_meta.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')
for line in csv_reader:
    machine = (line[0])
    #ts = (line[1])
    # machine_cpu is always = 96
    machine_cpu = int(line[4])
    if machine in colocated_machines.keys():
        for timestamp in colocated_machines[machine].keys():
            total_cpu = 0
            for name, cpu in colocated_machines[machine][timestamp].items():
                total_cpu += cpu
            if (total_cpu / 100) > machine_cpu:
                print "Got a colocation violation at ", machine, timestamp, machine_cpu, total_cpu
infile.close()
### Co-location interference calculation
