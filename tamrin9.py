n= 2
c = [[0 for j in range(n)] for i in range(n)]
a = [[2,3],
     [3,4]]

b = [[2,3],
     [3,4]]

for i in range(n):
    for j in range(n):
        for k in range(n):
            c[i][j] += a[i][k] * b[k][j]

print(c)