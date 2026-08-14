from copy import deepcopy

from models import Process
from sjf_preemptive import run_sjf
from fcfs import run_fcfs


def calculate_average(processes):

    if not processes:
        return 0, 0

    total_waiting_time = sum(
        process.waiting_time for process in processes
    )

    total_turnaround_time = sum(
        process.turnaround_time for process in processes
    )

    average_wt = total_waiting_time / len(processes)
    average_tat = total_turnaround_time / len(processes)

    return average_wt, average_tat


def display_result(algorithm_name, processes):

    average_wt, average_tat = calculate_average(processes)

    print()
    print("=" * 75)
    print(algorithm_name)
    print("=" * 75)

    print(
        f"{'PID':<10}"
        f"{'AT':<10}"
        f"{'BT':<10}"
        f"{'CT':<10}"
        f"{'TAT':<10}"
        f"{'WT':<10}"
    )

    print("-" * 60)

    for process in processes:

        print(
            f"{process.pid:<10}"
            f"{process.arrival_time:<10}"
            f"{process.burst_time:<10}"
            f"{process.completion_time:<10}"
            f"{process.turnaround_time:<10}"
            f"{process.waiting_time:<10}"
        )

    print("-" * 60)

    print(f"Average WT  : {average_wt:.2f}")
    print(f"Average TAT : {average_tat:.2f}")

    return average_wt, average_tat


def compare_results(sjf_processes, fcfs_processes):

    sjf_wt, sjf_tat = calculate_average(sjf_processes)
    fcfs_wt, fcfs_tat = calculate_average(fcfs_processes)

    print()
    print("=" * 75)
    print("SO SÁNH SJF PREEMPTIVE VÀ FCFS")
    print("=" * 75)

    print(
        f"{'Thuật toán':<25}"
        f"{'Average WT':<20}"
        f"{'Average TAT':<20}"
    )

    print("-" * 65)

    print(
        f"{'SJF Preemptive':<25}"
        f"{sjf_wt:<20.2f}"
        f"{sjf_tat:<20.2f}"
    )

    print(
        f"{'FCFS':<25}"
        f"{fcfs_wt:<20.2f}"
        f"{fcfs_tat:<20.2f}"
    )

    print("-" * 65)

    print("\nNHẬN XÉT VỀ AVERAGE WT:")

    if sjf_wt < fcfs_wt:

        print(
            "SJF Preemptive có Average WT thấp hơn FCFS."
        )

        print(
            f"SJF Preemptive: {sjf_wt:.2f}"
        )

        print(
            f"FCFS          : {fcfs_wt:.2f}"
        )

    elif sjf_wt > fcfs_wt:

        print(
            "FCFS có Average WT thấp hơn SJF Preemptive "
            "trong bộ dữ liệu này."
        )

        print(
            f"FCFS          : {fcfs_wt:.2f}"
        )

        print(
            f"SJF Preemptive: {sjf_wt:.2f}"
        )

    else:

        print(
            "Hai thuật toán có Average WT bằng nhau."
        )

    print("\nNHẬN XÉT VỀ AVERAGE TAT:")

    if sjf_tat < fcfs_tat:

        print(
            "SJF Preemptive có Average TAT thấp hơn FCFS."
        )

        print(
            f"SJF Preemptive: {sjf_tat:.2f}"
        )

        print(
            f"FCFS          : {fcfs_tat:.2f}"
        )

    elif sjf_tat > fcfs_tat:

        print(
            "FCFS có Average TAT thấp hơn SJF Preemptive "
            "trong bộ dữ liệu này."
        )

        print(
            f"FCFS          : {fcfs_tat:.2f}"
        )

        print(
            f"SJF Preemptive: {sjf_tat:.2f}"
        )

    else:

        print(
            "Hai thuật toán có Average TAT bằng nhau."
        )

    print("\nKẾT LUẬN:")

    if sjf_wt < fcfs_wt and sjf_tat < fcfs_tat:

        print(
            "SJF Preemptive hiệu quả hơn FCFS "
            "trong bộ dữ liệu đang xét."
        )

    elif sjf_wt > fcfs_wt and sjf_tat > fcfs_tat:

        print(
            "FCFS hiệu quả hơn SJF Preemptive "
            "trong bộ dữ liệu đang xét."
        )

    else:

        print(
            "Hai thuật toán có ưu thế khác nhau "
            "tùy theo tiêu chí đánh giá."
        )


def analyze_effects():

    print()
    print("=" * 75)
    print("PHÂN TÍCH CONVOY EFFECT VÀ STARVATION")
    print("=" * 75)

    print("\n1. CONVOY EFFECT - FCFS")

    print(
        "FCFS xử lý tiến trình theo thứ tự đến."
    )

    print(
        "Nếu một tiến trình có Burst Time lớn đứng đầu, "
        "các tiến trình ngắn phía sau phải chờ."
    )

    print(
        "Điều này có thể làm tăng Average Waiting Time "
        "và Average Turnaround Time."
    )

    print("\n2. STARVATION - SJF PREEMPTIVE")

    print(
        "SJF Preemptive ưu tiên tiến trình có "
        "thời gian còn lại ngắn nhất."
    )

    print(
        "Nếu liên tục xuất hiện các tiến trình ngắn, "
        "tiến trình có Burst Time dài có thể phải chờ rất lâu."
    )

    print(
        "Hiện tượng này được gọi là Starvation."
    )


def main():

    processes = [
        Process("P1", 0, 8),
        Process("P2", 1, 4),
        Process("P3", 2, 2),
        Process("P4", 3, 5)
    ]

    sjf_input = deepcopy(processes)
    fcfs_input = deepcopy(processes)

    sjf_result, sjf_gantt = run_sjf(sjf_input)

    fcfs_result, fcfs_gantt = run_fcfs(fcfs_input)

    display_result(
        "KẾT QUẢ SJF PREEMPTIVE",
        sjf_result
    )

    display_result(
        "KẾT QUẢ FCFS",
        fcfs_result
    )

    compare_results(
        sjf_result,
        fcfs_result
    )

    analyze_effects()


if __name__ == "__main__":
    main()
    
