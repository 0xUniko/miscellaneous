import math

w = 0.5
alpha = 0.3
sigma = 0.4
mu = 0.2
r = 0.05
theta = (mu - r)/sigma
b = 0.5
T = 1
x0 = 1
a = w + alpha * (1 - w)


def theta_tilda(x):
    if x >= x0:
        return a * (x - x0)
    if (1 - w) * x0 <= x < x0:
        return x - x0
    if x < (1 - w) * x0:
        return -w * x0


z0 = theta_tilda(x0 / math.exp(-r * T))


def attribution(**kw):
    global w, alpha, sigma, mu, r, theta, b, T, x0, a, z0
    var = [w, alpha, sigma, mu, r, b, T, x0]
    for i in enumerate(['w', 'alpha', 'sigma', 'mu', 'r', 'b', 'T', 'x0']):
        if i[1] in kw:
            var[i[0]] = kw[i[1]]
    w, alpha, sigma, mu, r, b, T, x0 = var[0], var[1], var[2], var[3], var[4], var[5], var[6], var[7]
    theta = (mu - r) / sigma
    a = w + alpha * (1 - w)
    z0 = theta_tilda(x0 / math.exp(-r * T))


def inverse_xi(x):
    return (-(r + theta ** 2 / 2) * T - math.log(x)) / theta / math.sqrt(T)


def zero_moment(downbdd, upbdd):
    if upbdd == 'infty':
        if downbdd > 0:
            return (1 + math.erf(inverse_xi(downbdd) / math.sqrt(2))) / 2
        else:
            return 1
    elif downbdd < upbdd:
        if downbdd > 0:
            return (math.erf(inverse_xi(downbdd) / math.sqrt(2)) - math.erf(inverse_xi(upbdd) / math.sqrt(2))) / 2
        elif upbdd > 0:
            return (1 - math.erf(inverse_xi(upbdd) / math.sqrt(2))) / 2
        else:
            return 0
    else:
        return 0


def first_moment(downbdd, upbdd):
    if upbdd == 'infty':
        if downbdd > 0:
            return math.exp(-r * T) * \
                   (1 + math.erf((inverse_xi(downbdd) + math.sqrt(T) * theta) / math.sqrt(2))) / 2
        else:
            return math.exp(-r * T)
    if downbdd < upbdd:
        if downbdd > 0:
            return math.exp(-r * T) * (math.erf((inverse_xi(downbdd) + math.sqrt(T) * theta) / math.sqrt(2)) -
                    math.erf((inverse_xi(upbdd) + math.sqrt(T) * theta) / math.sqrt(2))) / 2
        elif upbdd > 0:
            return math.exp(-r * T) * \
                   (1 - math.erf((inverse_xi(upbdd) + math.sqrt(T) * theta) / math.sqrt(2))) / 2
        else:
            return 0
    else:
        return 0


def second_moment(downbdd, upbdd):
    if upbdd == 'infty':
        if downbdd > 0:
            return math.exp((- 2 * r + theta ** 2) * T) * \
                   (1 + math.erf((inverse_xi(downbdd) + 2 * math.sqrt(T) * theta) / math.sqrt(2))) / 2
        else:
            return math.exp((- 2 * r + theta ** 2) * T)
    if downbdd < upbdd:
        if downbdd > 0:
            return math.exp((- 2 * r + theta ** 2) * T) * (math.erf((inverse_xi(downbdd) + 2 * math.sqrt(T) * theta)
                    / math.sqrt(2)) - math.erf((inverse_xi(upbdd) + 2 * math.sqrt(T) * theta) / math.sqrt(2))) / 2
        elif upbdd > 0:
            return math.exp((- 2 * r + theta ** 2) * T) * \
                   (1 - math.erf((inverse_xi(upbdd) + 2 * math.sqrt(T) * theta) / math.sqrt(2))) / 2
        else:
            return 0
    else:
        return 0
