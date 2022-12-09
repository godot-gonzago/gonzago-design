import os
import yaml
import hashlib
from pathlib import PurePath

source_path = PurePath(__file__).parent.joinpath("../source")

# A utility function that can be used in your code
def compute_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(65536): # 64kb chunks
            md5.update(chunk)
    return md5.hexdigest()

if __name__ == '__main__':
    print('Gathering files')
    print('===============')

    files_dict = {}
    for (root, dirs, files) in os.walk(source_path):
        for file in files:
            #file.endswith()
            file_path = source_path.joinpath(root, file)
            #print(f'Suffix: {file_path.suffix}')
            rel_path = str(file_path.relative_to(source_path))

            statinfo = os.stat(file_path)
            files_dict[rel_path] = {
                "size": statinfo.st_size,
                "lmod": statinfo.st_mtime,
                "hash": compute_md5(file_path)
            }

    print(yaml.dump(files_dict))

    #for key in files_dict:
    #    print(key)
    #    print(files_dict[key])
