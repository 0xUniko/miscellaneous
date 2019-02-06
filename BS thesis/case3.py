import math
import numpy as np
from scipy.optimize import root
from matplotlib import pyplot as plt

w = 0.4
alpha = 0.3
sigma = 1
mu = 2
r = 1
theta = (mu - r)/sigma
b = 1.1
T = 1
x0 = 1


def zero_moment(downbdd, upbdd):
    if upbdd == 'infty':
        if downbdd > 0:
            high = ((- r + theta ** 2 / 2) * T - math.log(downbdd)) / theta
            return (1 + math.erf((high + T * theta) / math.sqrt(2 * T))) / 2
        else:
            return 1
    elif downbdd < upbdd:
        if downbdd > 0:
            low = ((- r + theta ** 2 / 2) * T - math.log(upbdd)) / theta
            high = ((- r + theta ** 2 / 2) * T - math.log(downbdd)) / theta
            return (math.erf((high + T * theta) / math.sqrt(2 * T)) - math.erf((low + T * theta) / math.sqrt(2 * T))) / 2
        elif upbdd > 0:
            low = ((- r + theta ** 2 / 2) * T - math.log(upbdd)) / theta
            return (1 - math.erf((low + T * theta) / math.sqrt(2 * T))) / 2
        else:
            return 0
    else:
        return 0


def first_moment(downbdd, upbdd):
    if upbdd == 'infty':
        if downbdd > 0:
            high = ((- r + theta ** 2 / 2) * T - math.log(downbdd)) / theta
            return math.exp((- r + theta ** 2) * T) * (1 + math.erf((high + T * theta) / math.sqrt(2 * T))) / 2
        else:
            return math.exp((- r + theta ** 2) * T)
    if downbdd < upbdd:
        if downbdd > 0:
            low = ((- r + theta ** 2 / 2) * T - math.log(upbdd)) / theta
            high = ((- r + theta ** 2 / 2) * T - math.log(downbdd)) / theta
            return math.exp((- r + theta ** 2) * T) * (math.erf((high + T * theta) / math.sqrt(2 * T)) -
                math.erf((low + T * theta) / math.sqrt(2 * T))) / 2
        elif upbdd > 0:
            high = ((- r + theta ** 2 / 2) * T - math.log(upbdd)) / theta
            return math.exp((- r + theta ** 2) * T) * (1 - math.erf((high + T * theta) / math.sqrt(2 * T))) / 2
        else:
            return 0
    else:
        return 0


def second_moment(downbdd, upbdd):
    if upbdd == 'infty':
        if downbdd > 0:
            high = ((- r + theta ** 2 / 2) * T - math.log(downbdd)) / theta
            return math.exp((- 2 * r + 3 * theta ** 2) * T) * (1 + math.erf((high + T * theta) / math.sqrt(2 * T))) / 2
        else:
            return math.exp((- 2 * r + 3 * theta ** 2) * T)
    if downbdd < upbdd:
        if downbdd > 0:
            low = ((- r + theta ** 2 / 2) * T - math.log(upbdd)) / theta
            high = ((- r + theta ** 2 / 2) * T - math.log(downbdd)) / theta
            return math.exp((- 2 * r + 3 * theta ** 2) * T) * (math.erf((high + 2 * T * theta) / math.sqrt(2 * T)) -
                math.erf((low + 2 * T * theta) / math.sqrt(2 * T))) / 2
        elif upbdd > 0:
            low = ((- r + theta ** 2 / 2) * T - math.log(upbdd)) / theta
            return math.exp((- 2 * r + 3 * theta ** 2) * T) * (1 - math.erf((low + 2 * T * theta) / math.sqrt(2 * T))) / 2
        else:
            return 0
    else:
        return 0


