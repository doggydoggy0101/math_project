### 3.9

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

x = np.array([2,3,4,5,6,7,8,9,10,11])
e = np.array([3.2,2.9,-1.7,-2.0,-2.3,-1.2,-0.9,0.8,0.7,0.5])

sns.set_style("darkgrid")
fig = plt.figure(figsize=(10,6))
plt.plot(x,e)
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
plt.xlabel("rooms")
plt.ylabel("residual")
plt.savefig('hw3.png')