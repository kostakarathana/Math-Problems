Getting primes up to n
----------------------

Three methods were tested for getting primes up to n:

- Brute force (test whether each num up to n is divisible by a number preceding it other than 1 or itself)
- Optimised (same as brute force, but breaks instantly if a factor is found and only looks up to root(i) for searching for factors of the ith number)
- Sieve of Eratosthenes (much faster method that dynamically removes values from a list of 2->n based on whether they are mutliples of numbers 2->i, where i**2 is >= n)

Results (testing on n = 1000, 2000, 3000 .... 10000)

brute force:     [0.0, 0.008818864822387695, 0.03531789779663086, 0.08530831336975098, 0.1536867618560791, 0.2437119483947754, 0.35575127601623535, 0.48294782638549805, 0.6317870616912842, 0.8031010627746582]

optimised:     [9.5367431640625e-07, 0.00017118453979492188, 0.00032067298889160156, 0.0004992485046386719, 0.0008099079132080078, 0.0010058879852294922, 0.0013279914855957031, 0.0014541149139404297, 0.0017828941345214844, 0.0019199848175048828]

SOE :     # [4.0531158447265625e-06, 3.1948089599609375e-05, 6.198883056640625e-05, 9.179115295410156e-05, 0.0001270771026611328, 0.0001552104949951172, 0.0001938343048095703, 0.00023508071899414062, 0.0002598762512207031, 0.00031113624572753906]

![alt text](<all three methods compared.png>)
![alt text](<Sieve vs Opt.png>)