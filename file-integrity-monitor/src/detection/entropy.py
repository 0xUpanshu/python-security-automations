import math
from ..integrity import calculate_hash
from collections import Counter
from pathlib import Path


DEFAULT_SAMPLE_SIZE = 1024 * 1024  # 1 MB

def calculate_entropy(file_path: str, sample_size: int = DEFAULT_SAMPLE_SIZE) -> float:
    
    # Calculate Shannon entropy for a sample of a file.
    # Returns a value between 0.0 and 8.0.
    # 0.0  -> highly repetitive data. 8.0  -> maximum byte-level randomness
    path = Path(file_path)

    with path.open("rb") as file:
        data = file.read(sample_size)

    if not data:
        return 0.0

    frequencies = Counter(data)
    data_length = len(data)

    entropy = 0.0

    for count in frequencies.values():
        probability = count / data_length
        entropy -= probability * math.log2(probability)

    return entropy

def is_high_entropy(
    file_path: str,
    threshold: float = 7.2,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
) -> bool:
   
   # Determine whether a file has unusually high byte entropy.
    entropy = calculate_entropy(file_path, sample_size)
    return entropy >= threshold