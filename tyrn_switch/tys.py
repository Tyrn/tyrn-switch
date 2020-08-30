#!/usr/bin/env python

""" Setting links, maybe system variables, etc.,
    according to command line options.
"""

import sys

if sys.version_info < (3, 6, 0):
    sys.stderr.write("You need python 3.6 or later to run this script\n")
    sys.exit(1)

import os
import argparse
import warnings

LSHARE = "~/.local/share"
CONF = "~/.config"

LN_PATHS = [
    (f"{CONF}/arch-chronicle", f"{CONF}/nvim"),
    (LSHARE, f"{LSHARE}/nvim"),
]


def list_links():
    """ Lists the known links.
    """
    for _, link in LN_PATHS:
        os.system(f"ls -l {link}")


def remove_links():
    """ Removes the known links.
    """
    print("To be removed: ***********")
    list_links()
    for _, link in LN_PATHS:
        os.system(f"rm {link}")
    print("**************************\n")


def create_links(target):
    """ Creates the required links to [target].
    """
    remove_links()
    for target_base, link in LN_PATHS:
        os.system(f"ln -s {target_base}/{target} {link}")
    list_links()


# Option names.
ARG_NVIM_FISA = "-fa"
ARG_NVIM_GQ = "-gq"
ARG_LIST_OPTIONS = "-ls"
ARG_REMOVE_LINKS = "-rl"

VALID_ARGS = {
    ARG_NVIM_FISA: lambda: create_links("nvim-fisa"),
    ARG_NVIM_GQ: lambda: create_links("nvim-gq"),
    ARG_LIST_OPTIONS: list_links,
    ARG_REMOVE_LINKS: remove_links,
}


def main():
    """ The script entry point. Reads command line options
    and runs the script.
    """
    try:
        warnings.resetwarnings()
        warnings.simplefilter("ignore")

        VALID_ARGS[retrieve_arg()]()
    except KeyboardInterrupt as ex:
        sys.exit(ex)


def retrieve_arg():
    """ Creates and reads command line options.
    """
    parser = argparse.ArgumentParser(
        description="""Inhouse options: switching bits and pieces."""
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        ARG_NVIM_FISA,
        help="select fisa neovim config",
        const=ARG_NVIM_FISA,
        type=str,
        nargs="?",
    )
    group.add_argument(
        ARG_NVIM_GQ,
        help="select gq neovim config",
        const=ARG_NVIM_GQ,
        type=str,
        nargs="?",
    )
    group.add_argument(
        ARG_LIST_OPTIONS,
        help="list all the options as selected",
        const=ARG_LIST_OPTIONS,
        type=str,
        nargs="?",
    )
    group.add_argument(
        ARG_REMOVE_LINKS,
        help="remove option defining soft links",
        const=ARG_REMOVE_LINKS,
        type=str,
        nargs="?",
    )
    args = parser.parse_args()
    for _, value in args.__dict__.items():
        if value in VALID_ARGS.keys():
            return value
    return ARG_LIST_OPTIONS  # Listing is always harmless.


if __name__ == "__main__":
    main()
