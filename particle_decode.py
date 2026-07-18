from Schedule import Schedule
from Task import Task
from Particle import Particle
from Resource import Resource
def particle_decode(particle, tasks_dict, resources_dict, A):
    current_schedule = Schedule()
    res_available_time = {res_id: 0 for res_id in resources_dict.keys()}

    task_ids = list(tasks_dict.keys())

    completed_tasks = set()
    unscheduled_tasks = set(task_ids)

    while len(unscheduled_tasks) > 0:
        eligible_tasks = []
        for t_id in unscheduled_tasks:
            task = tasks_dict[t_id]
            if all(pred in completed_tasks for pred in task.predecessors):
                eligible_tasks.append(t_id)

        current_task_id = eligible_tasks[0]
        current_task = tasks_dict[current_task_id]

        task_index = task_ids.index(current_task_id)
        assigned_resource_id = particle.position[task_index]

        max_parent_end = 0
        for pred in current_task.predecessors:
            if pred in current_schedule.end_time:
                max_parent_end = max(max_parent_end, current_schedule.end_time[pred])

        resource_ready = res_available_time[assigned_resource_id]

        start_t = max(max_parent_end, resource_ready)
        end_t = start_t + current_task.duration

        current_schedule.start_time[current_task_id] = start_t
        current_schedule.end_time[current_task_id] = end_t
        current_schedule.assignments[current_task_id] = assigned_resource_id

        res_available_time[assigned_resource_id] = end_t
        completed_tasks.add(current_task_id)
        unscheduled_tasks.remove(current_task_id)

    min_start = min(current_schedule.start_time.values())
    max_end = max(current_schedule.end_time.values())
    current_makespan = max_end - min_start

    #thoi gian ngoi choi
    if current_makespan < A:
        last_task_id = max(current_schedule.end_time, key=current_schedule.end_time.get)

        delay_needed = A - current_makespan

        current_schedule.start_time[last_task_id] += delay_needed
        current_schedule.end_time[last_task_id] += delay_needed
    return current_schedule

def evaluate_fitness(particle, tasks_dict, resources_dict, A):
    current_schedule = particle_decode(particle, tasks_dict, resources_dict, A)
    makespan = current_schedule.calculate_makespan()
    fitness_score = abs(makespan - A)
    particle.fitness = fitness_score

    if particle.pbest_fitness is None or fitness_score < particle.pbest_fitness:
        particle.pbest_fitness = fitness_score
        particle.pbest_position = list(particle.position)
    
    return fitness_score, current_schedule

def reallocate(particle, tasks_dict, resources_dict):
    workloads = {res_id: 0 for res_id in resources_dict.keys()}

    task_ids = list(tasks_dict.keys())

    for i, t_id in enumerate(task_ids):
        assigned_resource = particle.position[i]
        task_duration = tasks_dict[t_id].duration
        workloads[assigned_resource] += task_duration

    busiest_resource_id = max(workloads, key=workloads.get)
    freest_resource_id = min(workloads, key=workloads.get)

    freest_resource = resources_dict[freest_resource_id]

    for i, t_id in enumerate(task_ids):
        if particle.position[i] == busiest_resource_id:
            task = tasks_dict[t_id]
            if task.skill_required in freest_resource.skills:
                particle.position[i] = freest_resource_id
                break

            