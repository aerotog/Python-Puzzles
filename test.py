from multiprocessing import Pool

def f(y):
    return y**y

if __name__ == '__main__':
    p = Pool(5)
    print(p.map(f, [1, 2, 3]))