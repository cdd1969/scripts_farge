from __future__ import division, print_function
import numpy as np

__author__ = 'Marcos Duarte, https://github.com/demotu/BMC'
__version__ = "1.0.3"
__license__ = "MIT"


def tnorm(y, axis=0, step=1, k=3, smooth=0, mask=None, show=False, ax=None):
    """Time normalization (from 0 to 100% with step interval).

    Time normalization is usually employed for the temporal alignment of data
    obtained from different trials with different duration (number of points).
    This code implements a procedure knwown as the normalization to percent
    cycle, the most simple and common method used among the ones available,
    but may not be the most adequate [1]_.

    NaNs and any value inputted as a mask parameter and that appears at the
    extremities are removed before the interpolation because this code does not
    perform extrapolation. For a 2D array, the entire row with NaN or a mask
    value at the extermity is removed because of alignment issues with the data
    from different columns. NaNs and any value inputted as a mask parameter and
    that appears in the middle of the data (which may represent missing data)
    are ignored and the interpolation is performed throught these points.

    This code can perform simple linear interpolation passing throught each
    datum or spline interpolation (up to quintic splines) passing through each
    datum (knots) or not (in case a smoothing parameter > 0 is inputted).

    See this IPython notebook [2]_.

    Parameters
    ----------
    y : 1-D or 2-D array_like
        Array of independent input data. Must be increasing.
        If 2-D array, the data in each axis will be interpolated.
    axis : int, 0 or 1, optional (default = 0)
        Axis along which the interpolation is performed.
        0: data in each column are interpolated; 1: for row interpolation
    step : float or int, optional (default = 1)
        Interval from 0 to 100% to resample y or the number of points y
        should be interpolated. In the later case, the desired number of
        points should be expressed with step as a negative integer.
        For instance, step = 1 or step = -101 will result in the same
        number of points at the interpolation (101 points).
        If step == 0, the number of points will be the number of data in y.
    k : int, optional (default = 3)
        Degree of the smoothing spline. Must be 1 <= k <= 5.
        If 3, a cubic spline is used.
        The number of data points must be larger than k.
    smooth : float or None, optional (default = 0)
        Positive smoothing factor used to choose the number of knots.
        If 0, spline will interpolate through all data points.
        If None, smooth=len(y).
    mask : None or float, optional (default = None)
        Mask to identify missing values which will be ignored.
        It can be a list of values.
        NaN values will be ignored and don't need to be in the mask.
    show : bool, optional (default = False)
        True (1) plot data in a matplotlib figure.
        False (0) to not plot.
    ax : a matplotlib.axes.Axes instance, optional (default = None).

    Returns
    -------
    yn : 1-D or 2-D array
        Interpolated data (if axis == 0, column oriented for 2-D array).
    tn : 1-D array
        New x values (from 0 to 100) for the interpolated data.

    Notes
    -----
    This code performs interpolation to create data with the desired number of
    points using a one-dimensional smoothing spline fit to a given set of data
    points (scipy.interpolate.UnivariateSpline function).

    References
    ----------
    .. [1] http://www.sciencedirect.com/science/article/pii/S0021929010005038
    .. [2] http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/TimeNormalization.ipynb

    See Also
    --------
    scipy.interpolate.UnivariateSpline:
    One-dimensional smoothing spline fit to a given set of data points.

    Examples
    --------
    >>> # Default options: cubic spline interpolation passing through
    >>> # each datum, 101 points, and no plot
    >>> y = [5,  4, 10,  8,  1, 10,  2,  7,  1,  3]
    >>> tnorm(y)

    >>> # Linear interpolation passing through each datum
    >>> y = [5,  4, 10,  8,  1, 10,  2,  7,  1,  3]
    >>> yn, tn = tnorm(y, k=1, smooth=0, mask=None, show=True)

    >>> # Cubic spline interpolation with smoothing
    >>> y = [5,  4, 10,  8,  1, 10,  2,  7,  1,  3]
    >>> yn, tn = tnorm(y, k=3, smooth=1, mask=None, show=True)

    >>> # Cubic spline interpolation with smoothing and 50 points
    >>> x = np.linspace(-3, 3, 100)
    >>> y = np.exp(-x**2) + np.random.randn(100)/10
    >>> yn, tn = tnorm(y, step=-50, k=3, smooth=1, show=True)

    >>> # Deal with missing data (use NaN as mask)
    >>> x = np.linspace(-3, 3, 100)
    >>> y = np.exp(-x**2) + np.random.randn(100)/10
    >>> y[0] = np.NaN # first point is also missing
    >>> y[30: 41] = np.NaN # make other 10 missing points
    >>> yn, tn = tnorm(y, step=-50, k=3, smooth=1, show=True)

    >>> # Deal with 2-D array
    >>> x = np.linspace(-3, 3, 100)
    >>> y = np.exp(-x**2) + np.random.randn(100)/10
    >>> y = np.vstack((y-1, y[::-1])).T
    >>> yn, tn = tnorm(y, step=-50, k=3, smooth=1, show=True)
    """

    from scipy.interpolate import UnivariateSpline

    y = np.asarray(y)
    if axis:
        y = y.T
    if y.ndim == 1:
        y = np.reshape(y, (-1, 1))
    # turn mask into NaN
    if mask is not None:
        y[y == mask] = np.NaN
    # delete rows with missing values at the extremities
    while y.size and np.isnan(np.sum(y[0])):
        y = np.delete(y, 0, axis=0)
    while y.size and np.isnan(np.sum(y[-1])):
        y = np.delete(y, -1, axis=0)
    # check if there are still data
    if not y.size:
        return None, None
    if y.size == 1:
        return y.flatten(), None

    t = np.linspace(0, 100, y.shape[0])
    if step == 0:
        tn = t
    elif step > 0:
        tn = np.linspace(0, 100, np.round(100 / step + 1))
    else:
        tn = np.linspace(0, 100, -step)
    yn = np.empty([tn.size, y.shape[1]]) * np.NaN
    for col in np.arange(y.shape[1]):
        # ignore NaNs inside data for the interpolation
        ind = np.isfinite(y[:, col])
        if np.sum(ind) > 1:  # at least two points for the interpolation
            spl = UnivariateSpline(t[ind], y[ind, col], k=k, s=smooth)
            yn[:, col] = spl(tn)

    if show:
        _plot(t, y, ax, tn, yn)

    if axis:
        y = y.T
    if yn.shape[1] == 1:
        yn = yn.flatten()

    return yn, tn