def subsituation(lda, muu):
    if muu == 0:
        if lda / 2 / (w + alpha * (1 - w)) > 0:
            if - lda ** 2 / 4 < w ** 2 * x0 ** 2 + lda * w * x0:
                return [['five', 0, 'infty']]
            else:
                return [['two', 0, 'infty']]
        else:
            if 0 < w ** 2 * x0 ** 2 + lda * w * x0:
                return [['four', 0, 'infty']]
            else:
                return [['two', 0, 'infty']]
    else:
        cutting1 = - lda * (w + alpha * (1 - w)) / muu
        cutting2 = - 2 * lda * (w + alpha * (1 - w)) / (muu * (1 + w + alpha * (1 - w)))
        cutting5_b = (w ** 2 * x0 ** 2 + lda * w * x0) / muu / x0 / (b - 1)
        cutting5_1_w = - (w * x0 ** 2 + lda * x0) / muu / x0
        cutting6 = (- 2 * w * x0 - lda) / muu
        cutting7 = - lda / muu
        delta3_b = 2 * lda * muu * (w + alpha * (1 - w)) ** 2 + 2 * muu * x0 - 4 * muu * b * x0 * \
                    (w + alpha * (1 - w)) ** 2 - 4 * muu ** 2 * (2 * lda ** 2 * (w + alpha * (1 - w)) ** 2 +
                    4 * (w + alpha * (1 - w)) ** 2 * (w ** 2 * x0 ** 2 + lda * w * x0))
        delta3_1_w = 2 * lda * muu * (w + alpha * (1 - w)) ** 2 + 2 * muu * x0 - 4 * muu * (1 - w) * x0 * \
                    (w + alpha * (1 - w)) ** 2 - 4 * muu ** 2 * (2 * lda ** 2 * (w + alpha * (1 - w)) ** 2 +
                    4 * (w + alpha * (1 - w)) ** 2 * (w ** 2 * x0 ** 2 + lda * w * x0))
        delta4_b = (2 * muu * lda - muu * b * x0 + 4 * muu * x0) ** 2 - 4 * muu ** 2 * \
                   (lda ** 2 + 4 * (w ** 2 * x0 ** 2 + lda * w * x0))
        delta4_1_w = (2 * muu * lda - muu * (1 - w) * x0 + 4 * muu * x0) ** 2 - 4 * muu ** 2 * \
                    (lda ** 2 + 4 * (w ** 2 * x0 ** 2 + lda * w * x0))
        if muu > 0:
            if delta3_1_w <= 0:
                e111 = [['five', cutting1, cutting6]]
            else:
                cutting3_1_w_low = (-(2 * muu * lda * (w + alpha * (1 - w)) + 2 * muu * x0 - 4 * muu * b * x0 *
                                      (w + alpha * (1 - w)) ** 2) - math.sqrt(delta3_1_w)) / 2 / muu ** 2
                cutting3_1_w_high = (-(2 * muu * lda * (w + alpha * (1 - w)) + 2 * muu * x0 - 4 * muu * b * x0 *
                                       (w + alpha * (1 - w)) ** 2) + math.sqrt(delta3_1_w)) / 2 / muu ** 2
                e111 = [['five', cutting1, min(cutting3_1_w_low, cutting6)], ['five', max(cutting1, cutting3_1_w_high), cutting6],
                        ['two', max(cutting1, cutting3_1_w_low), min(cutting3_1_w_high, cutting6)]]
            e112 = [['five', max(cutting1, cutting2, cutting6), cutting7],
                    ['three', max(cutting1, cutting6), min(cutting2, cutting7)]]
            e113 = [['five', max(cutting1, cutting7), 'infty']]
            e211 = [['two', 0, min(cutting1, cutting6)]]
            e212 = [['three', cutting6, min(cutting1, cutting7)]]
            e213 = [['four', cutting7, cutting1]]
            return e111 + e112 + e113 + e211 + e212 + e213
        else:
            if delta3_b <= 0:
                e121 = [['five', cutting6, cutting1]]
                e122 = [['five', max(cutting2, cutting7), min(cutting1, cutting6)],
                        ['three', cutting7, min(cutting1, cutting2, cutting6)]]
                e123 = [['five', 0, min(cutting1, cutting7)]]
            else:
                cutting3_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) + 2 * muu * x0 - 4 * muu * b * x0 *
                                      (w + alpha * (1 - w)) ** 2) - math.sqrt(delta3_b)) / 2 / muu ** 2
                cutting3_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) + 2 * muu * x0 - 4 * muu * b * x0 *
                                    (w + alpha * (1 - w)) ** 2) + math.sqrt(delta3_b)) / 2 / muu ** 2
                e121 = [['five', cutting6, min(cutting1, cutting3_b_low)], ['five', max(cutting3_b_high, cutting6), cutting1],
                        ['one', max(cutting6, cutting3_b_low), min(cutting1, cutting3_b_high)]]
                if delta4_b <= 0:
                    e122 = [['five', max(cutting2, cutting7), min(cutting1, cutting6)],
                            ['three', cutting7, min(cutting1, cutting2, cutting6)]]
                else:
                    cutting4_b_low = (-(2 * lda * muu - 4 * muu * b * x0 + 4 * muu * x0) - math.sqrt(delta4_b)) / 2 / muu ** 2
                    cutting4_b_high = (-(2 * lda * muu - 4 * muu * b * x0 + 4 * muu * x0) - math.sqrt(delta4_b)) / 2 / muu ** 2
                    e122 = [['five', max(cutting2, cutting7), min(cutting1, cutting3_b_low, cutting6)],
                            ['three', cutting7, min(cutting1, cutting2, cutting6, cutting4_b_low)],
                            ['one', max(cutting3_b_low, cutting4_b_low, cutting7),
                             max(cutting1, cutting3_b_high, cutting4_b_high, cutting6)]]
                e123 = [['five', 0, min(cutting1, cutting3_b_low, cutting7)], ['five', cutting3_b_high, min(cutting1, cutting7)],
                        ['one', cutting3_b_low, min(cutting1, cutting3_b_high, cutting7)]]
            e221 = [['four', cutting5_b, cutting1]]
            e222 = [['one', 0, min(cutting1, cutting5_b)]]
            return e121 + e122 + e123 + e221 + e222


