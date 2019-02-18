import logging
import os
import re
import datetime as dt

logging.basicConfig(filename=os.path.join(os.pardir, 'file_finder.log'),
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def get_directory_path():
    """
    Read and validate directory string from user input.
    :return: Directory path string.
    """
    path = input('Enter the directory path to be searched: ')

    if os.path.isdir(path):
        logging.info('Searching for files in directory {}'.format(path))
        return path
    else:
        error = NotADirectoryError('{} is not an existing directory.'.format(path))
        logging.error(error)
        raise error


def get_search_type():
    """
    Read file search criteria from user input (1 for filename regex, 2 for byte size).
    :return: Search criteria as an integer.
    """
    options = 'Enter 1 to find files with a name regex, or 2 to find files of at least some byte size: '
    search = input(options)

    try:
        search = int(search)

        if search in (1, 2):
            search_type = 'filename regex' if search == 1 else 'byte size'
            search_msg = 'Search criteria: {} ({})'.format(search, search_type)
            logging.info(search_msg)
            return search
        else:
            error = NotImplementedError('{} is not an implemented search criteria. '.format(search) + options)
            logging.error(error)
            raise error
    except ValueError as error:
        logging.error(error, exc_info=True)
        raise


def get_regex():
    """
    Read and validate the regex from user input that is to be used in a filename search.
    :return: Compiled regex object.
    """
    regex = input('Enter the filename regex to be used: ')

    try:
        return re.compile(regex)
    except re.error:
        logging.error('{} is not a valid regex.'.format(regex), exc_info=True)
        raise


def get_byte_size():
    """
    Read the minimum byte size from user input that is to be used in a file size search.
    :return: Byte size as an integer. Negative values are converted to zero.
    """
    byte_size = input('Enter the minimum file byte size: ')

    try:
        byte_size = int(byte_size)
        return byte_size if byte_size >= 0 else 0
    except ValueError:
        logging.error('{} is not an integer byte size.'.format(byte_size), exc_info=True)
        raise


def name_file_finder(directory, regex):
    """
    Search a directory for file names matching the provided regex.
    :param directory: Directory path string.
    :param regex: A compiled regex object.
    :return: List of tuples of the format (file name, file path) for all files that matched the regex.
    """

    matched_files = []
    start_time = dt.datetime.now()

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if regex.match(filename):
                matched_files.append((filename, root))

    end_time = dt.datetime.now()

    search_time_msg = 'Search time elapsed: {} microseconds'.format((end_time - start_time).microseconds)
    print(search_time_msg)
    logging.info(search_time_msg)

    return matched_files


def size_file_finder(directory, byte_size):
    """
    Search a directory for files that are at least as large as the provided byte size.
    :param directory: Directory path string.
    :param byte_size: Integer of the minimum byte size to be found.
    :return: List of tuples of the format (file name, file path) for all files meeting the minimum byte size.
    """
    matched_files = []
    start_time = dt.datetime.now()

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if os.path.getsize(os.path.join(root, filename)) >= byte_size:
                matched_files.append((filename, root))

    end_time = dt.datetime.now()
    search_time_msg = 'Search time elapsed: {} microseconds'.format((end_time - start_time).microseconds)
    print(search_time_msg)
    logging.info(search_time_msg)

    return matched_files


def file_finder():
    """
    Search a directory using a specified search criteria (by name regex or by minimum byte size) and display a list of
    the files found.
    """
    directory_path = get_directory_path()
    search_alg = get_search_type()

    if search_alg == 1:  # name regex search
        regex = get_regex()
        files_found = name_file_finder(directory_path, regex)
    else:  # file size search
        byte_size = get_byte_size()
        files_found = size_file_finder(directory_path, byte_size)

    if len(files_found) > 0:
        msg = 'Found the following {} file(s):\n{}'.format(len(files_found), '\n'.join(
            [name + ' - ' + path for (name, path) in files_found]))
        logging.info(msg)
        print(msg)
    else:
        msg = 'No files matched the search criteria.'
        logging.info(msg)
        print(msg)


if __name__ == '__main__':
    file_finder()
