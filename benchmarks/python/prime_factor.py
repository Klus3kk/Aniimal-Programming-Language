number = 13195
factors = []

divisor = 2
while divisor * divisor <= number:
    if number % divisor == 0:
        factors.append(divisor)
        number //= divisor
    else:
        if divisor == 2:
            divisor = 3
        else:
            divisor += 2

if number > 1:
    factors.append(number)

print("Factors:", factors)
