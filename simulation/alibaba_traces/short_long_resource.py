import csv
import os
#import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

### Calculate mean and median of batch tasks duration
#job_task_duration = defaultdict(list)
job_task_cpu = defaultdict(list)
job_duration = {}
infile = open('batch_task.csv', 'r')
csv_reader = csv.reader(infile, delimiter=',')
count = 0
# For each machine, task running time is the params 6 - 5
for line in csv_reader:
    # Only consider termiinated tasks
    if int(line[6]) < int(line[5]):
        continue
    job_name = line[2]
    if hash(job_name) % 101 == 0 and line[7] != '':
        start_time = int(line[5])
        end_time = int(line[6])
        task_duration = end_time - start_time
        cpu = int(line[7])
        #job_task_duration[job_name].append(task_duration)
        job_task_cpu[job_name].append(cpu)
infile.close()

job_mean  = []
#for _, tasks_durations in job_task_duration.items():
for _, tasks_cpus in job_task_cpu.items():
    job_mean.append(sum(tasks_cpus) / float(len(tasks_cpus)))
job_mean.sort()
print "Mean task cpus over all jobs is", np.mean(job_mean)
print "Median average task cpus over jobs is", np.percentile(job_mean, 50)
print "90th and 99th percentile average task cpus are ", np.percentile(job_mean, 90), "and ", np.percentile(job_mean, 99)

'''
job_total_dur = []
for job_name in job_duration.keys():
    job_total_dur.append(job_duration[job_name][1] - job_duration[job_name][0])
job_total_dur.sort()
print "Mean job durations over all jobs is", np.mean(job_total_dur)," sec"
print "Median durations over jobs is", np.percentile(job_total_dur, 50), "sec"
print "90th and 99th percentile job durations are ", np.percentile(job_total_dur, 90), "sec and ", np.percentile(job_total_dur, 99),"sec"

'''
