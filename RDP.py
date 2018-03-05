# Works with Python 3

# RDP.py

"""
A program that can be used instead of Recreational Dive Tables for calculating
Decompression Intervals between SCUBA Diving sessions. It is based on the tables
used by the PADI Organization.

For safety, this program rounds up user input values for planned dive depth and
duration (to the next highest table value) when the input values do not match
dive table values (e.g. an input depth of 27 feet, which gets rounded up to 35
feet).
"""
# import pandas and numpy

import pandas as pd
import numpy as np

import sys
import os
def restart_program():
    """
    Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function.
    """
    python = sys.executable
    os.execl(python, python, * sys.argv)

# import .csv file containing dive chart DataFrame
# replace "XXX" values in DataFrame with NaN (NumPy for 'Not a Number')
# RDP_chart.replace("XXX",np.nan)
RDP_chart = pd.read_csv('RDP_chart.csv', index_col = 0, na_values = "XXX")

# print the DataFrame
# print(RDP_chart)

# print welcome message

print("Welcome to the Recreational Dive Planner!\n"
"Please provide your planned dive information below.\n")

# now capture the planned dive depth and time as as inputs provided by the user

'''
Note: when user inputs depth, it must be a number (not a string)
- If the provided depth does not match any depths in our dive chart, the
provided depth must be rounded up to determine which column we will look in for
matching dive time. We can create a small function to prompt user for correct
input type.
'''

# LATER FEATURE: add option to select feet or meters

def get_depth():
    '''
    Creates a function that will get user input for depth
    In case user inputs incorrect (non-numeral) characters, shows error message
    '''
    depth = input("Planned dive depth (in feet): ")
    try:
        # depth must be an integer
        depth = int(depth)
        return depth
    # if user provides incorrect input (not a number), print error message and
    # provide another input prompt to enter correct value (a number)
    except ValueError:
        print("ERROR: Please enter your planned dive depth as an integer "+
        "value in feet")
        return get_depth()

# declare a variable that holds user input for planned depth dive
user_depth = get_depth()

if user_depth > 140:
    print("Your planned dive depth exceeds the limits of this program.\nPlease "
    "provide a value of 140 feet or less.")
    get_depth()

def get_time():
    '''
    Creates a function that will get user input for time
    In case user inputs incorrect (non-numeral) characters, shows error message
    '''
    time = input("Planned dive duration (in minutes): ")
    try:
        # time must be an integer
        time = int(time)
        return time
    # if user provides incorrect input (not a number), print error message and
    # provide another input prompt to enter correct value (a number)
    except ValueError:
        print("ERROR: Please enter your planned dive duration in minutes")
        return get_time()

# declare a variable that holds user input for planned dive duration
user_time = get_time()

'''
Get the label of "depth" to which you are going to descend

Declare variable "table_of_depths" comprised by taking the full RDP_chart and
creating a new DataFrame from it, using the depth labels from the top of each
column, create a new column header listing "depths" with float
versions of each starting depth
'''
table_of_depths = pd.DataFrame(RDP_chart.columns.astype("float64"),
    index = RDP_chart.columns, columns = ["depth"])
# print("table_of_depths")
# print(table_of_depths)

'''
other examples that are similar to the above, but not appropriate for our needs
-----
# Does not include the column header "depth"
# Row labels are just indices
table_of_depths2 = pd.DataFrame(RDP_chart.columns.astype("float64"))

-----
# Column depths are expressed as integers, not float values
table_of_depths3 = pd.DataFrame(RDP_chart.columns, index = RDP_chart.columns,
    columns = ["depth"])
'''
# Get the absolute value of the difference between user's depth input and the
# starting depth float values. Make it a variable.

abs_table_depths = (table_of_depths - user_depth).abs()

# Sort these new variables by "depth" float (from lowest to highest).

sorted_depths = abs_table_depths.sort_values(by = "depth")

# print("sorted_depths")
# print(sorted_depths)

# The rows representing depths are now sorted by their closeness to the user's
# depth input.

"""
IF the user's depth input does not exactly match a depth column label, we want
to find the value of the depth column label that is one up from the depth, so we
will essentially be rounding up to the next label.
"""

#sorted_depths.loc[sorted_depths.index,:]

#print("test, sorted_depths.loc[sorted_depths.index,:]")
#print(sorted_depths.loc[sorted_depths.index])

#Declare a new variable that will inform the program which 'depth' column to
#check in order to locate a dive time value that will yield the Pressure Group.

# pay attention to that greater ">=" symbol in line 132 - it ensures that when
# user enters exactly 35, 40, etc as depth, program does not round up to next
# depth column

depth_index = sorted_depths.loc[sorted_depths.index.astype("float64")
>= user_depth,:].index[0]

'''
Want to see if it worked?
print(
"depth_index - shows we have found the closest value to the user_depth input")
print(depth_index)
'''

# isolate the column that we will search within to fine a match dive time input
depth_column = RDP_chart.loc[:,depth_index]

# print(depth_column)

'''
Now, on to time...
'''
# Get the absolute value of the difference between user's time input and the
# starting dive duration float values. Make it a variable.
table_times = (depth_column - user_time)

# print("table_times = (depth_column - user_time)")
# print(table_times)

# convert table_times to a dataframe and label the column for time_for_depth
table_times = table_times.to_frame()

table_times.columns = ['time_for_depth']
'''
Get the DiveGroupLetter from simply getting .name (letter column) of the
smallest positive value in the 'time_for_depth' column after subtracting
user_time. This letter will then be passed to the next part of the program,
which will assess dive interval time.

We need to plan for possible IndexError, for when the user provides dive times
that exceed safe limits set by the dive chart. We will start with this.
'''
try:
    table_times.loc[table_times['time_for_depth'] >= 0].iloc[0]
except IndexError:
    print("\n\n----------\n\nWarning!\n\nThe dive duration you entered exceeds "
    "the limits of safety recommended by PADI.\nThis program will restart so "
    "you can provide safer input values.\n\n...\n...\n...\n")
    restart_program()

DiveGroupLetter = table_times.loc[table_times['time_for_depth']
    >= 0].iloc[0].name

# print(depth_column[np.logical_or(depth_column.index == DiveGroupLetter)])

print(
"\n----------\n"
"Planned dive depth (rounded): ", depth_index,"feet\n"
"Planned dive time (rounded): ", user_time,"minutes\n"
"Dive Group Letter: ", DiveGroupLetter)
