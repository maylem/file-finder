# file-finder

**Program Requirements**
>file-finder/requirements.txt
*Project written in Python 3.7.1*

**Code Coverage**
Code coverage report can be generated with the following command in file-finder/:
>`pytest --cov=src --cov-report=html test`

The latest coverage report can be found as an HTML in 
>file-finder/htmlcov/src_file_finder_py.html

Code coverage is at 95%. 

The logic that is not covered is concerned with getting the length of the list of files found, printing to stdout, and logging at the end of the program. Unit tests were not written to cover this section since (1) these were not functions that were implemented in the project, (2) the output of size/name_file_finder is constrained to an empty list in the case of 0 files being found, and (3) all prior functions were tested.

**Execution Time**
Execution time is displayed for only the period of time that the program is in a file search state.   
Microseconds were chosen since the search time for the created test directory was so small, but should be changed if searching larger directories.  
While the current implementation is linear, execution time could be improved upon by using the multiprocessing package to check multiple files' sizes/names in parallel across multiple processes.

Sample terminal execution of the program:
>file-finder/src>`python file_finder.py`  

>Enter the directory path to be searched: `../test/foo`

>Enter 1 to find files with a name regex, or 2 to find files of at least some byte size: `2`

>Enter the minimum file byte size: `1000`

>Search time elapsed: 1004 microseconds  
>Found the following 2 file(s):  
>bar.txt - ../test/foo  
>bar.txt - ../test/foo/bar  

