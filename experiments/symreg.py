import numpy as np


def target_poly(x, n_degrees):
    sum = 0
    for i in range(n_degrees):
        sum += np.power(x, i+1)
    return sum


def target_nguyen7(x):
    return np.log(x+1) + np.log(np.power(x, 2)+1)

def target_nguyen10(x):
    return 2 * np.sin(x[:,0]) * np.cos(x[:, 1])


def target_vladislasleva4(x):
    res = np.atleast_2d(np.power(x[:, 0] - 3, 2) + np.power(x[:, 1] - 3, 2) + np.power(x[:, 2] - 3, 2) +
                        np.power(x[:, 3] - 3, 2) + np.power(x[:, 4] - 3, 2))
    return 10/(5+res)


def target_pagie1(x):
    res = np.atleast_2d((1/(1+np.power(x[:, 0], -4))) + (1/(1+np.power(x[:, 1], -4))))
    return res


def target_korns1(x):
    res = np.atleast_2d(1.57 + (24.3*x[:, 3]))
    return res


def target_korns2(x):
    res = np.atleast_2d(0.23 + (14.2*((x[:, 3]+x[:, 1])/(3.0*x[:, 4]))))
    return res


def target_korns3(x):
    res = np.atleast_2d(-5.41 + (4.9*(((x[:, 3]-x[:, 0])+(x[:, 1]/x[:, 4]))/(3*x[:, 4]))))
    return res


def target_korns4(x):
    res = np.atleast_2d(-2.3 + (0.13*np.sin(x[:, 2])))
    return res


def target_korns5(x):
    res = np.atleast_2d(3.0 + (2.13*np.log(np.abs(x[:, 4]))))
    return res


def target_korns6(x):
    res = np.atleast_2d(1.3 + (0.13*np.sqrt(np.abs(x[:, 0]))))
    return res


def target_korns7(x):
    res = np.atleast_2d(213.80940889-(213.80940889*np.exp(-0.54723748542*x[:, 0])))
    return res


def target_korns8(x):
    res = np.atleast_2d(6.87 +(11*np.sqrt(np.abs(7.23*x[:, 0]*x[:, 3]*x[:, 4]))))
    return res


def target_korns9(x):
    res = np.atleast_2d((np.sqrt(np.abs(x[:, 0]))/np.log(np.abs(x[:, 1])))*(np.exp(x[:, 2])/np.power(x[:, 3], 2)))
    return res


def target_korns10(x):
    res = np.atleast_2d(0.81+(24.3*(((2.0*x[:, 1])+(3*np.power(x[:, 2], 2)))/(4*np.power(x[:, 3], 3) +
                                                                              5*np.power(x[:, 4], 4)))))
    return res


def target_korns11(x):
    res = np.atleast_2d(6.87 + (11*np.cos(7.23*np.power(x[:, 0], 3))))
    return res


def target_korns12(x):
    res = np.atleast_2d(2 - 2.1*np.cos(9.8*x[:, 3])*np.sin(1.3*x[:, 2]))
    return res


def target_korns13(x):
    res = np.atleast_2d(32 - (3*((np.tan(x[:, 0])/np.tan(x[:, 1]))*(np.tan(x[:, 2])/np.tan(x[:, 3])))))
    return res


def target_korns14(x):
    res = np.atleast_2d(22 - (4.2*((np.cos(x[:, 0])-np.tan(x[:, 1]))*(np.tanh(x[:, 2])/np.sin(x[:, 3])))))
    return res


def target_korns15(x):
    res = np.atleast_2d(12 - (6*((np.tan(x[:, 0])/np.exp(x[:, 1]))*(np.log(np.abs(x[:, 2]))-np.tan(x[:, 3])))))
    return res


def target_keijzer1(x):
    res = np.atleast_2d(0.3*x*np.sin(2*np.pi*x))
    return res


def target_keijzer2(x):
    res = np.atleast_2d(np.power(x, 3)*np.exp(-x)*np.cos(x)*np.sin(x)*(np.sin(np.sin(x))*np.cos(x) - 1))
    return res


def target_keijzer3(x):
    res = np.atleast_2d((30*x[:, 0]*x[:, 2])/((x[:, 0] - 10)*np.power(x[:, 1],2)))
    return res


