"""
General utility functions for understanding the data
"""
import os
import subprocess


def getFileSizeInGB(file_list):
    """
    :param: fileList, a list of paths to file
    :returns: size of the all the files in GB
    """
    if file_list is not None:
        return sum([os.lstat(data_file).st_size
                    for data_file in file_list]) / 1e9


def getFileList(data_dir, file_format):
    return [data_file for data_file in os.listdir(data_dir)
            if data_file.endswith(file_format)]


def capture_multiline_output(command):
    try:
        return str(subprocess.check_output(command, shell=True,
                                           stderr=subprocess.STDOUT)
                   ).split('\\n')
    except:
        return ''
