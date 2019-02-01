import os
import time


class Cleanup:
    """The somewhat automated garbage collection system"""

    def __init__(self):
        self.max_age_minutes = 20
        self.max_calls = 5
        self.path = './output'

        self.calls = 0

    def clean(self):
        if (self.calls < self.max_calls - 1):
            self.calls += 1
            return

        self.calls = 0
        now = time.time()

        for f in os.listdir(self.path):
            f = os.path.join(self.path, f)
            if (os.path.isfile(f) == False): continue

            file_time = os.stat(f).st_mtime
            if (file_time < (now - 60 * self.max_age_minutes)):
                os.remove(f)
