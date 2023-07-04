#!/usr/bin/python3

from enum import Enum


class BotsError(Enum):
    ERROR_NO_NETWORK = "we can't find such network."
    ERROR_NO_ACCOUNT = "we can't find such account."
    ERROR_NO_ELEMENT = "we can't find such element by xpath."


class NoElementFoundException(Exception):
    pass
