import numpy as np

X = np.array([[3,4,5],[2,1,7], [1,1,1]])
x0 = X[0,:]
x1 = X[1,:]
x2 = X[2,:]

def fadd(x, y):
    return x + y

def fmul(x, y):
    return x * y

def fsub(x, y):
    return x - y

def p(c):
    return np.sin(np.pi*c)

0.1*fadd(p(0.9)*x1, p(0.3)*x1) + 0.9*fmul(p(0.1)*x2, p(0.7)*x2)

0.9*fmul(p(0.1)*x2, p(0.7)*x2) + 0.1*fsub(p(0.9)*x1, p(0.3)*x1)

0.8*fmul(p(0.1)*x2, p(0.7)*x2) + 0.2*fsub(p(0.9)*x1, p(0.3)*x1)

0.7*fmul(p(0.1)*x2, p(0.7)*x2) + 0.3*fsub(p(0.9)*x1, p(0.3)*x1)

0.6*fmul(p(0.1)*x2, p(0.7)*x2) + 0.4*fsub(p(0.9)*x1, p(0.3)*x1)

0.5*fmul(p(0.1)*x2, p(0.7)*x2) + 0.5*fsub(p(0.9)*x1, p(0.3)*x1)

0.4*fmul(p(0.9)*x1, p(0.3)*x1) + 0.6*fsub(p(0.1)*x2, p(0.7)*x2)
