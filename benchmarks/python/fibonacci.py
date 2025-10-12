limit = 35
prev, curr = 0, 1

for i in range(limit + 1):
    if i == 0:
        continue_value = prev
    elif i == 1:
        continue_value = curr
    else:
        next_val = prev + curr
        prev, curr = curr, next_val
        continue_value = curr

print(f"Fib {limit} = {curr}")
