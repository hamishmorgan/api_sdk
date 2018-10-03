#!/usr/bin/env python
# coding=utf-8

from getpass import getpass
import logging
from pathlib import Path

import credentials
from bwproject import BWUser

import argparse


def authenticate(username: str, password: str, credentials_path=None) -> BWUser:
    """""
    Authenticate the given username and password pair, storing the access token in the credentials file.

    :param username: Brandwatch account usernames
    :param password: Brandwatch account password
    :param credentials_path: Path to where credentials should be stored
    :return: An authenticated BWUser object
    """
    return BWUser(username=username, password=password, token_path=credentials_path)


def main():
    logger = logging.getLogger("bwapi")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s: %(message)s", "%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    parser = argparse.ArgumentParser(description="Logging to Brandwatch and retrieve and access token.")

    parser.add_argument("--store", "-s", type=Path, metavar="PATH", default=credentials.DEFAULT_CREDENTIALS_PATH,
                        help="Path to where access tokens are stored. (Default: {})".format(
                            credentials.DEFAULT_CREDENTIALS_PATH))

    parser.add_argument("--username", "-u", type=str, help="Brandwatch username (probably your email address).")
    parser.add_argument("--password", "-p", type=str, help="Brandwatch password.")

    args = parser.parse_args()

    if args.username is None or args.password is None:
        print("Please enter your Brandwatch credentials below")
        if args.username is None:
            args.username = input("Username: ")
        if args.password is None:
            args.password = getpass("Password: ")

    try:
        print("Authenticating user: {}".format(args.username))
        user = authenticate(args.username, args.password, credentials_path=args.store)
        print("Success! Access token: {}".format(user.token))
    except KeyError as e:
        print(e)


if __name__ == "__main__":
    main()