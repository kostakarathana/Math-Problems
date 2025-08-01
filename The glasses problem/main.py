from math import gcd

def glasses_can_fill(x: float, y: float, z: float) -> bool:
    '''
    Given two glasses A,B of size x litres (A) and y litres (B) return True if with
    an infinite water supply you can perfectly fill an unmeasured container with z litres
    using only glasses A and B. The measurement must be perfect, not an estimate.
    '''
    if z == 0:
        return True  # zero is always trivially fillable
    if x == 0 and y == 0:
        return False
    if x == 0:
        return z % y == 0
    if y == 0:
        return z % x == 0

    d = gcd(int(x), int(y))
    return z % d == 0


if __name__ == "__main__":

    assert(glasses_can_fill(5, 3, 4))   # True: 5 - 3 = 2, 3 + 2 = 5, etc.
    assert(glasses_can_fill(6, 10, 8))  # True: GCD is 2, and 8 is a multiple of 2
    assert(glasses_can_fill(9, 6, 3))   # True: GCD 3, 3 is a multiple
    assert(glasses_can_fill(7, 5, 1))   # True: GCD 1, so anything ≤ max(7,5)
    assert(glasses_can_fill(4, 6, 2))   # True: GCD 2
    assert(glasses_can_fill(8, 14, 6))  # True: GCD 2
    assert(not glasses_can_fill(8, 14, 5)) # False: GCD 2, 5 is not a multiple
    assert(glasses_can_fill(2, 3, 1))   # True: GCD 1
    assert(not glasses_can_fill(2, 4, 5)) # False: GCD 2, 5 is not multiple
    assert(glasses_can_fill(7, 3, 4))   # True: GCD 1, and 4 is ≤ max
    assert(glasses_can_fill(12, 15, 3)) # True: GCD 3
    assert(not glasses_can_fill(12, 15, 7)) # False: GCD 3, 7 not multiple
    assert(glasses_can_fill(9, 15, 6))  # True: GCD 3
    assert(not glasses_can_fill(9, 15, 8))  # False: GCD 3, 8 not multiple
    assert(glasses_can_fill(10, 5, 5))  # True: 5 is one of the glasses
    assert(glasses_can_fill(10, 4, 2))  # True: GCD 2
    assert(not glasses_can_fill(10, 4, 3)) # False: GCD 2, 3 not multiple
    assert(glasses_can_fill(3, 6, 3))   # True: 3 is one of the glasses
    assert(glasses_can_fill(3, 5, 2))   # True: GCD 1
    assert(not glasses_can_fill(2, 4, 1)) # False: GCD 2

