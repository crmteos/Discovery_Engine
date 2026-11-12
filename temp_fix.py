#!/usr/bin/env python3
import sys

filepath = r'C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\06_Formalized_Model\06_Formalized_Model\src\axiomatic_transformer.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

add_functions = '''
# ---------------------------------------------------------------------------
# Basis Transformation Functions
# ---------------------------------------------------------------------------

def log10_to_log2(data: List[float]) -> List[float]:
    """Convert data from decimal (log10) basis to binary (log2) basis."""
    result = []
    for x in data:
        if x <= 0:
            result.append(0.0)
        else:
            result.append(math.log2(x))
    return result

def log2_to_log10(data: List[float]) -> List[float]:
    """Convert data from binary (log2) basis back to decimal (log10) basis."""
    result = []
    for x in data:
        if x <= 0:
            result.append(0.0)
        else:
            result.append(math.log10(x))
    return result

def time_to_frequency_spectrum(
    data: List[float],
    sample_interval: float = 1.0,
    return_phase: bool = False,
) -> Dict[str, Any]:
    """Transform a time-series parameter t into a frequency spectrum using DFT."""
    n = len(data)
    amplitudes = []
    frequencies = []
    for k in range(n // 2 + 1):
        amp = sum(
            data[n_idx] * math.cos(2 * math.pi * k * n_idx / n)
            for n_idx in range(n)
        )
        frequencies.append(k / (n * sample_interval))
        amplitudes.append(amp)
    return {"amplitudes": amplitudes, "frequencies": frequencies}
'''

# Insert after the load_modulating_keys function
marker = "\n\n    return keys\n\n_LOG = logging.getLogger('axiomatic_transformer')"
if marker in content:
    new_content = content.replace(marker, marker + add_functions)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Functions added successfully')
else:
    print('Marker not found, trying append...')
    if '_LOG = logging.getLogger("axiomatic_transformer")' in content:
        new_content = content + add_functions
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Functions appended at end')