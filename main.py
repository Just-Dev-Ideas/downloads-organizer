from sys import platform, argv
from enum import Enum
import getpass
import os
import shutil

# The types of files categorized in their own folder
Images     = Enum('Images', 'jpg jpeg png svg gif bmp')
Videos     = Enum('Videos', 'mp4 mkv mov avi wmv mpeg flv')
Archives   = Enum('Archives', 'zip 7z gz xz rar iso bz2')
Documents  = Enum('Documents', 'pdf doc docx ppt pptx xls xlsx rtf odt csv txt epub mobi ')
Installers = Enum('Installers', 'torrent sh deb exe appimage Appimage AppImage')
Others     = Enum('Others', '')

# The created categories must be added to the type_list variable
#
# !IMPORTANT: The last folder will be the backup one, in which all the files
# that are not recognized will be moved to. The backup folder must always be
# placed last in this list
type_list = [Images, Videos, Archives, Documents, Installers, Others]

def organize_files(path):
    print("==> Organizing files in: {}".format(path))

    # Find all the files in the searched path (this will exclude folders).
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    file_type_variation_list = []
    filetype_folder_dict = {}

    for file in files:
        # Get the file extension
        filetype = file.split('.')[-1]

        # Find the suitable folder for the file
        for type in type_list:
            if (filetype in type._member_names_):
                break

        # Find the folder or create it
        folder_name = os.path.join(path, type.__name__)
        if os.path.isdir(folder_name) == False:
            os.mkdir(folder_name)

        # Move file to folder
        src_path = os.path.join(path, file)
        dest_path = folder_name
        shutil.move(src_path, dest_path)

def get_path():
    if platform == "linux" or platform == "linux2":
        print("==> Running on linux")
        path = '/home/{}/Downloads'.format(getpass.getuser())
    elif platform == "darwin":
        print("==> Running on mac")
        path = 'Users/{}/Downloads'.format(getpass.getuser())
    elif platform == "win32":
        print("==> Running on windows")
        path = 'C:\\Users\\{}\\Downloads'.format(getpass.getuser())
    else:
        print("==> Could not determine platform.")
        path = None

    return path

def main():
    print("==> Getting folder path.")

    # If an argument is given use that as the path, otherwise check the OS and
    # try to get the correct path
    if len(argv) == 1:
        path = get_path()
    elif len(argv) == 2:
        print("==> Using path provided as argument.")
        path = argv[1]
    else:
        print("==> Too many arguments provided.")
        path = None

    # If a path is found, organize the files in that path
    if path is not None:
        organize_files(path)
        print("==> Success.")
    else:
        print("==> Closing script.")

if __name__ == "__main__":
    main()
