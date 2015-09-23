''' Plot the example of timelag and tidal efficiency dependencies
    againt distance from shore.
'''
import numpy as np
import matplotlib.pyplot as plt
try:
    import seaborn as sns
    _sns = True
except:
    _sns = False


if __name__ == '__main__':

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5), tight_layout=True)
    
    x = np.arange(3)
    ax1.plot(x, x)

    x = np.array([-2, -1, 0, 1, 2])
    ax1.plot(x, x*1.5+1)
    ax1.set_xlim([-1, 2])
    ax1.set_ylim([0, 3])
    xmin, xmax = ax1.get_xlim()
    ymin, ymax = ax1.get_ylim()

    # removing the default axis on all sides:
    for side in ['bottom', 'right', 'top', 'left']:
        ax1.spines[side].set_visible(False)

    ax1.xaxis.set_ticks_position('none')  # tick markers
    ax1.yaxis.set_ticks_position('none')


    # get width and height of axes object to compute
    # matching arrowhead length and width
    dps = fig.dpi_scale_trans.inverted()
    bbox = ax1.get_window_extent().transformed(dps)
    width, height = bbox.width, bbox.height

    # manual arrowhead width and length
    hw  = 1./30.*(ymax-ymin)
    hl  = 1./15.*(xmax-xmin)
    lw  = 1.  # axis line width
    ohg = 0.3  # arrow overhang

    # compute matching arrowhead length and width
    yhw = hw/(ymax-ymin)*(xmax-xmin) * height/width
    yhl = hl/(xmax-xmin)*(ymax-ymin) * width/height

    # draw x and y axis
    ax1.arrow(xmin, 0, xmax-xmin, 0., fc='k', ec='k', lw=lw,
             head_width=hw, head_length=hl, overhang=ohg,
             length_includes_head=True, clip_on=False)

    ax1.arrow(0, ymin, 0., ymax-ymin, fc='k', ec='k', lw=lw,
             head_width=yhw, head_length=yhl, overhang=ohg,
             length_includes_head=True, clip_on=False)

    #ax1.set_title('(A)')
    ax1.set_xlabel('Distance from shore [m]', size=12)
    ax1.text(0, ymax - .5, 'Timelag [minutes]', rotation=90, verticalalignment='top', horizontalalignment='right')
    #ax1.set_ylabel('Timelag [minutes]')
    ax1.grid(False)
    ax1.set_xticks([])
    ax1.set_yticks([])


    

    y = np.array([0., -1, -2.])
    x = np.arange(3)
    ax2.plot(x, y*1.1)
    
    y = np.array([0., -1, -2., -3])
    ax2.plot([-0.75, 0.25, 1.25, 2.25], y*1.5)
    ax2.set_xlim([-1, 2])
    ax2.set_ylim([-3, 0])
    xmin, xmax = ax2.get_xlim()
    ymin, ymax = ax2.get_ylim()

    # removing the default axis on all sides:
    for side in ['bottom', 'right', 'top', 'left']:
        ax2.spines[side].set_visible(False)

    ax2.xaxis.set_ticks_position('none')  # tick markers
    ax2.yaxis.set_ticks_position('none')


    # get width and height of axes object to compute
    # matching arrowhead length and width
    dps = fig.dpi_scale_trans.inverted()
    bbox = ax2.get_window_extent().transformed(dps)
    width, height = bbox.width, bbox.height



    # compute matching arrowhead length and width
    yhw = hw/(ymax-ymin)*(xmax-xmin) * height/width
    yhl = hl/(xmax-xmin)*(ymax-ymin) * width/height

    # draw x and y axis
    ax2.arrow(xmin, ymax, xmax-xmin, 0, fc='k', ec='k', lw=lw,
             head_width=hw, head_length=hl, overhang=ohg,
             length_includes_head=True, clip_on=False)

    ax2.arrow(0, ymax, 0., ymin-ymax, fc='k', ec='k', lw=lw,
             head_width=yhw, head_length=yhl, overhang=ohg,
             length_includes_head=True, clip_on=False)

    #ax2.set_title('(B)')
    ax2.set_xlabel('Distance from shore [m]', size=12)
    ax2.text(0, ymin + .25, 'Logarithm of Tidal Efficiency [-]', rotation=90, verticalalignment='bottom', horizontalalignment='right')
    #ax2.set_ylabel('Logarithm of Tidal Efficiency [-]')
    ax2.grid(False)
    ax2.xaxis.set_ticks_position('top')
    ax2.xaxis.set_label_position('top')
    ax2.set_xticks([])
    ax2.set_yticks([])

    plt.show()
