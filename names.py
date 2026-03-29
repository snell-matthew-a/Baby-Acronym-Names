import os
import pandas as pd

from itertools import product

# Set the baby gender and source names
baby_gender = "F"
source_names = ["alison", "phillip", "michael", "ginny", "janet"]

# names folder with census data
names_folder = os.path.join(os.path.dirname(__file__), "names")


def tally_names(names_folder):
    """
    Reads all of the baby names and combines the totals for each name across all years.
    Writes out one csv of boy names and one of girl names

    :param names_folder: Path to the folder containing the baby name data files
    """
    colNames = ["name", "gender", "count"]
    result = pd.DataFrame(columns=colNames)
    for filename in os.listdir(names_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(names_folder, filename)
            df2 = pd.read_csv(filepath, sep=",", header=None, names=colNames)
            result = pd.concat([result, df2], ignore_index=True)
            result = result.groupby(["name", "gender"]).sum().reset_index()
        print(f"Processed file: {filename}")

    result.to_csv("tally_names.csv", index=False)
    print("Data successfully saved to 'tally_names.csv'")


def validate_names(names_file, baby_gender, source_names):
    """
    Validates baby names against a set of source names and saves matching names to a CSV file.

    :param names_folder: Folder containing baby name data files
    :param baby_gender: Gender of the baby names to validate (e.g., "F" for female)
    :param source_names: List of source names to match against
    """
    match_set = create_matching_name_set(source_names)

    df = pd.read_csv(names_file, sep=",", header=0)
    df = df[df["gender"] == baby_gender]
    df = df[df["name"].apply(lambda x: len(x) == len(source_names))]
    df = df[df["name"].apply(lambda x: "".join(sorted(x.lower())) in match_set)]
    df = df.drop(columns="gender")
    df = df.sort_values(by="count", ascending=False).reset_index(drop=True)

    df.to_csv("matching_names.csv", index=False)
    print("Matching names successfully saved to 'matching_names.csv'")


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


validate_names("tally_names.csv", baby_gender, source_names)
