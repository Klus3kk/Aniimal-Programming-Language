Architecture
============

This document explains the internal architecture of the Animal language interpreter.

Overview
-------

The Animal interpreter follows a classic language implementation pattern with these major components:

1. **Lexer** - Converts source text into tokens
2. **Parser** - Converts tokens into an Abstract Syntax Tree (AST)
3. **Interpreter** - Executes the AST
4. **Runtime** - Provides the execution environment, standard library, and error handling

The interpreter is implemented in Go (and thanks to it :)) making it fast, portable, and easy to extend.

The lexer (``core/lexer.go``) is responsible for reading the source code and converting it into tokens. 

Key responsibilities:

- Converting source text into a stream of tokens
- Identifying keywords, operators, identifiers, literals, etc.
- Tracking source positions for error reporting
- Handling comments and whitespace

Example:

.. code-block:: animal

   x -> 5 meow 3

Gets converted to tokens:

.. code-block::

   [IDENTIFIER: "x", EQ: "->", INT: "5", PLUS: "meow", INT: "3", EOF]

Each token includes:
- Type (e.g., ``INT``, ``IDENTIFIER``, ``PLUS``)
- Value (the actual text, like ``"x"`` or ``"5"``)
- Position information (line, column) for error reporting

Parser
-----

The parser (``core/parser.go``) takes the tokens from the lexer and builds an Abstract Syntax Tree (AST) according to the language grammar. 

Key responsibilities:

- Implementing the language grammar rules
- Building an AST from tokens
- Reporting syntax errors
- Checking for valid language constructs

The parser uses a recursive descent approach, with functions that handle different grammatical constructs.

Example AST for ``x -> 5 meow 3``:

.. code-block::

   VarAssignNode {
     Var_Name_Tok: Token { Type: "IDENTIFIER", Value: "x" }
     Value_Node: BinOpNode {
       Left_Node: NumberNode { Token: { Type: "INT", Value: "5" } }
       Op_Tok: Token { Type: "PLUS", Value: "meow" }
       Right_Node: NumberNode { Token: { Type: "INT", Value: "3" } }
     }
   }

Interpreter
---------

The interpreter (``core/interpreter.go``) executes the AST by traversing it and performing the appropriate operations.

Key responsibilities:

- Visiting each node in the AST
- Executing the corresponding operations
- Managing variable scope through symbol tables
- Handling runtime errors
- Interacting with the standard library

The interpreter uses the visitor pattern to visit each node in the AST and execute it.

Runtime Environment
----------------

The runtime environment provides the context for program execution:

- **Symbol Table** (``core/symbol_table.go``) - Manages variables and their values
- **Context** (``core/context.go``) - Tracks execution context for error reporting
- **Standard Library** (``core/std/*.go``) - Provides built-in functions

WASM Support
----------

Animal includes WebAssembly (WASM) support (``wasm/main.go``), allowing it to be compiled to WASM and run in browsers.

This enables:
- In-browser Animal interpreters
- Integration with web applications
- Portable code execution

Execution Flow
------------

When you run an Animal program, the following steps occur:

1. The source code is read from a file or REPL input
2. The lexer converts the source code to tokens
3. The parser converts the tokens to an AST
4. The interpreter executes the AST, using:
   - Symbol tables for variable storage
   - Standard library for built-in functions
   - Runtime environment for execution context
5. The result is returned or output is printed

Error Handling
------------

Animal implements comprehensive error handling:

- **Lexical errors** - Invalid characters or unexpected tokens
- **Syntax errors** - Malformed expressions or statements
- **Runtime errors** - Type mismatches, undefined variables, division by zero, etc.

Errors include:
- Descriptive error messages
- Source code location (file, line, column)
- Context information when applicable

Error handling is implemented in ``core/errors.go`` and uses specialized error types.

Code Organization
---------------

The codebase is organized into these main directories:

- ``benchmarks/`` - Performance benchmarks
- ``cmd/animal/`` - Command-line interface entry point
- ``core/`` - Core language implementation
- ``core/std/`` - Standard library functions
- ``docs/`` - Documentation
- ``examples/`` - Example Animal programs
- ``tests/`` - Test suite
- ``wasm/`` - WebAssembly support
