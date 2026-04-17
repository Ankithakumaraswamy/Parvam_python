import numpy as np

# ─── 1. Array Creation ───────────────────────────────────────────
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# ─── 2. Basic Arithmetic (element-wise) ─────────────────────────
add      = a + b           # [11, 22, 33, 44, 55]
subtract = b - a           # [ 9, 18, 27, 36, 45]
multiply = a * b           # [10, 40, 90, 160, 250]
divide   = b / a           # [10., 10., 10., 10., 10.]
power    = a ** 2          # [ 1,  4,  9, 16, 25]
modulo   = b % 3           # [ 1,  2,  0,  1,  2]
floor_div = b // 3         # [ 3,  6, 10, 13, 16]

# ─── 3. Scalar Broadcasting ─────────────────────────────────────
scaled   = a * 5           # [ 5, 10, 15, 20, 25]
shifted  = a + 100         # [101, 102, 103, 104, 105]
centered = a - np.mean(a)  # [-2., -1.,  0.,  1.,  2.]

# ─── 4. Matrix Operations ────────────────────────────────────────
mat_mul  = A @ B                  # matrix multiplication
dot_prod = np.dot(A, B)           # same as @
transpose = A.T                   # [[1,3],[2,4]]
det       = np.linalg.det(A)      # determinant: -2.0
inv       = np.linalg.inv(A)      # inverse matrix
trace     = np.trace(A)           # sum of diagonal: 5
rank      = np.linalg.matrix_rank(A)

# ─── 5. Linear Algebra ───────────────────────────────────────────
eigenvalues, eigenvectors = np.linalg.eig(A)
U, S, Vt = np.linalg.svd(A)                    # SVD decomposition
L = np.linalg.cholesky(np.array([[4,2],[2,3]])) # Cholesky decomp

# Solve system of equations: Ax = b_vec
A_sys  = np.array([[2, 1], [5, 3]], dtype=float)
b_vec  = np.array([8, 13], dtype=float)
x_sol  = np.linalg.solve(A_sys, b_vec)          # [11., -14.]

# ─── 6. Aggregate / Reduction ────────────────────────────────────
total    = np.sum(a)           # 15
product  = np.prod(a)          # 120
cumsum   = np.cumsum(a)        # [ 1,  3,  6, 10, 15]
cumprod  = np.cumprod(a)       # [ 1,  2,  6, 24, 120]
diff     = np.diff(a)          # [1, 1, 1, 1]

# Axis-wise on 2D
row_sums = np.sum(A, axis=1)   # sum each row
col_sums = np.sum(A, axis=0)   # sum each column

# ─── 7. Statistical Functions ────────────────────────────────────
data = np.array([4, 8, 15, 16, 23, 42])
mean      = np.mean(data)
median    = np.median(data)
std       = np.std(data)
variance  = np.var(data)
p25, p75  = np.percentile(data, [25, 75])
iqr       = p75 - p25
z_scores  = (data - mean) / std       # standardize

# ─── 8. Trigonometry ─────────────────────────────────────────────
angles = np.array([0, 30, 45, 60, 90])
rad    = np.radians(angles)
sin_v  = np.sin(rad)
cos_v  = np.cos(rad)
tan_v  = np.tan(rad)
arcsin = np.arcsin(sin_v)             # back to radians
deg    = np.degrees(arcsin)           # back to degrees

# ─── 9. Exponential & Logarithm ──────────────────────────────────
x     = np.array([1, 2, 4, 8, 16])
exp_v = np.exp(x)                     # e^x
log_n = np.log(x)                     # natural log
log2  = np.log2(x)                    # log base 2
log10 = np.log10(x)                   # log base 10
sqrt  = np.sqrt(x)                    # square root
cbrt  = np.cbrt(x)                    # cube root
abs_v = np.abs(np.array([-3,-1,0,1,3]))

# ─── 10. Rounding ────────────────────────────────────────────────
vals    = np.array([1.234, 2.567, -3.891])
rounded = np.round(vals, 1)    # [1.2, 2.6, -3.9]
floored = np.floor(vals)       # [1., 2., -4.]
ceiled  = np.ceil(vals)        # [2., 3., -3.]
clipped = np.clip(data, 10, 30) # cap values to [10, 30]

# ─── 11. Complex Numbers ─────────────────────────────────────────
z = np.array([1+2j, 3-4j, -1+1j])
real_part = np.real(z)
imag_part = np.imag(z)
modulus   = np.abs(z)          # magnitude
conjugate = np.conj(z)
angle     = np.angle(z)        # phase in radians

# ─── 12. Polynomial Operations ───────────────────────────────────
# Coefficients for 2x³ - 3x² + x - 5
coeffs    = np.array([2, -3, 1, -5])
roots     = np.roots(coeffs)             # find roots
evaluated = np.polyval(coeffs, 3)        # evaluate at x=3 → 25
p1        = np.array([1, 2])             # x + 2
p2        = np.array([1, -1])            # x - 1
poly_prod = np.polymul(p1, p2)           # (x+2)(x-1) = x²+x-2
poly_der  = np.polyder(coeffs)           # derivative
poly_int  = np.polyint(coeffs)           # indefinite integral

# ─── 13. Random Math ─────────────────────────────────────────────
rng     = np.random.default_rng(seed=42)
uniform = rng.uniform(0, 1, size=5)     # uniform distribution
normal  = rng.normal(0, 1, size=5)      # standard normal
randint = rng.integers(1, 100, size=5)  # random integers

# ─── Quick Print Summary ─────────────────────────────────────────
print("=== Basic Arithmetic ===")
print(f"  add:       {add}")
print(f"  power:     {power}")
print("\n=== Matrix ===")
print(f"  A @ B:\n{mat_mul}")
print(f"  det(A):    {det:.1f}")
print(f"  eigenvals: {eigenvalues}")
print("\n=== Stats ===")
print(f"  mean:   {mean:.2f}, median: {median:.1f}, std: {std:.2f}")
print(f"  IQR:    {iqr:.1f}")
print("\n=== Trig (sin 0°→90°) ===")
print(f"  sin: {np.round(sin_v, 3)}")
print("\n=== Polynomial 2x³-3x²+x-5 ===")
print(f"  roots:  {np.round(roots, 3)}")
print(f"  at x=3: {evaluated}")