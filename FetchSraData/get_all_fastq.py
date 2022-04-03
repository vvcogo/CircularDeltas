import sys
import os
import subprocess

def main():
    primary_path = sys.argv[1]
    size = sys.argv[2]
    if  not os.path.exists(primary_path):
        print("Error, try [directory_name] [size_of_file]")

    for platform_dir in os.listdir(primary_path):
        if platform_dir != "changes_models_dict.txt" and platform_dir != "SraRunInfoCount.csv" and platform_dir != "SraRunInfoReturn.csv":
            platform_path = os.path.join(primary_path,platform_dir)
            for model_file in os.listdir(platform_path):
                path_model = os.path.join(platform_path,model_file)
                subprocess.call(["./methodology_script.sh",path_model,size])

                #subprocess.call("./methodology_script.sh %s %s" %(model_file, size))



if __name__ == "__main__":
    main()
