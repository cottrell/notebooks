import numpy as np
# notes mostly

def meshgrid_from_df(df, **kwargs):
    # this is useful because meshgrid is confusing ... is like 'real space' not i,j space ... things are flipped. 
    df = df.sort_index(axis=1).sort_index(axis=0)
    x, y = np.meshgrid(df.index.values, df.columns.values, **kwargs)
    z = df.values.T
    return x, y, z

def doplot_3d_from_df(df, zlabel=None, fig=None, num=1, kind='wireframe', meshgrid_kwargs={}, **plot_options):
    from mpl_toolkits import mplot3d
    import matplotlib.pyplot as plt
    if fig is None:
        fig = plt.figure(num=num)
    ax = plt.axes(projection='3d')
    xx, yy, zz = meshgrid_from_df(df, **meshgrid_kwargs)
    if kind == 'wirefram':
        ax.plot_wireframe(xx, yy, zz, **plot_options)
    else:
        raise Exception('nip')
    if df.index.names is not None:
        ax.set_xlabel(df.index.names[0])
    if df.columns.names is not None:
        ax.set_ylabel(df.columns.names[0])
    if zlabel is not None:
        ax.set_zlabel(zlabel)
    return fig, ax
