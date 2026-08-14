class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time

        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0

    def __str__(self):
        return (
            f"Process(pid={self.pid}, "
            f"arrival_time={self.arrival_time}, "
            f"burst_time={self.burst_time})"
        )