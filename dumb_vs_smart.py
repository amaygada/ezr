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

# def main(result_file_name, csv_file_name):
#     somes = []
#     d = read_data(csv_file_name)
#     for N in [20, 30, 40, 50]:
#         ns = stats.SOME(txt=f"N dumb={N}")
#         somes += [ns]
#         dumb = [guess(N,d) for _ in range(20)]
#         dumb = [d.chebyshev( lst.rows[0] ) for lst in dumb]
#         for i in dumb:
#             ns.add(i)
        
#         ns2 = stats.SOME(txt=f"N smart={N}")
#         somes += [ns2]
#         the.Last = N
#         smart = [d.shuffle().activeLearning() for _ in range(20)]
#         smart = [d.chebyshev( lst[0] ) for lst in smart]
#         for i in smart:
#             ns2.add(i)
#     redirect_output(result_file_name+"/"+csv_file_name.split(".csv")[0].replace('/','_')+".result")
#     stats.report(somes)
#     restore_output()

def main(result_file_name, csv_file_name):
    # Read the CSV data
    d = read_data(csv_file_name)
    
    # Chebyshev distance for initial rows (as-is state)
    b4 = [d.chebyshev(row) for row in d.rows]
    
    # Initialize the 'somes' list with the initial "as-is" state
    somes = [stats.SOME(b4, f"asIs,{len(d.rows)}")]
    
    # Define scoring policies for smart and dumb approaches
    scoring_policies = [
        ('dumb', lambda B, R: B - R),
        ('smart', lambda B, R: (exp(B) + exp(R)) / (1E-30 + abs(exp(B) - exp(R))))
    ]
    
    # Loop through the different scenarios and collect results
    for what, how in scoring_policies:
        for N in [20, 30, 40, 50]:  # Using N as in the original code
            for the.branch in [False, True]:
                start = time.time()
                result = []
                runs = 0
                repeats = 20  # Assuming this is the repeat count as per original logic
                
                # Generate results using smart and dumb logic
                for _ in range(repeats):
                    if what == 'dumb':
                        tmp = [guess(N, d)]
                        runs += len(tmp)
                        result += [d.chebyshev(tmp[0].rows[0])]  # Calculating chebyshev distance
                    else:  # what == 'smart'
                        tmp = d.shuffle().activeLearning(score=how)
                        result += [d.chebyshev(tmp[0])]  # Calculating chebyshev distance
                
                # Build the tag for labeling results
                pre = f"{what}/b={the.branch}" if N > 0 else "rrp"
                tag = f"{pre},{int(runs / repeats)}"
                print(tag, f": {(time.time() - start) / repeats:.2f} secs")
                
                # Add to 'somes' list
                somes += [stats.SOME(result, tag)]
    
    print('chalra hai', result_file_name, csv_file_name )
    # Save the results to a file
    redirect_output(result_file_name + "/" + csv_file_name.split(".csv")[0].replace('/', '_') + ".result")
    
    # Generate the final report
    stats.report(somes, 0.01)
    
    # Restore output to default
    restore_output()

with open('lo_dimension_file_paths.txt', 'r') as file:
    for line in file:
        value = line.strip()
        main("lo_dim_result", "data/optimize/"+value)

with open('hi_dimension_file_paths.txt', 'r') as file:
    for line in file:
        value = line.strip()
        main("hi_dim_result", "data/optimize/"+value)