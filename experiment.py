# def benchmark():
#     d = DATA().adds(csv(the.train))
#     b4 = [d.chebyshev(row) for row in d.rows]
#     somes = [stats.SOME(b4,f"asIs,{len(d.rows)}")]

# def option_run():
#     rnd = lambda z: z
#     scoring_policies = [
#         ('exploit', lambda B, R,: B - R),
#         ('explore', lambda B, R :  (exp(B) + exp(R))/ (1E-30 + abs(exp(B) - exp(R))))]
    
#     for what,how in scoring_policies:
#         for the.Last in [0,20, 30, 40]:
#             for the.branch in [False, True]:
#             start = time()
#             result = []
#             runs = 0
#             for _ in range(repeats):
#                 tmp=d.shuffle().activeLearning(score=how)
#                 runs += len(tmp)
#                 result += [rnd(d.chebyshev(tmp[0]))]

#             pre=f"{what}/b={the.branch}" if the.Last >0 else "rrp"
#             tag = f"{pre},{int(runs/repeats)}"
#             print(tag, f": {(time() - start) /repeats:.2f} secs")
#             somes +=   [stats.SOME(result,    tag)]