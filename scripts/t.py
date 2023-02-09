import numpy as np

s0 = np.random.get_state()
print(s0)

r = np.random.random(1)

s1 = np.random.get_state()
print(s1)

print(s1[1] == s0[1])