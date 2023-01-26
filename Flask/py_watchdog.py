import time
from concurrent.futures import ThreadPoolExecutor
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    def __init__(self, directory, max_workers=3):
        self.observer = Observer()
        self.directory = directory
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def run(self):
        event_handler = Handler(self.executor)
        self.observer.schedule(event_handler, self.directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except Exception as e:
            self.observer.stop()
            print(f"Error: {e}")
            self.executor.shutdown()

        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, executor):
        self.executor = executor

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            print(f"{event.src_path} created")
            self.executor.submit(process_file, event.src_path)
        elif event.event_type == 'modified':
            print(f"{event.src_path} modified")
            self.executor.submit(process_file, event.src_path)

        # check the number of task in queue
        task_in_queue = self.executor._work_queue.qsize()
        print(f"Number of task in queue: {task_in_queue}")



        # check the total number of workers
        total_workers = self.executor._max_workers
        print(f"Total number of workers: {total_workers}")

def process_file(file_path):
    import random

    random_number = random.randint(10, 30)
    print(f"{file_path} - {random_number} is processing")

    time.sleep(random_number)

    if random_number % 5 == 0:
        print(f"Break for file {file_path}")
        raise Exception(f"Break for file {file_path}")

    print(f"{file_path}  is processed")

    # check the number of task in queue
    task_in_queue = self.executor._work_queue.qsize()
    print(f"Number of task in queue: {task_in_queue}")


if __name__ == '__main__':
    try:
        w = Watcher("/Users/Dhaval/input/", max_workers=3)
        w.run()
    except Exception as e:
        print(f"Error: {e}")

