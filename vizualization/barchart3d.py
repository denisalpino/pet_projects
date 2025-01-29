import numpy as np

from numpy.typing import ArrayLike, NDArray
from typing import Sequence

from seaborn import color_palette
from plotly.graph_objects import Mesh3d, Figure, Frame


# Error messages
msg_ticks = 'The {} parameter must conform to the sequence protocol and contain string values'
msg_indent = 'The value of the indent parameter must be in the interval [0; 1)'
msg_bool = 'The argument passed to the {} parameter must be a boolean value'
msg_speed = 'The argument passed in the speed parameter must be an integer or float value'
msg_neg_speed = 'Speed multiplier сannot be a negative or zero value'
msg_neg_val = 'Negative value detected in the passed data array'
msg_shape = ("The passed array isn't reshapable according to the passed "
             "parameters xticks, yticks and animation_ticks.")
msg_cols = ('The passed argument for the data parameter contains {} columns, '
            'but {} ticks were passed for the x-axis.')
msg_rows = ('The passed argument for the data parameter contains {} rows, '
            'but {} ticks were passed for the y-axis.')
msg_depth = ('The passed argument for the data parameter contains {} depth '
             'levels, but {} ticks were passed for the animation axis.')
msg_two_to_three = ('A two-dimensional array cannot be converted to a '
                    'three-dimensional array. Remove the animation_ticks '
                    'parameter or change the shape of the array.')