def target_keijzer4(x):
    res = np.array([np.sum(1/np.array(range(1, i))) for i in x[:, 0]], ndmin=2)
    return res


def target_keijzer5(x):
    res = np.atleast_2d(np.log(x))
    return res


def target_keijzer6(x):
    res = np.atleast_2d(np.sqrt(x))
    return res


def target_keijzer7(x):
    res = np.atleast_2d(np.arcsinh(x))
    return res


def target_keijzer8(x):
    res = np.atleast_2d(np.power(x[:, 0], x[:, 1]))
    return res


def target_keijzer9(x):
    res = np.atleast_2d(x[:, 0]*x[:, 1] + np.sin((x[:, 0]-1)*(x[:, 1]-1)))
    return res


def target_keijzer10(x):
    res = np.atleast_2d(np.power(x[:, 0], 4)-np.power(x[:, 0], 3)+np.power(x[:, 1], 2)/2 - x[:, 1])
    return res


def target_keijzer11(x):
    res = np.atleast_2d(6*np.sin(x[:, 0])*np.cos(x[:, 1]))
    return res


def target_keijzer12(x):
    res = np.atleast_2d(8.0/(2 + np.power(x[:, 0], 2) + np.power(x[:, 1], 2)))
    return res


def target_keijzer13(x):
    res = np.atleast_2d(np.power(x[:, 0], 3)/5 + np.power(x[:, 1], 3)/2 - x[:, 1] - x[:, 0])
    return res


def get_benchmark_poly(rand, n_degrees):
    train_x = np.array([(rand.random()*2 - 1) for i in range(20)], ndmin=2).transpose()
    train_y = target_poly(train_x, n_degrees)
    return train_x, train_y, train_x, train_y


def get_benchmark_nguyen7(rand, n_degrees):
    train_x = np.array([(rand.random() * 2) for i in range(20)], ndmin=2).transpose()
    train_y = target_nguyen7(train_x)
    return train_x, train_y, train_x, train_y

def get_benchmark_nguyen10(rand, n_degrees):
    train_x = np.array([(rand.random() * 2 - 1, rand.random() * 2 - 1) for i in range(100)])
    train_y = target_nguyen10(train_x)
    return train_x, train_y, train_x, train_y


def get_benchmark_constant(rand, n_degrees):
    train_x = np.array([(rand.random() * 2) for i in range(20)], ndmin=2).transpose() - 1
    train_y = target_nguyen5(train_x)
    train_y[:] = 314.159
    return train_x, train_y, train_x, train_y


