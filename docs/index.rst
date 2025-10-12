Welcome to Animal Language Documentation
=====================================

**Animal** is a programming language that uses animal sounds and behaviors as programming constructs.

.. image:: https://img.shields.io/badge/version-1.1.0-blue
   :alt: Version 1.1.0

.. code-block:: animal

   howl greet(name) {
       roar "Hello", name
   }

   greet("World")  :: Prints "Hello World"

Features
--------

* **Intuitive Syntax**: Animal sounds replace traditional operators, for example ``meow`` is for addition, ``woof`` is for subtraction etc.
* **Expressive Control Flow**: ``growl``/``sniff``/``wag`` for conditionals, ``leap`` for for-loops, ``pounce`` for while-loops
* **Powerful Data Structures**: Lists with built-in methods and nestable structures
* **Custom Object System**: Define reusable components with the ``nest`` keyword
* **Integrated File I/O**: Read and write files with animal-themed functions

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting-started/installation
   getting-started/quick-start
   getting-started/editor-support
   getting-started/examples

.. toctree::
   :maxdepth: 2
   :caption: Language Reference

   language-reference/syntax
   language-reference/operators
   language-reference/control-flow
   language-reference/functions
   language-reference/data-structures
   language-reference/modules

.. toctree::
   :maxdepth: 2
   :caption: Standard Library

   standard-library/overview
   standard-library/math-functions
   standard-library/list-functions
   standard-library/string-functions
   standard-library/io-functions
   standard-library/audio-functions

.. toctree::
   :maxdepth: 2
   :caption: Development

   development/architecture
   development/benchmarks
   development/contributing
   development/testing
   development/roadmap
