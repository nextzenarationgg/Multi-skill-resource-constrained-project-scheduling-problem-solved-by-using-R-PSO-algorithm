from Schedule import Schedule
from Task import Task
from Particle import Particle
from Resource import Resource
import random
import math
def add_idle_time(schedule, tasks_dict, target_A):
    current_makespan = schedule.calculate_makespan()

    # Không cần chèn thời gian chờ nếu lịch đã bằng hoặc vượt A
    if current_makespan >= target_A:
        return

    delay_needed = target_A - current_makespan

    terminal_tasks = []

    # Terminal task là task không có successor
    for task_id in schedule.end_time:
        has_successor = any(
            task_id in task.predecessors
            for task in tasks_dict.values()
        )

        if not has_successor:
            terminal_tasks.append(task_id)

    if not terminal_tasks:
        return

    # Chọn terminal task kết thúc muộn nhất
    task_to_delay = max(
        terminal_tasks,
        key=lambda task_id: schedule.end_time[task_id]
    )

    # Dịch task sang phải nhưng giữ nguyên duration
    schedule.start_time[task_to_delay] += delay_needed
    schedule.end_time[task_to_delay] += delay_needed

def particle_decode(particle, tasks_dict, resources_dict, A):
    current_schedule = Schedule()
    res_available_time = {res_id: 0 for res_id in resources_dict.keys()}

    task_ids = sorted(tasks_dict.keys())

    completed_tasks = set()
    unscheduled_tasks = set(task_ids)

    while len(unscheduled_tasks) > 0:
        eligible_tasks = []
        for t_id in unscheduled_tasks:
            task = tasks_dict[t_id]
            if all(pred in completed_tasks for pred in task.predecessors):
                eligible_tasks.append(t_id)

        eligible_tasks.sort()

        if not eligible_tasks:
            raise ValueError(
                "Không thể lập lịch: dữ liệu predecessor có chu trình "
                "hoặc tham chiếu đến task không tồn tại."
            )
        
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

    add_idle_time(current_schedule,tasks_dict,A)
    return current_schedule

def evaluate_fitness(particle, tasks_dict, resources_dict, A):
    current_schedule = particle_decode(particle, tasks_dict, resources_dict, A)
    makespan = current_schedule.calculate_makespan()
    fitness_score = abs(makespan - A)
    particle.current_fitness = fitness_score

    if particle.pbest_fitness is None or fitness_score < particle.pbest_fitness:
        particle.pbest_fitness = fitness_score
        particle.pbest_position = list(particle.position)
    
    return fitness_score, current_schedule

def reallocate(particle,tasks_dict,resources_dict,A):
    task_ids = sorted(tasks_dict.keys())

    # Đánh giá nghiệm hiện tại
    old_schedule = particle_decode(particle,tasks_dict,resources_dict,A)

    old_fitness = abs(old_schedule.calculate_makespan() - A)

    workloads = {resource_id: 0 for resource_id in resources_dict}

    # Tính tổng thời gian làm việc của mỗi resource
    for i, task_id in enumerate(task_ids):
        resource_id = particle.position[i]
        workloads[resource_id] += tasks_dict[task_id].duration

    # Resource có tải lớn nhất
    busiest_resource_id = max(workloads,key=workloads.get)

    best_position = list(particle.position)
    best_fitness = old_fitness

    # Thử chuyển từng task của resource bận nhất
    for i, task_id in enumerate(task_ids):
        if particle.position[i] != busiest_resource_id:
            continue

        task = tasks_dict[task_id]

        # Thử tất cả resource khác có đủ kỹ năng
        for resource_id, resource in resources_dict.items():
            if resource_id == busiest_resource_id:
                continue

            is_capable = (task.req_skill_type in resource.skills and resource.skills[task.req_skill_type] >= task.req_skill_level)

            if not is_capable:
                continue

            # Tạm thời chuyển task
            candidate_position = list(particle.position)
            candidate_position[i] = resource_id

            old_position = particle.position
            particle.position = candidate_position

            candidate_schedule = particle_decode(particle,tasks_dict,resources_dict,A)

            candidate_fitness = abs(candidate_schedule.calculate_makespan() - A)

            # Khôi phục để tiếp tục thử nghiệm
            particle.position = old_position

            # Chỉ ghi nhận nếu nghiệm mới tốt hơn
            if candidate_fitness < best_fitness:
                best_fitness = candidate_fitness
                best_position = candidate_position

    # Chỉ cập nhật khi tìm được cách chuyển tốt hơn
    particle.position = best_position

    return best_fitness

def run_rpso(tasks_dict, resources_dict, A, num_particles = 30, max_iterations = 100):
    mutation_rate = 0.05
    task_ids = sorted(tasks_dict.keys())
    swarm = [Particle(tasks_dict, resources_dict) for _ in range(num_particles)]
    gbest_fitness = float('inf')
    gbest_position = None
    gbest_schedule = None
    

    for iteration in range(max_iterations):
        for particle in swarm:
            fitness, current_schedule = evaluate_fitness(particle, tasks_dict, resources_dict, A)

            if fitness < gbest_fitness:
                gbest_fitness = fitness
                gbest_position = list(particle.position)
                gbest_schedule = current_schedule

            if current_schedule.calculate_makespan() > A:
                reallocate(particle, tasks_dict, resources_dict, A)

                fitness, current_schedule = evaluate_fitness(particle, tasks_dict, resources_dict, A)

                if fitness < gbest_fitness:
                    gbest_fitness = fitness
                    gbest_position = list(particle.position)
                    gbest_schedule = current_schedule
        
        W = 0.7
        C1 = 1.5
        C2 = 1.5
        for particle in swarm:
            for i in range(len(particle.position)):
                r1 = random.random()
                r2 = random.random()
                particle.velocity[i] = (
                    W * particle.velocity[i]
                    + C1 * r1 * (particle.pbest_position[i] != particle.position[i])
                    + C2 * r2 * (gbest_position[i] != particle.position[i])
                )
                probability = 1 / (1 + math.exp(-particle.velocity[i]))
                if random.random() < probability:
                    if random.random() < 0.5:
                        particle.position[i] = particle.pbest_position[i]
                    else:
                        particle.position[i] = gbest_position[i]
                
                if random.random() < mutation_rate:
                    task_id = task_ids[i]
                    task = tasks_dict[task_id]

                    capable_resources = []

                    for resource_id, resource in resources_dict.items():
                        if (
                            task.req_skill_type in resource.skills
                            and resource.skills[task.req_skill_type]
                            >= task.req_skill_level
                        ):
                            capable_resources.append(resource_id)

                    alternative_resources = [
                        resource_id
                        for resource_id in capable_resources
                        if resource_id != particle.position[i]
                    ]

                    if alternative_resources:
                        particle.position[i] = random.choice(
                            alternative_resources
                        )
        print(f"Vòng lặp {iteration + 1}/{max_iterations} - Độ lệch tốt nhất hiện tại: {gbest_fitness}")
        if gbest_fitness == 0:
            print("ĐÃ TÌM THẤY LỊCH TRÌNH HOÀN HẢO!")
            break            

    return gbest_schedule, gbest_fitness