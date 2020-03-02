#
# EAGLE 
#
# Copyright 2016 Operating Systems Laboratory EPFL
#
# Modified from Sparrow - University of California, Berkeley 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#



import sys
import time
import logging
import random
import Queue
import bitmap
import copy
import collections
import pdb

class TaskDurationDistributions:
    CONSTANT, MEAN, FROM_FILE  = range(3)
class EstimationErrorDistribution:
    CONSTANT, RANDOM, MEAN  = range(3)

class Job(object):
    job_count = 1
    per_job_task_info = {}

    def __init__(self, task_distribution, line, estimate_distribution, off_mean_bottom, off_mean_top):
        global job_start_tstamps

        job_args                    = (line.split('\n'))[0].split()
        self.start_time             = float(job_args[0])
        self.num_tasks              = int(job_args[1])
        mean_task_duration          = int(float(job_args[2]))

        #dephase the incoming job in case it has the exact submission time as another already submitted job
        if self.start_time not in job_start_tstamps:
            job_start_tstamps[self.start_time] = self.start_time
        else:
            job_start_tstamps[self.start_time] += 0.01
            self.start_time = job_start_tstamps[self.start_time]
        
        self.id = Job.job_count
        Job.job_count += 1
        self.completed_tasks_count = 0
        self.end_time = self.start_time
        self.unscheduled_tasks = collections.deque()
        self.off_mean_bottom = off_mean_bottom
        self.off_mean_top = off_mean_top

        self.job_type_for_scheduling = BIG
        self.job_type_for_comparison = BIG

        self.file_task_execution_time(job_args)
        self.estimate_distribution = estimate_distribution

        if   estimate_distribution == EstimationErrorDistribution.MEAN:
            self.estimated_task_duration = mean_task_duration
        elif estimate_distribution == EstimationErrorDistribution.CONSTANT:
            self.estimated_task_duration = int(mean_task_duration+off_mean_top*mean_task_duration)
        elif estimate_distribution == EstimationErrorDistribution.RANDOM:
            top = off_mean_top*mean_task_duration
            bottom = off_mean_bottom*mean_task_duration
            self.estimated_task_duration = int(random.uniform(bottom,top)) 
            assert(self.estimated_task_duration <= int(top))
            assert(self.estimated_task_duration >= int(bottom))

        self.probed_workers = set()

    #Job class    """ Returns true if the job has completed, and false otherwise. """
    def update_task_completion_details(self, completion_time):
        self.completed_tasks_count += 1
        self.end_time = max(completion_time, self.end_time)
        assert self.completed_tasks_count <= self.num_tasks
        return self.num_tasks == self.completed_tasks_count


    #Job class
    def file_task_execution_time(self, job_args):
        for task_duration in (job_args[3:]):
           self.unscheduled_tasks.appendleft(int(float(task_duration)))
        assert(len(self.unscheduled_tasks) == self.num_tasks)

#####################################################################################################################
#####################################################################################################################
class Stats(object):
    STATS_TASKS_TOTAL_FINISHED = 0
    STATS_TASKS_LONG_FINISHED = 0   

#####################################################################################################################
#####################################################################################################################
class Event(object):
    def __init__(self):
        raise NotImplementedError("Event is an abstract class and cannot be instantiated directly")

    def run(self, current_time):
        """ Returns any events that should be added to the queue. """
        raise NotImplementedError("The run() method must be implemented by each class subclassing Event")

#####################################################################################################################
#####################################################################################################################

