import math

def area(shape: str, *dims: float) -> float:
    key = shape.strip().lower()
    if key == "circle":
        r, = dims; return math.pi * r * r
    if key == "rectangle":
        l, w = dims; return l * w
    if key == "square":
        s, = dims; return s * s
    if key == "triangle":
        b, h = dims; return 0.5 * b * h
    if key == "trapezoid":
        a, b, h = dims; return 0.5*(a+b)*h
    if key == "ellipse":
        a, b = dims; return math.pi*a*b
    raise ValueError("Unsupported shape")

def prompt_one_shot():
    while True:
        shape = input("Shape (or q to quit): ").strip()
        if shape.lower() in ("q","quit"):
            break
        s = input("Enter dimensions separated by spaces (e.g. \"3\" or \"4 5\"): ").strip()
        if s.lower() in ("q","quit"):
            break
        try:
            dims = tuple(float(x) for x in s.split())
            a = area(shape, *dims)
        except Exception as e:
            print("Error:", e); continue
        print(f"{shape.title()} area = {a:.4f}\n")

if __name__ == "__main__":
    prompt_one_shot()