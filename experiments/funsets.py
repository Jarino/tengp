import numpy as np

from tengp import FunctionSet

def pdivide(x, y):
    return np.divide(x, y, out=np.copy(x), where=y!=0)

def plog(x, y):
    return np.log(x, out=np.copy(x), where=x>0)

def psin(x, y):
    return np.sin(x)

def pcos(x, y):
    return np.cos(x)

def ppower(x, y):
    return np.power(x, y, out=np.copy(x), where=x>0|np.equal(np.mod(y, 1), 0), casting='unsafe')

def pow2(x, y):
    return x**2

def pow3(x, y):
    return x**3

def ptan(x, y):
    return np.tan(x)

def ptanh(x, y):
    return np.tanh(x)

def psqrt(x, y):
    return  np.sqrt(x, out=np.copy(x), where=x>0)

def pexp(x, y):
    return np.exp(x)

def pow_minus1(x, y):
    x = np.array(x, dtype=float)
    return np.power(x, -1, out=np.copy(x), where=x!=0)

def identity(x, y):
    return x

nguyen7_funset = FunctionSet()
nguyen7_funset.add(np.add, 2)
nguyen7_funset.add(np.subtract, 2)
nguyen7_funset.add(np.multiply, 2)
nguyen7_funset.add(pdivide, 2)
nguyen7_funset.add(plog, 2)
nguyen7_funset.add(psin, 2)
nguyen7_funset.add(pcos, 2)

nguyen7_funset_with_identity = FunctionSet()
nguyen7_funset_with_identity.add(identity, 2)
nguyen7_funset_with_identity.add(np.add, 2)
nguyen7_funset_with_identity.add(np.subtract, 2)
nguyen7_funset_with_identity.add(np.multiply, 2)
nguyen7_funset_with_identity.add(pdivide, 2)
nguyen7_funset_with_identity.add(plog, 2)
nguyen7_funset_with_identity.add(psin, 2)
nguyen7_funset_with_identity.add(pcos, 2)



keijzer_funset = FunctionSet()
keijzer_funset.add(np.add, 2)
keijzer_funset.add(np.multiply, 2)
keijzer_funset.add(psin, 2)
keijzer_funset.add(pcos, 2)
keijzer_funset.add(psqrt, 2)
keijzer_funset.add(plog, 2)
keijzer_funset.add(pow_minus1, 2)


korns_funset = FunctionSet()
korns_funset.add(np.add, 2)
korns_funset.add(np.subtract, 2)
korns_funset.add(np.multiply, 2)
korns_funset.add(pdivide, 2)
korns_funset.add(psin, 2)
korns_funset.add(pcos, 2)
korns_funset.add(ptan, 2)
korns_funset.add(ptanh, 2)
korns_funset.add(psqrt, 2)
korns_funset.add(pexp, 2)
korns_funset.add(plog, 2)
korns_funset.add(pow2, 2)
korns_funset.add(pow3, 2)

vlad_funset = FunctionSet()
vlad_funset.add(np.add, 2)
vlad_funset.add(np.subtract, 2)
vlad_funset.add(np.multiply, 2)
vlad_funset.add(pdivide, 2)
vlad_funset.add(ppower, 2)
vlad_funset.add(psin, 2)
vlad_funset.add(pcos, 2)
vlad_funset.add(psqrt, 2)
vlad_funset.add(pexp, 2)
vlad_funset.add(plog, 2)
vlad_funset.add(pow_minus1, 2)

pagie_funset = FunctionSet()
pagie_funset.add(np.add, 2)
pagie_funset.add(np.subtract, 2)
pagie_funset.add(np.multiply, 2)
pagie_funset.add(pdivide, 2)
pagie_funset.add(ppower, 2)
pagie_funset.add(psqrt, 2)
pagie_funset.add(plog, 2)
pagie_funset.add(pow_minus1, 2)
