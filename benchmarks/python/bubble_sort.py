numbers = [9, 5, 2, 7, 1, 10, 3]

n = len(numbers)
while n > 1:
    swapped = False
    for i in range(n - 1):
        if numbers[i] > numbers[i + 1]:
            numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]
            swapped = True
    if not swapped:
        break
    n -= 1

print("Sorted:", numbers)