def _plot(t, y, ax, tn, yn):
    """Plot results of the tnorm function, see its help."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib is not available.')
    else:
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(8, 5))

        ax.set_color_cycle(['b', 'r', 'b', 'g', 'b', 'y', 'b', 'c', 'b', 'm'])
        for col in np.arange(y.shape[1]):
            if y.shape[1] == 1:
                ax.plot(t, y[:, col], 'o-', lw=1, label='Original data')
                ax.plot(tn, yn[:, col], '.-', lw=2,
                        label='Interpolated')
            else:
                ax.plot(t, y[:, col], 'o-', lw=1)
                ax.plot(tn, yn[:, col], '.-', lw=2, label='Col= %d' % col)
            ax.locator_params(axis='y', nbins=7)
            ax.legend(fontsize=12, loc='best', framealpha=.5, numpoints=1)
        plt.xlabel('[%]')
        plt.tight_layout()
        plt.show()



if __name__ == '__main__':
  
    data_GW5 = [
    1.17,
    1.16,
    1.14,
    1.12,
    1.1,
    1.08,
    1.05,
    1.02,
    0.99,
    0.96,
    0.92,
    0.89,
    0.86,
    0.83,
    0.79,
    0.75,
    0.71,
    0.68,
    0.63,
    0.59,
    0.55,
    0.5,
    0.46,
    0.42,
    0.37,
    0.32,
    0.28,
    0.23,
    0.19,
    0.14,
    0.1,
    0.05,
    0.01,
    -0.03,
    -0.06,
    -0.1,
    -0.13,
    -0.16,
    -0.17,
    -0.16,
    -0.12,
    -0.02,
    0.09,
    0.18,
    0.26,
    0.33,
    0.38,
    0.43,
    0.48,
    0.52,
    0.58,
    0.63,
    0.68,
    0.73,
    0.78,
    0.84,
    0.9,
    0.93,
    0.97,
    1,
    1.03,
    1.07,
    1.1,
    1.14,
    1.16,
    1.18,
    1.21,
    1.22,
    1.24,
    1.25,
    1.26,
    1.26,
    1.27,
    1.26,
    1.25,
    1.24,
    1.22,
    1.19,
    1.16,
    1.14,
    1.11,
    1.08,
    1.05,
    1.02,
    0.99,
    0.95,
    0.92,
    0.88,
    0.85,
    0.81,
    0.78,
    0.74,
    0.7,
    0.67,
    0.63,
    0.59,
    0.55,
    0.51,
    0.47,
    0.43,
    0.39,
    0.34,
    0.3,
    0.26,
    0.22,
    0.19,
    0.16,
    0.13,
    0.1,
    0.09,
    0.1,
    0.12,
    0.18,
    0.27,
    0.35,
    0.42,
    0.48,
    0.54,
    0.59,
    0.64,
    0.69,
    0.75,
    0.81,
    0.87,
    0.93,
    0.99,
    1.05,
    1.1,
    1.15,
    1.19,
    1.23,
    1.26,
    1.29,
    1.33,
    1.36,
    1.39,
    1.42,
    1.45,
    1.48,
    1.5,
    1.5,
    1.5,
    1.5,
    1.49,
    1.47,
    1.46,
    1.44,
    1.42,
    1.39,
    1.36,
    1.33,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    0.2,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    1.63,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    0.35,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    np.nan,
    1.54,
    1.58,
    1.63,
    1.67,
    1.71,
    1.73,
    1.75,
    1.76,
    1.77,
    1.78,
    1.79,
    1.78,
    1.78,
    1.78,
    1.77,
    1.73,
    1.7,
    1.67,
    1.63,
    1.59,
    1.55,
    1.51,
    1.47,
    1.43,
    1.39,
    1.35,
    1.3,
    1.26,
    1.23,
    1.19,
    1.16,
    1.12,
    1.08,
    1.05,
    1.01,
    0.98,
    0.94,
    0.89,
    0.86,
    0.81,
    0.77,
    0.73,
    0.69,
    0.65,
    0.61,
    0.57,
    0.54,
    0.51,
    0.49,
    0.48,
    0.48,
    0.51,
    0.57,
    0.64,
    0.72,
    0.78,
    0.84,
    0.89,
    0.93,
    0.98,
    1.03,
    1.08,
    1.13,
    1.19,
    1.25,
    1.32,
    1.38,
    1.44,
    1.48,
    1.52,
    1.56,
    1.6,
    1.63,
    1.68,
    1.71,
    1.76,
    1.8,
    1.83,
    1.85,
    1.88,
    1.9,
    1.9,
    1.89,
    1.89,
    1.9,
    1.9,
    1.89,
    1.87,
    1.87,
    1.88,
    1.89,
    1.9,
    1.9,
    1.89,
    1.84,
    1.8,
    1.75,
    1.71,
    1.68,
    1.64,
    1.6,
    1.57,
    1.52,
    1.49,
    1.45,
    1.42,
    1.39,
    1.36,
    1.33,
    1.31,
    1.29,
    1.26,
    1.24,
    1.21,
    1.18,
    1.16,
    1.13,
    1.11,
    1.08,
    1.06,
    1.04,
    1.03,
    1.01,
    1.01,
    1.01,
    1.03,
    1.07,
    1.13,
    1.2,
    1.26,
    1.33,
    1.39,
    1.44,
    1.5,
    1.56]


    data_GW2 = [
            1, 
            0.98,
            0.95,
            0.93,
            0.92,
            0.9,
            0.87,
            0.85,
            0.82,
            0.8,
            0.77,
            0.73,
            0.69,
            0.66,
            0.62,
            0.58,
            0.53,
            0.49,
            0.45,
            0.41,
            0.37,
            0.33,
            0.3,
            0.26,
            0.22,
            0.19,
            0.16,
            0.13,
            0.11,
            0.1,
            0.12,
            0.15,
            0.21,
            0.28,
            0.33,
            0.39,
            0.43,
            0.47,
            0.51,
            0.54,
            0.58,
            0.62,
            0.66,
            0.71,
            0.75,
            0.79,
            0.83,
            0.87,
            0.9,
            0.92,
            0.94,
            0.96,
            0.98,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            0.99,
            0.97,
            0.95,
            0.93,
            0.91,
            0.89,
            0.87,
            0.85,
            0.82,
            0.8,
            0.76,
            0.73,
            0.69,
            0.65,
            0.62,
            0.57,
            0.53,
            0.49,
            0.45,
            0.41,
            0.36,
            0.32,
            0.29,
            0.25,
            0.21,
            0.18,
            0.14,
            0.11,
            0.08,
            0.06,
            0.04,
            0.04,
            0.04,
            0.08,
            0.13,
            0.18,
            0.23,
            0.28,
            0.33,
            0.37,
            0.41,
            0.45,
            0.49,
            0.54,
            0.59,
            0.65,
            0.7,
            0.74,
            0.79,
            0.84,
            0.87,
            0.9,
            0.93,
            0.96,
            0.98,
            1,
            1.03,
            1.05,
            1.06 ]


    data = data_GW2

    step = -len(data)
    yn, tn = tnorm(data, step=step, k=3, smooth=0, show=True)

    for i, y in enumerate(yn):
        print ('{0:.2f}'.format(y))