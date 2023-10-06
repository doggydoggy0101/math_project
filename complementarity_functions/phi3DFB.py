import matplotlib
import matplotlib.pyplot as plt
import numpy as np


x=np.linspace(-10, 10)
y=np.linspace(-10, 10)
X,Y=np.meshgrid(x,y)

def func(a,b):
    return np.power(np.sqrt(np.power(a,2)+np.power(b,2)),3)-np.power((a+b),3)

fig=plt.figure(figsize=(6,6))
matplotlib.rcParams['font.size']=12 
ax=fig.gca( projection='3d')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis._axinfo["grid"]['linewidth']=0.2
ax.yaxis._axinfo["grid"]['linewidth']=0.2
ax.zaxis._axinfo["grid"]['linewidth']=0.2

Z=func(X,Y)
ax.plot_surface(X,Y,Z,cmap=matplotlib.cm.coolwarm,alpha=0.9,linewidth=0.1,edgecolors='k')

ax.view_init(15,15)
# ax.grid(False)
# plt.title(r'$φ_{FB}$',fontsize=20)
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
ax.set_zticks([-4000,-2000,0,2000,4000,6000,8000,10000])
for t in ax.zaxis.get_major_ticks(): 
    t.label.set_fontsize(6)
# formatter = ticker.ScalarFormatter(useMathText=True)
# formatter.set_scientific(True) 
# formatter.set_powerlimits((-10,10)) 
# ax.zaxis.set_major_formatter(formatter) 

tz = ax.zaxis.get_offset_text()
tz.set_fontsize(7)
plt.show()
