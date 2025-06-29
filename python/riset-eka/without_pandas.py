from memory_profiler import profile

@profile
def test_without_pandas():
    print("This is a test function without pandas.")

test_without_pandas()