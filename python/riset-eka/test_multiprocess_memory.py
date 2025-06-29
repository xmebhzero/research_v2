import multiprocessing
import os
from memory_profiler import profile
from pandas_multiprocessing import run_pandas_analysis

@profile
def just_print():
    print("This function does not require any imports.")

@profile
def test_main():

    pandas_process = multiprocessing.Process(target=run_pandas_analysis)
    print(f"Main process (PID: {os.getpid()}): Starting pandas subprocess...")
    pandas_process.start()

    print(f"Main process (PID: {os.getpid()}): Waiting for pandas subprocess to finish...")
    pandas_process.join() # This blocks until the subprocess terminates

    print(f"Main process (PID: {os.getpid()}): Pandas subprocess finished.")

    # Run other tasks again to show pandas is not loaded in the main process memory
    print(f"Main process (PID: {os.getpid()}): Executing other tasks...")
    just_print()

test_main()