from memory_profiler import profile

@profile
def run_pandas_analysis():
    import pandas as pd
    import os

    print(f"Subprocess (PID: {os.getpid()}): Starting pandas task.")

    print("Processing data with pandas...")