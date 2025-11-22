from scipy.optimize import linprog

# Objective function coefficients (negative for maximization)
# Maximize 6A + 5B  →  Minimize -6A - 5B
c = [-6, -5]

# Constraints:
# A + B <= 5
# 3A + 2B <= 12
A = [
    [1, 1],
    [3, 2]
]

b = [5, 12]

# Bounds for A and B (>= 0)
bounds = [(0, None), (0, None)]

# Solve
result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

A_opt = result.x[0]
B_opt = result.x[1]
profit = 6*A_opt + 5*B_opt

print("Optimal A =", round(A_opt))
print("Optimal B =", round(B_opt))
print("Maximum Profit =", profit)
