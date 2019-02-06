import numpy as np
import matplotlib.pyplot as plt
import source
from MontelCarlo import *

# Painting diagrams
# fig, ax = plt.subplots(2, 3, sharey=True, figsize=(16, 10))
# for axs in ax.flatten():
#     for i in ['left', 'right', 'top']:
#         axs.spines[i].set_visible(False)
#     axs.set(xticks=[1, 2, 3], xlim=(0.6, 4), yticks=[], ylim=(0, 3))
#     axs.set_xticklabels([r'$bX_0$', r'$(1-w)X_0$', r'$X_0$'], fontsize=15)
#
# ax[0, 0].plot(np.linspace(1, 2), -np.linspace(1, 2) + 2.5)
# ax[0, 0].plot(np.linspace(2, 3), (np.linspace(2, 3) - 2) ** 2 + 0.5, 'C0')
# ax[0, 0].plot(np.linspace(3, 4), 4 * (np.linspace(3, 4) - 3.5) ** 2 + 0.5, 'C0')
# ax[0, 0].plot([2, 3.5], [0.5, 0.5], 'ko')
# ax[0, 0].text(0.5, 0.9, r'$x_3 < (1-w)X_0$', fontsize=20,
#               transform=ax[0, 0].transAxes, horizontalalignment='center', verticalalignment='top')
# ax[0, 0].set_ylabel('$\lambda_2>0$', labelpad=50, size=20, rotation='horizontal', verticalalignment='center')
#
# ax[0, 1].plot(np.linspace(1, 2), -0.5 * np.linspace(1, 2) + 2)
# ax[0, 1].plot(np.linspace(2, 3), 2 * (np.linspace(2, 3) - 2.5) ** 2 + 0.5, 'C0')
# ax[0, 1].plot(np.linspace(3, 4), 2 * (np.linspace(3, 4) - 3.5) ** 2 + 0.5, 'C0')
# ax[0, 1].plot([2.5, 3.5], [0.5, 0.5], 'ko')
# ax[0, 1].text(0.5, 0.9, r'$(1-w)X_0 \leq x_3 < X_0$', fontsize=20,
#               transform=ax[0, 1].transAxes, horizontalalignment='center', verticalalignment='top')
#
# ax[0, 2].plot(np.linspace(1, 2), -0.5 * np.linspace(1, 2) + 2.5)
# ax[0, 2].plot(np.linspace(2, 3), (np.linspace(2, 3) - 3) ** 2 + 0.5, 'C0')
# ax[0, 2].plot(np.linspace(3, 4), (np.linspace(3, 4) - 3.5) ** 2 + 0.25, 'C0')
# ax[0, 2].plot(3.5, 0.25, 'ko')
# ax[0, 2].text(0.5, 0.9, r'$X_0 \leq x_3$', fontsize=20,
#               transform=ax[0, 2].transAxes, horizontalalignment='center', verticalalignment='top')
#
# ax[1, 0].plot(np.linspace(1, 2), 0.5 * np.linspace(1, 2) - 0.25)
# ax[1, 0].plot(np.linspace(2, 3), (np.linspace(2, 3) - 2) ** 2 + 0.75, 'C0')
# ax[1, 0].plot(np.linspace(3, 4), 6 * (np.linspace(3, 4) - 3.5) ** 2 + 0.25, 'C0')
# ax[1, 0].plot([1, 3.5], [0.25, 0.25], 'ko')
# ax[1, 0].text(0.5, 0.9, r'$x_3 < (1-w)X_0$', fontsize=20,
#               transform=ax[1, 0].transAxes, horizontalalignment='center', verticalalignment='top')
# ax[1, 0].set_ylabel(r'$\lambda_2 \leq 0$', labelpad=50, size=20, rotation='horizontal', verticalalignment='center')
#
# ax[1, 1].plot(np.linspace(1, 2), np.linspace(1, 2) - 0.5)
# ax[1, 1].plot(np.linspace(2, 3), 4 * (np.linspace(2, 3) - 2.5) ** 2 + 0.5, 'C0')
# ax[1, 1].plot(np.linspace(3, 4), 4 * (np.linspace(3, 4) - 3.5) ** 2 + 0.5, 'C0')
# ax[1, 1].plot([1, 2.5, 3.5], [0.5, 0.5, 0.5], 'ko')
# ax[1, 1].text(0.5, 0.9, r'$(1-w)X_0 \leq x_3 < X_0$', fontsize=20,
#               transform=ax[1, 1].transAxes, horizontalalignment='center', verticalalignment='top')
#
# ax[1, 2].plot(np.linspace(1, 2), 1.5 * np.linspace(1, 2) - 1)
# ax[1, 2].plot(np.linspace(2, 3), (np.linspace(2, 3) - 3) ** 2 + 1, 'C0')
# ax[1, 2].plot(np.linspace(3, 4), 2 * (np.linspace(3, 4) - 3.5) ** 2 + 0.5, 'C0')
# ax[1, 2].plot([1, 3.5], [0.5, 0.5], 'ko')
# ax[1, 2].text(0.5, 0.9, r'$X_0 \leq x_3$', fontsize=20,
#               transform=ax[1, 2].transAxes, horizontalalignment='center', verticalalignment='top')
# fig.savefig('figures/diagram1.png')
#
#
# fig, ax = plt.subplots(2, 3, sharey=True, figsize=(16, 10))
# for axs in ax.flatten():
#     for i in ['left', 'right', 'top']:
#         axs.spines[i].set_visible(False)
#     axs.set(xticks=[1, 2, 3], xlim=(0.6, 4), yticks=[], ylim=(0, 3))
#     axs.set_xticklabels([r'$bX_0$', r'$(1-w)X_0$', r'$X_0$'], fontsize=15)
#
# ax[0, 0].plot(np.linspace(1, 2), -np.linspace(1, 2) + 2.5)
# ax[0, 0].plot(np.linspace(2, 3), 0.5 * (np.linspace(2, 3) - 2) ** 2 + 0.5, 'C0')
# ax[0, 0].plot(np.linspace(3, 4), (np.linspace(3, 4) - 3) ** 2 + 1, 'C0')
# ax[0, 0].plot(2, 0.5, 'ko')
# ax[0, 0].text(0.5, 0.9, r'$x_3 < (1-w)X_0$', fontsize=20,
#               transform=ax[0, 0].transAxes, horizontalalignment='center', verticalalignment='top')
# ax[0, 0].set_ylabel('$\lambda_2>0$', labelpad=50, size=20, rotation='horizontal', verticalalignment='center')
#
# ax[0, 1].plot(np.linspace(1, 2), -0.5 * np.linspace(1, 2) + 2)
# ax[0, 1].plot(np.linspace(2, 3), 2 * (np.linspace(2, 3) - 2.5) ** 2 + 0.5, 'C0')
# ax[0, 1].plot(np.linspace(3, 4), (np.linspace(3, 4) - 3) ** 2 + 1, 'C0')
# ax[0, 1].plot(2.5, 0.5, 'ko')
# ax[0, 1].text(0.5, 0.9, r'$(1-w)X_0 \leq x_3 < X_0$', fontsize=20,
#               transform=ax[0, 1].transAxes, horizontalalignment='center', verticalalignment='top')
#
# ax[0, 2].plot(np.linspace(1, 2), -0.5 * np.linspace(1, 2) + 2.5)
# ax[0, 2].plot(np.linspace(2, 3), (np.linspace(2, 3) - 3) ** 2 + 0.5, 'C0')
# ax[0, 2].plot(np.linspace(3, 4), (np.linspace(3, 4) - 3) ** 2 + 0.5, 'C0')
# ax[0, 2].plot(3, 0.5, 'ko')
# ax[0, 2].text(0.5, 0.9, r'$X_0 \leq x_3$', fontsize=20,
#               transform=ax[0, 2].transAxes, horizontalalignment='center', verticalalignment='top')
#
# ax[1, 0].plot(np.linspace(1, 2), 0.5 * np.linspace(1, 2) - 0.25)
# ax[1, 0].plot(np.linspace(2, 3), 0.25 * (np.linspace(2, 3) - 2) ** 2 + 0.75, 'C0')
# ax[1, 0].plot(np.linspace(3, 4), 0.25 * (np.linspace(3, 4) - 3) ** 2 + 1, 'C0')
# ax[1, 0].plot(1, 0.25, 'ko')
# ax[1, 0].text(0.5, 0.9, r'$x_3 < (1-w)X_0$', fontsize=20,
#               transform=ax[1, 0].transAxes, horizontalalignment='center', verticalalignment='top')
# ax[1, 0].set_ylabel(r'$\lambda_2 \leq 0$', labelpad=50, size=20, rotation='horizontal', verticalalignment='center')
#
# ax[1, 1].plot(np.linspace(1, 2), 0.5 * np.linspace(1, 2) - 0.25)
# ax[1, 1].plot(np.linspace(2, 3), 2 * (np.linspace(2, 3) - 2.5) ** 2 + 0.25, 'C0')
# ax[1, 1].plot(np.linspace(3, 4), (np.linspace(3, 4) - 3) ** 2 + 0.75, 'C0')
# ax[1, 1].plot([1, 2.5], [0.25, 0.25], 'ko')
# ax[1, 1].text(0.5, 0.9, r'$(1-w)X_0 \leq x_3 < X_0$', fontsize=20,
#               transform=ax[1, 1].transAxes, horizontalalignment='center', verticalalignment='top')
#
# ax[1, 2].plot(np.linspace(1, 2), 1.5 * np.linspace(1, 2) - 1)
# ax[1, 2].plot(np.linspace(2, 3), 1.5 * (np.linspace(2, 3) - 3) ** 2 + 0.5, 'C0')
# ax[1, 2].plot(np.linspace(3, 4), 1.5 * (np.linspace(3, 4) - 3) ** 2 + 0.5, 'C0')
# ax[1, 2].plot([1, 3], [0.5, 0.5], 'ko')
# ax[1, 2].text(0.5, 0.9, r'$X_0 \leq x_3$', fontsize=20,
#               transform=ax[1, 2].transAxes, horizontalalignment='center', verticalalignment='top')
# fig.savefig('figures/diagram2.png')