def barchart3d(
        data: ArrayLike, *, xticks: Sequence[str] = None, yticks: Sequence[str] = None,
        xlabel: str = None, ylabel: str = None, zlabel: str = None,
        title: str = None, animation_ticks: Sequence[str] = None,
        animation_title: str = None, cmap: str = 'magma_r', width: int = None,
        height: int = None, indent: float = 0.1, log_scale: bool = False,
        sort: bool = False, speed: int | float = 1
) -> Figure:
    '''
    Builds 3D bar chart with animation capability.

    Parameters
    ----------
        data: numpy.typing.ArrayLike
            One-/two-/three-dimensional array of non-negative values. If a
            one-dimensional array is passed, its shape must be reshapable to
            two-dimensional (if only xticks and yticks are passed) or
            three-dimensional (if animation_ticks are passed) using
            numpy.reshape().
        xticks: Sequence[str], default None
            Ticks for x scale i.e. columns in data
        yticks: Sequence[str], default None
            Ticks for y scale i.e. rows in data
        xlabel: str, default None
            The name of x scale i.e. columns in data
        ylabel: str, default None
            The name of y scale i.e. rows in data
        zlabel: str, default None
            The name of what the values in the data mean
        title: str, default None
            The title of barplot
        animation_ticks: Sequence[str], default None
            Ticks for animation scale i.e. depth of data (if not None)
        animation_title: str, default None
            The titile for animation scale
        cmap: str, default 'magma_r'
            The name of colormap for barplot. Possible palette values include:
                1. name of matplotlib colormap
                2. 'husl' or 'hls'
                3. 'ch:<cubehelix arguments>'
                4. 'light:<color>', 'dark:<color>', 'blend:<color>,<color>',
                5. a sequence of colors in any format matplotlib accepts
        width: int, default None
            Width of the graph (in pixels)
        height: int, default None
            Height of the graph (in pixels)
        indent: float, dafault 0.1
            Bar spacing, that must be in the interval [0; 1)
        log_scale: bool, default False
            Whether it's necessary to logarithmize the values on the
            z-axis that were passed to the data parameter. When set to True,
            z-scale values are hidden because they aren't relevant
        sort: bool, default False
            Determines whether sorting is necessary. If set to True, sorting is
            performed on the x and y axes
        speed: int or float, default 1
            Animation speed multiplier. Cannot be a negative or zero value

    Returns
    -------
    return plotly.graph_objects.Figure()

    Notes
    -----
    Note that the final dimensionality of the data to be reflected in the
    barplot is determined by the xticks, yticks and animation_ticks (if given)
    parameters.

    There are several scenarios of the function operation depending on the
    dimensionality of the passed array:
    1. if a one-dimensional array is input, it will be converted to a two- or
    three-dimensional array, depending on whether the animation_ticks parameter
    is passed and whether the number of values in the current array is
    comparable to the expected number.
    2. if a two-dimensional array is input, it won't be converted to
    a three-dimensional array. In this case, a check will be performed to see if
    the shape of the array matches the sizes of the passed xtick and ytick
    sequences. If you pass animation_ticks together with a two-dimensional
    array, an exception will be raised.
    3. if a three-dimensional array is input, only a check will be performed to
    see if the shape of the array matches the sizes of the passed xtick, ytick
    and animation_ticks sequences.

    If there is a need to move text in ticks, axis labels or title to a new
    line, it's necessary to pass a string containing HTML tag <br> in the
    appropriate place to the input of the corresponding parameter.
    '''

    # Validate passed arguments
    _validate_args(
        data=data, xticks=xticks, yticks=yticks, animation_ticks=animation_ticks,
        log_scale=log_scale, indent=indent, sort=sort, speed=speed
    )

    # Trying to get the correct NDarray based on the given arguments for ticks.
    data = _get_reshaped_data(
        data=data, xticks=xticks, yticks=yticks, animation_ticks=animation_ticks
    )

    depth, nrows, ncols = data.shape

    if sort:
        data, xticks, yticks = _get_sorted_data(
            data=data, xticks=xticks, yticks=yticks)

    # Determine the side size of one bar
    bar_side = 1 - indent

    figure_config = dict()

    # Format axis captions and chart name, if they are set
    xlabel = f'<b>{xlabel}</b>' if xlabel else ''
    ylabel = f'<b>{ylabel}</b>' if ylabel else ''
    zlabel = f'<b>{zlabel}</b>' if zlabel else ''
    title = f'<b>{title}</b>' if title else None
    animation_title = f'{animation_title}: ' if animation_title else None

    # Looking for the aspect ratio to make the bars square rather than rectangular
    x_aspect = 1
    y_aspect = nrows / ncols
    z_aspect = min(x_aspect, y_aspect)

    # Customizes the height, width, indents, lettering, and aspect ratio of the shape
    figure_config['layout'] = dict(
        width=width, height=height, margin=dict(l=40, r=40, b=60, t=0),
        title=dict(text=title, font=dict(size=20), x=0.5, y=0.95),
        scene=dict(
            aspectmode='manual',
            aspectratio=dict(x=x_aspect, y=y_aspect, z=z_aspect),
            xaxis=dict(title=xlabel, tickvals=list(range(ncols)), ticktext=xticks),
            yaxis=dict(title=ylabel, tickvals=list(range(nrows)), ticktext=yticks),
            zaxis=dict(title=zlabel, showticklabels=(not log_scale))
        )
    )

    # Create the basic (first) figure
    first_screen = _get_list_of_bars(
        mat=data[0], xticks=xticks, yticks=yticks, xlabel=xlabel, ylabel=ylabel,
        bar_side=bar_side, cmap=cmap, log_scale=log_scale, ncols=ncols, nrows=nrows
    )
    figure_config['data'] = first_screen

    # If a three-dimensional array, create frames and slider
    if depth > 1:
        frames = [
            Frame(
                data=_get_list_of_bars(
                    mat=data[level], xticks=xticks, yticks=yticks,
                    xlabel=xlabel, ylabel=ylabel, bar_side=bar_side, cmap=cmap,
                    log_scale=log_scale, ncols=ncols, nrows=nrows
                ),
                name=animation_ticks[level]
            )
            for level in range(depth)
        ]
        figure_config['frames'] = frames

        # Configure the display of the current value on the slider,
        # the location and animation of the slider slider
        sliders_dict = dict(
            active=0,
            currentvalue=dict(
                font=dict(size=16), prefix=animation_title,
                visible=True,
                xanchor="left"
            ),
            transition=dict(duration=500 / speed, easing='cubic-in-out'),
            len=0.9, x=0.1, pad=dict(b=10, t=15),
            steps=[]
        )

        # Filling the slider with steps
        steps = [
            dict(
                args=[[tick], dict(duration=300 / speed, mode='immediate')],
                label=tick, method="animate"
            )
            for tick in animation_ticks
        ]
        sliders_dict['steps'] = steps

        # Configure the display of the buttons location, their appearance and
        # animation method
        updatemenus_dict = dict(
            direction='left', pad=dict(r=20, t=40),
            xanchor="right", yanchor="top", x=0.1, y=0,
            type='buttons',
            buttons=[
                dict(
                    args=[
                        None,
                        dict(
                            frame=dict(duration=300 / speed),
                            fromcurrent=True,
                            transition=dict(
                                duration=300 / speed, easing='quadratic-in-out'
                            )
                        )
                    ],
                    label='►',
                    method="animate"
                ),
                dict(
                    args=[[None], dict(mode='immediate')],
                    label='❚❚',
                    method="animate"
                )
            ]
        )
        figure_config['layout'].update(dict(
            sliders=[sliders_dict],
            updatemenus=[updatemenus_dict]
        ))

    fig = Figure(figure_config)

    return fig


def _validate_args(
        *, data, xticks, yticks, animation_ticks, log_scale, indent, sort, speed
) -> None:
    '''
    Checks whether the values and types of the passed objects match the
    required ones.
    '''
    def is_seq(x): return hasattr(x, '__getitem__') and hasattr(x, '__len__')
    def contains_str(x): return all((isinstance(elem, str) for elem in x))

    if not (is_seq(xticks) and contains_str(xticks)):
        raise TypeError(msg_ticks.format('xticks'))
    if not (is_seq(yticks) and contains_str(yticks)):
        raise TypeError(msg_ticks.format('yticks'))

    if animation_ticks and not (is_seq(animation_ticks) and contains_str(animation_ticks)):
        raise TypeError(msg_ticks.format('animation_ticks'))

    if not isinstance(log_scale, bool):
        raise TypeError(msg_bool.format('log_scale'))
    if not isinstance(sort, bool):
        raise TypeError(msg_bool.format('sort'))
    if not isinstance(speed, int | float):
        raise TypeError(msg_speed)

    if not (0 <= indent < 1):
        raise ValueError(msg_indent)
    if np.min(data) < 0:
        raise ValueError(msg_neg_val)
    if speed <= 0:
        raise ValueError(msg_neg_speed)

    return


