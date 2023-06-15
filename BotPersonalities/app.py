import os

from dotenv import load_dotenv

import calculateSimilarity as cal
import visualization as v

# Load environment variables from .env file
load_dotenv()

def group_lines(filename):
    groups = []
    current_group = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()

            if line:
                current_group.append(line)
            elif current_group:
                groups.append(current_group)
                current_group = []

        if current_group:
            groups.append(current_group)

    return groups

within_user = input("Calculate similarity scroe within long/short descriptions? Please answer y/n.")
btw_short_user = input("Calculate similarity scroe between short descriptions? Please answer y/n. ")
btw_long_user = input("Calculate similarity scroe between long descriptions? Please answer y/n. ")
btw_all_user = input("Calculate similarity scroe between all descriptions? Please answer y/n.")

# transform user input
if within_user.lower() == 'y':
    within_user = True
elif within_user.lower() == 'n':
    within_user = False
else:
    print("Invalid input. Defaulting to False.")
    within_user = False
if btw_short_user.lower() == 'y':
    btw_short_user = True
elif btw_short_user.lower() == 'n':
    btw_short_user = False
else:
    print("Invalid input. Defaulting to False.")
    btw_short_user = False
if btw_long_user.lower() == 'y':
    btw_long_user = True
elif btw_long_user.lower() == 'n':
    btw_long_user = False
else:
    print("Invalid input. Defaulting to False.")
    btw_long_user = False
if btw_all_user.lower() == 'y':
    btw_all_user = True
elif btw_all_user.lower() == 'n':
    btw_all_user = False
else:
    print("Invalid input. Defaulting to False.")
    btw_all_user = False
    
within_sys = bool(os.getenv("WITHIN_GROUPS"))
btw_short_sys = bool(os.getenv("BETWEEN_SHORT_GROUPS"))
btw_long_sys = bool(os.getenv("BETWEEN_LONG_GROUPS"))
btw_all_sys = bool(os.getenv("BETWEEN_ALL_GROUPS"))

within = within_sys and within_user
btw_short = btw_short_sys and btw_short_user
btw_long = btw_long_sys and btw_long_user
btw_all = btw_all_sys and btw_all_user

similarityFileType = '.npy'
if within:
    filename = 'responses_all.txt'
    line_all_groups = group_lines(filename)
    # Ensure that we have at least two line groups

    if len(line_all_groups) >= 2:
        npyFileName = "Within Pair"
        cal.compare_similarities_within(line_all_groups, npyFileName)
    else:
        print("Insufficient line groups for comparison.")
    v.visualization(npyFileName, similarityFileType)

if btw_short:
    filename = 'responses_short.txt'
    line_short_groups = group_lines(filename)
    # Ensure that we have at least two line groups

    if len(line_short_groups) >= 2:
        npyFileName = "Between Short Description"
        cal.compare_similarities_between(line_short_groups, npyFileName)
    else:
        print("Insufficient line groups for comparison.")
    v.visualization(npyFileName, similarityFileType)

if btw_long:
    filename = 'responses_long.txt'
    line_long_groups = group_lines(filename)
    # Ensure that we have at least two line groups

    if len(line_long_groups) >= 2:
        npyFileName = "Between Long Description"
        cal.compare_similarities_between(line_long_groups, npyFileName)
    else:
        print("Insufficient line groups for comparison.")
    v.visualization(npyFileName, similarityFileType)

if btw_all:
    filename = 'responses_all.txt'
    line_all_groups = group_lines(filename)
    # Ensure that we have at least two line groups
    npyFileName = "Between all Description"
    if len(line_all_groups) >= 2:
        cal.compare_similarities_between(line_all_groups, npyFileName)
    else:
        print("Insufficient line groups for comparison.")
    v.visualization(npyFileName, similarityFileType)

