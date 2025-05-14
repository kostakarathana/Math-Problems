'''
given two numbers, find their greatest common denominator
'''

def gcd(a, b):
    '''
    We know gcd(a,b) = gcd(b, a (mod b))
    '''
    if a % b == 0:
        return  b
    return gcd(b, a % b)

print(gcd(139350,139350*150))