import time


# simple timer class for benchmarking with build in for nice printing
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        self.current_lap_start = self.start
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.perf_counter()
        self.elapsed = self.end - self.start

    def start(self):
        self.start = time.perf_counter()
        self.end = None
        return self

    def stop(self):
        self.end = time.perf_counter()
        self.elapsed = self.end - self.start

    @property
    def lap(self):
        lap_time = time.perf_counter() - self.current_lap_start
        self.current_lap_start = time.perf_counter()
        return lap_time

    @property
    def current_elapsed(self):
        return time.perf_counter() - self.start

    # stringify it nicely to three decimal seconds
    def __str__(self):
        value = getattr(self, "elapsed", self.current_elapsed)
        rounded = round(value, 3)
        return f"{rounded} sec"

    # format
    def __format__(self, spec):
        value = getattr(self, "elapsed", self.current_elapsed)
        if spec.endswith("ms"):
            return f"{value * 1000:.0f} ms"
        return f"{value:.3f} sec"

    # nice raw debug output
    def __repr__(self):
        return f"Timer(start={self.start}, end={self.end}, elapsed={getattr(self, 'elapsed', None)})"
