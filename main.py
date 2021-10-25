import json

from glob import glob
from pprint import pprint
from multiprocessing import Process
from typing import Dict, List
from csv import DictWriter


def analyze_jsons() -> None: 

    field_names = [
            "builder_name", 
            "config_name",
            "is_config",
            "description_size",
            "download_size", 
            "has_homepage",
            "has_version",
            "has_license",
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

                row = {
                    "builder_name": loaded_json.get("builder_name"),
                    "config_name": loaded_json.get("config_name"), 
                    "is_config": 1 if loaded_json.get("config_name") != "default" else 0,
                    "description_size": description_size,
                    "download_size": loaded_json.get("download_size"),
                    "has_homepage": 1 if loaded_json.get("homepage") else 0,
                    "has_version": 1 if loaded_json.get("version") else 0,
                    "has_license": 1 if loaded_json.get("license") else 0,
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