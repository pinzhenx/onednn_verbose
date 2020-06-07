try:
    import numpy as np
    mean = np.mean
    std = np.std
except ImportError:
    import statistics
    mean = statistics.mean
    std = statistics.pstdev
