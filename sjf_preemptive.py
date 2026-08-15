from copy import deepcopy
from models import Process
def run_sjf(processes: list[Process]) -> tuple[list[Process], list[tuple[str, int, int]]]:
    completed_processes = deepcopy(processes)
    gantt_chart = []
    if not completed_processes:
        return completed_processes, gantt_chart
    for process in completed_processes:
        process.remaining_time = process.burst_time
        process.completion_time = 0
        process.turnaround_time = 0
        process.waiting_time = 0
        process.response_time = -1
        process.started = False
    current_time = 0
    completed_count = 0
    total_processes = len(completed_processes)
    while completed_count < total_processes:
        ready_queue = [
            process
            for process in completed_processes
            if process.arrival_time <= current_time
            and process.remaining_time > 0
        ]
        if not ready_queue:
            next_process = min(
                (
                    process
                    for process in completed_processes
                    if process.remaining_time > 0
                ),
                key=lambda process: (
                    process.arrival_time,
                    process.pid
                )
            )
            start_time = current_time
            current_time = max(current_time, next_process.arrival_time)
            end_time = current_time
            if start_time < end_time:
                if (
                    gantt_chart
                    and gantt_chart[-1][0] == "IDLE"
                    and gantt_chart[-1][2] == start_time
                ):
                    process_id, old_start_time, _ = gantt_chart[-1]
                    gantt_chart[-1] = (
                        process_id,
                        old_start_time,
                        end_time
                    )
                else:
                    gantt_chart.append(
                        ("IDLE", start_time, end_time)
                    )
            continue
        current_process = min(
            ready_queue,
            key=lambda process: (
                process.remaining_time,
                -process.arrival_time,
                process.pid
            )
        )
        if not current_process.started:
            current_process.started = True
            current_process.response_time = (
                current_time - current_process.arrival_time
            )
        start_time = current_time
        current_time += 1
        current_process.remaining_time -= 1
        end_time = current_time
        if (
            gantt_chart
            and gantt_chart[-1][0] == current_process.pid
            and gantt_chart[-1][2] == start_time
        ):
            process_id, old_start_time, _ = gantt_chart[-1]
            gantt_chart[-1] = (
                process_id,
                old_start_time,
                end_time
            )
        else:
            gantt_chart.append(
                (
                    current_process.pid,
                    start_time,
                    end_time
                )
            )
        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            current_process.turnaround_time = (
                current_process.completion_time
                - current_process.arrival_time
            )
            current_process.waiting_time = (
                current_process.turnaround_time
                - current_process.burst_time
            )
            completed_count += 1
    return completed_processes, gantt_chart
