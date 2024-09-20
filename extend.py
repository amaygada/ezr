import sys,random
from ezr import the, DATA, csv, dot

hi_dim = "hi_dimension_file_paths.txt"
lo_dim = "lo_dimension_file_paths.txt"

def show(lst):
  return print(*[f"{word:6}" for word in lst], sep="\t")

def myfun(train):
  d    = DATA().adds(csv(train))
  x    = len(d.cols.x)
  size = len(d.rows)
  dim  = "small" if x <= 5 else ("med" if x < 12 else "hi")
  size = "small" if size< 500 else ("med" if size<5000 else "hi")
  return [dim, size, x,len(d.cols.y), len(d.rows), train[17:]]

def append_to_file(file_name, lst):
  with open(file_name, 'a') as file:
    lst = [str(l) for l in lst]
    a = [f"{word:6}" for word in lst]
    file.write('\t'.join(a) +  "\n" )

def separate_and_show():
  for arg in sys.argv:
    if arg[-4:] == ".csv":
      result = myfun(arg)
      show(result)
      if result[0] != "small":
        append_to_file(hi_dim, result)
      else:
        append_to_file(lo_dim, result)
  return lo_dim, hi_dim

# random.seed(the.seed) #  not needed here, but good practice to always take care of seeds
# show(["dim", "size","xcols","ycols","rows","file"])
# show(["------"] * 6)
# separate_and_show()

for arg in sys.argv:
  print(arg)