import py_compile
import sys

filepath = r"C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator\src\search_intake_adapter.py"
try:
    py_compile.compile(filepath, doraise=True)
    print("SYNTAX OK - file compiles successfully")
    sys.exit(0)
except py_compile.PyCompileError as e:
    print(f"SYNTAX ERROR: {e}")
    sys.exit(1)