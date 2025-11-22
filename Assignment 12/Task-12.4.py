import math

def f(x):
    return 2 * x**3 + 4 * x + 5

def df(x):
    return 6 * x**2 + 4

def gradient_descent(
    lr=1e-4,           # Very small learning rate for safety
    n_iter=10000,      # Number of iterations
    clip_value=100.0,  # Clip gradients within [-clip_value, clip_value]
    x_clip=1e2         # Cap |x| to avoid explosion
):
    x = 0.0
    for i in range(n_iter):
        grad = df(x)
        # Gradient Clipping
        grad = max(min(grad, clip_value), -clip_value)
        x = x - lr * grad
        # Prevent x from growing too large
        x = max(min(x, x_clip), -x_clip)
        # Optional: break if gradient is very small (close to minimum)
        if abs(grad) < 1e-8:
            break
    return x

if __name__ == "__main__":
    min_x = gradient_descent()
    print(f"Minimum at x ≈ {min_x}")
    print(f"f(x) ≈ {f(min_x)}")



