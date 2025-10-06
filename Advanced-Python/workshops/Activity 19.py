# Question 7
def F7(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return F7(n-1) + F7(n-2)

n = int(input("entrer un nombre: "))
print(F7(n))
