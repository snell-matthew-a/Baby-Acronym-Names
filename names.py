import os
import pandas as pd

from itertools import product

# names folder with census data
names_folder = os.path.join(os.path.dirname(__file__), "names")
names_file = os.path.join(os.path.dirname(__file__), "names", "tally_names.csv")


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
        print(f"Processed file: {filename}", end="\r")

    result.to_csv("names/tally_names.csv", index=False)
    print("Data successfully saved to 'tally_names.csv'")


def validate_names(baby_gender, source_names, names_file=names_file, save=True):
    """
    Validates baby names against a set of source names and saves matching names to a CSV file.

    :param names_folder: Folder containing baby name data files
    :param baby_gender: Gender of the baby names to validate (e.g., "F" for female)
    :param source_names: List of source names to match against
    :param save: Whether to save the matching names to a CSV file (default: True)
    """
    match_set = create_matching_name_set(source_names)

    df = pd.read_csv(names_file, sep=",", header=0)
    df = df[df["gender"] == baby_gender]
    df = df[df["name"].apply(lambda x: len(x) == len(source_names))]
    df = df[df["name"].apply(lambda x: "".join(sorted(x.lower())) in match_set)]
    df = df.drop(columns="gender")
    df = df.sort_values(by="count", ascending=False).reset_index(drop=True)

    if save:
        df.to_csv("matching_names.csv", index=False)
        print("Matching names successfully saved to 'matching_names.csv'")

    return df


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


def get_gender(prompt="Enter the baby's gender (M/F), or Q to quit: "):
    # Prompt the user to input the baby's gender
    while True:
        value = input(prompt).strip()
        if value in ["M", "F"]:
            return value
        if value == "Q":
            print("Exiting the program.")
            exit()
        print("Invalid input. Please enter 'M' for male or 'F' for female.")


def get_names(prompt="Enter the source names (comma-separated): "):
    # Prompt the user to input the source names
    while True:
        value = input(prompt).strip()
        if value:
            source_names = [name.strip() for name in value.split(",")]
            return source_names
        print("Invalid input. Please enter at least one name.")


def get_save(prompt="Do you want to save the matching names to a CSV file? (Y/N): "):
    # Prompt the user to decide whether to save the matching names
    while True:
        value = input(prompt).strip().upper()
        if value in ["Y", "N"]:
            return value == "Y"
        print("Invalid input. Please enter 'Y' for yes or 'N' for no.")


if __name__ == "__main__":
    if not os.path.exists(names_file):
        print(f"Tallying names from source files...")
        tally_names(names_folder)

    # Prompt the user for baby gender, source names, and whether to save the results
    baby_gender = get_gender()
    source_names = get_names()
    save = get_save()

    # Validate the names and store in a dataframe
    names = validate_names(baby_gender, source_names, save=save)

    # Print the matching names    print("\nMatching Names:")
    print(f"{len(names)} matching names found, here are the top 100:")
    with pd.option_context("display.max_rows", 100, "display.max_columns", None):
        print(names.head(100))
