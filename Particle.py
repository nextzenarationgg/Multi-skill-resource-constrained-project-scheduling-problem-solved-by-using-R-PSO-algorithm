import random

class Particle:
    def __init__(self, tasks_dict, resources_dict):

        task_ids = sorted(tasks_dict.keys())

        self.position = []
        self.velocity = []

        # Khởi tạo lời giải ngẫu nhiên hợp lệ
        for task_id in task_ids:

            task = tasks_dict[task_id]

            capable_resources = []

            for resource_id, resource in resources_dict.items():

                if (
                    task.req_skill_type in resource.skills
                    and resource.skills[task.req_skill_type] >= task.req_skill_level
                ):
                    capable_resources.append(resource_id)

            if not capable_resources:
                raise ValueError(
                    f"Không có resource phù hợp cho Task {task_id}"
                )

            self.position.append(random.choice(capable_resources))

            
            self.velocity.append(0.0)

        self.current_fitness = float("inf")

        self.pbest_position = self.position.copy()

        self.pbest_fitness = float("inf")