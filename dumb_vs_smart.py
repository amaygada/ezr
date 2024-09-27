import sys,random
from ezr import the, DATA, csv, dot, xval
import stats , time
from math import exp

def guess(N, d):
    # pick N rows at random
    some = random.choices(d.rows, k=N)
    # sort them on chebyshev
    return d.clone().adds(some).chebyshevs()

def read_data(file_path):
    return DATA().adds(csv(file_path))

def redirect_output(filename):
    sys.stdout = open(filename, 'w')

def restore_output():
    sys.stdout = sys.__stdout__

def main(result_file_name, csv_file_name):
    # Read the CSV data
    d = read_data(csv_file_name)
    
    # Chebyshev distance for initial rows (as-is state)
    b4 = [d.chebyshev(row) for row in d.rows]
    
    # Initialize the 'somes' list with the initial "as-is" state
    somes = [stats.SOME(b4, f"asIs")]
    
    # Define scoring policies for smart and dumb approaches
    scoring_policies = [
        ('exploit', lambda B, R: B - R),
        ('explore', lambda B, R: (exp(B) + exp(R)) / (1E-30 + abs(exp(B) - exp(R))))
    ]
    
    # Loop through the different scenarios and collect results
    for what, how in scoring_policies:
        for N in [20, 30, 40, 50]:  # Using N as in the original code
            for the.branch in [False, True]:
                
                # Generate results using smart and dumb logic
                if (what=='exploit') and (the.branch):
                    dumb = [guess(N,d) for _ in range(20)]
                    dumb = [d.chebyshev( lst.rows[0] ) for lst in dumb]
                    tag = f"Dumb/ s=NA/ b=NA/ N={N}"
                    somes += [stats.SOME(dumb, tag)]

                the.Last = N
                smart = [d.shuffle().activeLearning(score=how) for _ in range(20)]
                smart = [d.chebyshev( lst[0] ) for lst in smart]

                tag = f"Smart/s={what}/b={the.branch}/N={N}"
                somes += [stats.SOME(smart, tag)]
    
    # Save the results to a file
    if result_file_name != "":
        redirect_output(result_file_name + "/" + csv_file_name.split(".csv")[0].replace('/', '_') + ".result")
    
    # Generate the final report
    stats.report(somes, 0.01)
    
    # Restore output to default
    if result_file_name != "":
        restore_output()

# with open('lo_dimension_file_paths.txt', 'r') as file:
#     for line in file:
#         value = line.strip()
#         print(value)
#         main("lo_dim_result", "data/optimize/"+value)

# with open('hi_dimension_file_paths.txt', 'r') as file:
#     for line in file:
#         value = line.strip()
#         print(value)
#         main("hi_dim_result", "data/optimize/"+value)

main("", sys.argv[1])