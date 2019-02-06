import numpy as np
from scipy.optimize import root
import matplotlib.pyplot as plt
import source


samples = np.random.randn(100)


def xi(x):
    return np.exp(-(source.r + source.theta ** 2 / 2) * source.T - source.theta * np.sqrt(source.T) * x)


def x_star(lda, muu, xi):
    x1 = source.b * source.x0
    x2 = (1 - source.w) * source.x0
    x3 = lda / 2 + muu * xi / 2 + source.x0
    x4 = source.x0
    x5 = lda / 2 / source.a + source.x0 + muu * xi / 2 / source.a ** 2
    x = np.array([x1, x2, x3, x4, x5])

    def f(x):
        return source.theta_tilda(x) ** 2 - lda * source.theta_tilda(x) - muu * xi * x
    y = np.array([f(x1), f(x2), f(x3), f(x4), f(x5)])
    return x[np.argmin(y)]


def expectation(lda, muu):
    return sum([source.theta_tilda((x_star(lda, muu, xi(samples[i])))) for i in range(100)]) / 100


def expectation2(lda, muu):
    return sum([xi(samples[i]) * x_star(lda, muu, xi(samples[i])) for i in range(100)]) / 100


def square_of_l2_norm(lda, muu):
    return sum([source.theta_tilda((x_star(lda, muu, xi(samples[i])))) ** 2 for i in range(100)]) / 100


def mv(z):
    def constraint(x):
        return expectation(x[0], x[1]) - z, expectation2(x[0], x[1]) - source.x0

    sol = root(constraint, [0, 0])
    lda, muu = sol.x
    success = sol.success

    print('lda=', lda, 'muu=', muu)
    print('expectation=', expectation(lda, muu), 'expectation2=', expectation2(lda, muu))
    print('w=', source.w, 'sigma=', source.sigma, 'z=', z)
    print('success=', success)

    return square_of_l2_norm(sol.x[0], sol.x[1]) - z ** 2, sol.success


# fig, ax = plt.subplots(figsize=(16, 10))
# source.attribution(sigma=0.2)
# points = np.array([[z, mv(z)[0]] for z in np.linspace(source.z0 - 0.5, source.z0 + 0.5) if mv(z)[1]]).T.reshape(2, -1)
# ax.plot(points[0], points[1])
# ax.axvline(ymax=0.8, x=source.z0, c='C1', linestyle='dashed')
# ax.text(0.5, 0.95, r'$w={}, \alpha={}, \sigma={}, \mu={}, r={}, b={}, X_0={}$'
#         .format(source.w, source.alpha, source.sigma, source.mu, source.r, source.b, source.x0), fontsize=20,
#             transform=ax.transAxes, horizontalalignment='center', verticalalignment='top')
# ax.set_ylabel('variance', fontsize=20)
# ax.set_xlabel('mean', fontsize=20)
# fig.savefig('figures/test/1.png')