class JobArrival(Event, file):

    def __init__(self, simulation, task_distribution, job, jobs_file):
        self.simulation = simulation
        self.task_distribution = task_distribution
        self.job = job
        self.jobs_file = jobs_file

    def run(self, current_time):
        print(current_time, ":   Big Job arrived!!", self.job.id, " num tasks ", self.job.num_tasks, " estimated_duration ", self.job.estimated_task_duration)
        btmap = self.simulation.cluster_status_keeper.get_btmap()

        workers_queue_status = self.simulation.cluster_status_keeper.get_queue_status()
        possible_workers = self.simulation.big_partition_workers_hash
        worker_indices = self.simulation.find_workers_long_job_prio(self.job.num_tasks, self.job.estimated_task_duration, workers_queue_status, current_time, self.simulation, possible_workers)
        self.simulation.cluster_status_keeper.update_workers_queue(worker_indices, True, self.job.estimated_task_duration)

        Job.per_job_task_info[self.job.id] = {}
        for tasknr in range(0,self.job.num_tasks):
            Job.per_job_task_info[self.job.id][tasknr] =- 1

        new_events = self.simulation.send_probes(self.job, current_time, worker_indices, btmap)

        # Creating a new Job Arrival event for the next job in the trace
        line = self.jobs_file.readline()
        if (line == ''):
            return new_events

        self.job = Job(self.task_distribution, line, self.job.estimate_distribution, self.job.off_mean_bottom, self.job.off_mean_top)
        new_events.append((self.job.start_time, self))
        self.simulation.jobs_scheduled += 1
        return new_events


#####################################################################################################################
#####################################################################################################################

class PeriodicTimerEvent(Event):
    def __init__(self,simulation):
        self.simulation = simulation

    def run(self, current_time):
        new_events = []
        total_load       = str(int(10000*(1-self.simulation.total_free_slots*1.0/(TOTAL_WORKERS*SLOTS_PER_WORKER)))/100.0)
        big_load         = str(int(10000*(1-self.simulation.free_slots_big_partition*1.0/len(self.simulation.big_partition_workers)))/100.0)
        print >> load_file,"total_load: " + total_load + " big_load: " + big_load + " current_time: " + str(current_time)

        if(not self.simulation.event_queue.empty()):
            new_events.append((current_time + MONITOR_INTERVAL,self))
        return new_events

#####################################################################################################################
#####################################################################################################################

class ProbeEvent(Event):
    def __init__(self, worker, job_id, task_length, job_type_for_scheduling, btmap):
        self.worker = worker
        self.job_id = job_id
        self.task_length = task_length
        self.job_type_for_scheduling = job_type_for_scheduling
        self.btmap = btmap

    def run(self, current_time):
        return self.worker.add_probe(self.job_id, self.task_length, self.job_type_for_scheduling, current_time,self.btmap)

#####################################################################################################################
#####################################################################################################################

class ClusterStatusKeeper():
    def __init__(self):
        self.worker_queues = {}
        self.btmap = bitmap.BitMap(TOTAL_WORKERS)
        for i in range(0, TOTAL_WORKERS):
           self.worker_queues[i] = 0


    def get_queue_status(self):
        return self.worker_queues

    def get_btmap(self):
        return self.btmap

    def update_workers_queue(self, worker_indices, increase, duration):
        for worker in worker_indices:
            queue = self.worker_queues[worker]
            if increase:
                queue += duration
                self.btmap.set(worker) 
            else:
                queue -= duration
                if(queue == 0):
                    self.btmap.flip(worker) 
            assert queue >= 0, (" offending value for queue: %r %i " % (queue,worker))
            self.worker_queues[worker] = queue

#####################################################################################################################
#####################################################################################################################

class NoopGetTaskResponseEvent(Event):
    def __init__(self, worker):
        self.worker = worker

    def run(self, current_time):
        return self.worker.free_slot(current_time)

#####################################################################################################################
#####################################################################################################################

class TaskEndEvent():
    def __init__(self, worker, status_keeper, job_id, job_type_for_scheduling, estimated_task_duration, this_task_id):
        self.worker = worker
        self.status_keeper = status_keeper
        self.job_id = job_id
        self.job_type_for_scheduling = job_type_for_scheduling
        self.estimated_task_duration = estimated_task_duration
        self.this_task_id = this_task_id

    def run(self, current_time):
        global stats
        stats.STATS_TASKS_TOTAL_FINISHED += 1
        self.status_keeper.update_workers_queue([self.worker.id], False, self.estimated_task_duration)
        del Job.per_job_task_info[self.job_id][self.this_task_id]
        self.worker.tstamp_start_crt_big_task =- 1
        return self.worker.free_slot(current_time)


