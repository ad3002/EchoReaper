import threading
import time

class TimeoutException(Exception):
    pass

def run_with_timeout(func, args=(), kwargs={}, timeout=5):
    class ThreadWithStop(threading.Thread):
        def __init__(self, target, args, kwargs):
            super().__init__(target=target, args=args, kwargs=kwargs)
            self._stop_event = threading.Event()

        def stop(self):
            self._stop_event.set()

        def stopped(self):
            return self._stop_event.is_set()

    def wrapper(stop_event, *args, **kwargs):
        try:
            result[0] = func(*args, **kwargs, stop_event=stop_event)
        except Exception as e:
            exception[0] = e

    result = [None]
    exception = [None]
    stop_event = threading.Event()

    thread = ThreadWithStop(target=wrapper, args=(stop_event, *args), kwargs=kwargs)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        thread.stop()
        thread.join()
        raise TimeoutException(f"Function {func.__name__} exceeded the time limit of {timeout} seconds")

    if exception[0]:
        raise exception[0]

    return result[0]

# Example usage
def example_function(sleep_time, stop_event):
    start_time = time.time()
    while time.time() - start_time < sleep_time:
        if stop_event.is_set():
            return "Function stopped"
        time.sleep(0.1)  # Sleep briefly to prevent high CPU usage
    return "Function completed"

# This should complete successfully
print(run_with_timeout(example_function, args=(2,), timeout=5))

# This should be stopped and raise a TimeoutException
try:
    print(run_with_timeout(example_function, args=(10,), timeout=5))
except TimeoutException as e:
    print(e)
