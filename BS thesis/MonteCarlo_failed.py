import numpy as np
from scipy.optimize import root
import source


samples = np.random.randn(10000)


def theta_tilda(x):
    if x >= source.x0:
        return source.a * (x - source.x0)
    if (1 - source.w) * source.x0 <= x < source.x0:
        return x - source.x0
    if x < (1 - source.w) * source.x0:
        return -source.w * source.x0


def xi(x):
    return np.exp(-(source.r + source.theta ** 2) * source.T - source.theta * np.sqrt(source.T) * x)


def x_star(lda, muu, xi):
    x1 = source.b * source.x0
    x2 = (1 - source.w) * source.x0
    x3 = lda / 2 + muu * xi / 2
    x4 = source.x0
    x5 = lda / 2 / source.a + source.x0 + muu * xi / 2 / source.a ** 2

    def f(x):
        return theta_tilda(x) ** 2 - lda * theta_tilda(x) - muu * xi * x
    if muu > 0:
        if source.x0 <= x5:
            if xi <= -(2 * source.w * source.x0 - lda) / muu and f(x2) <= f(x5):
                return x2
            if -lda / muu <= xi <= -2 * lda * source.a / muu / (1 + source.a):
                return x3
            else:
                return x5
        else:
            if xi <= -(2 * source.w * source.x0 - lda) / muu:
                return x2
            if -lda / muu <= xi:
                return x4
            else:
                return x3
    if muu < 0:
        if source.x0 <= x5:
            if xi > -(2 * source.w * source.x0 - lda) / muu and f(x1) > f(x5):
                return x5
            if -lda / muu > xi > -(2 * source.w * source.x0 - lda) / muu \
                and xi > -2 * lda * source.a / muu / (1 + source.a):
                return x5
            if -lda / muu > xi and f(x1) > f(x5):
                return x5
            if -lda / muu <= xi <= -2 * lda * source.a / muu / (1 + source.a) \
                and xi <= -2 * lda * source.a / muu / (1 + source.a) and f(x1) > f(x3):
                return x3
            else:
                return x1
        else:
            if -lda / muu > xi and f(x1) > f(x4):
                return x4
            if -lda / muu <= xi <= -2 * lda * source.a / muu / (1 + source.a) and f(x1) > f(x3):
                return x3
            else:
                return x1
    else:
        if source.x0 <= x5:
            if lda / 2 <= -source.w * source.x0:
                if f(x1) >= f(x5):
                    return x5
                else:
                    return x1
            if -source.w * source.x0 <= lda / 2 <= 0:
                if f(x3) >= f(x5):
                    return x5
                else:
                    return x3
            else:
                return x5
        else:
            if lda / 2 <= -source.w * source.x0:
                return x1
            if -source.w * source.x0 <= lda / 2 <= 0:
                return x3
            else:
                return x4


def expectation(lda, muu):
    return sum([theta_tilda((x_star(lda, muu, xi(samples[i])))) for i in range(10000)]) / 10000


def expectation2(lda, muu):
    return sum([xi(samples[i]) * x_star(lda, muu, xi(samples[i])) for i in range(10000)]) / 10000


def square_of_l2_norm(lda, muu):
    return expectation(lda, muu) ** 2


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


print(mv(source.z0))
