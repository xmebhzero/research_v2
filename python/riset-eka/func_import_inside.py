from memory_profiler import profile

class RequirePandas:
    @profile
    def func(self):
        import pandas as pd
        print("Pandas is required for this function.")

class RequireNothing:
    @profile
    def func(self):
        print("This function does not require any imports.")


RequirePandas().func()
RequireNothing().func()