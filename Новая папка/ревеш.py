def main(a, c):  
    a = list(range(a + 1))
    while len(a) > 1:
        t = c % len(a)
        a = a[t:] + a[:t]
        a.pop()
    return a[0]
        
if __name__ == '__main__':
    n = int(input())
    k = int(input())
    print(main(n, k))
