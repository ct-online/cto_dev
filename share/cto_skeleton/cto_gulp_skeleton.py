#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    File name: cto_gulp_skeleton.py
    Author: Dennis Brinkrolf
    Date created: 3/20/2020
    Date last modified: 3/21/2020
    Python Version: 3.6.9
"""
import argparse
import errno
import os
import shutil
import traceback
from pathlib import Path


def read_file(file_path) -> list:
    """
    This function read a file by a given file path and return the content.
    :param file_path:
    :return:
    """

    fp = open(file_path, 'r', encoding="utf-8")
    result = fp.readlines()
    fp.close()
    return result


def write_file(file_path, content: list) -> None:
    """
    This function write a file by a given file path and content.
    :param file_path:
    :param content:
    :return
    """

    fp = open(file_path, "w")
    fp.writelines(content)
    fp.close()


def upper_at_positon(my_string: str, n: int) -> str:
    """
    This function changes the character at position n to an uppercase letter and returns the changed string as result.
    :param my_string:
    :param n:
    :return:
    """

    tmp = list(my_string)
    tmp[n] = tmp[n].upper()
    return ''.join(tmp)


def replace_in_file(file_content: list, replace_old: str, replace_new: str) -> list:
    """
    This function replace strings in a whole file line by line and return the changed file as list.
    :param file_content: content of the file.
    :param replace_old: search string.
    :param replace_new: replace string.
    :return: content of the new file.
    """

    result = []

    for line in file_content:
        result.append(line.replace(replace_old, replace_new))

    return result


def copy_directory(src, dst):
    """
    # https://stackoverflow.com/questions/1994488/copy-file-or-directories-recursively-in-python
    :param src:
    :param dst:
    :return:
    """

    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


def list_files(dst_directory: str) -> list:
    """
    This function return all files except for "package.json" in a given directory as a list of Path objects.
    :param dst_directory:
    :return: list of Path objects
    """

    result = []

    for elem in Path(dst_directory).rglob("*.*"):
        if elem.name == "package.json":
            continue
        result.append(elem)
    return result


def change_project_file(dst_directory: str, module_name: str, version: str, description: str) -> None:
    """
    This function change the content of the package.json template file using the given information of the module.
    :param dst_directory:
    :param module_name:
    :param version:
    :param description:
    :return:
    """

    result = []

    package_file = dst_directory + os.sep + "package.json"
    package_content = read_file(package_file)
    for line in package_content:
        result.append(line.replace("{name}", module_name).
                      replace("{version}", version).replace("{desc}", description))

    write_file(package_file, result)


def rename_files(dst_directory: str, plugin_name: str) -> None:
    """
    This function rename all template file names to the given plugin name.
    :param dst_directory:
    :param plugin_name:
    :return:
    """

    files = list_files(dst_directory)
    for file in files:
        if "template" in file.name:
            src_path = str(file)
            dst_path = src_path.replace("template", plugin_name)
            os.rename(src_path, dst_path)


def change_file_content(files: list, plugin_name: str) -> None:
    """
    This function replace the content of the template files using the given plugin_name and saves them.
    :param files:
    :param plugin_name:
    :return:
    """

    for file in files:
        file_content = read_file(file)

        if file.name == "t_" + plugin_name + ".js" or (
                file.name == plugin_name.lower() + ".js" and file.parts[-2] == "common"):
            project_name_upper = upper_at_positon(plugin_name, 0)
            file_content = replace_in_file(file_content, "{template_upper}", project_name_upper)
        file_content = replace_in_file(file_content, "{template}", plugin_name.lower())

        write_file(file, file_content)


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="CTO-Plugin skeleton for gulp.")
    parser.add_argument("module",
                        help="Name of the module")

    parser.add_argument("plugin_name",
                        help="Name of the plugin")

    parser.add_argument("version",
                        help="Version of the module")

    parser.add_argument("description",
                        help="Description of the module")

    args = parser.parse_args()
    module_name = args.module
    plugin_name = args.plugin_name
    module_version = args.version
    module_description = args.description

    try:
        # Copy template folder to destination folder.
        src_directory = os.path.join("", *["lib", "module"])
        dst_directory = os.path.join("", *["skeleton", module_name])
        copy_directory(src_directory, dst_directory)

        # Rename template folder to the given module folder.
        rename_src = os.path.join("", *[dst_directory, "src", "template"])
        rename_dst = os.path.join("", *[dst_directory, "src", module_name.lower()])
        os.rename(rename_src, rename_dst)

        # Change the content of the package.json template file using the given information of the module.
        change_project_file(dst_directory, module_name, module_version, module_description)

        # Change all template file names to the given plugin name.
        rename_files(dst_directory, plugin_name.lower())

        # Change the content of the template files and save them.
        files = list_files(dst_directory)
        change_file_content(files, plugin_name)

        print("=> Your CTO plugin skeleton used by gulp is ready.\nModule: {}\nPlugin: {}\nLocation: {}".format(
            module_name, plugin_name, os.getcwd() + os.sep + "skeleton"))

    except Exception as e:
        print("An error has occurred => {}".format(e))
        traceback.print_exc()


if __name__ == "__main__":
    main()