#####################################################################################################################
#####################################################################################################################

class Worker(object):
    def __init__(self, simulation, num_slots, id, index_first_big):
        self.simulation = simulation
        # List of times when slots were freed, for each free slot (used to track the time the worker spends idle).
        self.free_slots = []
        while len(self.free_slots) < num_slots:
            self.free_slots.append(0)

        self.queued_big = 0
        self.queued_probes = []
        self.id = id
        self.executing_big = False
        self.tstamp_start_crt_big_task = -1
        self.estruntime_crt_task = -1
        assert(id >= index_first_big)
        self.in_big = True
        self.btmap = None

    #Worker class
    def add_probe(self, job_id, task_length, job_type_for_scheduling, current_time, btmap):
        global stats
        self.queued_probes.append([job_id,task_length,(self.executing_big == True or self.queued_big > 0)])
        self.queued_big     = self.queued_big + 1
        self.btmap          = copy.deepcopy(btmap)

        if len(self.queued_probes) > 0 and len(self.free_slots) > 0:
            return self.process_next_probe_in_the_queue(current_time)
        else:
            return []

    #Worker class
    def free_slot(self, current_time):
        self.free_slots.append(current_time)
        self.simulation.increase_free_slots_for_load_tracking(self)
        self.executing_big = False

        if len(self.queued_probes) > 0:
            return self.process_next_probe_in_the_queue(current_time)
        
        return []

    #Worker class
    def process_next_probe_in_the_queue(self, current_time):
        global stats
        self.free_slots.pop(0)
        self.simulation.decrease_free_slots_for_load_tracking(self)
        pos = 0
        job_id = self.queued_probes[pos][0]
        estimated_task_duration = self.queued_probes[pos][1]

        self.executing_big = self.simulation.jobs[job_id].job_type_for_scheduling == BIG
        if self.executing_big:
            self.queued_big                 = self.queued_big -1
            self.tstamp_start_crt_big_task  = current_time
            self.estruntime_crt_task        = estimated_task_duration
        else:
            self.tstamp_start_crt_big_task = -1

        was_successful, events = self.simulation.get_task(job_id, self, current_time)
        job_bydef_big = (self.simulation.jobs[job_id].job_type_for_comparison == BIG)

        if(not was_successful or job_bydef_big):
            #so the probe remains if SBP is on, was succesful and is small        
            self.queued_probes.pop(pos)

        return events

#####################################################################################################################
#####################################################################################################################