# fig, ax = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(16, 10))
# for i in enumerate([0.3, 0.4, 0.8]):
#     for j in enumerate([0.1, 0.5, 1]):
#         source.attribution(w=i[1], sigma=j[1])
#         points = np.array([[z, mv(z)[0]] for z in np.linspace(source.z0 - 0.5, source.z0 + 0.5)
#                            if mv(z)[1]]).T.reshape(2, -1)
#         ax[i[0], j[0]].plot(points[0], points[1])
#         ax[i[0], j[0]].axvline(ymax=0.8, x=source.z0, c='C1', linestyle='dashed')
#         ax[i[0], j[0]].text(0.5, 0.95, r'$w={}, \sigma={}$'.format(i[1], j[1]), fontsize=20,
#                             transform=ax[i[0], j[0]].transAxes, horizontalalignment='center', verticalalignment='top')
#         ax[i[0], j[0]].xaxis.set_tick_params(which='both', labelbottom=True)
# for i in range(3):
#     ax[i, 0].set_ylabel('variance', fontsize=20)
#     ax[2, i].set_xlabel('mean', fontsize=20)
# fig.savefig('figures/w_sigma.png')


fig, ax = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(16, 10))
for i in enumerate([0.08, 0.2, 0.4]):
    for j in enumerate([0.3, 0.8, 1.05]):
        source.attribution(mu=i[1], b=j[1])
        points = np.array([[z, mv(z)[0]] for z in np.linspace(source.z0 - 0.5, source.z0 + 0.5)
                           if mv(z)[1]]).T.reshape(2, -1)
        ax[i[0], j[0]].plot(points[0], points[1])
        ax[i[0], j[0]].axvline(ymax=0.8, x=source.z0, c='C1', linestyle='dashed')
        ax[i[0], j[0]].text(0.5, 0.95, r'$\mu={}, b={}$'.format(i[1], j[1]), fontsize=20,
                            transform=ax[i[0], j[0]].transAxes, horizontalalignment='center', verticalalignment='top')
        ax[i[0], j[0]].xaxis.set_tick_params(which='both', labelbottom=True)
for i in range(3):
    ax[i, 0].set_ylabel('variance', fontsize=20)
    ax[2, i].set_xlabel('mean', fontsize=20)
fig.savefig('figures/mu_b.png')
