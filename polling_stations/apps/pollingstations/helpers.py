import re


def format_postcode_no_space(postcode):
    return re.sub('[^A-Z0-9]', '', postcode.upper())


def format_postcode_with_space(postcode):
    pc = format_postcode_no_space(postcode)
    return pc[:-3] + ' ' + pc[-3:]