def _get_reshaped_data(*, data, xticks, yticks, animation_ticks) -> NDArray:
    '''
    Converts an ArrayLike object to an NDarray, checks that the dimensionality
    and size of the original array are correct relative to the expected ones,
    and reshapes the data if necessary.
    '''
    data = np.array(data)

    dims = data.shape

    # Getting the required data shape
    x_len = len(xticks)
    y_len = len(yticks)
    animation_len = len(animation_ticks) if animation_ticks else 1

    match len(dims):
        case 1:
            depth, nrows, ncols = 1, 1, dims

            if data.size != x_len * y_len * animation_len:
                raise ValueError(msg_shape)

            data = np.reshape(data, (animation_len, y_len, x_len))
        case 2:
            depth, nrows, ncols = 1, *dims

            if ncols != x_len:
                raise ValueError(msg_cols.format(ncols, x_len))
            if nrows != y_len:
                raise ValueError(msg_rows.format(nrows, y_len))
            if animation_ticks:
                raise ValueError(msg_two_to_three)

            data = np.reshape(data, (animation_len, *dims))
        case 3:
            depth, nrows, ncols = dims

            if ncols != x_len:
                raise ValueError(msg_cols.format(ncols, x_len))
            if nrows != y_len:
                raise ValueError(msg_rows.format(nrows, y_len))
            if depth != animation_len:
                raise ValueError(msg_depth.format(depth, animation_len))
        case _:
            raise ValueError(msg_shape)

    return data


def _get_sorted_data(
        *, data: NDArray, xticks: Sequence[str], yticks: Sequence[str]
) -> tuple[NDArray, Sequence[str], Sequence[str]]:
    mat_sum = data.sum(axis=0)

    # Find the sums by axes for further sorting
    row_sum = mat_sum.sum(axis=1)
    col_sum = mat_sum.sum(axis=0)

    # Find the order of rows and columns and take their indices
    row_order: list[int] = [
        np.where(row_sum == val)[0][0]
        for val in sorted(row_sum, reverse=True)
    ]
    col_order: list[int] = [
        np.where(col_sum == val)[0][0]
        for val in sorted(col_sum, reverse=True)
    ]

    # Changing the order of the labels
    row_labels = [yticks[ind] for ind in row_order]
    col_labels = [xticks[ind] for ind in col_order]

    # Create a tensor with correct arrangement of columns and rows
    data = data[:, row_order, :][:, :, col_order]

    return data, col_labels, row_labels


def _get_list_of_bars(
        mat: ArrayLike, xticks: Sequence[str], yticks: Sequence[str],
        xlabel: str, ylabel: str, bar_side: float, cmap: str, log_scale: bool,
        ncols: int, nrows: int
) -> list[Mesh3d]:
    traces: list[Mesh3d] = []

    mat_unique_vals = np.unique(mat)

    # Creating a color palette
    n_colors = mat_unique_vals.size
    colors = color_palette(palette=cmap, n_colors=n_colors)

    # The matrix is processed so that the maximum value is located in the far
    # corner of the figure
    for y in range(nrows):
        for x in range(ncols):
            val = mat[y, x]

            # Get the coordinates of the bar
            x_min, x_max = x - bar_side / 2, x + bar_side / 2
            y_min, y_max = y - bar_side / 2, y + bar_side / 2

            # Get the color for the current value from the color palette array
            color = colors[np.where(mat_unique_vals == val)[0][0]]
            rgb_str = f'rgb({", ".join(str(int(i * 255)) for i in color)})'

            # Customize the legend in the pop-up window that appears when
            # hovering over the bar
            if xlabel and ylabel:
                hovertext = (
                    f'{xlabel}: {xticks[x].replace("<br>", " ")}<br>'
                    f'{ylabel}: {yticks[y].replace("<br>", " ")}<br>'
                    f'<b>Value</b>: {val}'
                )
            else:
                hovertext = (
                    f'{xticks[x]}<br>'
                    f'{yticks[y]}<br>'
                    f'<b>Value</b>: {val}'
                )

            bar = Mesh3d(
                x=[x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max],
                y=[y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min],
                z=[0] * 4 + [np.log(val + 1) if log_scale else val] * 4,
                alphahull=0,
                color=rgb_str, flatshading=True,
                hovertext=hovertext, hoverinfo='text'
            )
            traces.append(bar)

    return traces
