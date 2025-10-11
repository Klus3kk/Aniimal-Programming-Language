# Animal Language

[![Documentation Status](https://readthedocs.org/projects/animal/badge/?version=latest)](https://animal.readthedocs.io/en/latest/?badge=latest)
[![Go Report Card](https://goreportcard.com/badge/github.com/Klus3kk/animal)](https://goreportcard.com/report/github.com/Klus3kk/animal)
[![Release](https://img.shields.io/github/v/release/Klus3kk/animal)](https://github.com/Klus3kk/animal/releases)

Animal is a programming language that uses animal sounds and characteristics as its core syntax elements. It brings a playful way to programming with a complete feature set of basic commands (and also new ones!).

## Quick Start

```bash
go install github.com/Klus3kk/animal/cmd/animal@latest
animal
animal path/to/script.anml
```

Try this simple Animal program:

```animal
roar "Hello from the animal kingdom!"

age -> 5
weight -> 10
total -> age meow weight  

roar "Total:", total
```

## Features

- **Intuitive Syntax**: Programming concepts mapped to animal behaviors
- **Rich Standard Library**: Built-in functions for common operations
- **Object-Oriented**: `nest` structures for custom object definitions
- **Functional Capabilities**: First-class functions with `howl`
- **Web Assembly Support**: Run Animal in browsers
- **Interactive REPL**: Try code snippets instantly

## Documentation

Complete documentation is available at [animal.readthedocs.io](https://animal.readthedocs.io/).

## Core Syntax

### Operators

| Symbol | Animal Word | Meaning        |
|--------|-------------|----------------|
| `+`    | `meow`      | Addition       |
| `-`    | `woof`      | Subtraction    |
| `*`    | `moo`       | Multiplication |
| `/`    | `drone`     | Division       |
| `%`    | `squeak`    | Modulo         |
| `^`    | `soar`      | Exponentiation |
| `==`   | `sniff`     | Equality       |
| `!=`   | `growl`     | Inequality     |

### Control Flow

```animal
-- Conditionals
n -> 5

growl n <= 1 {
    roar 1 
} wag {
    roar n moo n 
}


-- Loops
leap i from 0 to 5 {
    roar i
}

-- Functions
howl calculate_area(length, width) {
    length moo width sniffback  -- Multiplication
}

area -> calculate_area(5, 10)
roar "Area:", area
```

## Installation

### Prerequisites

- Go 1.18 or higher

### From Source

```bash
# Clone the repository
git clone https://github.com/Klus3kk/animal.git
cd animal

# Build from source
go build -o animal ./cmd/animal

# Run the tests
go test ./...
```

### From Go Install

```bash
go install github.com/Klus3kk/animal/cmd/animal@latest
```

## Online Compiler

Try Animal without installation using [online compiler](https://animal-lang.github.io/animal-playground).

## Examples

### Simple Calculator

```animal
howl calculator() {
    roar "Simple Calculator"
    roar "Enter first number:"
    num1 -> input_number()
    
    roar "Enter second number:"
    num2 -> input_number()
    
    roar "Sum:", num1 meow num2
    roar "Difference:", num1 woof num2
    roar "Product:", num1 moo num2
    roar "Quotient:", num1 drone num2
}

calculator()
```
