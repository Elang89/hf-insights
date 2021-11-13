import shutil

from glob import glob
from pprint import pprint
from multiprocessing import Process
from uuid import uuid4



def copy_files(arrow_paths):
    for path in arrow_paths: 
        path_splits = path.split("/")
        current_file = path_splits[-1]
        config = path_splits[-4]
        
        filename = f"{uuid4()}-{config}-{current_file}"
        
        current_path = f"comparisons/{filename}"
        
        print(filename)
        
        shutil.copyfile(path, current_path)


def main() -> None: 
    arrows = "/mnt/e/HFDatasets/**/*train*.arrow"
    arrow_paths = glob(arrows, recursive=True)[760:]

    
    arrow_paths = [arrow_paths[x:x + 80] for x in range(0, len(arrow_paths), 80)]
    
    producers = [Process(target=copy_files, args=(arrow_paths[x],)) for x in range(0, len(arrow_paths))]
    
    for producer in producers:
        producer.start()
    


if __name__ == "__main__":
    main()