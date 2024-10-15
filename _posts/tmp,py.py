

#%%
import numpy as np

import matplotlib.pyplot as plt


#%%

vs = np.array([0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2])/3
rs = np.array([0.0473, 0.0309, 0.0212, 0.0161, 0.0135, 0.0120, 0.0111, 0.0105])


plt.plot(vs, rs, '.-')
plt.xlabel('Velocity (c)')
plt.ylabel('radius')

plt.grid(True)

# %%
