# ASE HW3

## extend.py
- This divides the dataset into 2 parts.
    - low_dimension datasets
    - high dimension datasets

- After running this file, and doing some manual processing, I get 2 files:
    - hi_dimension_file_paths.txt
    - lo_dimension_file_paths.txt

- As the name suggests, these have the file paths to the high dimension and low dimension datasets.


## dumb_vs_smart.py
- This file has the implementation of the pseudo code in HW3 assignment.

- To run this for individual files
    - python3 dumb_vs_smart.py <filepath_for_csv>
    - This will output the stats.report on the console.


## test.py
- This file has all the tests for checking if the functions used in dumb_vs_smart.py work as expected

- To run the tests
    - pytest test.py


## Makefile
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


## Results
- For individual dataset result go to the folders 
    - hi_dim_result
    - lo_dim_result

- Each result file inside these folders tells which method is doing better.
- The results are sorted.
- The top most is the best

## Bottleneck
- We were unable to successfully run rq.sh on our data.
- We believe it is a formatting issue.
- We were hence not able to get the summary result.
- All our conclusions will be on the basis of the indidual results.

## Conclusions
- We conclude that JJR1 holds true for only some low dimension output. Even when it holds true, the standard deviation is large.
    - (For example in lo_dim_result/data_optimize_config_SS-D.result)
    - the standard deviation is 0.14

- On the other hand JJR2 holds true for high dimension data.

- Therefore, we agree with JJR2 and disagree with JJR1.