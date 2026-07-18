class Schedule:
    def __init__(self):
        self.start_time = {} #Bk
        self.end_time = {} #Ek
        self.assignments = {} #Atuv, 1.9

    def calculate_makespan(self) -> int: #f(P)
        # Chua co task nao ket thuc tra ve 0
        if not self.end_time:
            return 0
        
        return max(self.end_time.values())
    
    def print_schedule(self):

        print("\n===== SCHEDULE =====")

        for task_id in sorted(self.start_time):

            print(
                f"Task {task_id}: "
                f"Start={self.start_time[task_id]}, "
                f"End={self.end_time[task_id]}, "
                f"Resource={self.assignments[task_id]}"
            )

        print(f"\nMakespan = {self.calculate_makespan()}")