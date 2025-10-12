String Functions
================

Animal ships with a collection of built-in helpers for manipulating text. Because strings are used for both user interaction and symbolic error messages, these helpers are available everywhere without any imports.

Operators
---------

``purr``
   Concatenation operator. Joins two strings together.

   .. code-block:: animal

      greeting -> "Hello"
      name -> " Lynx"
      roar greeting purr name          :: Hello Lynx

Core Functions
--------------

``nuzzle(text1, text2)``
   Function form of concatenation. Accepts strings or lists; when lists are passed they are concatenated as well.

   .. code-block:: animal

      roar nuzzle("Animal ", "Kingdom")    :: Animal Kingdom
      merged -> nuzzle([1, 2], [3])        :: [1, 2, 3]

``pelt(value, times)``
   Repeats *value* ``times`` and returns the concatenated string. ``value`` is converted to a string automatically.

   .. code-block:: animal

      roar pelt("*", 5)     :: *****
      roar pelt(42, 3)      :: 424242

``rat(text)``
   Returns an uppercase version of *text*.

   .. code-block:: animal

      roar rat("howl softly")     :: HOWL SOFTLY

``mole(text)``
   Returns a lowercase version of *text*.

   .. code-block:: animal

      roar mole("LOUD PACK")      :: loud pack

``snipe(text, symbol = " ")``
   Trims leading and trailing instances of *symbol* (defaults to whitespace).

   .. code-block:: animal

      roar snipe("  padded  ")    :: padded
      roar snipe("--alpha--", "-"):: alpha

``ferret(text, start, length)``
   Extracts a substring beginning at *start* with *length* characters.

   .. code-block:: animal

      roar ferret("snowleopard", 4, 3)   :: leo

``badger(text, needle)``
   Returns ``true`` when *needle* occurs in *text*, otherwise ``false``.

   .. code-block:: animal

      growl badger("lynx den", "lynx") {
          roar "Found it!"
      }

``squirrel(text, delimiter)``
   Splits *text* using *delimiter* and returns a list of segments.

   .. code-block:: animal

      words -> squirrel("alpha,beta,gamma", ",")
      roar words       :: ["alpha", "beta", "gamma"]

``parrot(list)``
   Joins every element of *list* (which must contain only strings) into a single string.

   .. code-block:: animal

      pack -> ["lynx", "otter", "mink"]
      roar parrot(pack)   :: lynxottermink

Conversion Helpers
------------------

Several string helpers interact with numbers. They live in the math module but are frequently used when working with strings:

``purr(number, base)``
   Converts a number to a string representation in the supplied *base* (2–36).

``scent(text, base)``
   Parses *text* as a number written in the supplied *base*.

See :doc:`math-functions` for full examples.

Putting It Together
-------------------

The following snippet demonstrates several helpers in tandem:

.. code-block:: animal

   input -> "  lynx,otter,Mink  "
   clean -> snipe(mole(input))
   pack -> squirrel(clean, ",")

   pack.sniff("stoat")
   banner -> pelt("-", 10)
   update -> rat(nuzzle("pack update: ", parrot(pack)))

   roar banner
   roar update
