import numpy as np

def F(x):
    a1, b1, c1, d1 = 1, 2, 3, 6
    a2, b2, c2, d2 = 4, 5, 6, 15
    a3, b3, c3, d3 = 7, 8, 9, 24
    return np.array([
        a1 * x[0] + b1 * x[1] + c1 * x[2] - d1,
        a2 * x[0] + b2 * x[1] + c2 * x[2] - d2,
        a3 * x[0] + b3 * x[1] + c3 * x[2] - d3
    ])

def J(x):
    a1, b1, c1 = 1, 2, 3
    a2, b2, c2 = 4, 5, 6
    a3, b3, c3 = 7, 8, 9
    return np.array([
        [a1, b1, c1],
        [a2, b2, c2],
        [a3, b3, c3]
    ])

def newton_raphson(F, J, x0, tol=1e-6, max_iter=100, reg=1e-6):
    x = x0
    for i in range(max_iter):
        f = F(x)
        if np.linalg.norm(f) < tol:
            return x
        J_reg = J(x) + reg * np.eye(3)
        J_inv = np.linalg.inv(J_reg)
        x = x - J_inv @ f
    return x

x0 = np.array([0, 0, 0])

solution = newton_raphson(F, J, x0)
print("解为:", solution)
