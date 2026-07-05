class Schedule:
    def __init__(self):
        self.start_time = {} #Bk
        self.end_time = {} #Ek
        self.assignment = {} #Atuv, 1.9

    def calculate_makespan(self) -> int: #f(P)
        # Chua co task nao ket thuc tra ve 0
        if not self.end_time:
            return 0
        
        return max(self.end_time.values())