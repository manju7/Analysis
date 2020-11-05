# Übung
# Python
# Part 1:
# Q1:
import numpy as np
import matplotlib.pyplot as plt

# Q2:
def read_year_to_anomaly_data(filename):
    '''Opens the file, iterate over the entries, extract the first two columns of the file and returns a dictionary'''
    # Open file
    with open(filename) as file:
        dict = {}
        # Iterate over each line in file
        for line in file:
            # Only take lines which start with two spaces
            if line[:2] == "  ":
                # Split lines
                lineX = line.split()
                # Create a dictionary with years as keys (integers) and temperature anomalies as values (floats)
                dict[int(lineX[0])] = float(lineX[1])
        return dict

# Q3:
def create_line_plot(data, out_filename):
    '''Creates line plot of the key,value pairs in the dictionary'''
    fig, ax = plt.subplots()
    ax.set_xlabel("Year")
    ax.set_ylabel("Global Temperatur Anomaly")
    ax.set_title("Annual Global Temperatur Anomaly")
    x = list(data.keys())
    y = list(data.values())
    plt.plot(x, y)
    plt.savefig(out_filename)
    return fig, ax

# Part 2:
# Q1:
class ColorMapper:
    '''Map temperature values to colors'''
    def __init__(self, values, cmap_str="RdBu_r"):
        '''Constructor with max absolute value and color mapper as attributes'''
        abs_values = []
        for i in values:
            abs_value = abs(i)
            abs_values.append(abs_value)
            self.max_abs_value = max(abs_values)
            self.cmap = plt.get_cmap(cmap_str)

    def get_color(self, value):
        '''Take temperature value and returns corresponding color'''
        color = self.cmap(value)
        return color

# Q2:
def construct_blocks(data,bottom=0.0,height=1.0):
    '''Creates vertical stripes: Takes three arguments and return a list of tuples, each with five elements'''
    list_of_tuples = []
    for i in data:
        tuple_i = (i, bottom, 1, height, data[i])
        list_of_tuples.append(tuple_i)
    return list_of_tuples

# Q3:
def calculate_anomalies_per_decade(dictionary):
    '''Calculate average anomaly per decade'''
    dic_decades = {}
    years = []
    sum_value = 0
    for i in dictionary:
        if len(years) < 9: #decade does not include the last year
            years.append(i)
            sum_value += dictionary[i]

            if i == list(dictionary.keys())[-1]:
                dic_decades[(years[0], years[len(years)-1]+1)] = sum_value / len(years)

        else:
            years.append(i)
            sum_value += dictionary[i]
            dic_decades[(years[0], years[len(years)-1]+1)] = sum_value / len(years)
            years = []
            sum_value = 0

    print(dic_decades)

#Part 3: Looking at Latitudes
#Q1:
def read_latitude_year_to_anomaly_data(filename):
    '''Returns a dictionary of dictionaries (outer: latitudes as keys --> floats / inner: years as keys --> int and anomalies as values --> floats)'''
    with open(filename) as input_file:
        file = input_file.read().splitlines()
        outer_dictionary = {}
        for line in file:
            lineX = line.split()
            # If latitude.key not in outer dictionary
            if float(lineX[1]) not in outer_dictionary.keys():
                # Assign latitude to keys of the outer dictionary and create an empty inner dictionary
                outer_dictionary[float(lineX[1])] = {}
            # Create for each latitude key the inner dictionary with the corresponding key-/value pair
            outer_dictionary[float(lineX[1])][int(lineX[0])] = float(lineX[2])
        return outer_dictionary

# Q2:
def get_values_from_nested_dict(nested_dictionary):
    '''Returns a list of all values contained in all sub-directories'''
    list_of_all_values = []
    for key in nested_dictionary:
        for subkey in nested_dictionary[key]:
            list_of_all_values.append(nested_dictionary[key][subkey])
    return list_of_all_values

# Q3:
def construct_latitude_blocks(nested_dictionary):
    '''Returns a list of tuples, each with 5 elements (year,latitude,width=1,height,temperature anomaly)'''
    list_of_tuples = []
    for latitude in nested_dictionary:
        for year in nested_dictionary[latitude]:
            list_of_tuples.append((year, latitude, 1, 5, nested_dictionary[latitude][year]))
    return list_of_tuples

# Part 4: CO2 emissions
# Q1:
#sort -n -k3 -k4 -r -t"," annual-co-emissions-by-region.csv | grep -E "[A-Z]{3}" | head > top10_CO2.csv
#sort -n -k3 -k4 -r -t"," annual-co-emissions-by-region.csv | grep -E ".+,[A-Z]{3}," | head > top10_CO2.csv

# Q2:
def find_top10_emitting_countries(filename):
    '''Returns a list of tuples (full country name, CO2 emission) the 10 highest emitting countries'''
    with open(filename) as input_file:
        file = input_file.read().splitlines()
        empty_list = []
        for line in file:
            lineX = line.split(",")
            if len(lineX[1]) == 3:
                year = int(lineX[2])
                element = float(lineX[3])
                data = [year,element,(lineX[0],element)]
                empty_list.append(data)
        sorted_list = sorted(empty_list,reverse=True)
        output = []
        for line in sorted_list:
            output.append(line[2])
        return output[:10]

# Q3:
def read_population_data(filename, year_value):
    with open(filename) as input_file:
        file = input_file.read().splitlines()
        empty_dict = {}
        for line in file:
            lineX = line.split(",")
            if len(lineX[1]) == 3 and int(lineX[2])==year_value:
                region = lineX[0]
                population_size = int(lineX[3])
                empty_dict[region] = population_size
        return empty_dict

# Numpy test:
import numpy as np
import pandas as pd
df = pd.read_csv("annual-co-emissions-by-region.csv")

# Sort by value:
#print(df.sort_values(by="Annual CO₂ emissions (tonnes )"))
# Filter by column:
# print("sfrf")
# code_three_digits = df[df["Code"].str.len()==3]
# sort_by_year = code_three_digits[code_three_digits["Year"] == 2017]
# sort_by_emissions = sort_by_year.sort_values("Annual CO₂ emissions (tonnes )",ascending=False)
# print(sort_by_emissions.head(10))
# # Get max-value of Annual CO2 emissions:
# column = sort_by_emissions["Annual CO₂ emissions (tonnes )"]
# max_value = column.max()
# print(max_value)






