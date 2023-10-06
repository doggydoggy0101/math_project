import matplotlib
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

x=np.linspace(-10, 10)
y=np.linspace(-10, 10)
X,Y=np.meshgrid(x,y)
kk=0.2
def func(a,b):
    return np.power(np.sqrt(np.power(a,2)+np.power(b,2)),9)-np.power((a+b),9)

fig=plt.figure(figsize=(6,6))
matplotlib.rcParams['font.size']=12
ax=fig.gca( projection='3d')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis._axinfo["grid"]['linewidth']=kk
ax.yaxis._axinfo["grid"]['linewidth']=kk
ax.zaxis._axinfo["grid"]['linewidth']=kk

Z=func(X,Y)
ax.plot_surface(X,Y,Z,cmap=matplotlib.cm.coolwarm,alpha=0.99,linewidth=0.1,edgecolors='k')

ax.view_init(15,15)
# ax.grid(False)
# plt.title(r'$φ_{FB}$',fontsize=20)
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
ax.set_zticks([-4*10**11,-2*10**11,0,2*10**11,4*10**11])
for t in ax.zaxis.get_major_ticks(): 
    t.label.set_fontsize(6)

formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True) 
formatter.set_powerlimits((-1,1)) 
ax.zaxis.set_major_formatter(formatter) 
tz = ax.zaxis.get_offset_text()
tz.set_fontsize(7)

plt.show()