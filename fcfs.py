def run_fcfs(processes):

    processes = sorted(
        processes,
        key=lambda process: process.arrival_time
    )

    completed_processes = []
    gantt_chart = []
    current_time = 0

    for current_process in processes:

        if current_time < current_process.arrival_time:

            gantt_chart.append(
                (
                    "IDLE",
                    current_time,
                    current_process.arrival_time
                )
            )

            current_time = current_process.arrival_time

        start_time = current_time

        current_process.started = True

        current_process.response_time = (
            start_time
            - current_process.arrival_time
        )

        end_time = (
            start_time
            + current_process.burst_time
        )

        current_process.completion_time = end_time
        current_process.remaining_time = 0

        current_process.turnaround_time = (
            current_process.completion_time
            - current_process.arrival_time
        )

        current_process.waiting_time = (
            current_process.turnaround_time
            - current_process.burst_time
        )

        current_time = end_time

        gantt_chart.append(
            (
                current_process.pid,
                start_time,
                end_time
            )
        )

        completed_processes.append(current_process)

    return completed_processes, gantt_chart