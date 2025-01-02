from genericpath import isdir
import os
import shutil


def delete_folder(path):
    if os.path.isfile(path):
        os.remove(path)
        return
    if len(os.listdir(path)) > 0:
        for item in os.listdir(path):
            delete_folder(path + f"/{item}")
    if os.path.isdir(path):
        os.removedirs(path)
    return


def copy_folder(source, dest):
    if len(os.listdir(source)) > 0:
        for item in os.listdir(source):
            if os.path.isfile(source + f"/{item}"):
                shutil.copy(source + f"/{item}", dest + f"/{item}")
            else:
                os.mkdir(dest + f"/{item}")
                copy_folder(source + f"/{item}", dest + f"/{item}")


def main():
    cwd = os.getcwd()
    public_directory = cwd + "/public"
    static_directory = cwd + "/static"
    if os.path.isdir(public_directory):
        delete_folder(public_directory)
    os.makedirs("public")
    copy_folder(static_directory, public_directory)


if __name__ == "__main__":
    main()
