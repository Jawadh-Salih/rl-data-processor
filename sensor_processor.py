import argparse
from datetime import datetime, timedelta
from multiprocessing import Process, Queue
from random import randint, random
from statistics import mean, stdev
from time import sleep

sensor_memory = list()


class SensorData:
    def __init__(self, value, timestamp) -> None:
        self.value = value
        self.timestamp = timestamp

    def to_dict(self):
        return {"value": self.value, "timestamp": self.timestamp}


def sensor_worker(queue: Queue, start_time, offset, mode):
    current_time = start_time
    sensing_interval = 1
    iterator = iter(int, 1) if mode == "i" else iter(range(mode))
    for i in iterator:
        # Generate missing (5% probability) and corrupted (10% probability) data.
        data = SensorData(randint(0, 100), current_time)
        chance = random()
        if chance < 0.05:  # Probability of missing data
            data = SensorData(None, current_time)
        elif chance < 0.1:  # Probability to get corrupted data
            data = SensorData(randint(100, 1000), current_time)
        current_time = current_time + timedelta(seconds=sensing_interval)
        queue.put(data)
        offset = offset + 1
        print(f"Sensor: collected chunk of {offset}")
        sleep(sensing_interval)


def data_worker(queue: Queue, chunk_size):
    while True:
        chunk = list()
        for i in range(chunk_size):
            d = queue.get()
            chunk.append(d)

        print(f"Processor: received chunk of {len(chunk)}")
        missing_count = sum(1 for s in chunk if s.value is None)
        corrupted_count = sum(1 for s in chunk if s.value and s.value > 100)
        values = [s.value for s in chunk if s.value and s.value >= 0 and s.value <= 100]

        print("Statistics")
        print(f"Processable number of data is : {len(values)}")

        print(f"Average of the block : {mean(values)}")
        print(f"Maximum of the block : {max(values)}")
        print(f"Minimum of the block : {min(values)}")
        print(f"Standard Deviation of the block : {stdev(values)}")
        print(f"Missing data from the block : {missing_count}")
        print(f"Corrupted data from the block : {corrupted_count}")
        sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sensor data simulator and processor")
    parser.add_argument(
        "mode", help="'i' for infinite mode, or a number for finite mode (e.g. 50)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=None,
        help="Number of samples per chunk (default: 10%% of samples in finite mode, 5 in infinite mode)",
    )
    args = parser.parse_args()

    if args.mode == "i":
        mode = "i"
        chunk_size = args.chunk_size if args.chunk_size is not None else 100
    else:
        mode = int(args.mode)
        chunk_size = (
            args.chunk_size if args.chunk_size is not None else max(1, mode // 10)
        )
        if mode < chunk_size:
            raise ValueError(
                f"Number of samples ({mode}) must be >= chunk size ({chunk_size})"
            )
        if mode % chunk_size != 0:
            raise ValueError(
                f"Number of samples ({mode}) must be a multiple of chunk size ({chunk_size})"
            )

    memory_size = 0
    q = Queue()
    sensor = Process(target=sensor_worker, args=(q, datetime.now(), memory_size, mode))
    processor = Process(target=data_worker, args=(q, chunk_size))

    sensor.start()
    processor.start()
    sensor.join()
    processor.join()
