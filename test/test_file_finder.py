import pytest
from src.file_finder import *
import re

CURR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
BAD_PATH = os.path.join(CURR_PATH, 'bar/')
EMPTY_DIR_PATH = os.path.join(CURR_PATH, 'foo/bar/baz/')
FOO_PATH = os.path.join(CURR_PATH, 'foo/')
FOO_BAR_PATH = os.path.join(CURR_PATH, 'foo/bar')


def test_get_directory_empty_path(mocker):
    mocker.patch('builtins.input', return_value='')
    with pytest.raises(NotADirectoryError):
        get_directory_path()


def test_get_directory_bad_path(mocker):
    mocker.patch('builtins.input', return_value=BAD_PATH)
    with pytest.raises(NotADirectoryError):
        get_directory_path()


def test_get_directory_good_path(mocker):
    mocker.patch('builtins.input', return_value=FOO_PATH)
    assert get_directory_path() == FOO_PATH


def test_get_search_type_not_integer(mocker):
    mocker.patch('builtins.input', return_value='a')
    with pytest.raises(ValueError):
        get_search_type()


def test_get_search_type_not_implemented(mocker):
    mocker.patch('builtins.input', return_value='0')
    with pytest.raises(NotImplementedError):
        get_search_type()


def test_get_search_type_regex(mocker):
    mocker.patch('builtins.input', return_value='1')
    assert get_search_type() == 1


def test_get_search_type_size(mocker):
    mocker.patch('builtins.input', return_value='2')
    assert get_search_type() == 2


def test_get_regex_invalid_regex(mocker):
    mocker.patch('builtins.input', return_value='(?=.*foo')
    with pytest.raises(re.error):
        get_regex()


def test_get_regex_valid_regex(mocker):
    regex = '(?=.*foo)'
    mocker.patch('builtins.input', return_value=regex)
    assert get_regex() == re.compile(regex)


def test_get_byte_size_not_integer(mocker):
    mocker.patch('builtins.input', return_value='a')
    with pytest.raises(ValueError):
        get_byte_size()


def test_get_byte_size_negative_integer(mocker):
    mocker.patch('builtins.input', return_value='-1')
    assert get_byte_size() == 0


def test_get_byte_size_integer(mocker):
    mocker.patch('builtins.input', return_value='0')
    assert get_byte_size() == 0


def test_name_file_finder_empty_directory():
    assert name_file_finder(EMPTY_DIR_PATH, re.compile('(?=.*foo)')) == []


def test_name_file_finder_regex_match():
    expected = [('foo.txt', FOO_PATH), ('foo.txt', FOO_BAR_PATH)]
    actual = name_file_finder(FOO_PATH, re.compile('(?=.*foo)'))
    assert actual == expected


def test_size_file_finder_empty_directory():
    assert size_file_finder(EMPTY_DIR_PATH, 0) == []


def test_size_file_finder_all_files():
    expected = [('bar.txt', FOO_PATH), ('foo.txt', FOO_PATH), ('bar.txt', FOO_BAR_PATH), ('foo.txt', FOO_BAR_PATH)]
    actual = size_file_finder(FOO_PATH, 0)
    assert actual == expected


def test_size_file_finder_all_files_at_least_1kb():
    expected = [('bar.txt', FOO_PATH), ('bar.txt', FOO_BAR_PATH)]
    actual = size_file_finder(FOO_PATH, 1000)
    assert actual == expected


def test_file_finder_run_regex_search(mocker):
    mocker.patch('src.file_finder.get_directory_path', return_value=FOO_PATH)
    mocker.patch('src.file_finder.get_search_type', return_value=1)
    mocker.patch('src.file_finder.get_regex', return_value=re.compile('(?=.*foo)'))
    regex_search = mocker.patch('src.file_finder.name_file_finder',
                                return_value=name_file_finder(FOO_PATH, re.compile('(?=.*foo)')))
    file_finder()
    assert regex_search.called


def test_file_finder_run_size_search(mocker):
    mocker.patch('src.file_finder.get_directory_path', return_value=FOO_PATH)
    mocker.patch('src.file_finder.get_search_type', return_value=2)
    mocker.patch('src.file_finder.get_byte_size', return_value=0)
    size_search = mocker.patch('src.file_finder.size_file_finder',
                               return_value=size_file_finder(FOO_PATH, 0))
    file_finder()
    assert size_search.called
