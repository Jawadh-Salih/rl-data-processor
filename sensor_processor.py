# I want to generate a stream of data.
# Basically this should run it's own process and generate random data and save and
# should have send function process the data.This generate 100, and sends.
#

from datetime import datetime, timedelta
from multiprocessing import Process, Queue
from random import randint, random
from statistics import mean, stdev
from time import sleep

CHUNK_SIZE = 5


sensor_memory = list()


class SensorData:
    def __init__(self, value, timestamp) -> None:
        self.value = value
        self.timestamp = timestamp

    def to_dict(self):
        return {"value": self.value, "timestamp": self.timestamp}


def sensor_worker(queue: Queue, start_time, offset):
    current_time = start_time
    sensing_interval = 1
    # while True:
    for i in range(50):
        # I n±eed to deliberately miss some data.
        # I need to deliberate corrupt some data.
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


def data_worker(queue: Queue):
    while True:
        # for i in  range(10):
        # Get the first 100 data from the queue and remove them from the queue

        chunk = list()
        for i in range(CHUNK_SIZE):
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
        # TODO corrupted


if __name__ == "__main__":
    memory_size = 0
    q = Queue()
    sensor = Process(target=sensor_worker, args=(q, datetime.now(), memory_size))
    processor = Process(target=data_worker, args=(q,))

    sensor.start()
    processor.start()
    sensor.join()
    processor.join()
