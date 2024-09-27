# ASE HW3

### extend.py
- This divides the dataset into 2 parts.
    - low_dimension datasets
    - high dimension datasets

- After running this file, and doing some manual processing, I get 2 files:
    - hi_dimension_file_paths.txt
    - lo_dimension_file_paths.txt

- As the name suggests, these have the file paths to the high dimension and low dimension datasets.


### dumb_vs_smart.py
- This file has the implementation of the pseudo code in HW3 assignment.

- To run this for individual files
    - python3 dumb_vs_smart.py <filepath_for_csv>
    - This will output the stats.report on the console.


### test.py
- This file has all the tests for checking if the functions used in dumb_vs_smart.py work as expected

- To run the tests
    - pytest test.py


### Makefile
- Makefile has been modified to add 2 actions: actlodim and acthidim
- Both these run to generate a bash script that gets the output for low dimension and high dimension files respectively

- to run the makefile action for low dimension datasets
    - make Act=branch actlodim > ~/tmp/branch.sh
    - to run the rq.sh script for summary
        - cd ~/tmp
        - bash branch.sh
        - cd branch
        - bash /workspaces/ezr/etc/rq.sh

- to run the makefile action for high dimension datasets
    - make Act=branch acthidim > ~/tmp/branch.sh
    - to run the rq.sh script for summary
        - cd ~/tmp
        - bash branch.sh
        - cd branch
        - bash /workspaces/ezr/etc/rq.sh