class Simulation(object):
    def __init__(self, WORKLOAD_FILE,ESTIMATION,off_mean_bottom,off_mean_top,nr_workers):
        TOTAL_WORKERS = int(nr_workers)
        self.total_free_slots = SLOTS_PER_WORKER * TOTAL_WORKERS
        self.jobs = {}
        self.event_queue = Queue.PriorityQueue()
        self.workers = []

        while len(self.workers) < TOTAL_WORKERS:
            self.workers.append(Worker(self, SLOTS_PER_WORKER, len(self.workers),0))
        self.worker_indices = range(TOTAL_WORKERS)
        self.off_mean_bottom = off_mean_bottom
        self.off_mean_top = off_mean_top
        self.ESTIMATION = ESTIMATION
        self.big_partition_workers_hash = {}

        self.big_partition_workers = self.worker_indices[0:]         # so including the worker before :
        for node in self.big_partition_workers:
            self.big_partition_workers_hash[node] = 1

        print("Size of self.big_partition_workers_hash:           ", len(self.big_partition_workers_hash))

        self.free_slots_big_partition = len(self.big_partition_workers)
        self.jobs_scheduled = 0
        self.cluster_status_keeper = ClusterStatusKeeper()
        self.WORKLOAD_FILE = WORKLOAD_FILE

        self.btmap = None

    #Simulation class
    def find_workers_long_job_prio(self, num_tasks, estimated_task_duration, workers_queue_status, current_time, simulation, hash_workers_considered):
        workers_needed = num_tasks
        prio_queue = Queue.PriorityQueue()

        empty_nodes = []  #performance optimization
        for index in hash_workers_considered:
            qlen          = workers_queue_status[index]                
            worker_obj    = simulation.workers[index]
            worker_id     = index

            if qlen == 0 :
                empty_nodes.append(worker_id)
                if(len(empty_nodes) == workers_needed):
                    break
            else: 
                start_of_crt_big_task = worker_obj.tstamp_start_crt_big_task
                assert(current_time >= start_of_crt_big_task)
                adjusted_waiting_time = qlen

                if(start_of_crt_big_task != -1):
                    executed_so_far = current_time - start_of_crt_big_task
                    estimated_crt_task = worker_obj.estruntime_crt_task
                    adjusted_waiting_time = 2*NETWORK_DELAY + qlen - min(executed_so_far,estimated_crt_task)

                assert adjusted_waiting_time >= 0, " offending value for adjusted_waiting_time: %r" % adjusted_waiting_time                 
                prio_queue.put((adjusted_waiting_time,worker_id))

        #performance optimization 
        if(len(empty_nodes) == workers_needed):
            return empty_nodes
        else:
            chosen_worker_indices = empty_nodes
            for nodeid in chosen_worker_indices:
                prio_queue.put((estimated_task_duration,nodeid))

        queue_length,worker = prio_queue.get()
        while (workers_needed > len(chosen_worker_indices)):
            next_queue_length,next_worker = prio_queue.get()
            while(queue_length <= next_queue_length and len(chosen_worker_indices) < workers_needed):
                chosen_worker_indices.append(worker)
                queue_length += estimated_task_duration

            prio_queue.put((queue_length,worker))
            queue_length = next_queue_length
            worker = next_worker 

        assert workers_needed == len(chosen_worker_indices)
        return chosen_worker_indices

    #Simulation class
    def send_probes(self, job, current_time, worker_indices, btmap):
        return self.send_probes_eagle(job, current_time, worker_indices, btmap)

    #Simulation class
    def send_probes_eagle(self, job, current_time, worker_indices, btmap):
        global stats
        self.jobs[job.id] = job
        probe_events = []
        pdb.set_trace()
        for worker_index in worker_indices:
            probe_events.append((current_time + NETWORK_DELAY, ProbeEvent(self.workers[worker_index], job.id, job.estimated_task_duration, job.job_type_for_scheduling, btmap)))
            job.probed_workers.add(worker_index)
        
        return probe_events

    #Simulation class
    #bookkeeping for tracking the load
    def increase_free_slots_for_load_tracking(self, worker):
        self.total_free_slots += 1
        assert(worker.in_big)
        self.free_slots_big_partition += 1


    #Simulation class
    #bookkeeping for tracking the load
    def decrease_free_slots_for_load_tracking(self, worker):
        self.total_free_slots -= 1
        assert(worker.in_big)
        self.free_slots_big_partition -= 1


    #Simulation class
    def get_task(self, job_id, worker, current_time):
        job = self.jobs[job_id]
        #account for the fact that this is called when the probe is launched but it needs an RTT to talk to the scheduler
        get_task_response_time = current_time + 2 * NETWORK_DELAY
        
        if len(job.unscheduled_tasks) == 0 :
            return False, [(get_task_response_time, NoopGetTaskResponseEvent(worker))]

        this_task_id=job.completed_tasks_count
        Job.per_job_task_info[job_id][this_task_id] = current_time
        events = []
        task_duration = job.unscheduled_tasks.pop()
        task_completion_time = task_duration + get_task_response_time
        print(current_time, " worker:", worker.id, " task from job ", job_id, " task duration: ", task_duration, " will finish at time ", task_completion_time)
        is_job_complete = job.update_task_completion_details(task_completion_time)

        if is_job_complete:
            print >> finished_file, task_completion_time," estimated_task_duration: ",job.estimated_task_duration, " by_def: ",job.job_type_for_comparison, " total_job_running_time: ",(job.end_time - job.start_time)

        events.append((task_completion_time, TaskEndEvent(worker, self.cluster_status_keeper, job.id, job.job_type_for_scheduling, job.estimated_task_duration, this_task_id)))

        if len(job.unscheduled_tasks) == 0:
            logging.info("Finished scheduling tasks for job %s" % job.id)
        return True, events

    #Simulation class
    def run(self):
        last_time = 0

        self.jobs_file = open(self.WORKLOAD_FILE, 'r')

        self.task_distribution = TaskDurationDistributions.FROM_FILE

        estimate_distribution = EstimationErrorDistribution.MEAN
        if(self.ESTIMATION == "MEAN"):
            estimate_distribution = EstimationErrorDistribution.MEAN
            self.off_mean_bottom = self.off_mean_top = 0
        elif(self.ESTIMATION == "CONSTANT"):
            estimate_distribution = EstimationErrorDistribution.CONSTANT
            assert(self.off_mean_bottom == self.off_mean_top)
        elif(self.ESTIMATION == "RANDOM"):
            estimate_distribution = EstimationErrorDistribution.RANDOM
            assert(self.off_mean_bottom > 0)
            assert(self.off_mean_top > 0)
            assert(self.off_mean_top>self.off_mean_bottom)

        line = self.jobs_file.readline()
        new_job = Job(self.task_distribution, line, estimate_distribution, self.off_mean_bottom, self.off_mean_top)
        self.event_queue.put((float(line.split()[0]), JobArrival(self, self.task_distribution, new_job, self.jobs_file)))
        self.jobs_scheduled = 1
        self.event_queue.put((float(line.split()[0]), PeriodicTimerEvent(self)))

        while (not self.event_queue.empty()):
            current_time, event = self.event_queue.get()
            assert current_time >= last_time
            last_time = current_time
            new_events = event.run(current_time)
            for new_event in new_events:
                self.event_queue.put(new_event)

        print("Simulation ending, no more events")
        self.jobs_file.close()

