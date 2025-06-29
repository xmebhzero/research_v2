import polars as pl

from memory_profiler import profile

@profile
def test_with_polars():
    print("This is a test function WITH polars.")

test_with_polars()