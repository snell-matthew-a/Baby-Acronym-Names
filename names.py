import csv
import os
import pandas as pd
import pickle

# Read all txt files from the names folder
names_folder = os.path.join(os.path.dirname(__file__), 'names')
baby_names = set()

for filename in os.listdir(names_folder):
    if filename.endswith('.txt'):
        filepath = os.path.join(names_folder, filename)
        df = pd.read_csv(filepath, sep=',', header=None)
        for row in df.itertuples(index=False):
            # grabbing all female names that are 5 letters long
            if row[1] == 'F' and len(row[0]) == 5:
                baby_names.add(row[0])

# Write the list of baby names to a pickle file
os.makedirs('names', exist_ok=True)
with open(os.path.join('names', 'female_baby_names.pkl'), 'wb') as f:
    pickle.dump(baby_names, f)

# Generate a list of all possible combinations of 5 letters from the names list
from itertools import product

alison = ['a', 'l', 'i', 's', 'o', 'n']
phillip = ['p', 'h', 'i', 'l', 'l', 'i', 'p']
michael = ['m', 'i', 'c', 'h', 'a', 'e', 'l']
ginny = ['g', 'i', 'n', 'n', 'y']
janet = ['j', 'a', 'n', 'e', 't']

string_matches = list(product(alison, phillip, michael, ginny, janet))

for n in range(len(string_matches)):
    string_matches[n] = ''.join(sorted(string_matches[n]))

# Check if any of the combinations match a name in the baby names list
with open(os.path.join('names', 'female_baby_names.pkl'), 'rb') as f:
    baby_names = pickle.load(f)

matching_names = list()
for name in baby_names:
    if ''.join(sorted(name.lower())) in string_matches:
        matching_names.append(name)

matching_names.sort()
matching_names = [[item] for item in matching_names]

def save_list_to_csv(data_list, filename):
    """
    Saves a list (1D or 2D) to a CSV file.
    
    :param data_list: List of values or list of lists
    :param filename: Output CSV file name
    """
    # Validate input type
    if not isinstance(data_list, list):
        raise TypeError("data_list must be a list.")
    if not filename.lower().endswith(".csv"):
        raise ValueError("Filename must have a .csv extension.")

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # If it's a list of lists, write rows directly
            if all(isinstance(row, (list, tuple)) for row in data_list):
                writer.writerows(data_list)
            else:
                # Convert 1D list to a single row
                writer.writerow(data_list)

        print(f"Data successfully saved to '{filename}'")

    except OSError as e:
        print(f"Error writing to file: {e}")

save_list_to_csv(matching_names, "matching_names.csv")