import os, shutil


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


def create_file(dir_path: str, file_name: str = ""):
    assert type(dir_path) == str
    assert type(file_name) == str

    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, file_name)
