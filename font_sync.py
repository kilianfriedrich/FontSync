# Google Fonts Sync
# by Kilian Friedrich
#
# 2019-05-04
#
# font_sync.py:
#
# This script is the core of this project and will actually sync the fonts with help of the other scripts when it's
# called via the command line. Too, it can be called from outside (e.g. from font_sync_gui.py) so that the sync(...)
# function can be used in other scenarios.
#
# Copyright after CC BY-NC-SA 4.0
# You are free to:
#   SHARE - copy and redistribute the material in any medium or format
#   ADAPT - remix, transform, and build upon the material
# Under the following terms:
#   ATTRIBUTION - You must give appropriate credit, provide a link to the license, and indicate if changes were made.
#                 You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or
#                 your use.
#   NONCOMMERCIAL - You may not use the material for commercial purposes.
#   SHAREALIKE - If you remix, transform, or build upon the material, you must distribute your contributions under the
#                same license as the original.
# Follow https://creativecommons.org/licenses/by-nc-sa/4.0/ for more information.

from urllib import request as internet
from glob import glob as get_files
from zipfile import ZipFile as ZIPFile
from os import makedirs as make_dir, remove as remove_file

from logging import log
from filter.gfonts_filter import filter_fonts
from gfonts_values import validate
from args import args_interface as args

outputdir = '/Library/Fonts' if sys.platform.lower().startswith('darwin') \
    else 'C:/Windows/Fonts' if sys.platform.lower().startswith('win') else '/usr/share/fonts'


# this script takes filter as arguments, checks them and syncs fonts
def sync(_filter=None, fonts=None, gui=None, folder=outputdir):
    fonts = fonts if fonts is not None else filter_fonts(*_filter)

    # create target folder if it doesn't exist
    make_dir(folder, exist_ok=True)

    # get all filtered fonts and iterate through them
    for i in range(0, len(fonts)):

        from gui.main_frame import cancel
        if cancel:
            break

        font_family = fonts[i]

        if gui is not None:
            gui[0].set(i)

        # get target directory / target file
        dir_name = font_family.family_name.replace(' ', '')
        dir_path = (folder + dir_name) if folder.endswith('/') or folder.endswith('\\') else (folder + '/' + dir_name)
        zip_path = dir_path + '.zip'  # fonts will be downloaded as .zip and extracted

        # get download URL
        download_name = font_family.family_name.replace(' ', '+')
        download_url = 'https://fonts.google.com/download?family={}'.format(download_name)

        log(font_family.family_name + ' - Downloading ' + font_family.family_name + ' from ' + download_url + ' to '
            + zip_path + '...', lbl=gui)

        open(zip_path, 'x')

        internet.urlretrieve(download_url, zip_path)  # retrieve zip file
        zip_file = ZIPFile(zip_path, 'r')  # open zip file

        log(font_family.family_name + ' - Clearing ' + dir_path + '/*...', lbl=gui)

        make_dir(dir_path, exist_ok=True)  # create target path if not existing

        # clear target folder if it already existed
        files = get_files(dir_path + '/*')
        for f in files:
            remove_file(f)

        log(font_family.family_name + ' - Extracting ' + zip_path + '...', lbl=gui)

        zip_file.extractall(dir_path)  # extract files

        # delete non-ttf files
        files = get_files(dir_path + '/*')
        for f in files:

            if not f.endswith('.ttf'):
                remove_file(f)

        log(font_family.family_name + ' - Deleting ' + zip_path + '...', lbl=gui)

        remove_file(zip_path)  # remove zip file after extraction


# just execute if this script is called via command line directly! (not via font_sync_gui.py)
if __name__ == '__main__':
    # sync with command line arguments
    sync(_filter=validate(args.get_list('category'), args.get_str('subset'), args.get_int('stylecount'),
                          args.get_int('thickness'), args.get_int('slant'), args.get_int('width')))
