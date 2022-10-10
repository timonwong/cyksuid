import timeit

rounds = 1000000
svix_timer = timeit.timeit(
    "k = gen()", setup="from ksuid import Ksuid; gen = Ksuid", number=rounds
)
cyksuid_timer = timeit.timeit(
    "k = gen()",
    setup="from cyksuid import ksuid; gen = ksuid.ksuid",
    number=rounds,
)

delta = (cyksuid_timer - svix_timer) / svix_timer
gain = (svix_timer - cyksuid_timer) / cyksuid_timer

print(
    f"""
Benchmark results (rounds={rounds})):
svix: {svix_timer}
cyksuid: {cyksuid_timer}

delta: {delta*100:.2f}%
performance increase: {gain*100:.2f}%
"""
)
