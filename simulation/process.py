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
# Format of the output file -
# ---------------------------
# Cluster Size 4000
# 50th Percentile - ..
# 90th Percentile - ..
# 99th Percentile - ..
#
# Cluster Size 8000
# ...


import sys
import numpy as np

if(len(sys.argv) != 6): 
    print "Incorrent number of parameters."
    sys.exit(1)

# Process the finished file which has the job response times recorded
# pypy process.py finished_file eagle short yahoo 4000 
infile = open(sys.argv[1], 'r')
outfile = open(sys.argv[2].lower()+"_"+sys.argv[3]+"_"+sys.argv[4], 'a+')
jobrunningtime = []
for line in infile:
    job_short_long = "short" if ('by_def:  0' in line) else "long"
    if job_short_long != sys.argv[3]:
        continue
    #This is the type of job we are looking for
    jobrunningtime.append(float(line.split('total_job_running_time: ')[1]))

infile.close()

jobrunningtime.sort()
outfile.write("%s\t%s\n"% ("Cluster Size ", sys.argv[5]))
outfile.write("%s\t%s\n"% ("50th percentile: ",  np.percentile(jobrunningtime, 50))) 
outfile.write("%s\t%s\n" % ("90th percentile: ", np.percentile(jobrunningtime, 90))) 
outfile.write("%s\t%s\n" % ("99th percentile: ", np.percentile(jobrunningtime, 99))) 
outfile.close()