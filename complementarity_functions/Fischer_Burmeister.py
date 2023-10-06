import matplotlib
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np


x=np.linspace(-10, 10)
y=np.linspace(-10, 10)
X,Y=np.meshgrid(x,y)

v=15
w=40

def func(a,b):
    return np.sqrt(np.power(a,2)+np.power(b,2))-(a+b)

fig = plt.figure(figsize=(8,6))
plt.tight_layout(pad=2)
matplotlib.rcParams['font.size']=12 

ax = fig.add_subplot(221, projection='3d')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis._axinfo["grid"]['linewidth']=0.2
ax.yaxis._axinfo["grid"]['linewidth']=0.2
ax.zaxis._axinfo["grid"]['linewidth']=0.2
plt.title(r'$φ_{FB}$',fontsize=10)

Z=func(X,Y)
ax.plot_surface(X,Y,Z,cmap=matplotlib.cm.coolwarm,alpha=0.9,linewidth=0.1,edgecolors='k')
ax.view_init(v,w)

plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
ax.set_zticks([0,10,20,30])
for t in ax.zaxis.get_major_ticks(): 
    t.label.set_fontsize(6)

formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True) 
formatter.set_powerlimits((-10,10)) 
ax.zaxis.set_major_formatter(formatter) 

tz = ax.zaxis.get_offset_text()
tz.set_fontsize(7)



ax = fig.add_subplot(222, projection='3d')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis._axinfo["grid"]['linewidth']=0.2
ax.yaxis._axinfo["grid"]['linewidth']=0.2
ax.zaxis._axinfo["grid"]['linewidth']=0.2

Z=np.minimum(X,Y)
ax.plot_surface(X,Y,Z,cmap=matplotlib.cm.coolwarm,alpha=0.9,linewidth=0.1,edgecolors='k')
ax.view_init(v,w)
plt.title(r'$φ_{NR}$',fontsize=10)
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
ax.set_zticks([-10,-5,0,5,10])
for t in ax.zaxis.get_major_ticks(): 
    t.label.set_fontsize(6)

ax = fig.add_subplot(223, projection='3d')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis._axinfo["grid"]['linewidth']=0.2
ax.yaxis._axinfo["grid"]['linewidth']=0.2
ax.zaxis._axinfo["grid"]['linewidth']=0.2

Z=np.power(np.abs(func(X,Y)),2)*0.5
ax.plot_surface(X,Y,Z,cmap=matplotlib.cm.coolwarm,alpha=0.9,linewidth=0.1,edgecolors='k')
ax.view_init(v,w)

plt.title(r'$ψ_{FB}$',fontsize=10)
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
ax.set_zticks([100,200,300,400,500])
for t in ax.zaxis.get_major_ticks(): 
    t.label.set_fontsize(6)



ax = fig.add_subplot(224, projection='3d')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis._axinfo["grid"]['linewidth']=0.2
ax.yaxis._axinfo["grid"]['linewidth']=0.2
ax.zaxis._axinfo["grid"]['linewidth']=0.2


Z=np.power(np.abs(np.minimum(X,Y)),2)*0.5
ax.plot_surface(X,Y,Z,cmap=matplotlib.cm.coolwarm,alpha=0.9,linewidth=0.1,edgecolors='k')
ax.view_init(v,w)

plt.title(r'$ψ_{NR}$',fontsize=10)
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
ax.set_zticks([10,20,30,40,50])
for t in ax.zaxis.get_major_ticks(): 
    t.label.set_fontsize(6)

plt.show()