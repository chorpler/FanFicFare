#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018, Jim Miller

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
from glob import glob
import time
from datetime import datetime
from pathlib import Path


try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Pip install tomli for Python < 3.11

from makezip import createZipFile

# Locate your pyproject.toml
pyproject_path = Path(__file__).parent / "pyproject.toml"
version = ""

if pyproject_path.is_file():
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
        # Get the version (Handles standard [project] or poetry format)
        version = data.get("project", {}).get("version") or data.get("tool", {}).get("poetry", {}).get("version")


def rename_if_exists(file_path_str):
    file_path = Path(file_path_str)

    # 1. Check if the target file already exists
    if file_path.is_file():
        # # Create a backup name (e.g., data.txt -> data.txt.bak)
        # backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        #
        # # 2. Rename the old file
        # file_path.rename(backup_path)
        # print(f"Old file renamed to: {backup_path}", file=sys.stderr)
        # 2. Get the last modified timestamp
        mod_time = os.path.getmtime(file_path)

        # 3. Convert timestamp to a readable, safe string format (e.g., YYYYMMDD_HHMMSS)
        timestamp_str = datetime.fromtimestamp(mod_time).strftime('%Y%m%d_%H%M%S')

        # 4. Create the new backup filename
        dir_name, file_name = os.path.split(file_path)
        name, ext = os.path.splitext(file_name)
        backup_name = f"{name}_{timestamp_str}{ext}"
        backup_path = os.path.join(dir_name, backup_name)

        # 5. Rename the existing file
        os.rename(file_path, backup_path)
        print(f"Existing file renamed to: {backup_name}", file=sys.stderr)

if __name__=="__main__":
    filename="FanFicFare.zip"
    if version:
        filename = f"FanFicFare-{version}.zip"
    exclude=['*.pyc','*~','*.xcf','*[0-9].png','*.po','*.pot','*default.mo','*Thumbs.db']
    rename_if_exists(filename)

    os.chdir('calibre-plugin')
    files=['plugin-defaults.ini','plugin-example.ini','about.html',
           'images','translations']
    files.extend(glob('*.py'))
    files.extend(glob('plugin-import-name-*.txt'))
    # 'w' for overwrite
    createZipFile("../"+filename,"w",
                  files,
                  exclude=exclude)

    os.chdir('../included_dependencies')
    files=[
        'cloudscraper',
        'requests',
        'requests_toolbelt',
        'requests_file.py',
        'urllib3',
        'certifi',
        'idna',
        'brotlidecpy', # still needed for cal5.
        ]
    createZipFile("../"+filename,"a",
                  files,
                  exclude=exclude)

    os.chdir('..')
    # 'a' for append
    files=['fanficfare']
    createZipFile(filename,"a",
                  files,
                  exclude=exclude)






    # # 3. Save the new file
    # file_path.write_text(content, encoding='utf-8')
    # print(f"New file saved to: {file_path}")

# Example usage
# save_with_backup("data.txt", "This is the new content.")






# file_path = "target_file.txt"
#
# # 1. Check if the file already exists
# if os.path.exists(file_path):
#     # 2. Get the last modified timestamp
#     mod_time = os.path.getmtime(file_path)
#
#     # 3. Convert timestamp to a readable, safe string format (e.g., YYYYMMDD_HHMMSS)
#     timestamp_str = datetime.fromtimestamp(mod_time).strftime('%Y%m%d_%H%M%S')
#
#     # 4. Create the new backup filename
#     dir_name, file_name = os.path.split(file_path)
#     name, ext = os.path.splitext(file_name)
#     backup_name = f"{name}_{timestamp_str}{ext}"
#     backup_path = os.path.join(dir_name, backup_name)
#
#     # 5. Rename the old file
#     os.rename(file_path, backup_path)
#     print(f"Old file renamed to: {backup_name}")
#
# # 6. Save your new file here
# with open(file_path, 'w') as f:
#     f.write("Your new file content goes here.")
# print("New file saved.")
#
#
#
#
