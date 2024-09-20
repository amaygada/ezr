import sys,random
from ezr import the, DATA, csv, dot, xval
import stats

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
    somes = []
    d = read_data(csv_file_name)
    for N in [20, 30, 40, 50]:
        ns = stats.SOME(txt=f"N dumb={N}")
        somes += [ns]
        dumb = [guess(N,d) for _ in range(20)]
        dumb = [d.chebyshev( lst.rows[0] ) for lst in dumb]
        for i in dumb:
            ns.add(i)
        
        ns2 = stats.SOME(txt=f"N smart={N}")
        somes += [ns2]
        the.Last = N
        smart = [d.shuffle().activeLearning() for _ in range(20)]
        smart = [d.chebyshev( lst[0] ) for lst in smart]
        for i in smart:
            ns2.add(i)
    redirect_output(result_file_name+"/"+csv_file_name.split(".csv")[0].replace('/','_')+".result")
    stats.report(somes)
    restore_output()

with open('lo_dimension_file_paths.txt', 'r') as file:
    for line in file:
        value = line.strip()
        main("lo_dim_result", "data/optimize/"+value)

with open('hi_dimension_file_paths.txt', 'r') as file:
    for line in file:
        value = line.strip()
        main("hi_dim_result", "data/optimize/"+value)