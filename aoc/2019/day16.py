import aocd
import numpy as np

data = np.fromiter(aocd.data, dtype=int)
pattern = np.array([0, 1, 0, -1])

signal = data.copy()
signal_pattern = np.array([np.resize(np.repeat(pattern, (i + 1)), len(signal) + 1)[1:] for i in range(len(signal))])

for _ in range(100):
    signal = np.abs(np.dot(signal_pattern, signal)) % 10

print("Part One:", "".join(str(n) for n in signal[:8]))

# observation: the i-th row in signal_pattern starts with i-1 zeros and i ones
# signal_pattern: [[ 1  0 -1  0]
#                  [ 0  1  1  0]
#                  [ 0  0  1  1]
#                  [ 0  0  0  1]]
# thus, for 2i - 1 <= n, i.e. i < n/2, the next phase's value is sum(signal[i:])

signal = np.tile(data, 10000)
start = int("".join(str(n) for n in data[:7]))
if 2 * start - 1 <= len(signal):
    raise ValueError("invalid input")

signal = signal[start:]
for _ in range(100):
    # cum_sum = signal.sum()
    # for i, s in enumerate(signal):
    #     signal[i] = partial_sum % 10
    #     partial_sum -= s
    signal = signal[::-1].cumsum()[::-1] % 10

print("Part Two:", "".join(str(n) for n in signal[:8]))
