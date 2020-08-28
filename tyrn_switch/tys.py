#!/usr/bin/env python

import sys

if sys.version_info < (3, 6, 0):
    sys.stderr.write("You need python 3.6 or later to run this script\n")
    sys.exit(1)

import os
import argparse
import warnings
from pathlib import Path


LSHARE = "~/.local/share"
CONF = "~/.config"
TARGET = f"{CONF}/arch-chronicle"


AG = None


def list_links():
    os.system(f"ls -l {CONF}/nvim")
    os.system(f"ls -l {LSHARE}/nvim")


def remove_links():
    print("To be removed:")
    list_links()
    os.system(f"rm {CONF}/nvim")
    os.system(f"rm {LSHARE}/nvim")


def options():
    """
    Processes selected options.
    """
    if AG.list_options:
        list_links()
    elif AG.remove_links:
        remove_links()
    elif AG.nvim_fisa:
        os.system(f"ln -s {TARGET}/nvim-fisa {CONF}/nvim")
        os.system(f"ln -s {LSHARE}/nvim-fisa {LSHARE}/nvim")
        list_links()
    elif AG.nvim_gq:
        os.system(f"ln -s {TARGET}/nvim-gq {CONF}/nvim")
        os.system(f"ln -s {LSHARE}/nvim-gq {LSHARE}/nvim")
        list_links()

    print(f"options(): {AG}")


def retrieve_args():
    """
    Creates and reads command line options.
    """
    parser = argparse.ArgumentParser(
        description="""
Inhouse options: switching bits and pieces.
    """
    )

    parser.add_argument(
        "-fa",
        "--nvim-fisa",
        help="select fisa neovim config",
        action="store_true",
    )
    parser.add_argument(
        "-gq",
        "--nvim-gq",
        help="select gq neovim config",
        action="store_true",
    )
    parser.add_argument(
        "-ls",
        "--list-options",
        help="list all the options as selected",
        action="store_true",
    )
    parser.add_argument(
        "-rl",
        "--remove-links",
        help="remove option defining soft links",
        action="store_true",
    )
    return parser.parse_args()


def main():
    """
    The script entry point.
    Reads command line options
    and runs the script.
    """
    global AG

    try:
        warnings.resetwarnings()
        warnings.simplefilter("ignore")

        AG = retrieve_args()
        options()
    except KeyboardInterrupt as ex:
        sys.exit(ex)


if __name__ == "__main__":
    main()
