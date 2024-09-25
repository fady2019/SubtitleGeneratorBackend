import os, shutil


def get_file_name(file_path: str):
    return os.path.splitext(os.path.basename(file_path))[0]


def delete_file(file_path: str | None):
    if not file_path or not os.path.exists(file_path):
        return

    os.remove(file_path)


def delete_dir(dir_path: str | None, only_if_empty=True):
    if not dir_path or not os.path.exists(dir_path):
        return

    if only_if_empty:
        os.rmdir(dir_path)
    else:
        shutil.rmtree(dir_path)


def add_suffix_to_file_name(file_path: str, suffix: str, sep: str = "__"):
    dirname = os.path.dirname(file_path)
    filename, ext = os.path.splitext(os.path.basename(file_path))
    new_path = os.path.join(dirname, f"{filename}{sep}{suffix}{ext}")
    return new_path