def expectation(lda, muu):
    def five(downbdd, upbdd):
        return muu / (2 * (w + alpha * (1 - w))) * first_moment(downbdd, upbdd) + lda / 2 * zero_moment(downbdd, upbdd)

    def four(downbdd, upbdd):
        return 0

    def three(downbdd, upbdd):
        return muu / 2 * first_moment(downbdd, upbdd) + lda / 2 * zero_moment(downbdd, upbdd)

    def two(downbdd, upbdd):
        return - w * x0 * zero_moment(downbdd, upbdd)

    def one(downbdd, upbdd):
        return - w * x0 * zero_moment(downbdd, upbdd)

    sub = subsituation(lda, muu)
    expt = 0
    for item in sub:
        expt += eval(item[0])(item[1], item[2])
    return expt


def expectation2(lda, muu):
    def five(downbdd, upbdd):
        return (lda / (2 * (w + alpha * (1 - w))) + x0) * first_moment(downbdd, upbdd) + \
               muu / (2 * (w + alpha * (1 - w)) ** 2) * second_moment(downbdd, upbdd)

    def four(downbdd, upbdd):
        return x0 * first_moment(downbdd, upbdd)

    def three(downbdd, upbdd):
        return (lda / 2 + x0) * first_moment(downbdd, upbdd) + muu / 2 * second_moment(downbdd, upbdd)

    def two(downbdd, upbdd):
        return (1 - w) * x0 * zero_moment(downbdd, upbdd)

    def one(downbdd, upbdd):
        return b * x0 * zero_moment(downbdd, upbdd)

    sub = subsituation(lda, muu)
    expt = 0
    for item in sub:
        expt += eval(item[0])(item[1], item[2])
    return expt


def square_of_l2_norm(lda, muu):
        def five(downbdd, upbdd):
            return muu ** 2 / 4 / (w + alpha * (1 - w)) ** 2 * second_moment(downbdd, upbdd) + \
                   lda * muu / (w + alpha * (1 - w)) * first_moment(downbdd, upbdd) / 2 + \
                   lda ** 2 / 4 * zero_moment(downbdd, upbdd)

        def four(downbdd, upbdd):
            return 0

        def three(downbdd, upbdd):
            return muu ** 2 / 4 * second_moment(downbdd, upbdd) + lda * muu * first_moment(downbdd, upbdd) / 2 + \
                   lda ** 2 / 4 * zero_moment(downbdd, upbdd)

        def two(downbdd, upbdd):
            return w ** 2 * x0 ** 2 * zero_moment(downbdd, upbdd)

        def one(downbdd, upbdd):
            return w ** 2 * x0 ** 2 * zero_moment(downbdd, upbdd)

        sub = subsituation(lda, muu)
        expt = 0
        for item in sub:
            expt += eval(item[0])(item[1], item[2])
        return expt


def mv(z):
    def constraint(x):
        return expectation(x[0], x[1]) - z, expectation2(x[0], x[1]) - x0

    lda, muu = root(constraint, [0, 0]).x

    return square_of_l2_norm(lda, muu) - z ** 2


fig, ax = plt.subplots(3, 3, sharex=True, sharey=True)
for i in enumerate([0.3, 0.4, 0.8]):
    for j in enumerate([0.1, 1, 5]):
        w = i[1]
        sigma = j[1]
        ax[i[0], j[0]].plot(np.linspace(-1, 0, 10), [mv(zz) for zz in np.linspace(-1, 0, 10)])
        ax[i[0], j[0]].text(0.5, 0.95, r'$w={}, \sigma={}$'.format(w, sigma), fontsize=20,
            transform=ax[i[0], j[0]].transAxes, horizontalalignment='center', verticalalignment='top')
for i in range(3):
    ax[i, 0].set_ylabel('variance', fontsize=20)
    ax[2, i].set_xlabel('mean', fontsize=20)
