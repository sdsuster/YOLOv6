import sys
from omegaconf import OmegaConf
import os


def main():
    args = sys.argv[1:]
    assert len(args) == 1, "Need to pass dataset yaml"
    yaml_path = args[0]



    config = OmegaConf.load(yaml_path)
    n = config.nc

    hashmap = {}
    for i in range(n):
        hashmap[i] = 0
    label_path = os.path.join(config.train, "..", "labels")
    print("Indexing..")
    for file in os.listdir(label_path):
        with open(os.path.join(label_path, file), 'r') as file:
            # Iterate through each line in the file
            for line in file:
                # Strip any leading/trailing whitespace characters (like newline)
                stripped_line = line.strip()
                # Split the line by spaces
                parts = stripped_line.split(' ')
                # Get the first value
                first_value = parts[0]
                # Print or use the first value as needed
                hashmap[int(first_value)] += 1

    print(hashmap)

if __name__ == "__main__":
    main()