import sys
import os
import shutil


def chek_error(handler):
    def wrapper(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except (shutil.ReadError):
            print("Unfamiliar format. Archive, cannot be unpacked. Import an additional library.")
            
    return wrapper


def get_main_path():
    main_path = ""
    args = sys.argv
    if len(args) == 1:
        main_path = input("Enter path to your folder: ")   
    else:
        main_path = args[1]
    while True:
        if not os.path.exists(main_path):
            if main_path:
                print(f"{main_path} not exist")
            main_path = input("Enter path to your folder: ")
        else:
            if os.path.isdir(main_path):
                break
            else:
                print(f"{main_path} this is not a folder")
                main_path = ""

    return path_handler(main_path)


video_folder = ["avi", "mp4", "mov", "mkv", "gif"]
audio_folder = ["mp3", "ogg", "wav", "amr", "m4a", "wma"]
images_folder = ["jpeg", "png", "jpg", "svg"]
doc_folder = ["doc", "docx", "txt", "pdf", "xlsx", "pptx", "html", "scss", "css", "map"]
arch_folder = ["zip", "gz", "tar", "rar"]


def normalize(file):
    map = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i", "й": "y", 
    "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", 
    "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya", "і": "i", "є": "e", "ї": "i", "А": "A", 
    "Б": "B", "В": "V", "Г": "G", "Д": "D", "Е": "E", "Ё": "E", "Ж": "h", "З": "Z", "И": "I", "Й": "Y", "К": "K", "Л": "L", 
    "М": "M", "Н": "N", "О": "O", "П": "P", "Р": "R", "С": "S", "Т": "T", "У": "U", "Ф": "F", "Х": "H", "Ц": "Ts", "Ч": "Ch", 
    "Ш": "Sh", "Щ": "Sch", "Ъ": "", "Ы": "Y", "Ь": "", "Э": "E", "Ю": "Yu", "Я": "Ya", "І": "I", "Є": "E",  "Ї": "I"}
    lists = file.split(".")
    name_file = ".".join(lists[0:-1])
    new_name = ""
    for el in name_file:
        if el in map:
            new_name += map[el]
        elif (ord("A") <= ord(el) <= ord("Z")) or (ord("a") <= ord(el) <= ord("z")) or el.isdigit():
            new_name += el
        else:
            new_name += "_"

    return new_name + "." + lists[-1]


def path_handler(main_path):

    video_path = os.path.join(main_path, "video")
    if not os.path.exists(video_path):
        os.makedirs(video_path)

    audio_path = os.path.join(main_path, "audio")
    if not os.path.exists(audio_path):
        os.makedirs(audio_path)

    images_path = os.path.join(main_path, "images")
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    documents_path = os.path.join(main_path, "documents")
    if not os.path.exists(documents_path):
        os.makedirs(documents_path)

    archives_path = os.path.join(main_path, "archives")
    if not os.path.exists(archives_path):
        os.makedirs(archives_path)

    other_path = os.path.join(main_path, "other")
    if not os.path.exists(other_path):
        os.makedirs(other_path)

    return around_dir(main_path, video_path, audio_path, images_path, documents_path, archives_path, other_path)


@chek_error
def file_handler(file, file_path, main_path, video_path, audio_path, images_path, documents_path, archives_path, other_path):
    file_name_divide = normalize(file).split(".")
    file_ending = ""
    if len(file_name_divide) > 1:
        file_ending = file_name_divide[-1]
    if not file_ending.lower():
        return None
    else:
        if file_ending in video_folder:
            new_path = os.path.join(video_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(video_path, normalize(file)))
        elif file_ending in audio_folder:
            new_path = os.path.join(audio_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(audio_path, normalize(file)))
        elif file_ending in images_folder:
            new_path = os.path.join(images_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(images_path, normalize(file)))
        elif file_ending in doc_folder:
            new_path = os.path.join(documents_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(documents_path, normalize(file)))
        elif file_ending in arch_folder:
            new_path = os.path.join(archives_path, file)
            shutil.unpack_archive(shutil.move(file_path, new_path), os.path.join(archives_path, normalize(file).rstrip(file_ending)))
            os.rename(os.path.join(archives_path, file), os.path.join(archives_path, normalize(file)), )
        else:
            new_path = os.path.join(other_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(other_path, normalize(file)))
        
    return None


def del_empty_dirs(main_path):
    for dir in os.listdir(main_path):
        dirs_path = os.path.join(main_path, dir)
        if os.path.isdir(dirs_path):
            del_empty_dirs(dirs_path)
            if not os.listdir(dirs_path):
                os.rmdir(dirs_path)

    return None


def around_dir(main_path, video_path, audio_path, images_path, documents_path, archives_path, other_path):
    files = os.listdir(main_path)
    for file in files:
        file_path = os.path.join(main_path, file)
        if os.path.isfile(file_path):
            file_handler(file, file_path, main_path, video_path, audio_path, images_path, documents_path, archives_path, other_path)
        else:
            around_dir(file_path, video_path, audio_path, images_path, documents_path, archives_path, other_path)

    return del_empty_dirs(main_path) 
            

if __name__ == "__main__":
    get_main_path()