def get_benchmark_keijzer(rand, n_degrees):
    if n_degrees == 1:
        train_x = np.arange(-1, 1, 0.1)
        train_y = target_keijzer1(train_x).transpose()
        test_x = np.arange(-1, 1, 0.001)
        test_y = target_keijzer1(test_x).transpose()
    elif n_degrees == 2:
        train_x = np.arange(-2, 2, 0.1)
        train_y = target_keijzer1(train_x).transpose()
        test_x = np.arange(-2, 2, 0.001)
        test_y = target_keijzer1(test_x).transpose()
    elif n_degrees == 3:
        train_x = np.arange(-3, 3, 0.1)
        train_y = target_keijzer1(train_x).transpose()
        test_x = np.arange(-3, 3, 0.001)
        test_y = target_keijzer1(test_x).transpose()
    elif n_degrees == 4:
        train_x = np.arange(0, 10, 0.05)
        train_y = target_keijzer2(train_x).transpose()
        test_x = np.arange(0.05, 10.05, 0.05)
        test_y = target_keijzer2(test_x).transpose()
    elif n_degrees == 5:
        train_x = np.array([[rand.random() * 2 - 1,
                             rand.random() + 1,
                             rand.random() * 2 - 1] for i in range(1000)], ndmin=2)
        train_y = target_keijzer3(train_x).transpose()
        test_x = np.array([[rand.random() * 2 - 1,
                             rand.random() + 1,
                             rand.random() * 2 - 1] for i in range(10000)], ndmin=2)
        test_y = target_keijzer3(test_x).transpose()
    elif n_degrees == 6:
        train_x = np.atleast_2d(np.arange(1, 50, 1)).transpose()
        train_y = target_keijzer4(train_x).transpose()
        test_x = np.atleast_2d(np.arange(1, 120, 1)).transpose()
        test_y = target_keijzer4(test_x).transpose()
    elif n_degrees == 7:
        train_x = np.arange(1, 100, 1)
        train_y = target_keijzer5(train_x).transpose()
        test_x = np.arange(1, 100, 0.1)
        test_y = target_keijzer5(test_x).transpose()
    elif n_degrees == 8:
        train_x = np.arange(1, 100, 1)
        train_y = target_keijzer6(train_x).transpose()
        test_x = np.arange(1, 100, 0.1)
        test_y = target_keijzer6(test_x).transpose()
    elif n_degrees == 9:
        train_x = np.arange(1, 100, 1)
        train_y = target_keijzer7(train_x).transpose()
        test_x = np.arange(1, 100, 0.1)
        test_y = target_keijzer7(test_x).transpose()
    elif n_degrees == 10:
        train_x = np.array([[rand.random(),
                             rand.random()] for i in range(100)], ndmin=2)
        train_y = target_keijzer8(train_x).transpose()
        xv, yv = np.meshgrid(np.arange(0, 1, 0.01), np.arange(0, 1, 0.01))
        test_x = np.array([xv.flatten(), yv.flatten()]).T
        test_y = target_keijzer8(test_x).transpose()
    elif n_degrees == 11:
        train_x = np.array([[rand.random()*6 - 3,
                             rand.random()*6 - 3] for i in range(20)], ndmin=2)
        train_y = target_keijzer9(train_x).transpose()
        xv, yv = np.meshgrid(np.arange(-3, 3, 0.1), np.arange(-3, 3, 0.1))
        test_x = np.array([xv.flatten(), yv.flatten()]).T
        test_y = target_keijzer9(test_x).transpose()
    elif n_degrees == 12:
        train_x = np.array([[rand.random()*6 - 3,
                             rand.random()*6 - 3] for i in range(20)], ndmin=2)
        train_y = target_keijzer10(train_x).transpose()
        xv, yv = np.meshgrid(np.arange(-3, 3, 0.1), np.arange(-3, 3, 0.1))
        test_x = np.array([xv.flatten(), yv.flatten()]).T
        test_y = target_keijzer10(test_x).transpose()
    elif n_degrees == 13:
        train_x = np.array([[rand.random()*6 - 3,
                             rand.random()*6 - 3] for i in range(20)], ndmin=2)
        train_y = target_keijzer11(train_x).transpose()
        xv, yv = np.meshgrid(np.arange(-3, 3, 0.1), np.arange(-3, 3, 0.1))
        test_x = np.array([xv.flatten(), yv.flatten()]).T
        test_y = target_keijzer11(test_x).transpose()
    elif n_degrees == 14:
        train_x = np.array([[rand.random()*6 - 3,
                             rand.random()*6 - 3] for i in range(20)], ndmin=2)
        train_y = target_keijzer12(train_x).transpose()
        xv, yv = np.meshgrid(np.arange(-3, 3, 0.1), np.arange(-3, 3, 0.1))
        test_x = np.array([xv.flatten(), yv.flatten()]).T
        test_y = target_keijzer12(test_x).transpose()
    elif n_degrees == 15:
        train_x = np.array([[rand.random()*6 - 3,
                             rand.random()*6 - 3] for i in range(20)], ndmin=2)
        train_y = target_keijzer13(train_x).transpose()
        xv, yv = np.meshgrid(np.arange(-3, 3, 0.1), np.arange(-3, 3, 0.1))
        test_x = np.array([xv.flatten(), yv.flatten()]).T
        test_y = target_keijzer13(test_x).transpose()
    else:
        print('Degree %d not defined for this problem.' %n_degrees)
    return train_x, train_y, test_x, test_y