#####################################################################################################################
#globals

finished_file   = open('finished_file', 'w')
load_file       = open('load_file', 'w')
stats_file      = open('stats_file', 'w')

NETWORK_DELAY = 0.0005
BIG = 1

job_start_tstamps = {}

random.seed(123456798)
if(len(sys.argv) != 8):
    print("Incorrent number of parameters.")
    sys.exit(1)


WORKLOAD_FILE                    = sys.argv[1]
SLOTS_PER_WORKER                 = int(sys.argv[2])           #
MONITOR_INTERVAL                 = int(sys.argv[3])           #
ESTIMATION                       = sys.argv[4]                # MEAN, CONSTANT or RANDOM
OFF_MEAN_BOTTOM                  = float(sys.argv[5])         # > 0
OFF_MEAN_TOP                     = float(sys.argv[6])         # >= OFF_MEAN_BOTTOM
TOTAL_WORKERS                    = int(sys.argv[7])

t1 = time.time()

stats = Stats()
s = Simulation(WORKLOAD_FILE,ESTIMATION,OFF_MEAN_BOTTOM,OFF_MEAN_TOP,TOTAL_WORKERS)
s.run()

print("Simulation ended in ", (time.time() - t1), " s ")

finished_file.close()
load_file.close()

print >> stats_file, "STATS_TASKS_TOTAL_FINISHED:             ",          stats.STATS_TASKS_TOTAL_FINISHED
print >> stats_file, "STATS_TASKS_LONG_FINISHED:             ",          stats.STATS_TASKS_LONG_FINISHED
print >> stats_file, "STATS_JOBS_FINISHED:             ",          s.jobs_scheduled
stats_file.close()