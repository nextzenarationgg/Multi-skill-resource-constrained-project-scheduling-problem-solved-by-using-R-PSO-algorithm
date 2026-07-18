from Task import Task
from Resource import Resource
from decode import run_rpso


def main():
    print("--- KHỞI TẠO DỮ LIỆU GIẢ LẬP ---")

    # Danh sách nhân sự
    resources = [
        Resource(
            resource_id=1,
            skills={
                "X": 3,
                "Y": 1
            }
        ),

        Resource(
            resource_id=2,
            skills={
                "X": 2,
                "Y": 3
            }
        ),

        Resource(
            resource_id=3,
            skills={
                "X": 1,
                "Y": 2
            }
        )
    ]

    # Danh sách công việc
    tasks = [
        Task(
            task_id=1,
            duration=2,
            predecessors=[],
            req_skill_type="X",
            req_skill_level=2
        ),

        Task(
            task_id=2,
            duration=3,
            predecessors=[1],
            req_skill_type="Y",
            req_skill_level=2
        ),

        Task(
            task_id=3,
            duration=4,
            predecessors=[1],
            req_skill_type="X",
            req_skill_level=3
        ),

        Task(
            task_id=4,
            duration=2,
            predecessors=[2],
            req_skill_type="Y",
            req_skill_level=1
        ),

        Task(
            task_id=5,
            duration=3,
            predecessors=[2, 3],
            req_skill_type="X",
            req_skill_level=2
        ),

        Task(
            task_id=6,
            duration=2,
            predecessors=[4],
            req_skill_type="Y",
            req_skill_level=2
        ),

        Task(
            task_id=7,
            duration=3,
            predecessors=[5, 6],
            req_skill_type="X",
            req_skill_level=2
        )
    ]

    # Chuyển list thành dictionary
    tasks_dict = {
        task.task_id: task
        for task in tasks
    }

    resources_dict = {
        resource.resource_id: resource
        for resource in resources
    }

    # Thời gian mục tiêu
    target_a = 5

    print("\n--- BẮT ĐẦU CHẠY THUẬT TOÁN R-PSO ---")

    best_schedule, best_fitness = run_rpso(
        tasks_dict=tasks_dict,
        resources_dict=resources_dict,
        A=target_a,
        num_particles=20,
        max_iterations=50
    )

    print("\n--- KẾT QUẢ TỐI ƯU ---")

    if best_schedule is None:
        print("Không tìm được lịch trình phù hợp.")
        return

    makespan = best_schedule.calculate_makespan()

    print(f"Thời gian mục tiêu: {target_a} ngày")
    print(f"Thời gian thực tế: {makespan} ngày")
    print(f"Độ lệch fitness: {best_fitness}")

    print("\n--- LỊCH TRÌNH CHI TIẾT ---")

    for task_id in sorted(tasks_dict.keys()):
        start = best_schedule.start_time[task_id]
        end = best_schedule.end_time[task_id]
        resource_id = best_schedule.assignments[task_id]

        print(
            f"Việc {task_id}: "
            f"Bắt đầu ngày {start} -> "
            f"Kết thúc ngày {end} | "
            f"Giao cho thợ {resource_id}"
        )


if __name__ == "__main__":
    main()