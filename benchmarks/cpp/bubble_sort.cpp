#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers{9, 5, 2, 7, 1, 10, 3};
    std::size_t n = numbers.size();

    while (n > 1) {
        bool swapped = false;
        for (std::size_t i = 0; i + 1 < n; ++i) {
            if (numbers[i] > numbers[i + 1]) {
                std::swap(numbers[i], numbers[i + 1]);
                swapped = true;
            }
        }
        if (!swapped) {
            break;
        }
        --n;
    }

    std::cout << "Sorted: [";
    for (std::size_t i = 0; i < numbers.size(); ++i) {
        std::cout << numbers[i];
        if (i + 1 < numbers.size()) {
            std::cout << ", ";
        }
    }
    std::cout << "]\n";
}
