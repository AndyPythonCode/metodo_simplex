def f(numero):
    for i in range(numero):
        yield [1 if i == k else 0 for k in range(numero)]

a = f(5)

print(next(a))
print(next(a))

a = "24"

print(a.find("."))