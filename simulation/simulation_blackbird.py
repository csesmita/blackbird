#
# Copyright 2013 The Regents of The University California
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

""" Simulations a random assignment of tasks to workers. """

import math
import numpy
import Queue
import time
import random
import threading
import sys

from util import Job, TaskDistributions

#All times simulated are in milliseconds
MEDIAN_TASK_DURATION = 10000
NETWORK_DELAY = 0.5
TASKS_PER_JOB = 10
SLOTS_PER_WORKER = 2
TOTAL_WORKERS = 10
INTERARRIVAL = 1.0 * MEDIAN_TASK_DURATION/100
IS_MUTITHREADED = False

class Event(object):
    """ Abstract class representing events. """
    def __init__(self):
        raise NotImplementedError("Event is an abstract class and cannot be "
                                  "instantiated directly")

    def run(self, current_time):
        """ Returns any events that should be added to the queue. """
        raise NotImplementedError("The run() method must be implemented by "
                                  "each class subclassing Event")

"""
Event to signify a job arriving at a scheduler node
Does the following - 
1. Adds the job into scheduler queue
"""
class JobArrival(Event):
    event_count = 0
    job_arrival = [0.0, 0.90, 1.55, 1.876, 2.50, 3.4, 6.0, 7.88, 9.88, 10.5, 11.5]
    NUM_STATIC_ARRIVALS = 10
    """ Event to signify a job arriving at a scheduler. """
    def __init__(self, simulation, interarrival_delay, task_distribution, worker_index):
        self.simulation = simulation
        self.interarrival_delay = interarrival_delay
        self.task_distribution = task_distribution
        self.worker_index = worker_index

    def run(self, current_time):
        job = Job(TASKS_PER_JOB, current_time, self.task_distribution,
                  MEDIAN_TASK_DURATION)
        #print "Job %s arrived at %s at worker %s" % (job.id, current_time, self.worker_index)
        # Inform the scheduler node that a new job is now ready to be scheduled
        new_events = self.simulation.send_task(job, current_time, self.worker_index)
        # Add new Job Arrival event, for the next job to arrive after this one.
        new_events = []
        arrival_delay = random.expovariate(1.0 / self.interarrival_delay)
        worker_index = random.choice(self.simulation.worker_indices)
        new_events.append((current_time + arrival_delay,
                            JobArrival(self.simulation, self.interarrival_delay,
                                       self.task_distribution, worker_index)))
        return new_events

class TaskArrival(Event):
    """ Event to signify a task arriving at a worker. """
    def __init__(self, future_time, worker, task_duration, job_id):
        self.worker = worker
        self.task_duration = task_duration
        self.job_id = job_id
        self.worker.enqueue_future_task(future_time, task_duration, job_id)

    def run(self, current_time):
        #print "Processing TaskArrival for job", self.job_id, "at time ", current_time
        return self.worker.add_task(current_time)

class TaskEndEvent():
    def __init__(self, worker):
        self.worker = worker

    def run(self, current_time):
        #print "Processing TaskEndEvent at time ", current_time
        return self.worker.free_slot(current_time)

#Acts as both the Worker and the Scheduler classes
class Worker(object):
    def __init__(self, simulation, num_slots, id):
        self.simulation = simulation
        self.free_slots = num_slots
        # Just a list of (task duration, job id) pairs.
        self.queued_tasks = Queue.PriorityQueue()
        self.future_tasks = Queue.PriorityQueue()
        self.id = id

    def enqueue_future_task(self, future_time, task_duration, job_id):
        #print "Enqueuing future Task for job %s at worker %s for future time %s" % (job_id, self.id, future_time)
        self.future_tasks.put((future_time, [task_duration, job_id]))
        #print "Future tasks queue is as follows - ", self.future_tasks.queue

    def add_task(self, current_time):
        # Add tasks from future queue
        #print "Future tasks queue is as follows - ", self.future_tasks.queue
        last_future_time = 0
        while(not self.future_tasks.empty()):
            future_time, queue_details = self.future_tasks.get()
            assert last_future_time <= future_time
            last_future_time = future_time
            if future_time <= current_time:
                # Add in the task_duration and job id to the queue
                # Since future time is less than current_time,
                # current_time will account for queueing delays
                self.queued_tasks.put((queue_details[0], queue_details[1]))
                #print "Task for job %s will be processed at worker %s at time %f" % (queue_details[1], self.id, current_time)
            else:
                self.future_tasks.put((future_time, queue_details))
                break
        return self.maybe_start_task(current_time)

    def free_slot(self, current_time):
        """ Frees a slot on the worker and attempts to launch another task in that slot. """
        self.free_slots += 1
        get_task_events = self.add_task(current_time)
        return get_task_events

    # Add the future queue here only if the queue size has been seen, i.e.
    # This node sees its own future queue in NETWORK_DELAY time.
    # This node sees other nodes' queue lengths only at (now + 2*NETWORK_DELAY)
    # NETWORK_DELAY to travel from scheduler node to that worker node,
    # and then NETWORK_DELAY for update to go from that worker node to all other scheduler nodes.
    def queue_length(self, worker_index, current_time):
        count_future_seen = 0
        limit = current_time - 2 * NETWORK_DELAY
        if self.id == worker_index:
            limit = current_time - NETWORK_DELAY
        while(self.future_tasks.queue[count_future_seen][0] < limit) :
            count_future_seen += 1
        if self.free_slots > 0:
            assert self.queued_tasks.empty()
            return -self.free_slots + count_future_seen
        return self.queued_tasks.qsize() + count_future_seen

    def maybe_start_task(self, current_time):
        if not self.queued_tasks.empty() and self.free_slots > 0:
            # Account for "running" task
            self.free_slots -= 1
            task_duration, job_id = self.queued_tasks.get()
            #print "Launching task for job %s on worker %s at %f (duration %f)" % (job_id, self.id, current_time, task_duration)
            task_end_time = current_time + task_duration
            #print ("Task for job %s on worker %s launched at %s; will complete at %s" %
            #       (job_id, self.id, current_time, task_end_time))
            #print "Task for job %s finished at %f" % (job_id, task_end_time)
            self.simulation.add_task_completion_time(job_id, task_end_time)
            return [(task_end_time, TaskEndEvent(self))]
        return []

