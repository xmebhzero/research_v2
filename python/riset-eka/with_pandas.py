import pandas as pd

from memory_profiler import profile

@profile
def test_with_pandas():
    print("This is a test function WITH pandas.")

test_with_pandas()