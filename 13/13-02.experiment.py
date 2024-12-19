from sympy import symbols, Eq, solve

# Define symbolic variables
a, b = symbols("a b", integer=True)

# Define the equations
eq1 = Eq(a * 26 + b * 67, 10000000012748)
eq2 = Eq(a * 66 + b * 21, 10000000012176)

# Solve the system of equations
solution = solve([eq1, eq2], (a, b))

# Output the solution
print("Solution:", solution)

if solution:
    [a, b] = solution.values()
    print(f"Tokens: {a * 3 + b}")
    print(f"Button A: {a}, Button B: {b}")
