"""This modules provides strng formatting functions

prepare_data_for_db insert:
    formatting data to be inserted in database table
concat_list:
    concatenate list elements in a string w/wo separator
to_str:
    transform value to str
is_str:
    test if value is str
concat_key_value:
    concatenate key values of a dictionnary
    {key1: value1, key2: value2} --> ['key1 value1', 'key2 value2']
"""


def prepare_data_for_db_insert(data_list, primary_key=False):
    """Prepare data to be insert in a database

    str elements are surrounded with quotes 'text'
    primary_key allows to include first null value in the string

    Parameters
    ----------
    data_list: list
        elements to include in the str
        [val_int1, val_int2, ..., val_str_1]
    primary_key: bool
        include first Null value in the string (default: False)

    Returns
    -------
    str
        "(val_int1, val_int2, ..., 'val_str_1')"
        or
        "(Null, val_int1, val_int2, ..., 'val_str_1')"
    """
    if primary_key:
        return "(NULL, " + concat_list(data_list, ",", quote_str=True) + ")"
    else:
        return "(" + concat_list(data_list, ",", quote_str=True) + ")"


def concat_list(str_list, sep, quote_str=False):
    """Concat elements of a list into a string with a separator,

    if quote_str is True, surround str elements with quotes 'text'

    Parameters
    ----------
    str_list: list
        list of elements to concatenate
    sep: str
        separator
    quote_str: bool
        if True, surround str elements with quotes 'text' (default: False)

    Returns
    -------
    str:
        string of
    """
    # First element from the list
    first_element = to_str(str_list[0], quote_str)
    concat_str = first_element

    # If there are more than 1 element in the list, transform it to
    # str if needed and concatenate it
    if len(str_list) > 0:
        for i in range(1, len(str_list)):
            new_element = to_str(str_list[i], quote_str)
            concat_str = concat_str + sep + new_element
    return concat_str


def to_str(val, quote_str=False):
    """test if a value's type is str. It not, transform it to str

    if quote_str is True, surround str elements with quotes 'text'

    Parameters
    ----------
    val: 1dim value
        value to test and transform
    quote_str: bool
        if True, surround str elements with quotes 'text' (default: False)

    Returns
    -------
    str:
        processed value
    """
    if is_str(val) and quote_str:
        return "\'" + val + "\'"
    elif is_str(val):
        return val
    else:
        return str(val)


def is_str(txt):
    """test if a value's type is string

    Parameters
    ----------
    txt:
        value to test

    Returns
    -------
    bool:
        True if txt is str, False otherwise
    """
    return type(txt) == str


def concat_key_value(str_dict):
    """concat keys and values of dict containing strings elements
    into a list

    Parameters
    ----------
    str_dict: dict
        dict to process
        {key1: value1, key2: value2}

    Returns
    -------
    list
        ['key1 value1', 'key2 value2']
    """
    return [key + ' ' + value for key, value in str_dict.items()]
