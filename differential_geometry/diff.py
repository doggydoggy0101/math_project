import numpy as np 
from sympy import *
import matplotlib.pyplot as plt 

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

t = np.linspace(-10,10,100)

x, y, z = 2*np.cos(t), 2*np.sin(t), 5*t
x1, y1, z1 = np.gradient(x,t), np.gradient(y,t), np.gradient(z,t)
x2, y2, z2 = np.gradient(x1,t), np.gradient(y1,t), np.gradient(z1,t)

x_1, y_1, z_1 = -2*np.sin(t), 2*np.cos(t), 5
x_2, y_2, z_2 = -2*np.cos(t), -2*np.sin(t), 0

r=Symbol('r')
xs, ys, zs = 2*cos(r), 2*sin(r), 5*r
xs1, ys1, zs1 = diff(xs,r), diff(ys,r), diff(zs,r)
xs2, ys2, zs2 = diff(xs1,r), diff(ys1,r), diff(zs1,r)

fig = plt.figure(figsize=(10,6))
plt.tight_layout(pad=2)

ax=fig.add_subplot(231, projection='3d')
ax.xaxis._axinfo["grid"]['linewidth']=0.2
ax.yaxis._axinfo["grid"]['linewidth']=0.2
ax.zaxis._axinfo["grid"]['linewidth']=0.2
ax.plot(x,y,z)

Ab1=np.sqrt(np.power(x1,2)+np.power(y1,2)+np.power(z1,2))
Ab2=np.sqrt(np.power(x_1,2)+np.power(y_1,2)+np.power(z_1,2))

Tx1, Ty1, Tz1 = x1/Ab1.mean(), y1/Ab1.mean(), z1/Ab1.mean()
ax=fig.add_subplot(232, projection='3d')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis._axinfo["grid"]['linewidth']=0.2
ax.yaxis._axinfo["grid"]['linewidth']=0.2
ax.zaxis._axinfo["grid"]['linewidth']=0.2
ax.plot(t,Tx1,0)
ax.plot(t,Ty1,0)
# plt.title("電腦微分",fontsize=10)
plt.legend(['Tx', 'Ty'])

Tx2, Ty2, Tz2 = x_1/Ab2[0], y_1/Ab2[0], z_1/Ab2[0]
ax=fig.add_subplot(233, projection='3d')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis._axinfo["grid"]['linewidth']=0.2
ax.yaxis._axinfo["grid"]['linewidth']=0.2
ax.zaxis._axinfo["grid"]['linewidth']=0.2
ax.plot(t,Tx2,0)
ax.plot(t,Ty2,0)
plt.legend(['Tx', 'Ty'])


Cx1, Cy1, Cz1 = y1*z2-y2*z1, -x1*z2+x2*z1, x1*y2-x2*y1
ax=fig.add_subplot(235, projection='3d')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis._axinfo["grid"]['linewidth']=0.2
ax.yaxis._axinfo["grid"]['linewidth']=0.2
ax.zaxis._axinfo["grid"]['linewidth']=0.2
ax.plot(t,Cx1,0)
ax.plot(t,Cy1,0)
plt.legend(['Cx', 'Cy'])

Cx2, Cy2, Cz2 = y_1*z_2-y_2*z_1, -x_1*z_2+x_2*z_1, x_1*y_2-x_2*y_1
ax=fig.add_subplot(236, projection='3d')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis._axinfo["grid"]['linewidth']=0.2
ax.yaxis._axinfo["grid"]['linewidth']=0.2
ax.zaxis._axinfo["grid"]['linewidth']=0.2
ax.plot(t,Cx2,0)
ax.plot(t,Cy2,0)
plt.legend(['Cx', 'Cy'])

K1=np.sqrt(np.power(Cx1,2)+np.power(Cy1,2)+np.power(Cz1,2))/np.power(Ab1,3)
K2=np.sqrt(np.power(Cx2,2)+np.power(Cy2,2)+np.power(Cz2,2))/np.power(Ab2,3)

plt.show()