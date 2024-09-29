import numpy as np
import matplotlib.pyplot as plt

def ellipse(x1, x2):
    "2*x1**2 + 3*x2**2 <= 5"
    return 2*(x1 - 1.2)**2 + 3*(x2 - 1.2)**2 - 1

dom = np.linspace(0, 3, 100)
xx, yy = np.meshgrid(dom, dom)
zz = ellipse(xx, yy)

x = xx[zz <= 0]
y = yy[zz <= 0]
num_set = len(x)

rays = [[x[i], y[i], 1] for i in range(num_set)]
hemisphere = np.array([ray / np.linalg.norm(ray) for ray in rays])
top_view = hemisphere.copy()
top_view[:, 2] = 0

def view_settings(ax):
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
    ax.set_zlim(0, 2.2)
    ax.view_init(elev=15, azim=-45)

def draw_sphere(ax):
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, color="tab:gray", alpha=0.1)

def draw_circle(ax):
    theta = np.linspace(0, 2*np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)
    ax.plot(x, y, lw=1, c="black")


fig = plt.figure(figsize=(9, 12), dpi=500)

ax1 = fig.add_subplot(321, projection='3d')
ax1.scatter(x, y, np.zeros(num_set), s=0.01, c="tab:red")
ax1.set_title("Convex Set", y=-0.05)
view_settings(ax1)

ax2 = fig.add_subplot(322, projection='3d')
ax2.scatter(x, y, np.zeros(num_set), s=0.01, c="tab:red")
ax2.scatter(x, y, np.ones(num_set), s=0.01, c="tab:blue")
for ray in rays:
    ax2.plot([0, ray[0]], [0, ray[1]], [0, ray[2]], lw=0.01, c="tab:blue")
ax2.set_title("Convex Cone", y=-0.05)
view_settings(ax2)

ax3 = fig.add_subplot(323, projection='3d')
ax3.scatter(x, y, np.ones(num_set), s=0.01, c="tab:blue")
for ray in rays:
    ax3.plot([0, ray[0]], [0, ray[1]], [0, ray[2]], lw=0.01, c="tab:blue")
ax3.scatter(*zip(*hemisphere), s=0.01, c="tab:green")
ax3.set_title("Hemisphere Model", y=-0.05)
draw_sphere(ax3)
view_settings(ax3)

ax4 = fig.add_subplot(324, projection='3d')
ax4.scatter(*zip(*hemisphere), s=0.01, c="tab:green")
ax4.set_title("Hemisphere Model (another angle)", y=-0.05)
draw_sphere(ax4)
view_settings(ax4)
ax4.view_init(elev=15, azim=45)

ax5 = fig.add_subplot(325, projection='3d')
ax5.scatter(*zip(*hemisphere), s=0.01, c="tab:green")
ax5.scatter(*zip(*top_view), s=0.01, c="tab:orange")
ax5.set_title("Top-view Model", y=-0.05)
draw_sphere(ax5)
draw_circle(ax5)
view_settings(ax5)

ax6 = fig.add_subplot(326)
ax6.scatter(*zip(*top_view[:, :2]), s=0.01, c="tab:orange")
ax6.set_title("Top-view Model (another angle)", y=-0.05)
draw_circle(ax6)
ax6.set_xlim(-2.4, 2.4)
ax6.set_ylim(-2, 2)
ax6.set_axis_off()

plt.tight_layout()
plt.savefig("docs/ellipse.png")
