# IAE 101 (Fall 2024)
# HW 1, Problem 4

def temp_converter(temperature, new_unit):
    # ADD YOUR CODE HERE
    if(new_unit == 'F'):
        return ((temperature * 9) / 5) + 32
    elif(new_unit == 'C'):
        return ((temperature - 32) * 5) / 9


# DO NOT DELETE THE FOLLOWING LINES OF CODE! YOU MAY
# CHANGE THE FUNCTION CALLS TO TEST YOUR WORK WITH
# DIFFERENT INPUT VALUES.
if __name__ == "__main__":
    print("temp_converter(100,'C') is", temp_converter(100, 'C'))
    print()
    print("temp_converter(0,'F') is", temp_converter(0, 'F'))
    print()
    print("temp_converter(212,'C') is", temp_converter(212, 'C'))
    print()
    print("temp_converter(32,'C') is", temp_converter(32, 'C'))
    print()
    print("temp_converter(50,'F') is", temp_converter(50, 'F'))
    print()
