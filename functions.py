import yaml
import time
import re


# Function to find next empty row
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return int(len(str_list)+1)

def salutations(version):
    print(f"Welcome to Courier!\nVersion {version}\n")
    print("Courier is preparing your data..")

    time.sleep(2)


def remove_whitespace(data):
    return re.sub("\s", "", data)

def remove_special(data):
    return re.sub("[\!\@\#\$\%\^\&\*\(\)\[\]\{\}]", "", data)


# Function to load config file
def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def write_yaml(data, file_path):
    stream = open(file_path, "w")
    yaml.dump(data, stream)