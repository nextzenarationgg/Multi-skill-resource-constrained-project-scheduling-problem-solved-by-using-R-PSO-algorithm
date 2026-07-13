from Schedule import Schedule
def particle_decode(particle, tasks_dict, resources_dict):
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
    return current_schedule
