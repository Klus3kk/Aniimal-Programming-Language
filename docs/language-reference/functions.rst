Functions
=========

In Animal, functions are defined using the ``howl`` keyword, which allows for creating reusable blocks of code.

Defining Functions
----------------

Basic syntax:

.. code-block:: animal

   howl function_name(parameter1, parameter2, ...) {
       // Function body
       // Optional: value sniffback
   }

Example:

.. code-block:: animal

   howl greet(name) {
       roar "Hello,", name
   }

   greet("Simba")  :: Prints "Hello, Simba"

Return Values
-----------

Use the ``sniffback`` keyword to return values from functions:

.. code-block:: animal

   howl add(a, b) {
       result -> a meow b
       result sniffback
   }

   sum -> add(5, 3)  :: sum = 8

You can also return directly without storing in a variable:

.. code-block:: animal

   howl multiply(x, y) {
       x moo y sniffback
   }

Early returns are supported:

.. code-block:: animal

   howl safe_divide(a, b) {
       growl b == 0 {
           "Cannot divide by zero" sniffback
       }

       a drone b sniffback
   }

Parameters
---------

Function parameters follow these rules:

- Parameters are passed by value for primitive types
- Lists and objects are passed by reference
- Parameter names follow the same rules as variable names

Default parameters are not supported in the current version.

Function Scope
------------

Functions create their own local scope:

.. code-block:: animal

   x -> 10  :: Global variable

   howl test() {
       x -> 20  :: Local variable, shadows global x
       roar x   :: Prints 20
   }

   test()
   roar x  :: Prints 10 (global x is unchanged)

Variables defined inside a function are not accessible outside that function.

Recursive Functions
----------------

Animal supports recursive functions:

.. code-block:: animal

   howl factorial(n) {
       growl n <= 1 {
           1 sniffback
       }

       n moo factorial(n woof 1) sniffback
   }

   roar factorial(5)  :: Prints 120

Function Limitations
-----------------

In the current version of Animal:

- Functions cannot be defined inside other functions
- There is no support for anonymous functions/lambdas
- Function overloading is not supported
