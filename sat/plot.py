import pandas as pd
import matplotlib.pyplot as plt
import logging
import seaborn as sns
import os
sns.set()
DPI = 72.27

logger = logging.getLogger(__name__)
_MAX_HEATMAP_ENTRIES = 200


def plot_heatmap(data_frame, title, folder, file_name):
    number_of_entries = data_frame.shape[0]
    if number_of_entries > _MAX_HEATMAP_ENTRIES:
        logger.warn("Number of entries is %d an exceeds limit of %d. Will skip creation of heatmap" % (
            number_of_entries, _MAX_HEATMAP_ENTRIES))
        return
    fontsize_pt = plt.rcParams['ytick.labelsize']
    # compute the required figure height
    matrix_height_pt = fontsize_pt * number_of_entries *1.02
    matrix_height_in = matrix_height_pt / DPI
    entry_offset = number_of_entries * 0.2
    figure_size = int(round(matrix_height_in + entry_offset))
    # colors
    color_map = plt.get_cmap('autumn_r', 10)
    #color_map.set_under('white')
    #color_map.set_over('black')
   # ten_percent = int(round(number_of_entries * 0.1))
    #max_ten_percent = sorted(data_frame.values.flatten())[-ten_percent:]
    #vmax = min(max_ten_percent)
    # build figure
    fig, ax = plt.subplots(figsize=(figure_size, figure_size))
    ax.set_title(title)
    # add heatmap
    sns.heatmap(data_frame, square=True, fmt="d", ax=ax,
                xticklabels=True, yticklabels=True,
                annot_kws={"size": 8}, annot=True,
                cbar_kws={"shrink": 0.5},
                cmap=color_map,  
                #vmin=1, vmax=vmax,
                linewidths=0.5, linecolor="grey"
                )
    _writeFigure(fig, folder, file_name)


def plot_stacked_barchart(data, ylabel, title, folder, file_name):
    column0 = data[data.columns[0]].values
    column1 = data[data.columns[1]].values
    total = column0 + column1
    data["total"] = total
    # Set general plot properties
    sns.set_style("white")
    sns.set_context({"figure.figsize": (24, 10)})
    # Plot 1 - background - "total" (top) series
    sns.barplot(x=data.index, y=data.total, color="red")
    # Plot 2 - overlay - "bottom" series
    bottom_plot = sns.barplot(x=data.index, y=column0, color="green")
    top_bar = plt.Rectangle((0, 0), 1, 1, fc="red", edgecolor='none')
    bottom_bar = plt.Rectangle((0, 0), 1, 1, fc='green',  edgecolor='none')
    legend = plt.legend([bottom_bar, top_bar], [data.columns[0],
                                                'Total'], loc=1, ncol=2, prop={'size': 16})
    legend.draw_frame(False)
    bottom_plot.set_ylabel(ylabel)
    bottom_plot.set_title(title)
    # Optional - Make plot look nicer
    sns.despine(left=True)
    for label in bottom_plot.get_xticklabels():
        if len(label._text) > 60:
            label._text = "..."+label._text[-60:]
    bottom_plot.set_xticklabels(bottom_plot.get_xticklabels(), rotation=90)
    _writeFigure(bottom_plot.get_figure(), folder, file_name)


def _writeFigure(figure, folder, file_name):
    path = os.path.join(folder, file_name)
    figure.savefig(path, bbox_inches='tight')
    plt.close(figure)
