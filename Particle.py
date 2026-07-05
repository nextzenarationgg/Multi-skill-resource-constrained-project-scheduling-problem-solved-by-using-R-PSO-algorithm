import random
class Particle:
    def __init__(self, num_tasks):
        # tao mang vi tri va van toc voi cac so thuc ngau nhien
        self.position = [random.uniform(0.0, 100.0) for _ in range(num_tasks)]

        # van toc
        self.velocity = [0.0 for _ in range(num_tasks)]

        # lich su tot nhat cua hat
        self.best_position = self.position.copy

        self.best_fitness = -1.0
        self.current_fitness  = -1.0 #|f(P) - A|