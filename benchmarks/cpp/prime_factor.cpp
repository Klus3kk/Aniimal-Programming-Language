#include <iostream>
#include <vector>

int main() {
    long long number = 13195;
    std::vector<long long> factors;

    long long divisor = 2;
    while (divisor * divisor <= number) {
        if (number % divisor == 0) {
            factors.push_back(divisor);
            number /= divisor;
        } else {
            if (divisor == 2) {
                divisor = 3;
            } else {
                divisor += 2;
            }
        }
    }

    if (number > 1) {
        factors.push_back(number);
    }

    std::cout << "Factors: [";
    for (std::size_t i = 0; i < factors.size(); ++i) {
        std::cout << factors[i];
        if (i + 1 < factors.size()) {
            std::cout << ", ";
        }
    }
    std::cout << "]\n";
}
