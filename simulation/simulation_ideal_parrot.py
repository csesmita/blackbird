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
import random
import Queue
from util import Job, TaskDistributions

MEDIAN_TASK_DURATION = 100
NETWORK_DELAY = 0.5
TASKS_PER_JOB = 2
SLOTS_PER_WORKER = 1
TOTAL_WORKERS = 3

def get_percentile(N, percent, key=lambda x:x):
    if not N:
        return 0
    k = (len(N) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0 + d1

def plot_cdf(values, filename):
    values.sort()
    f = open(filename, "w")
    for percent in range(100):
        fraction = percent / 100.
        f.write("%s\t%s\n" % (fraction, get_percentile(values, fraction)))
    f.close()

class Event(object):
    """ Abstract class representing events. """
    def __init__(self):
        raise NotImplementedError("Event is an abstract class and cannot be "
                                  "instantiated directly")

    def run(self, current_time):
        """ Returns any events that should be added to the queue. """
        raise NotImplementedError("The run() method must be implemented by "
                                  "each class subclassing Event")

class JobArrival(Event):
    """ Event to signify a job arriving at a scheduler. """
    def __init__(self, simulation, interarrival_delay, task_distribution):
        self.simulation = simulation
        self.interarrival_delay = interarrival_delay
        self.task_distribution = task_distribution

    def run(self, current_time):
        print "Processing JobArrival at time ", current_time
        job = Job(TASKS_PER_JOB, current_time, self.task_distribution, MEDIAN_TASK_DURATION)
        print "Job %s arrived at %s" % (job.id, current_time)
        # Schedule job.
        new_events = self.simulation.send_tasks(job, current_time)
        # Add new Job Arrival event, for the next job to arrive after this one.
        arrival_delay = random.expovariate(1.0 / self.interarrival_delay)
        new_events.append((current_time + arrival_delay, self))
        print "Returning %s events which are - " % len(new_events)
        for event in new_events:
            print event
        return new_events

class TaskArrival(Event):
    """ Event to signify a task arriving at a worker. """
    def __init__(self, worker, task_duration, job_id):
        self.worker = worker
        self.task_duration = task_duration
        self.job_id = job_id
        self.worker.enqueue_task(task_duration, job_id)

    def run(self, current_time):
        print "Processing TaskArrival at time ", current_time
        return self.worker.add_task(current_time, self.job_id)

class TaskEndEvent():
    def __init__(self, worker):
        self.worker = worker

    def run(self, current_time):
        print "Processing TaskEndEvent at time ", current_time
        return self.worker.free_slot(current_time)

class Worker(object):
    def __init__(self, simulation, num_slots, id):
        self.simulation = simulation
        self.free_slots = num_slots
        # Just a list of (task duration, job id) pairs.
        self.queued_tasks = Queue.Queue()
        self.id = id
        self.num_queued_tasks = 0

    def enqueue_task(self, task_duration, job_id):
        print "Task for job %s arrived at worker %s" % (job_id, self.id)
        self.queued_tasks.put((task_duration, job_id))
        self.num_queued_tasks += 1

    def add_task(self, current_time, job_id):
        print "Task for job %s processed at worker %s" % (job_id, self.id)
        return self.maybe_start_task(current_time)

    def free_slot(self, current_time):
        """ Frees a slot on the worker and attempts to launch another task in that slot. """
        self.free_slots += 1
        get_task_events = self.maybe_start_task(current_time)
        return get_task_events

    def queue_length(self):
        queue_length = self.num_queued_tasks
        if self.free_slots > 0:
            assert self.num_queued_tasks == 0
            return -self.free_slots
        return queue_length

    def maybe_start_task(self, current_time):
        """
        if not self.queued_tasks.empty() and self.simulation.free_slots > 0:
            # Account for "running" task
            self.free_slots -= 1
            task_duration, job_id = self.queued_tasks.get()
            self.num_queued_tasks -= 1
            #print "Launching task for job %s on worker %s" % (job_id, self.id)
            task_end_time = current_time + task_duration
            print ("Task for job %s on worker %s launched at %s; will complete at %s" %
            (job_id, self.id, current_time, task_end_time))
            self.simulation.add_task_completion_time(job_id, task_end_time)
            return [(task_end_time, TaskEndEvent(self))]
        return []
        """
        if not self.queued_tasks.empty() and self.free_slots > 0:
            # Account for "running" task
            self.free_slots -= 1
            task_duration, job_id = self.queued_tasks.get()
            #print "Launching task for job %s on worker %s" % (job_id, self.id)
            task_end_time = current_time + task_duration
            print ("Task for job %s on worker %s launched at %s; will complete at %s" %
                   (job_id, self.id, current_time, task_end_time))
            self.simulation.add_task_completion_time(job_id, task_end_time)
            return [(task_end_time, TaskEndEvent(self))]
        return []

class Simulation(object):
    def __init__(self, num_jobs, file_prefix, load, task_distribution):
        avg_used_slots = load * SLOTS_PER_WORKER * TOTAL_WORKERS
        self.interarrival_delay = (1.0 * MEDIAN_TASK_DURATION * TASKS_PER_JOB / avg_used_slots)
        print ("Interarrival delay: %s (avg slots in use: %s)" %
               (self.interarrival_delay, avg_used_slots))
        self.jobs = {}
        self.remaining_jobs = num_jobs
        self.event_queue = Queue.PriorityQueue()
        self.workers = []
        self.file_prefix = file_prefix
        self.num_free_slots = TOTAL_WORKERS * SLOTS_PER_WORKER
        while len(self.workers) < TOTAL_WORKERS:
            self.workers.append(Worker(self, SLOTS_PER_WORKER, len(self.workers)))
        self.worker_indices = range(TOTAL_WORKERS)
        self.task_distribution = task_distribution
        self.unscheduled_jobs = []
    """
    def schedule_tasks(self, job, current_time):
        self.jobs[job.id] = job
        self.unscheduled_jobs.append(job)
        #print "Job %s arrived at %s" % (job.id, current_time)
        return self.maybe_launch_tasks(current_time)
    

    def maybe_launch_tasks(self, current_time):
        task_end_events = []
        while self.num_free_slots > 0 and len(self.unscheduled_jobs) > 0:
            self.num_free_slots -= 1
            job = self.unscheduled_jobs[0]
            task_duration = job.unscheduled_tasks[0]
            job.unscheduled_tasks = job.unscheduled_tasks[1:]
            # if len(job.unscheduled_tasks) == 0:
            # logging.info("Finished scheduling tasks for job %s" % job.id)
            print ("Launching task for job %s at %s (duration %s); %s remaining slots" %
                   (job.id, current_time + NETWORK_DELAY, task_duration, self.num_free_slots))
            task_end_time = current_time + task_duration + NETWORK_DELAY
            scheduler_notify_time = task_end_time + NETWORK_DELAY
            task_end_events.append((scheduler_notify_time, TaskEndEvent(self)))

            job_complete = job.task_completed(task_end_time)
            if job_complete:
                #print "Completed job %s in %s" % (job.id, job.end_time - job.start_time)
                self.remaining_jobs -= 1
                self.unscheduled_jobs = self.unscheduled_jobs[1:]
        return task_end_events
        
    def free_slot(self, current_time):
        self.num_free_slots += 1
        return self.maybe_launch_tasks(current_time)    
    """

    # Assigns tasks to the highly ranked node
    def send_tasks(self, job, current_time):
        self.jobs[job.id] = job
        #random.shuffle(self.worker_indices)
        print "Number of unscheduled tasks for job id ", job.id," is ", len(job.unscheduled_tasks)
        print "Printing highly ranked node - "
        for i, worker in enumerate(sorted(self.workers, key=lambda worker: worker.num_queued_tasks)):
            print "Worker ", worker.id, " with queue_length ", worker.queue_length()
        task_arrival_events = []
        #for i, worker_index in enumerate(self.worker_indices[:len(job.unscheduled_tasks)]):
        # Emit scheduling placement one task at a time
        task_index = 0

        for worker in sorted(self.workers, key=lambda worker: worker.num_queued_tasks):
            if task_index == len(job.unscheduled_tasks):
                break
            print "Assigning task %s to worker %s" % (task_index, worker.id)
            task_arrival_events.append(
                (current_time + NETWORK_DELAY,
                 TaskArrival(self.workers[worker.id], job.unscheduled_tasks[task_index], job.id)))
            task_index += 1
        return task_arrival_events

    def add_task_completion_time(self, job_id, completion_time):
        job_complete = self.jobs[job_id].task_completed(completion_time)
        if job_complete:
            self.remaining_jobs -= 1

    def run(self):
        self.event_queue.put((0, JobArrival(self, self.interarrival_delay, self.task_distribution)))
        last_time = 0
        while self.remaining_jobs > 0:
            current_time, event = self.event_queue.get()
            print "Got EVENT ", event
            assert current_time >= last_time
            last_time = current_time
            new_events = event.run(current_time)
            for new_event in new_events:
                self.event_queue.put(new_event)

        print ("Simulation ended after %s milliseconds (%s jobs started)" %
               (last_time, len(self.jobs)))
        complete_jobs = [j for j in self.jobs.values() if j.completed_tasks_count == j.num_tasks]
        print "%s complete jobs" % len(complete_jobs)
        response_times = [job.end_time - job.start_time for job in complete_jobs
                          if job.start_time > 500]
        if len(response_times) > 0:
            print "Included %s jobs" % len(response_times)
            plot_cdf(response_times, "%s_response_times.data" % self.file_prefix)
            print "Average response time: ", numpy.mean(response_times)

            longest_tasks = [job.longest_task for job in complete_jobs]
            plot_cdf(longest_tasks, "%s_ideal_response_time.data" % self.file_prefix)
        return response_times

def main():
    sim = Simulation(2, "parrot", 0.90, TaskDistributions.CONSTANT)
    sim.run()

if __name__ == "__main__":
    main()
