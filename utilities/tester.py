import sys
import json

changed_directories = set(sys.argv[1].split(' '))

with open("lambda_layers_map.json", 'r') as infile:
    lambda_layers_map = json.load(infile)

with open("layers_to_build.txt", 'w') as outfile:
    for layer, dirs in lambda_layers_map.items():
        if any(dir in changed_directories for dir in dirs):
            outfile.write(f"{layer} {' '.join(dirs)}\n") # write layer and dirs in a space-separated line