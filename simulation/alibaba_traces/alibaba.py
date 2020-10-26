import csv
import os
#import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

timestamps = []
line_numbers = []
def insertion(line_num, timestamp):
    to_print = False
    global timestamps
    global line_numbers
    pos = 0 
    if to_print:
        print "Inserting - ", timestamp
    while pos in range(len(timestamps)):
        if timestamp >= timestamps[pos]:
            pos += 1
            continue
        break
    timestamps.insert(pos, timestamp)
    if to_print:
        print "Ending with timestamps - ", timestamps
    line_numbers.insert(pos, line_num)

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
infile.close()

only_batch = machines_running_batch - machines_running_containers
print "Total number of machines running ONLY batch instances (from batch_instances - container_meta)", len(only_batch)
only_container = machines_running_containers - machines_running_batch
print "Total number of machines running ONLY container instances (from container_meta - batch_instances)", len(only_container)
only_colocated = machines_running_containers.intersection(machines_running_batch)
print "Total number of machines running BOTH container AND batch instances (from container_meta.intersection(batch_instances))", len(only_colocated)

no_mention_machines = all_machines - machines_running_batch - machines_running_containers
print "Machines in machine_meta but not in container or batch meta", no_mention_machines

colocated_file = open('colocated_machines_list', 'a+')
for machine in only_colocated:
    colocated_file.write("%s " %machine)
colocated_file.close()

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
infile.close()

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
### CPU utilization over time for machines hosting containers

