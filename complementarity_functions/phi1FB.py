import matplotlib
import matplotlib.pyplot as plt
import numpy as np


x=np.linspace(-10, 10)
y=np.linspace(-10, 10)
X,Y=np.meshgrid(x,y)

def func(a,b):
    return np.sqrt(np.power(a,2)+np.power(b,2))-(a+b)

fig=plt.figure(figsize=(6,6))
matplotlib.rcParams['font.size']=12 
ax=fig.gca( projection='3d')

Z=func(X,Y)
ax.plot_surface(X,Y,Z,cmap=matplotlib.cm.jet,alpha=0.9,linewidth=0.1,edgecolors='k')

ax.view_init(20,-110)
# ax.grid(False)
# plt.title(r'$φ_{FB}$',fontsize=20)
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
ax.set_zticks([0,10,20,30])
for t in ax.zaxis.get_major_ticks(): 
    t.label.set_fontsize(6)

tz = ax.zaxis.get_offset_text()
tz.set_fontsize(6)
plt.show()



