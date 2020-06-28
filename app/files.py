from pathlib import Path

dry_run = True

def scan_dir(dir_full_path):
    p = Path(dir_full_path)
    if not p.exists():
        return [],[]
    if not p.is_dir():
        return [],[]
    files_in_path = (entry for entry in p.iterdir() if entry.is_file())
    subdirs_in_path = (entry for entry in p.iterdir() if entry.is_dir())
    return sorted(files_in_path), sorted(subdirs_in_path)

def rename_files_remove_suffix(file_full_path, suffix, file_suffixes):
    for file_suffix in file_suffixes:
        rename_file_remove_suffix(file_full_path, suffix, file_suffix)


def remove_srt_files(dir_full_path):
    recursive_remove_files_with_suffix(dir_full_path, ".srt")

def recursive_remove_files_with_suffix(dir_full_path, suffix):
    files, subdirs = scan_dir(dir_full_path)
    for name in files:
        f = Path(name)
        if f.is_file() and f.name.endswith(suffix):
            print("remove file ", f.absolute())
            if not dry_run:
                f.unlink()  ## DELETE the file!!
    for dir in subdirs:
        recursive_remove_files_with_suffix(dir, suffix)


def rename_files_remove_suffix(dir_full_path, suffix, file_suffix):
    files, subdirs = scan_dir(dir_full_path)
    for name in files:
        rename_file_remove_suffix(Path(name).absolute(), suffix, file_suffix)
    for subdir in subdirs:
        rename_files_remove_suffix(Path(subdir).absolute(), suffix, file_suffix)

def rename_file_remove_suffix(file_full_path, suffix, file_suffix):
    p = Path(file_full_path)
    if p.is_file():
        current_name = p.name
        if current_name.endswith(file_suffix):
            print("file name:", p.absolute())
            print("current name:", current_name)
            curr_name = current_name[:-len(file_suffix)]
            if (curr_name.endswith(suffix)):
                desired_name = curr_name[:-len(suffix)] + file_suffix
                print("desired name:", desired_name)
                desired_full_path = str(p.parent.absolute()) + "/" + desired_name
                print("desired name full path:", desired_full_path)
                if not dry_run:
                    p.rename(desired_full_path)


'''compare list of dirs and files to same list in Google Drive'''


if __name__ == '__main__':
    dir = '/home/evyatar/Downloads/video/0ready for upload/ek3074 - Data/Udemy - AWS Database RDS DynamoDB Neptune (Updated) [900MB]'
    #dir = '/home/evyatar/Downloads/video/0ready for upload/ek3073 - Python/Udemy - Real time Data Analysis and Visualization in Python [680MB]'
    remove_srt_files(dir)

    # dir = '/home/evyatar/Downloads/video/0ready for upload/ek3074 - Data/Udemy - AWS Database RDS DynamoDB Neptune (Updated) [900MB]/1. Introduction to AWS'
    rename_files_remove_suffix(dir, '--- [ FreeCourseWeb.com ] ---', ".mp4")
    #rename_files_remove_suffix(dir, '--- [ FreeCourseWeb.com ] ---', ".srt")