'''
### Co-location interference calculation
# Workaround. Bug in container_usage.csv where container_id is not visible
# So only considering container meta, and not container usage.
machines_containers_mapping = {}
infile = open('container_meta.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')
#outfile = open('machines_containers_mapping', 'w+')
for params in csv_reader:
    container = params[0]
    machine = params[1]
    timestamp = int(params[2])
    cpu_req = int(params[5])
    cpu_limit = int(params[6])
    # {machine:{timestamp:{container1:cpu, container2:cpu,...}, timestamp:{} ... }}
    if machine not in machines_containers_mapping.keys():
        machines_containers_mapping[machine] = {}
    if timestamp not in machines_containers_mapping[machine].keys():
        machines_containers_mapping[machine][timestamp] = {}
    machines_containers_mapping[machine][timestamp][container] = cpu_req
    #outfile.write("%s,%d,%s,%f\n"% (machine, timestamp, container, cpu_req))
infile.close()
#outfile.close()

# Now do the same for batch jobs for machines and timestamps - batch_instance
#machines_batch_mapping = {}
infile = open('batch_instance.csv', 'r')
#outfile = open('machines_batch_mapping', 'w+')
csv_reader = csv.reader(infile, delimiter=',')
count = 0
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
    #outfile.write("%s,%s,%d,%d,%f,%f\n"% (machine, instance_name, start_time, end_time, cpu_avg, cpu_max))
    count += 1
    if count == 3000:
        outfile.flush()
        os.fsync(outfile)
        count = 0
infile.close()
#outfile.close()

for machine in machines_containers_mapping.keys():
    if machine not in machines_batch_mapping.keys():
        del machines_containers_mapping[machine]

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
infile = open('machine_meta.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')
previous_machine = ''
for line in csv_reader:
    machine = (line[0])
    if machine == previous_machine:
        continue
    # machine_cpu is always = 96
    machine_cpu = int(line[4])
    if machine in colocated_machines.keys():
        for timestamp in colocated_machines[machine].keys():
            total_cpu = 0.0
            names = []
            for name, cpu in colocated_machines[machine][timestamp].items():
                total_cpu += cpu
                names.append(name)
            total_cpu = total_cpu / 100.0  
            if total_cpu > machine_cpu:
                print "Got a colocation violation at ", machine, timestamp, "cpu = ",total_cpu, names
    previous_machine = machine
infile.close()
### Co-location interference calculation

##### Filter all CSV files for info only on colocated machines
infile = open('results/colocated_machines_list', 'r')
colocated_machines = set(infile.read().split(' '))
print "Total number of machines running BOTH container and batch instances", len(colocated_machines) 
infile.close()

infile = open('container_usage.csv', 'r')
outfile = open('filtered_container_usage.csv', 'w+')
csv_reader = csv.reader(infile, delimiter=',')
for params in csv_reader:
    if params[1] in colocated_machines:
        for param in params:
            outfile.write("%s, " %param)
        outfile.write("\n")
infile.close()
outfile.close()

##### Generation of Trace File for DC Utilization calculcation in colocated machines
infile = open('batch_task.csv', 'r')
outfile = open('batch_traces', 'w+')
write = csv.writer(outfile)
csv_reader = csv.reader(infile, delimiter=',')
batch_traces = {}
count = 0    
for params in csv_reader:
    task_name = params[0]
    instance_num = int(params[1]) if params[1] != '' else 0
    job_name = params[2]
    task_type = params[3]
    status = params[4]
    start_time = int(params[5])
    end_time = int(params[6]) if int(params[6]) > 0 else float('inf')
    plan_cpu = float(params[7]) if params[7] != '' else 0.0
    if start_time > end_time:
        print params
    if job_name not in batch_traces.keys():
        # Arrival time is assumed to be the start time of the earliest task.
        # Number of tasks to place for the job = sum(instance_num) over tasks.
        # For now, marking cpu_avg and cpu_max both 0. They will come from batch_instances.csv.
        batch_traces[job_name] = [start_time, instance_num, 0, [end_time - start_time], [plan_cpu], [0], [0], job_name, [task_name], [task_type], [status]]
    else:    
        # Store the smallest timestamp seen.
        if start_time < batch_traces[job_name][0]:
            batch_traces[job_name][0] = start_time
        # Increment number of tasks
        batch_traces[job_name][1] += instance_num
        batch_traces[job_name][3].append(end_time- start_time)
        batch_traces[job_name][4].append(plan_cpu)
        batch_traces[job_name][5].append(0)
        batch_traces[job_name][6].append(0)
        batch_traces[job_name][8].append(task_name)
        batch_traces[job_name][9].append(task_type)
        batch_traces[job_name][10].append(status)

for job_name in batch_traces.keys():
    # Flatten the list
    flat_list = []
    job_list = batch_traces[job_name]
    for sublist in job_list:
        if isinstance(sublist, list):
            for item in sublist:
                flat_list.append(item)
    write.writerow(flat_list)
    count += 1
    if count == 5000:
        outfile.flush()
        os.fsync(outfile)
        count = 0
infile.close()
outfile.close()

timestamps = []
line_numbers = []
def insertion(line_num, timestamp):
    global timestamps
    global line_numbers
    pos = 0 
    while pos in range(len(timestamps)):
        if timestamp >= timestamps[pos]:
            pos += 1
            continue
        break
    timestamps.insert(pos, timestamp)
    line_numbers.insert(pos, line_num)


print "Process container_meta"
infile = open('container_meta.csv', 'r')
outfile = open('container_traces', 'w+')
write = csv.writer(outfile, delimiter=' ')
csv_reader = csv.reader(infile, delimiter=',')
container_traces = {}
count = 0
for params in csv_reader:
    job_name = params[0]
    machine_id = params[1]
    time_stamp = int(params[2])
    app_du = params[3]
    status = params[4]
    cpu_req = int(params[5])/100
    cpu_limit = int(params[6])/100
    if job_name not in container_traces.keys():
        # Arrival time is assumed to be the start time of the earliest task.
        # Number of tasks to place for the job = sum(instance_num) over tasks.
        # For now, marking cpu_avg and cpu_max both 0. They will come from container_usage.csv.
        container_traces[job_name] = [time_stamp,1, 0, 0, cpu_req, 0, cpu_limit, job_name, machine_id, app_du, status]
        continue
    # Store the smallest timestamp seen, and the current duration.
    if time_stamp < container_traces[job_name][0]:
        container_traces[job_name][0] = time_stamp
    if time_stamp > container_traces[job_name][0]:
        container_traces[job_name][3] = time_stamp - container_traces[job_name][0]

print "Write container_traces"
for job_name in container_traces.keys():
    write.writerow(container_traces[job_name])
    count += 1
    if count == 5000:
        outfile.flush()
        os.fsync(outfile)
        count = 0
infile.close()
outfile.close()

print "Read traces for tiemstamp arrangement"
infile = open("container_traces", 'r')
csv_reader = csv.reader(infile, delimiter=' ')
line_num = 0
lines = []
for line in csv_reader:
    timestamp_value = int(line[0]) 
    insertion(line_num, timestamp_value)
    line_num += 1
    lines.append(line)
infile.close()

print "Write timestamped traces file"
outfile = open("container_traces_timestamped", 'w+')
write = csv.writer(outfile, delimiter=' ')
count = 0
for idx in line_numbers:
    write.writerow(lines[idx])
    count += 1
    if count == 5000:
        outfile.flush()
        os.fsync(outfile)
        count = 0
outfile.close()

infile = open('batch_task.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')
matches = 0
count = 0
for params in csv_reader:
    task_name = params[0]
    hash_task_name = hash(task_name) % 31
    count += 1
    if hash_task_name == 1:
        matches += 1

##### Generation of Trace File for DC Utilization calculcation in colocated machines
infile = open('batch_task.csv', 'r')
outfile = open('batch_traces', 'w+')
write = csv.writer(outfile)
csv_reader = csv.reader(infile, delimiter=',')
batch_traces = {}
count = 0    
for params in csv_reader:
    task_name = params[0]
    instance_num = int(params[1]) if params[1] != '' else 0
    job_name = params[2]
    task_type = params[3]
    status = params[4]
    start_time = int(params[5])
    end_time = int(params[6]) if int(params[6]) > 0 else float('inf')
    plan_cpu = float(params[7]) if params[7] != '' else 0.0
    if start_time > end_time:
        print params
    if job_name not in batch_traces.keys():
        # Arrival time is assumed to be the start time of the earliest task.
        # Number of tasks to place for the job = sum(instance_num) over tasks.
        # For now, marking cpu_avg and cpu_max both 0. They will come from batch_instances.csv.
        batch_traces[job_name] = [start_time, instance_num, 0, [end_time - start_time], [plan_cpu], [0], [0], job_name, [task_name], [task_type], [status]]
    else:    
        # Store the smallest timestamp seen.
        if start_time < batch_traces[job_name][0]:
            batch_traces[job_name][0] = start_time
        # Increment number of tasks
        batch_traces[job_name][1] += instance_num
        batch_traces[job_name][3].append(end_time- start_time)
        batch_traces[job_name][4].append(plan_cpu)
        batch_traces[job_name][5].append(0)
        batch_traces[job_name][6].append(0)
        batch_traces[job_name][8].append(task_name)
        batch_traces[job_name][9].append(task_type)
        batch_traces[job_name][10].append(status)

for job_name in batch_traces.keys():
    # Flatten the list
    flat_list = []
    job_list = batch_traces[job_name]
    for sublist in job_list:
        if isinstance(sublist, list):
            for item in sublist:
                flat_list.append(item)
    write.writerow(flat_list)
    count += 1
    if count == 5000:
        outfile.flush()
        os.fsync(outfile)
        count = 0
infile.close()
outfile.close()

'''       
