import csv
import os
import pandas as pd

from itertools import product

# Set the baby gender and source names
baby_gender = "F"
source_names = ["alison", "phillip", "michael", "ginny", "janet"]

# names folder with census data
names_folder = os.path.join(os.path.dirname(__file__), "names")


def validate_names(names_folder, baby_gender, source_names):
    """
    Validates baby names against a set of source names and saves matching names to a CSV file.

    :param names_folder: Folder containing baby name data files
    :param baby_gender: Gender of the baby names to validate (e.g., "F" for female)
    :param source_names: List of source names to match against
    """
    match_set = create_matching_name_set(source_names)

    baby_names = dict()
    for filename in os.listdir(names_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(names_folder, filename)
            df = pd.read_csv(filepath, sep=",", header=None)
            for row in df.itertuples(index=False):
                if row[1] == baby_gender and len(row[0]) == len(
                    source_names
                ):  # First check name gender and length
                    if (
                        "".join(sorted(row[0].lower())) in match_set
                    ):  # Then check it against all the combinations
                        baby_names[row[0]] = baby_names.get(row[0], 0) + row[2]
        print(f"Processed file: {filename}")

    baby_names = sorted(baby_names.items(), key=lambda x: x[1], reverse=True)
    baby_names = [[item[0], item[1]] for item in baby_names]
    baby_names.insert(0, ["Name", "Count"])  # Add header row

    save_list_to_csv(baby_names, "matching_names.csv")


def create_matching_name_set(source_names):
    """
    Creates a set of all possible combinations of letters from the source names.

    :param source_names: List of source names
    :return: Set of unique combinations of letters
    """
    # Generate a list of unique letters from each name
    unique_letters = [set(name.lower()) for name in source_names]

    # Generate all possible combinations of letters (one from each name)
    string_matches = list(product(*unique_letters))

    # Sort and join the letters to create a standardized format
    sorted_combinations = {
        "".join(sorted(combination)) for combination in string_matches
    }

    return sorted_combinations


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


validate_names(names_folder, baby_gender, source_names)
