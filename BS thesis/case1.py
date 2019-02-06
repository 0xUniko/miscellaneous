from scipy.optimize import root
import source


def attribution_case():
    global w, alpha, sigma, r, mu, theta, b, T, x0, a
    w = source.w
    alpha = source.alpha
    sigma = source.sigma
    r = source.r
    mu = source.mu
    theta = (mu - r)/sigma
    b = source.b
    T = source.T
    x0 = source.x0
    a = w + alpha * (1 - w)


def subsituation(lda, muu):
    attribution_case()
    if muu == 0:
        if x0 + lda / 2 / a > b * x0:
            return [['one', 0, 'infty']]
        else:
            return [['two', 0, 'infty']]
    if muu > 0:
        return [['one', (2 * a ** 2 * (b - 1) * x0 - lda * a) / muu, 'infty'],
                ['two', 0, (2 * a ** 2 * (b - 1) * x0 - lda * a) / muu]]
    elif muu < 0:
        return [['one', 0, (2 * a ** 2 * (b - 1) * x0 - lda * a) / muu],
                ['two', (2 * a ** 2 * (b - 1) * x0 - lda * a) / muu, 'infty']]


def expectation(lda, muu):
    attribution_case()

    def one(downbdd, upbdd):
        return (x0 + lda / 2 / a) * source.zero_moment(downbdd, upbdd) + muu / 2 / a ** 2 * source.first_moment(downbdd, upbdd)

    def two(downbdd, upbdd):
        return b * x0 * source.zero_moment(downbdd, upbdd)

    sub = subsituation(lda, muu)
    expt = 0
    for item in sub:
        expt += eval(item[0])(item[1], item[2])
    return a * (expt - x0)


def expectation2(lda, muu):
    attribution_case()

    def one(downbdd, upbdd):
        return (x0 + lda / 2 / a) * source.first_moment(downbdd, upbdd) + muu / 2 / a ** 2 * source.second_moment(downbdd, upbdd)

    def two(downbdd, upbdd):
        return b * x0 * source.zero_moment(downbdd, upbdd)

    sub = subsituation(lda, muu)
    expt = 0
    for item in sub:
        expt += eval(item[0])(item[1], item[2])
    return expt


def square_of_l2_norm(lda, muu):
    attribution_case()

    def one(downbdd, upbdd):
        return (lda / 2 / a) ** 2 * source.zero_moment(downbdd, upbdd) + lda / a * muu / 2 / a ** 2 * \
                source.first_moment(downbdd, upbdd) + muu ** 2 / 4 / a ** 4 * source.second_moment(downbdd, upbdd)

    def two(downbdd, upbdd):
        return (b - 1) ** 2 * x0 ** 2 * source.zero_moment(downbdd, upbdd)

    sub = subsituation(lda, muu)
    expt = 0
    for item in sub:
        expt += eval(item[0])(item[1], item[2])
    return a ** 2 * expt


def mv(z):
    attribution_case()

    def constraint(x):
        return expectation(x[0], x[1]) - z, expectation2(x[0], x[1]) - x0

    sol = root(constraint, [0, 0])
    lda, muu = sol.x
    success = sol.success

    print('lda=', lda, 'muu=', muu)
    print('expectation=', expectation(lda, muu), 'expectation2=', expectation2(lda, muu))
    print('w=', source.w, 'sigma=', source.sigma, 'z=', z)
    print('success=', success)

    return square_of_l2_norm(sol.x[0], sol.x[1]) - z ** 2, sol.success


print(mv(source.z0-0.5), mv(source.z0), mv(source.z0+0.5))
