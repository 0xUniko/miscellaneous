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
b = 1
T = 1
x0 = 1


def ttheta(x):
    if x >= x0:
        return (w + alpha * (1 - w)) * (x - x0)
    if (1 - w) * x0 <= x:
        return x - x0
    return - w * x


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


def expectation(lda, muu):
    def right(downbdd, upbdd):
        return muu / (2 * (w + alpha * (1 - w))) * first_moment(downbdd, upbdd) + lda / 2 * zero_moment(downbdd, upbdd)

    def middle(downbdd, upbdd):
        return muu / 2 * first_moment(downbdd, upbdd) + lda / 2 * zero_moment(downbdd, upbdd)

    def left(downbdd, upbdd):
        return - w * x0 * zero_moment(downbdd, upbdd)

    if muu == 0:
        if

    if muu >= 0:
        if (2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) ** 2 - \
                4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0) <= 0:
            e11 = right(0, (- 2 * w * x0 - lda) / muu)
        else:
            one_1_w_low = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) - math.sqrt(
                (2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) ** 2 -
                4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / (
                                      2 * muu ** 2)

            one_1_w_high = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) + math.sqrt(
                (2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) ** 2 -
                4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / (
                                       2 * muu ** 2)
            e11 = right(0, min((- 2 * w * x0 - lda) / muu, one_1_w_low) +
                   right(one_1_w_high, (- 2 * w * x0 - lda) / muu)) + \
                   left(one_1_w_low, min((- 2 * w * x0 - lda) / muu, one_1_w_high))

        e12 = right(max((- 2 * w * x0 - lda) / muu,
                  ( - 2 * lda * (w + alpha * (1 - w)) / (muu * (1 + w + alpha * (1 - w))))), - lda/muu) + \
               middle((- 2 * w * x0 - lda) / muu,
                  min(- lda / muu, (- 2 * lda * (w + alpha * (1 - w)) / (muu * (1 + w + alpha * (1 - w))))))

        e13 = lda / 2 + muu * math.exp((- r + theta ** 2) * T) / 2 / (w + alpha * (1 - w)) - right(0, - lda / muu)

        return e11 + e12 + e13

    else:
        if (2*muu*lda*(w+alpha*(1-w))-muu*b*x0)**2-4*muu**2*(lda**2*(w+alpha*(1-w))**2+w**2*x0**2+lda*w*x0) <= 0:
            e21 = lda / 2 + muu * math.exp((- r + theta ** 2) * T) / 2 / (w + alpha * (1 - w)) - \
                   right(0, (- 2 * w * x0 - lda) / muu)
        else:
            one_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) -
                         math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                            4 * muu ** 2 * (lda ** 2 *(w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) \
                        / (2 * muu ** 2)

            one_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) +
                          math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                            4 * muu ** 2 * (lda ** 2 *(w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                         (2 * muu ** 2)
            e21 = right((- 2 * w * x0 - lda) / muu, one_b_low) + \
                   lda / 2 + muu * math.exp((- r + theta ** 2) * T) / 2 / (w + alpha * (1 - w)) - \
                    right(0, max((- 2 * w * x0 - lda) / muu, one_b_high)) + \
                   left(max((- 2 * w * x0 - lda) / muu, one_b_low), one_b_high)

        if (2*muu*lda*(w+alpha*(1-w))-muu*b*x0)**2-4*muu**2*(lda**2*(w+alpha*(1-w))**2+w**2*x0**2+lda*w*x0) <= 0 or \
           (2*muu*lda*(w+alpha*(1-w))-muu*b*x0)**2-4*muu**2*(lda**2*(w+alpha*(1-w))**2+w**2*x0**2+lda*w*x0) <= 0:
            e22 = right(- lda / muu, min((- 2 * w * x0 - lda) / muu, (- 2 * lda * (w + alpha * (1 - w)) /
                                                                           (muu * (1 + w + alpha * (1 - w)))))) + \
                   middle(max(- lda / muu, (- 2 * lda * (w + alpha * (1 - w)) /
                                                (muu * (1 + w + alpha * (1 - w))))), (- 2 * w * x0 - lda) / muu)
        else:
            one_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) -
                         math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                        4 * muu ** 2 * (lda ** 2 *(w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                        (2 * muu ** 2)

            one_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) +
                          math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                        4 * muu ** 2 * (lda ** 2 *(w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                         (2 * muu ** 2)
            two_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) ** 2 - muu * b * x0) - math.sqrt(
                (2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / (
                                    2 * muu ** 2)

            two_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) ** 2 - muu * b * x0) + math.sqrt(
                (2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / (
                                     2 * muu ** 2)
            e22 = right(max(one_b_high, - lda / muu), min((- 2 * w * x0 - lda) / muu,
                    (-2 * lda * (w + alpha * (1 - w))) / (muu * (1 + w + alpha * (1 - w))))) + \
                   right(- lda / muu, min((- 2 * w * x0 - lda) / muu, one_b_low,
                    (-2 * lda * (w + alpha * (1 - w))) / (muu * (1 + w + alpha * (1 - w))))) + \
                   middle(max(- lda / muu, (-2 * lda * (w + alpha * (1 - w))) / (muu * (1 + w + alpha * (1 - w)))),
                    min((- 2 * w * x0 - lda) / muu, two_b_low)) + \
                   middle(max(- lda / muu, two_b_low, (-2 * lda * (w + alpha * (1 - w))) / (muu * (1 + w + alpha * (1 - w)))),
                    (- 2 * w * x0 - lda) / muu) + \
                   left(max(- lda / muu, two_b_low, one_b_low), min((- 2 * w * x0 - lda) / muu, two_b_high, one_b_high))

        if (2*muu*lda*(w+alpha*(1-w))-muu*b*x0)**2-4*muu**2*(lda**2*(w+alpha*(1-w))**2+w**2*x0**2+lda*w*x0) <= 0:
            e23 = right(0, - lda / muu)
        else:
            one_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) -
                         math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                                   4 * muu ** 2 * (lda ** 2 * (
                                     w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                        (2 * muu ** 2)

            one_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) +
                          math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                                    4 * muu ** 2 * (lda ** 2 * (
                                      w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                         (2 * muu ** 2)
            e23 = right(0, min(- lda / muu, one_b_low)) + right(one_b_high, - lda / muu) + \
                   left(one_b_low, min(- lda / muu, one_b_high))

    return e21 + e22 + e23


def expectation2(lda, muu):
    def right2(downbdd, upbdd):
        return (lda / (2 * (w + alpha * (1 - w))) + x0) * first_moment(downbdd, upbdd) + \
               muu / (2 * (w + alpha * (1 - w)) ** 2) * second_moment(downbdd, upbdd)

    def middle2(downbdd, upbdd):
        return (lda / 2 + x0) * first_moment(downbdd, upbdd) + muu / 2 * second_moment(downbdd, upbdd)

    def left2(downbdd, upbdd):
        return (1 - w) * x0 * zero_moment(downbdd, upbdd)

    if muu >= 0:
        if (2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) ** 2 - \
                4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0) <= 0:
            e11 = right2(0, (- 2 * w * x0 - lda) / muu)
        else:
            one_1_w_low = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) - math.sqrt(
                (2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) ** 2 -
                4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / (
                                      2 * muu ** 2)

            one_1_w_high = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) + math.sqrt(
                (2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) ** 2 -
                4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / (
                                       2 * muu ** 2)
            e11 = right2(0, min((- 2 * w * x0 - lda) / muu, one_1_w_low) +
                   right2(one_1_w_high, (- 2 * w * x0 - lda) / muu)) + \
                   left2(one_1_w_low, min((- 2 * w * x0 - lda) / muu, one_1_w_high))

        e12 = right2(max((- 2 * w * x0 - lda) / muu,
                  ( - 2 * lda * (w + alpha * (1 - w)) / (muu * (1 + w + alpha * (1 - w))))), - lda/muu) + \
               middle2((- 2 * w * x0 - lda) / muu,
                  min(- lda / muu, (- 2 * lda * (w + alpha * (1 - w)) / (muu * (1 + w + alpha * (1 - muu))))))

        e13 = lda / 2 + muu * math.exp((- r + theta ** 2) * T) / 2 / (w + alpha * (1 - w)) - right2(0, - lda / muu)

        return e11 + e12 + e13

    else:
        if (2*muu*lda*(w+alpha*(1-w))-muu*b*x0)**2-4*muu**2*(lda**2*(w+alpha*(1-w))**2+w**2*x0**2+lda*w*x0) <= 0:
            e21 = lda / 2 + muu * math.exp((- r + theta ** 2) * T) / 2 / (w + alpha * (1 - w)) - \
                   right2(0, (- 2 * w * x0 - lda) / muu)
        else:
            one_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) -
                         math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                            4 * muu ** 2 * (lda ** 2 *(w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) \
                        / (2 * muu ** 2)

            one_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) +
                          math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                            4 * muu ** 2 * (lda ** 2 *(w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                         (2 * muu ** 2)
            e21 = right2((- 2 * w * x0 - lda) / muu, one_b_low) + \
                   lda / 2 + muu * math.exp((- r + theta ** 2) * T) / 2 / (w + alpha * (1 - w)) - \
                    right2(0, max((- 2 * w * x0 - lda) / muu, one_b_high)) + \
                   left2(max((- 2 * w * x0 - lda) / muu, one_b_low), one_b_high)

        if (2*muu*lda*(w+alpha*(1-w))-muu*b*x0)**2-4*muu**2*(lda**2*(w+alpha*(1-w))**2+w**2*x0**2+lda*w*x0) <= 0 or \
           (2*muu*lda*(w+alpha*(1-w))-muu*b*x0)**2-4*muu**2*(lda**2*(w+alpha*(1-w))**2+w**2*x0**2+lda*w*x0) <= 0:
            e22 = right2(- lda / muu, min((- 2 * w * x0 - lda) / muu, (- 2 * lda * (w + alpha * (1 - w)) /
                                                                           (muu * (1 + w + alpha * (1 - w)))))) + \
                   middle2(max(- lda / muu, (- 2 * lda * (w + alpha * (1 - w)) /
                                                (muu * (1 + w + alpha * (1 - w))))), (- 2 * w * x0 - lda) / muu)
        else:
            one_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) -
                         math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                        4 * muu ** 2 * (lda ** 2 *(w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                        (2 * muu ** 2)

            one_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) +
                          math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                        4 * muu ** 2 * (lda ** 2 *(w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                         (2 * muu ** 2)
            two_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) ** 2 - muu * b * x0) - math.sqrt(
                (2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / (
                                    2 * muu ** 2)

            two_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) ** 2 - muu * b * x0) + math.sqrt(
                (2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / (
                                     2 * muu ** 2)
            e22 = right2(max(one_b_high, - lda / muu), min((- 2 * w * x0 - lda) / muu,
                    (-2 * lda * (w + alpha * (1 - w))) / (muu * (1 + w + alpha * (1 - w))))) + \
                   right2(- lda / muu, min((- 2 * w * x0 - lda) / muu, one_b_low,
                    (-2 * lda * (w + alpha * (1 - w))) / (muu * (1 + w + alpha * (1 - w))))) + \
                   middle2(max(- lda / muu, (-2 * lda * (w + alpha * (1 - w))) / (muu * (1 + w + alpha * (1 - w)))),
                    min((- 2 * w * x0 - lda) / muu, two_b_low)) + \
                   middle2(max(- lda / muu, two_b_low, (-2 * lda * (w + alpha * (1 - w))) / (muu * (1 + w + alpha * (1 - w)))),
                    (- 2 * w * x0 - lda) / muu) + \
                   left2(max(- lda / muu, two_b_low, one_b_low), min((- 2 * w * x0 - lda) / muu, two_b_high, one_b_high))

        if (2*muu*lda*(w+alpha*(1-w))-muu*b*x0)**2-4*muu**2*(lda**2*(w+alpha*(1-w))**2+w**2*x0**2+lda*w*x0) <= 0:
            e23 = right2(0, - lda / muu)
        else:
            one_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) -
                         math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                                   4 * muu ** 2 * (lda ** 2 * (
                                     w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                        (2 * muu ** 2)

            one_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) +
                          math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                                    4 * muu ** 2 * (lda ** 2 * (
                                      w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                         (2 * muu ** 2)
            e23 = right2(0, min(- lda / muu, one_b_low)) + right2(one_b_high, - lda / muu) + \
                   left2(one_b_low, min(- lda / muu, one_b_high))

        return e21 + e22 + e23


def variation(lda, muu):
        def right(downbdd, upbdd):
            return muu ** 2 / 4 / (w + alpha * (1 - w)) ** 2 * second_moment(downbdd, upbdd) + \
                   lda * muu / (w + alpha * (1 - w)) * first_moment(downbdd, upbdd) / 2 + \
                   lda ** 2 / 4 * zero_moment(downbdd, upbdd)

        def middle(downbdd, upbdd):
            return muu ** 2 / 4 * second_moment(downbdd, upbdd) + lda * muu * first_moment(downbdd, upbdd) / 2 + \
                   lda ** 2 / 4 * zero_moment(downbdd, upbdd)

        def left(downbdd, upbdd):
            return w ** 2 * x0 ** 2 * zero_moment(downbdd, upbdd)

        if muu >= 0:
            if (2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) ** 2 - \
                    4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0) <= 0:
                v11 = right(0, (- 2 * w * x0 - lda) / muu)
            else:
                one_1_w_low = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) - math.sqrt(
                    (2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) ** 2 -
                    4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / (
                                      2 * muu ** 2)

                one_1_w_high = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) + math.sqrt(
                    (2 * muu * lda * (w + alpha * (1 - w)) - muu * (1 - w) * x0) ** 2 -
                    4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / (
                                       2 * muu ** 2)
                v11 = right(0, min((- 2 * w * x0 - lda) / muu, one_1_w_low) +
                            right(one_1_w_high, (- 2 * w * x0 - lda) / muu)) + \
                      left(one_1_w_low, min((- 2 * w * x0 - lda) / muu, one_1_w_high))

            v12 = right(max((- 2 * w * x0 - lda) / muu,
                            (- 2 * lda * (w + alpha * (1 - w)) / (muu * (1 + w + alpha * (1 - w))))), - lda / muu) + \
                  middle((- 2 * w * x0 - lda) / muu,
                         min(- lda / muu, (- 2 * lda * (w + alpha * (1 - w)) / (muu * (1 + w + alpha * (1 - w))))))

            v13 = lda ** 2 / 4 + lda * muu * math.exp((- r + theta ** 2) * T) / 2 / (w + alpha * (1 - w)) + \
                  muu ** 2 / 4 / (w + alpha * (1 - w)) ** 2 * math.exp((- 2 * r + 3 * theta ** 2) * T) - \
                  right(0, - lda / muu)

            return v11 + v12 + v13

        else:
            if (2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 - 4 * muu ** 2 * (
                    lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0) <= 0:

                v21 = lda ** 2 / 4 + lda * muu * math.exp((- r + theta ** 2) * T) / 2 / (w + alpha * (1 - w)) + \
                      muu ** 2 / 4 / (w + alpha * (1 - w)) ** 2 * math.exp((- 2 * r + 3 * theta ** 2) * T) - \
                      right(0, (- 2 * w * x0 - lda) / muu)
            else:
                one_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) -
                             math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                                       4 * muu ** 2 * (lda ** 2 * (
                                         w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) \
                            / (2 * muu ** 2)

                one_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) +
                              math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                                        4 * muu ** 2 * (lda ** 2 * (
                                          w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                             (2 * muu ** 2)
                v21 = right((- 2 * w * x0 - lda) / muu, one_b_low) + \
                      lda ** 2 / 4 + lda * muu * math.exp((- r + theta ** 2) * T) / 2 / (w + alpha * (1 - w)) + \
                      muu ** 2 / 4 / (w + alpha * (1 - w)) ** 2 * math.exp((- 2 * r + 3 * theta ** 2) * T) - \
                      right(0, max((- 2 * w * x0 - lda) / muu, one_b_high)) + \
                      left(max((- 2 * w * x0 - lda) / muu, one_b_low), one_b_high)

            if (2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 - 4 * muu ** 2 * (
                    lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0) <= 0 or \
                    (2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 - 4 * muu ** 2 * (
                    lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0) <= 0:
                v22 = right(- lda / muu, min((- 2 * w * x0 - lda) / muu, (- 2 * lda * (w + alpha * (1 - w)) /
                                                                          (muu * (1 + w + alpha * (1 - w)))))) + \
                      middle(max(- lda / muu, (- 2 * lda * (w + alpha * (1 - w)) /
                                               (muu * (1 + w + alpha * (1 - w))))), (- 2 * w * x0 - lda) / muu)
            else:
                one_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) -
                             math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                                       4 * muu ** 2 * (lda ** 2 * (
                                         w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                            (2 * muu ** 2)

                one_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) +
                              math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                                        4 * muu ** 2 * (lda ** 2 * (
                                          w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                             (2 * muu ** 2)
                two_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) ** 2 - muu * b * x0) - math.sqrt(
                    (2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                    4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / (
                                    2 * muu ** 2)

                two_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) ** 2 - muu * b * x0) + math.sqrt(
                    (2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                    4 * muu ** 2 * (lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / (
                                     2 * muu ** 2)
                v22 = right(max(one_b_high, - lda / muu), min((- 2 * w * x0 - lda) / muu,
                                                              (-2 * lda * (w + alpha * (1 - w))) / (
                                                                          muu * (1 + w + alpha * (1 - w))))) + \
                      right(- lda / muu, min((- 2 * w * x0 - lda) / muu, one_b_low,
                                             (-2 * lda * (w + alpha * (1 - w))) / (muu * (1 + w + alpha * (1 - w))))) + \
                      middle(max(- lda / muu, (-2 * lda * (w + alpha * (1 - w))) / (muu * (1 + w + alpha * (1 - w)))),
                             min((- 2 * w * x0 - lda) / muu, two_b_low)) + \
                      middle(max(- lda / muu, two_b_low,
                                 (-2 * lda * (w + alpha * (1 - w))) / (muu * (1 + w + alpha * (1 - w)))),
                             (- 2 * w * x0 - lda) / muu) + \
                      left(max(- lda / muu, two_b_low, one_b_low),
                           min((- 2 * w * x0 - lda) / muu, two_b_high, one_b_high))

            if (2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 - 4 * muu ** 2 * (
                    lda ** 2 * (w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0) <= 0:
                v23 = right(0, - lda / muu)
            else:
                one_b_low = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) -
                             math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                                       4 * muu ** 2 * (lda ** 2 * (
                                     w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                            (2 * muu ** 2)

                one_b_high = (-(2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) +
                              math.sqrt((2 * muu * lda * (w + alpha * (1 - w)) - muu * b * x0) ** 2 -
                                        4 * muu ** 2 * (lda ** 2 * (
                                      w + alpha * (1 - w)) ** 2 + w ** 2 * x0 ** 2 + lda * w * x0))) / \
                             (2 * muu ** 2)
                v23 = right(0, min(- lda / muu, one_b_low)) + right(one_b_high, - lda / muu) + \
                      left(one_b_low, min(- lda / muu, one_b_high))

            return v21 + v22 + v23


def mv(z):
    def constraint(x):
        return expectation(x[0], x[1]) - z, expectation2(x[0], x[1]) - x0

    lda, muu = root(constraint, [0, 1]).x

    return variation(lda, muu) - z ** 2


fig, ax = plt.subplots()
ax.plot(np.linspace(-1, 1, 10), [mv(zz) for zz in np.linspace(-1, 1, 10)])
plt.show()

# print('v11=', v11, 'right=', right(0, (- 2 * w * x0 - lda) / muu))
#             print('v12=', v12, 'right=', right(max((- 2 * w * x0 - lda) / muu,
#                   ( - 2 * lda * (w + alpha * (1 - w)) / (muu * (1 + w + alpha * (1 - w))))), - lda/muu),
#               'middle=', middle((- 2 * w * x0 - lda) / muu,
#                   min(- lda / muu, (- 2 * lda * (w + alpha * (1 - w)) / (muu * (1 + w + alpha * (1 - w)))))))
#             print('v13=', v13)