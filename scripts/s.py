import numpy as np
from pathlib import Path
import pickle

state = np.random.get_state()

p = Path('state.pickle')
if p.exists():
    with open(p, 'rb') as f:
        previous_state = pickle.load(f)

    print(f"state equal to previous state? {np.all(state[1]==previous_state[1])}", )

with open(p, 'wb') as f:
    pickle.dump(state, f)
