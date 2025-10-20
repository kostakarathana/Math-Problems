
def karatsuba(x: int, y: int) -> int:
    # base case, small numbers:
    if x < 10 or y < 10:
        return x * y # small enough to multiply without worry of n^2 theoretically

    # calculate size of numbers
    n = max(len(str(x)), len(str(y)))
    m = n // 2 # midpoint

    # Split x and y into high and low parts
    high_x, low_x = divmod(x, 10**m)
    high_y, low_y = divmod(y, 10**m)

    # Three recursive multiplications
    z0 = karatsuba(low_x, low_y)                  # low * low
    z2 = karatsuba(high_x, high_y)                # high * high
    z1 = karatsuba(low_x + high_x, low_y + high_y) - z2 - z0  # cross terms

    # Combine results
    return (z2 * 10**(2*m)) + (z1 * 10**m) + z0





if __name__ == "__main__":
    print(karatsuba(100, 100))
    print(karatsuba(1552945, 10485240))



