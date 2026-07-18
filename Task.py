class Task:
    def __init__(self, task_id, duration, predecessors, req_skill_type, req_skill_level):
        self.task_id = task_id
        self.duration = duration #tj, 1.6
        self.predecessors = predecessors if predecessors is not None else [] #Ci
        self.req_skill_type = req_skill_type #gri
        self.req_skill_level = req_skill_level #hri


