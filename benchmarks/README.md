# Benchmarks

This directory collects small benchmark programs for comparing Animal against Python and C++.
Each algorithm lives in three files with matching names inside the `animal/`, `python/`, and
`cpp/` subdirectories.

Provided algorithms:

- `bubble_sort` – naive O(n²) sort over an integer slice
- `fibonacci` – iterative Fibonacci sequence up to N
- `prime_factor` – trial division prime factorisation for a single integer

## Running the programs yourself

1. Build the Animal interpreter locally (`go build -o animal ./cmd/animal`) if you do not
   already have the CLI on your PATH.
2. Compile the C++ sources using any modern compiler, e.g.:

   ```bash
   g++ -O3 cpp/bubble_sort.cpp -o cpp/bubble_sort
   g++ -O3 cpp/fibonacci.cpp -o cpp/fibonacci
   g++ -O3 cpp/prime_factor.cpp -o cpp/prime_factor
   ```

3. Run the benchmarks:

   ```bash
   ./animal benchmarks/animal/bubble_sort.anml
   python3 benchmarks/python/bubble_sort.py
   ./benchmarks/cpp/bubble_sort  # after compilation
   ```

   Repeat for the other algorithms.

Feel free to adapt the input sizes or wrap these scripts in your preferred timing harness.
They intentionally print basic results so you can verify behaviour before timing.