def get_benchmark_korns(rand, n_degrees):
    train_x = np.array([[rand.random() * 100 - 50,
                         rand.random() * 100 - 50,
                         rand.random() * 100 - 50,
                         rand.random() * 100 - 50,
                         rand.random() * 100 - 50] for i in range(10000)])
    test_x = np.array([[rand.random() * 100 - 50,
                         rand.random() * 100 - 50,
                         rand.random() * 100 - 50,
                         rand.random() * 100 - 50,
                         rand.random() * 100 - 50] for i in range(10000)])
    if n_degrees == 1:
        train_y = target_korns1(train_x).transpose()
        test_y = target_korns1(test_x).transpose()
    elif n_degrees == 2:
        train_y = target_korns2(train_x).transpose()
        test_y = target_korns2(test_x).transpose()
    elif n_degrees == 3:
        train_y = target_korns3(train_x).transpose()
        test_y = target_korns3(test_x).transpose()
    elif n_degrees == 4:
        train_y = target_korns4(train_x).transpose()
        test_y = target_korns4(test_x).transpose()
    elif n_degrees == 5:
        train_y = target_korns5(train_x).transpose()
        test_y = target_korns5(test_x).transpose()
    elif n_degrees == 6:
        train_y = target_korns6(train_x).transpose()
        test_y = target_korns6(test_x).transpose()
    elif n_degrees == 7:
        train_y = target_korns7(train_x).transpose()
        test_y = target_korns7(test_x).transpose()
    elif n_degrees == 8:
        train_y = target_korns8(train_x).transpose()
        test_y = target_korns8(test_x).transpose()
    elif n_degrees == 9:
        train_y = target_korns9(train_x).transpose()
        test_y = target_korns9(test_x).transpose()
    elif n_degrees == 10:
        train_y = target_korns10(train_x).transpose()
        test_y = target_korns10(test_x).transpose()
    elif n_degrees == 11:
        train_y = target_korns11(train_x).transpose()
        test_y = target_korns11(test_x).transpose()
    elif n_degrees == 12:
        train_y = target_korns12(train_x).transpose()
        test_y = target_korns12(test_x).transpose()
    elif n_degrees == 13:
        train_y = target_korns13(train_x).transpose()
        test_y = target_korns13(test_x).transpose()
    elif n_degrees == 14:
        train_y = target_korns14(train_x).transpose()
        test_y = target_korns14(test_x).transpose()
    elif n_degrees == 15:
        train_y = target_korns15(train_x).transpose()
        test_y = target_korns16(test_x).transpose()
    else:
        print('No problem Korns-%s' %n_degrees)

    return train_x, train_y, test_x, test_y


def get_benchmark_vladislasleva4(rand, n_degrees):
    train_x = np.array([[rand.random() * 6 + 0.05,
                         rand.random() * 6 + 0.05,
                         rand.random() * 6 + 0.05,
                         rand.random() * 6 + 0.05,
                         rand.random() * 6 + 0.05] for i in range(1024)])

    train_y = target_vladislasleva4(train_x).transpose()
    test_x = np.array([[rand.random() * 6.6 - 0.25,
                         rand.random() * 6.6 - 0.25,
                         rand.random() * 6.6 - 0.25,
                         rand.random() * 6.6 - 0.25,
                         rand.random() * 6.6 - 0.25] for i in range(5000)])

    test_y = target_vladislasleva4(test_x).transpose()
    return train_x, train_y, test_x, test_y


def get_benchmark_pagie1(rand, n_degrees):
    cntr = 0
    train_x = np.zeros([529, 2])
    for i in np.arange(-4, 5, 0.4):
        for j in np.arange(-4, 5, 0.4):
            train_x[cntr, 0] = i
            train_x[cntr, 1] = j
            cntr += 1
    train_y = target_pagie1(train_x).transpose()
    return train_x, train_y, train_x, train_y

def get_benchmark_constant(rand, n_degrees):
    train_x = np.array([(rand.random() * 2) for i in range(20)], ndmin=2).transpose() - 1
    train_y = target_nguyen5(train_x)
    train_y[:] = 314.159
    return train_x, train_y, train_x, train_y

def get_benchmark_multivar(rand, n_degrees):
    np.random.seed(int(rand.random()*100))
    train_x = np.random.rand(100, n_degrees)
    train_y = np.atleast_2d(np.sum(np.sin(train_x), 1)).transpose()
    test_x = np.random.rand(100, n_degrees)
    test_y = np.atleast_2d(np.sum(np.sin(train_x), 1)).transpose()
    return train_x, train_y, test_x, test_y

if __name__ == "__main__":
    import random
    print(get_benchmark_multivar(random.Random(), 10))
