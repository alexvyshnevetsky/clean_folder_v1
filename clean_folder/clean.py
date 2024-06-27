'''
This program is used to automatically sort files in a user-defined directory.

Files will be sorted as follows:
images ('JPEG', 'PNG', 'JPG', 'SVG')
documents ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX' )
audio ('MP3', 'OGG', 'WAV', 'AMR')
video ('AVI', 'MP4', 'MOV', 'MKV')
archives ('ZIP', 'GZ', 'TAR')
python ('.py')
other 

To start the program, write the address of the directory to be sorted in the command line.

Example of a line to run the program: python .\python_sort.py -s 'C:/Folder/Next_folder/Destination_Folder'

'''

import argparse
from pathlib import Path
import shutil
import re
import os
from datetime import datetime


parser = argparse.ArgumentParser(description='Sort data in folder')
parser.add_argument('--source', '-s', required=True, help='Write destination in format \'C:/Folder/Next_folder/Destination_Folder\'')
args = vars(parser.parse_args())
sourse = args.get('source')

DESTINATION = Path(sourse)


directive_extension = {'images':['.jpeg', '.png', '.jpg', '.svg'],
                       'documents':['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'], 
                       'audio':['.MP3', '.OGG', '.WAV', '.AMR'],
                       'video':['.avi', '.mp4', '.mov', '.mkv'],
                       'archives':['.zip', '.gz', '.tar'],
                       'python':['.py'],
                       'other': []
                       }


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
    
for cyrilic, trans in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrilic)] = trans
    TRANS[ord(cyrilic.upper())] = trans.upper()


def normalize(name: str):
    translate_name = name.translate(TRANS)
    translate_name = re.sub(r'\W', '_', translate_name)
    return translate_name


def create_new_folder(file: Path):
    for key in directive_extension.keys():
        new_folder = file / key
        new_folder.mkdir(exist_ok=True, parents=True)


def read_folder(path: Path): 
    for element in path.iterdir():
        if element.is_dir():
            read_folder(element)
        else:
            move_elements(element)    


def log_message(title, messege, path):

    log_p = path / 'logs.txt'
    encoding = 'utf-8'
    with open(log_p, 'a+', encoding=encoding, errors="replace") as logs:
        now = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        logs.write(f'|{title} - {now}\n|{messege}\n')


def move_elements(file: Path):
    if file.is_file():
        ext_file = file.suffix.lower()
        print(ext_file)

        for folder, extensions in directive_extension.items():
            if ext_file in extensions:

                global DESTINATION
                dest_dir = DESTINATION / folder

                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_file = dest_dir / file.name
            
                messege_d = f"Moving {file} to {dest_file}"
                
                print(f'in process: {messege_d}')
                shutil.move(str(file), str(dest_file))
                log_message('Moving', messege_d, DESTINATION)

                # rename
                nn = file.name.split('.')
                convert_name = normalize(nn[0]) + '.' + nn[1]
                new_file_dest = dest_dir / convert_name

                messege_r = f"Renaming {dest_file} to {new_file_dest}"
                print(f'in process: {messege_r}')
                shutil.move(str(dest_file), str(new_file_dest))
                log_message('Rename', messege_r, DESTINATION)
                break
        else:
            dest_dir = file.parent / 'other'
            dest_file = dest_dir / file.name
            dest_dir.mkdir(parents=True, exist_ok=True)

            messege_m = f"Moving {file} to {dest_file}"
            print(f'in process: {messege_m}')
            shutil.move(str(file), str(dest_file))
            log_message('Move', messege_m, DESTINATION)

            #  rename 
            nn = file.name.split('.')
            convert_name = normalize(nn[0]) + '.' + nn[1]
            new_file_dest = dest_dir / convert_name
    
            messege_rm = f"Renaming {dest_file} to {new_file_dest}"
            print(f'in process: {messege_rm}')
            shutil.move(str(dest_file), str(new_file_dest))
            log_message('Rename', messege_rm, DESTINATION)


def unpack_archive(directory: Path):

    for name in os.listdir(directory):

        try:
            messege_a = f"Archive {name} file unpacked successfully."
            print(f'in unpacked process: {name}')
            new_folder = directory / name
            new_folder_str = str(new_folder)
            new_folder_str_without_extension = new_folder_str.rsplit('.', 1)[0]
            shutil.unpack_archive(directory / name, new_folder_str_without_extension )  
            log_message('Unpacked', messege_a, new_folder_str_without_extension)
        except:
            print(f'{name} Not Archive or broken')
            
        messege_d = f"Archive {name} file deleted successfully."
        print(f'in delete process: {name}')
        os.remove(directory / name)
        log_message('Delete Archive', messege_d, directory)


def dell_empty(directory: Path):

    for name in os.listdir(directory):
        dell_dir = directory / name
        if name not in directive_extension.keys():
            try:
                messege_d = f"Folder {name} deleted successfully."
                dell_dir.rmdir()
                print(messege_d)
                log_message('Delete folder', messege_d, directory)             
            except:
                messege_not = f"Folder {name} doesn't exist or full"
                print(messege_not)
                log_message('Repor: folder doesn\'t exist or full', messege_not, directory)  


def main():
    while True:

        create_empty = input('Do you want to create empty folders if there are no files of the corresponding type in the sorted directory? Enter Y or N:')

        if create_empty.lower() == 'y':
            print("yes")

            read_folder(DESTINATION) 
            arhive_dir = DESTINATION / 'archives'
            unpack_archive(arhive_dir)
            dell_empty(DESTINATION)
            create_new_folder(DESTINATION)
            break

        elif create_empty.lower() == 'n':
            print("no")

            read_folder(DESTINATION) 
            arhive_dir = DESTINATION / 'archives'
            unpack_archive(arhive_dir)
            dell_empty(DESTINATION)
            break

        else:
            print("wrong input")


if __name__ == "__main__":
    main()