import os


def get_index(i):
    index = 0
    while True:
        if not os.path.isdir(f'data/{i}/{index}_num'):
            break
        else:
            index += 1
    return index
