import numpy as np

from utils.visualize import plot_2Dhomogenization

# ellipse, parabola
# SET = "ellipse"
SET = "parabola"

if SET == "ellipse":

    def ellipse(x1, x2):
        return 2 * (x1 - 1.2) ** 2 + 3 * (x2 - 1.2) ** 2 - 1

    dom = np.linspace(0, 3, 100)
    xx, yy = np.meshgrid(dom, dom)
    zz = ellipse(xx, yy)

elif SET == "parabola":

    def parabola(x1, x2):
        return (x1 - 0.6) ** 2 - (x2 - 0.6)

    dom = np.linspace(-2, 4, 150)
    xx, yy = np.meshgrid(dom, dom)
    zz = parabola(xx, yy)


x = xx[zz <= 0]
y = yy[zz <= 0]

rays = [[x[i], y[i], 1] for i in range(len(x))]
hemisphere = np.array([ray / np.linalg.norm(ray) for ray in rays])
top_view = hemisphere.copy()
top_view[:, 2] = 0

plot_2Dhomogenization(x, y, rays, hemisphere, top_view, fig_name=SET, dpi=240)
