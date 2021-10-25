import json

from glob import glob
from pprint import pprint
from multiprocessing import Process
from typing import Dict, List, Union, Tuple
from csv import DictWriter

#TODO: features and reviews

def extract_splits(json_data: Dict[str, str]) -> Dict[str, str]: 
    train = json_data.get("train", False)
    test = json_data.get("test", False)
    validation = json_data.get("validation", False)
    data = {}

    if train:
        data.update({"has_train_split": 1})
    else:
        data.update({"has_train_split": 0})
    
    if test: 
        data.update({"has_test_split": 1})
    else:
        data.update({"has_test_split": 0})

    if validation: 
        data.update({"has_validation_split": 1})
    else: 
        data.update({"has_validation_split": 0})
        

    return data


def extract_citation_information(json_data: str):
    pass


def check_versioning(json_data: Union[dict, str]) -> str:
    version = json_data

    if isinstance(json_data, str): 
        return version
    elif isinstance(version, dict):
        version_str = version.get("version_str")
        return version_str


def analyze_jsons() -> None: 

    field_names = [
            "builder_name", 
            "config_name",
            "is_config",
            "description_size",
            "download_size(bytes)", 
            "has_homepage",
            "version",
            "has_license",
            "has_train_split",
            "has_test_split",
            "has_validation_split"
    ]
    result_file = open("data.csv", "w")

    writer = DictWriter(result_file, fieldnames=field_names)
    writer.writeheader()

    with open("jsons.txt", "r") as file:
        results = file.readlines()

        for result in results:
            json_file_path = result.strip("\n")
            with open(json_file_path, "r") as jsonfile:
                loaded_json = json.load(jsonfile)
                description_size = len(loaded_json["description"])
                has_version = check_versioning(loaded_json["version"])
                splits = extract_splits(loaded_json["splits"])

                row = {
                    "builder_name": loaded_json.get("builder_name"),
                    "config_name": loaded_json.get("config_name"), 
                    "is_config": 1 if loaded_json.get("config_name") != "default" else 0,
                    "description_size": description_size,
                    "download_size(bytes)": loaded_json.get("download_size"),
                    "has_homepage": 1 if loaded_json.get("homepage") else 0,
                    "version": has_version,
                    "has_license": 1 if loaded_json.get("license") else 0,
                    "has_train_split": splits.get("has_train_split"),
                    "has_test_split": splits.get("has_test_split"),
                    "has_validation_split": splits.get("has_validation_split")
                }

                writer.writerow(row)
    result_file.close()




def main() -> None: 
    # jsons = "/mnt/e/Data/HFDatasets/**/dataset_info.json"
    # arrows = "/mnt/e/Data/HFDatasets/**/*.arrow"

    # arrow_results = glob(arrows, recursive=True)
    # json_results = glob(jsons, recursive=True)

    # with open("arrows.txt", "w") as file:
    #     for x in arrow_results:
    #         str_to_write = f"{x}\n"
    #         file.write(str_to_write)

    # with open("jsons.txt", "w") as file: 
    #     for y in json_results:
    #         str_to_write = f"{y}\n"
    #         file.write(str_to_write)

    analyze_jsons()



if __name__ == "__main__":
    main()