#!/usr/bin/env python3
"""Part 2: Syntax validation and processor execution"""
import py_compile, os
from pathlib import Path

PROJECT = r"C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine"

# Validate syntax
print("Checking intake_processor.py syntax...")
try:
    py_compile.compile(f"{PROJECT}/05_Knowledge_Aggregator/intake_processor.py", doraise=True)
    print("Syntax OK\n")
except py_compile.PyCompileError as e:
    print(f"Syntax error: {e}")
    import sys; sys.exit(1)

# Execute processor
print("Executing intake_processor.py...")
result = os.system(f'python "{PROJECT}/05_Knowledge_Aggregator/intake_processor.py" 2>&1')
print(f"\nProcessor exit code: {result}")