def format_residential_address(address_parts):
    # use this function to format an address with commas
    # e.g: 1 Foo street, Bar Town
    # We store Residential Addresses in this format because we show
    # them in a list/drop down (i.e: in a single line format)
    address = ", ".join([part for part in address_parts if part.strip()])
    return address


def format_polling_station_address(address_parts):
    # use this function to format an address with line breaks
    # e.g: 1 Foo street\nBar Town
    # We store Polling Station Addresses in this format because we show
    # them in isolation on a page (i.e: in a multi line format)
    address = "\n".join([part for part in address_parts if part.strip()])
    return address
