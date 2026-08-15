from models import Process


def load_test_case(filename):

    processes = []

    with open(filename, "r") as file:

        for line in file:

            pid, at, bt = line.split()

            processes.append(
                Process(
                    pid,
                    int(at),
                    int(bt)
                )
            )

    return processes