# This class generates Job Arrivals
class Simulation(object):
    def __init__(self, num_jobs, load, task_distribution):
        avg_used_slots = load * SLOTS_PER_WORKER * TOTAL_WORKERS
        self.interarrival_delay = (1.0 * MEDIAN_TASK_DURATION * TASKS_PER_JOB / avg_used_slots)
        print ("Interarrival delay: %s (avg slots in use: %s)" %
               (self.interarrival_delay, avg_used_slots))
        self.jobs = {}
        self.remaining_jobs = num_jobs
        self.workers = []
        while len(self.workers) < TOTAL_WORKERS:
            self.workers.append(Worker(self, SLOTS_PER_WORKER, len(self.workers)))
        self.worker_indices = range(TOTAL_WORKERS)
        self.task_distribution = task_distribution
        self.unscheduled_jobs = []
        self.response_times = []

    def send_task(self, job, current_time, worker_index):
        #print "Number of unscheduled tasks for job id ", job.id," is ", len(job.unscheduled_tasks)
        task_arrival_events = []
        task_index = 0
        while task_index < len(job.unscheduled_tasks):
        worker = sorted(self.workers, key=lambda worker: (worker.queue_length(worker_index, current_time)))[0]
            #print "Assigning task %s to worker %s" % (task_index, worker.id)
            task_arrival_events.append(
                (current_time + NETWORK_DELAY,
                 TaskArrival(current_time + NETWORK_DELAY, self.workers[worker.id],
                             job.unscheduled_tasks[task_index], job.id)))
            task_index += 1
        return task_arrival_events

    def add_task_completion_time(self, job_id, completion_time):
        job_complete = self.jobs[job_id].task_completed(completion_time)
        if job_complete:
            self.remaining_jobs -= 1


    def run(self):
        print "Parameters - MEDIAN_TASK_DURATION - ", MEDIAN_TASK_DURATION, \
            "NETWORK_DELAY - ", NETWORK_DELAY, "TASKS_PER_JOB - ", TASKS_PER_JOB, "SLOTS_PER_WORKER - ", \
            SLOTS_PER_WORKER, "TOTAL_WORKERS - ", TOTAL_WORKERS, "INTERARRIVAL_RATE - ", INTERARRIVAL
        worker_index = random.choice(self.worker_indices)
        self.event_queue.put((0,JobArrival(self, self.interarrival_delay, self.task_distribution, worker_index)))
        start_time = time.time()
        last_time = 0
        while self.remaining_jobs > 0:
            current_time, event = self.event_queue.get()
            assert current_time >= last_time
            last_time = current_time
            new_events = event.run(current_time)
            for new_event in new_events:
                self.event_queue.put(new_event)
        now_time = time.time()
        print ("Simulation ended after %s milliseconds (%s jobs started)" %
               (last_time, len(self.jobs)))
        complete_jobs = [j for j in self.jobs.values() if j.completed_tasks_count == j.num_tasks]
        print "%s complete jobs" % len(complete_jobs)
        response_times = []
        if len(complete_jobs) > 0:
            response_times = [job.end_time - job.start_time for job in complete_jobs]
            print "Included %s jobs" % len(response_times)
            print "Average response time: ", numpy.mean(response_times)
        print "Total time to run the code - ", (now_time - start_time), "sec"
        return response_times


def main():
    if len(sys.argv) < 2:
        print "Please provide the number of jobs to be run per scheduler"
        sys.exit(0)
    sim = Simulation(int(sys.argv[1]), "blackbird", 0.95, TaskDistributions.CONSTANT)
    sim.run()


if __name__ == "__main__":
    main()
