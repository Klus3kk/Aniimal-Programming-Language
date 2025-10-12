#include <iostream>

int main() {
    constexpr int limit = 35;
    long long prev = 0;
    long long curr = 1;

    for (int i = 0; i <= limit; ++i) {
        if (i == 0) {
            // do nothing, prev already 0
        } else if (i == 1) {
            // do nothing, curr already 1
        } else {
            long long next = prev + curr;
            prev = curr;
            curr = next;
        }
    }

    std::cout << "Fib " << limit << " = " << curr << '\n';
}
