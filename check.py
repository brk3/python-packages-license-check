#!/usr/bin/env python
import pkg_resources
import argparse
import sys

from pip.utils import get_installed_distributions


def main():
    parser = argparse.ArgumentParser(description="Read all installed packages from sys.path and list licenses.")
    args = parser.parse_args()

    meta_files_to_check = ['PKG-INFO', 'METADATA']

    for installed_distribution in get_installed_distributions():
        license = 'UNKNOWN'
        for metafile in meta_files_to_check:
            if not installed_distribution.has_metadata(metafile):
                continue
            for line in installed_distribution.get_metadata_lines(metafile):
                if 'License: ' in line or 'Classifier: License' in line:
                    (k, v) = line.split(': ', 1)
                    if v == 'UNKNOWN':
                        continue
                    license = v
                    break
        project_name = installed_distribution.project_name
        version = installed_distribution.version
        home = '/'.join(['https://pypi.python.org/pypi', project_name, version])
        sys.stdout.write('"{}","{}","{}","{}"\n'.format(project_name, version, license, home))

if __name__ == "__main__":
    main()
