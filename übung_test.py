# Part 1:
# Q1:

import übung
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Q2:
year_to_anomaly_dict = übung.read_year_to_anomaly_data("Land_and_Ocean_summary.txt")

# Q3:
übung.create_line_plot(year_to_anomaly_dict, "anomalies_per_year.png")

# Part 2:
# Q1:
from übung import ColorMapper
color_mapper = ColorMapper(year_to_anomaly_dict.values())
print(color_mapper.get_color(0.0))

# Q2:
year_blocks = übung.construct_blocks(year_to_anomaly_dict)
print(year_blocks)

def plot_blocks(list_of_blocks, color_mapper,
                colorbar=True,
                figure_width=20, figure_height=5):
    '''
    Visualize list of blocks, where each block is specified in the format
    (x-coordinate, y-coordinate, width, height, value). The color_mapper is
    used to look up colors corresponding to the values provided in each block.
    :param list_of_blocks: List of (x-coordinate, y-coordinate, width, height, value) tuples
    :param color_mapper: Used to lookup values for each block
    :param colorbar: Whether to include a color bar
    :param figure_width: Width of figure
    :param figure_height: Height of figure
    :return: None
    '''

    fig, ax = plt.subplots(1, figsize=(figure_width, figure_height))
    ax.set_title("Average anomaly per decade")
    x_values = []
    y_values = []
    for block in list_of_blocks:
        rect = matplotlib.patches.Rectangle(block[:2], block[2], block[3],
                                            linewidth=1, edgecolor='none',
                                            facecolor=color_mapper.get_color(block[-1]))
        ax.add_patch(rect)
        x_values += [block[0], block[0]+block[2]]
        y_values += [block[1], block[1]+block[3]]

    ax.set_xlim(min(x_values), max(x_values))
    ax.set_ylim(min(y_values), max(y_values))

    if colorbar:
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(plt.gca())
        ax_cb = divider.new_horizontal(size="1%", pad=0.1)
        matplotlib.colorbar.ColorbarBase(ax_cb, cmap=color_mapper.cmap,
                                         orientation='vertical',
                                         norm=matplotlib.colors.Normalize(
                                             vmin=-color_mapper.max_abs_value,
                                             vmax=color_mapper.max_abs_value))
    plt.gcf().add_axes(ax_cb)
    #plt.show()

plot_blocks(year_blocks, color_mapper)

# Q3:
anomalies_per_decade = übung.calculate_anomalies_per_decade(year_to_anomaly_dict)

#Part 3: Looking at Latitudes
#Q1:
latitude_year_to_anomaly_dict = übung.read_latitude_year_to_anomaly_data("anomalies_per_latitude.txt")
print(latitude_year_to_anomaly_dict[87.5][2018])

# Q2:
latitude_year_anomalies = übung.get_values_from_nested_dict(latitude_year_to_anomaly_dict)
color_mapper_latitudes = ColorMapper(latitude_year_anomalies)

# Q3:
year_latitude_blocks = übung.construct_latitude_blocks(latitude_year_to_anomaly_dict)
plot_blocks(year_latitude_blocks, color_mapper_latitudes)

# Part 4: CO2 emissions
# Q1:
top10_emitting_countries = übung.find_top10_emitting_countries(("annual-co-emissions-by-region.csv"))

def plot_emissions(list_of_tuples, population_dict=None, figure_width=15, figure_height=5):
    '''
    Create a bar plot of CO2 emissions. If population_dict is provided, resize
    bars so that width reflect population size and height denotes emission per
    capita.

    :param list_of_tuples: List of (country-name, value) tuples
    :param population_dict: Dictionary of (country-name, population) pairs
    :param figure_width: Width of figure
    :param figure_height: Height of figure
    :return:
    '''

    # Create new figure
    fig,ax = plt.subplots(1, figsize=(figure_width, figure_height))

    # Choose color map
    cmap = plt.get_cmap("Spectral")

    heights = []
    labels = []
    widths = []
    colors = []
    for i, entry in enumerate(list_of_tuples):
        heights.append(entry[1])
        # Scale down height of bar with population size
        if population_dict is not None:
            heights[-1] /= population_dict[entry[0]]
        labels.append(entry[0])
        colors.append(cmap(i/len(list_of_tuples)))
    if population_dict is None:
        x = range(len(list_of_tuples))
        widths = [0.9] * len(list_of_tuples)
    else:
        max_width = 0
        for entry in list_of_tuples[:-1]:
            max_width = max(max_width, population_dict[entry[0]])
        x = np.arange(len(list_of_tuples)) * max_width
        for entry in list_of_tuples:
             widths.append(population_dict[entry[0]])

    # Create bar plot and set tick values
    plt.bar(x, height=heights, width=widths, color=colors)
    plt.ylabel("Annual CO2 emissions (tonnes)")
    plt.xticks(x, labels, rotation=45, ha="right")
    plt.show()

plot_emissions(top10_emitting_countries)

# Q3:
population_dict = übung.read_population_data("population.csv",2017)
plot_emissions(top10_emitting_countries,population_dict=population_dict)