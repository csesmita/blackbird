# This file is used for generating CDF graphs of various JRT data collected,
# and comparing them against various systems.
#
# Command run in the following format -
# pypy process.py finished_file eagle short yahoo 4000 
#
# This indicates processing of Yahoo traces by Eagle simulator for short jobs
# with number of nodes in the cluster = 4000 and job response times given in
# finished file. This script gets called within the simulation_main.py file 
# when the finished file is generated for a run. All parameters are passed 
# from within it.
#
# Name of the Output file - eagle_short_yahoo
# This file gets overwritten for every run for the same scheduler design for
# the same set of traces for the same type of job for different cluster sizes.
#
# Format of the output files -
# ---------------------------
# Percentile file:
#
# Cluster Size 4000
# 50th Percentile - ..
# 90th Percentile - ..
# 99th Percentile - ..
#
# Cluster Size 8000
# ...
#
# Time comparison
# jobid : response_time
# jobid : response_time
# ...


import sys
import numpy as np
import operator

# Process the finished file which has the job response times recorded
# pypy process.py finished_file eagle short yahoo 4000 
infile = open("pigeon_results", 'r')
look_for = "long"
outfile = open("pigeon"+"_"+look_for+"_"+"3000", 'a+')
jobrunningtime = []
for line in infile:
    #jobid, short == 1, num_tasks, total_running_time, total_wait_time
    line_split = line.split("  ")
    print line_split[0], line_split[1], line_split[2], line_split[3], line_split[4]
    job_short_long = "short" if (int(line_split[1]) == 1) else "long"
    print job_short_long
    #This is the type of job we are looking for
    if job_short_long != look_for:
        continue
    runningtime = float(line_split[3])
    jobrunningtime.append(runningtime)

infile.close()

print jobrunningtime.sort()
outfile.write("%s\t%s\n"% ("Cluster Size ", "3000"))
outfile.write("%s\t%s\n"% ("50th percentile: ",  np.percentile(jobrunningtime, 50)))
outfile.write("%s\t%s\n" % ("90th percentile: ", np.percentile(jobrunningtime, 90)))
outfile.write("%s\t%s\n" % ("99th percentile: ", np.percentile(jobrunningtime, 99)))
outfile.close()
