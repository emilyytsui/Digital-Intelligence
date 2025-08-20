# IAE 101 (Fall 2024)
# HW 2, Problem 3

def reverse1(s):
    reverse = ''

    for i in range(len(s) - 1, -1, -1):
        reverse += s[i]

    return reverse

def reverse2(s):
    reverse2 = s

    reverse2 = reverse2[ : : -1]

    return reverse2


# DO NOT DELETE THE FOLLOWING LINES OF CODE! YOU MAY
# CHANGE THE FUNCTION CALLS TO TEST YOUR WORK WITH
# DIFFERENT INPUT VALUES.
if __name__ == "__main__":
    print("reverse1(\"Mississippi\") is:", reverse1("Mississippi"))
    print()
    print("reverse2(\"Mississippi\") is:", reverse2("Mississippi"))
    print()
    print("reverse1(\"Connetquot\") is:", reverse1("Connetquot"))
    print()
    print("reverse2(\"Connetquot\") is:", reverse2("Connetquot"))
    print()
    print("reverse1(\"Wyandanch\") is:", reverse1("Wyandanch"))
    print()
    print("reverse2(\"Wyandanch\") is:", reverse2("Wyandanch"))
    print()
    print("reverse1(\"Ronkonkoma\") is:", reverse1("Ronkonkoma"))
    print()
    print("reverse2(\"Ronkonkoma\") is:", reverse2("Ronkonkoma"))
    print()
