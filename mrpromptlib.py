import mrmsglib
import mrprintlib

lang = "en"


def askForString(prompt):
    return input("{prompt}: ".format(prompt=prompt))


def askForInteger(prompt):
    while (True):
        value = input("{prompt}: ".format(prompt=prompt))
        if (value.isdigit()):
            break
        print("Input must be an integer, try again: ")
    return int(value)


def askForInteger(prompt):
    while (True):
        value = input("{prompt}: ".format(prompt=prompt))
        if (value.isdecimal()):
            break
        print("Input must be a decimal number, try again: ")
    return int(value)