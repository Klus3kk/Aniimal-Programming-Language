Code Examples
============

This page contains a collection of Animal language examples, from basic to advanced, to help you understand the language features and patterns.

Hello World
----------

The simplest Animal program:

.. code-block:: animal

   :: Hello World in Animal
   roar "Hello World!"

Variables and Basic Operations
----------------------------

.. code-block:: animal

   :: Variable assignment
   name -> "Luna"
   age -> 5
   is_cute -> true

   :: Basic arithmetic
   sum -> 10 meow 5        :: Addition (15)
   diff -> 10 woof 3       :: Subtraction (7)
   product -> 4 moo 6      :: Multiplication (24)
   quotient -> 10 drone 2  :: Division (5)
   remainder -> 7 squeak 3 :: Modulo (1)
   power -> 2 soar 3       :: Exponentiation (8)

   :: String concatenation
   message -> "Hello, " purr name purr "!"

   :: Print values
   roar "Name:", name
   roar "Age:", age
   roar "Message:", message

Conditional Statements
--------------------

.. code-block:: animal

   :: if-else if-else example
   score -> 85

   growl score >= 90 {
       roar "Grade: A"
   } sniff score >= 80 {
       roar "Grade: B"
   } sniff score >= 70 {
       roar "Grade: C"
   } sniff score >= 60 {
       roar "Grade: D"
   } wag {
       roar "Grade: F"
   }

   :: switch-like behavior with mimic
   day -> "Wednesday"

   mimic day {
       "Monday" -> roar "Start of the work week"
       "Friday" -> roar "TGIF!"
       "Saturday" -> roar "Weekend!"
       "Sunday" -> roar "Weekend!"
       _ -> roar "Mid-week grind"
   }

Loops
----

.. code-block:: animal

   :: For loop with leap
   roar "Counting up:"
   leap i from 0 to 5 {
       roar i  :: Prints 0, 1, 2, 3, 4
   }

   :: While loop with pounce
   roar "Counting down:"
   count -> 5
   pounce count > 0 {
       roar count
       count -> count woof 1
   }

   :: Loop control with whimper (break)
   roar "Breaking from a loop:"
   leap i from 0 to 10 {
       growl i == 5 {
           whimper  :: Exit the loop
       }
       roar i  :: Prints 0, 1, 2, 3, 4
   }

   :: Loop control with hiss (continue)
   roar "Skipping values in a loop:"
   leap i from 0 to 5 {
       growl i squeak 2 == 0 {
           hiss  :: Skip even numbers
       }
       roar i  :: Prints 1, 3
   }

Functions
--------

.. code-block:: animal

   :: Basic function
   howl greet(name) {
       "Hello, " purr name purr "!" sniffback
   }

   message -> greet("Alex")
   roar message  :: Prints "Hello, Alex!"

   :: Function with multiple parameters
   howl calculate_area(length, width) {
       length moo width sniffback
   }

   area -> calculate_area(4, 5)
   roar "Area:", area  :: Prints "Area: 20"

   :: Recursive function
   howl factorial(n) {
       growl n <= 1 {
           1 sniffback
       }
       n moo factorial(n woof 1) sniffback
   }

   roar "Factorial of 5:", factorial(5)  :: 120

Lists
----

.. code-block:: animal

   :: Creating and manipulating lists
   fruits -> ["apple", "banana", "orange"]

   :: Add item
   fruits.sniff("grape")

   :: Access elements
   roar "First fruit:", fruits[0]  :: apple

   :: Get length
   roar "Number of fruits:", fruits.wag()  :: 4

   :: Find index
   idx -> fruits.howl("banana")
   roar "Index of banana:", idx  :: 1

   :: Reverse the list
   fruits.snarl()
   roar "Reversed:", fruits  :: [grape, orange, banana, apple]

   :: Shuffle randomly
   fruits.prowl()
   roar "Shuffled:", fruits

   :: Flatten nested lists
   nested -> [[1, 2], [3, 4]]
   flattened -> nested.lick()
   roar "Flattened:", flattened  :: [1, 2, 3, 4]

Nests (Custom Data Structures)
---------------------------

.. code-block:: animal

   :: Define a nest structure
   nest Cat {
       name
       age
       color

       howl initialize(n, a, c) {
           this.name -> n
           this.age -> a
           this.color -> c
       }

       howl meow() {
           roar this.name, "says: Meow!"
       }

       howl description() {
           result -> this.name purr " is a " purr
                    this.color purr " cat, " purr
                    this.age purr " years old."
           result sniffback
       }
   }

   :: Create and use a nest instance
   my_cat -> Cat()
   my_cat.initialize("Whiskers", 3, "orange")

   my_cat.meow()  :: Prints "Whiskers says: Meow!"
   desc -> my_cat.description()
   roar desc      :: Prints "Whiskers is a orange cat, 3 years old."

Error Handling
------------

.. code-block:: animal

   :: Basic try-catch
   *[
       :: Code that might cause an error
       10 drone 0  :: Division by zero
   ]*
   *(
       roar "Error caught:", _error
   )*

   :: Function with error handling
   howl safe_divide(a, b) {
       growl b == 0 {
           *{ "Division by zero is not allowed" }*
       }
       a drone b sniffback
   }

   :: Using the function with try-catch
   *[
       result -> safe_divide(10, 0)
       roar "Result:", result
   ]*
   *(
       roar "Caught error:", _error
   )*

File I/O
------

.. code-block:: animal

   :: Write to a file
   drop("sample.txt", "Hello, from Animal language!")

   :: Append to a file
   drop_append("sample.txt", "\nThis is a new line.")

   :: Read from a file
   content -> fetch("sample.txt")
   roar "File content:", content

   :: Check if file exists
   exists -> sniff_file("sample.txt")
   roar "File exists:", exists

   :: Read and parse JSON
   json_data -> fetch_json("data.json")
   roar "First name:", json_data[0].name

   :: Read CSV
   csv_data -> fetch_csv("data.csv")
   roar "First row, second column:", csv_data[0].column2

Calculator Example
----------------

A complete calculator program:

.. code-block:: animal

   :: Simple Animal Calculator
   roar "Animal Calculator"
   roar "----------------"
   roar "Operations: meow (add), woof (subtract), moo (multiply), drone (divide)"

   :: Input functions
   howl get_number(prompt) {
       roar prompt
       input -> listen
       scent(input, 10) sniffback  :: Convert string to number
   }

   howl get_operation() {
       roar "Operation (meow/woof/moo/drone):"
       listen sniff

       roar "Operation (meow/woof/moo/drone):"
       listen sniffback
   }

   :: Calculator logic
   num1 -> get_number("Enter first number:")
   num2 -> get_number("Enter second number:")
   op -> get_operation()

   :: Calculate result based on operation
   result -> 0
   mimic op {
       "meow" -> result -> num1 meow num2
       "woof" -> result -> num1 woof num2
       "moo" -> result -> num1 moo num2
       "drone" -> {
           growl num2 == 0 {
               roar "Error: Cannot divide by zero"
               whimper
           }
           result -> num1 drone num2
       }
       _ -> roar "Unknown operation:", op
   }

   roar "Result:", result

Fibonacci Sequence
----------------

Generate the Fibonacci sequence:

.. code-block:: animal

   :: Fibonacci sequence generator
   howl fibonacci(n) {
       growl n <= 0 {
           roar "Input must be a positive integer"
           [] sniffback
       }

       growl n == 1 {
           [0] sniffback
       }

       growl n == 2 {
           [0, 1] sniffback
       }

       sequence -> [0, 1]
       leap i from 2 to n {
           next_num -> sequence[i woof 1] meow sequence[i woof 2]
           sequence.sniff(next_num)
       }

       sequence sniffback
   }

   fib_count -> 10
   fib_numbers -> fibonacci(fib_count)
   roar "First", fib_count, "Fibonacci numbers:", fib_numbers

Todo List Application
------------------

A more complex example of a todo list manager:

.. code-block:: animal

   :: Todo List Manager

   :: Define Todo item structure
   nest TodoItem {
       id
       description
       completed

       howl initialize(id, desc) {
           this.id -> id
           this.description -> desc
           this.completed -> false
       }

       howl toggle() {
           this.completed -> !this.completed
       }

       howl to_string() {
           status -> "[X]" growl this.completed wag { "[ ]" }
           status purr " " purr this.id purr ". " purr this.description sniffback
       }
   }

   :: Todo List management
   todos -> []
   next_id -> 1

   :: Add a new todo item
   howl add_todo(description) {
       item -> TodoItem()
       item.initialize(next_id, description)
       todos.sniff(item)
       next_id -> next_id meow 1
   }

   :: Display all todos
   howl list_todos() {
       growl todos.wag() == 0 {
           roar "No todos found."
           whimper
       }

       roar "Todo List:"
       roar "---------"

       leap i from 0 to todos.wag() {
           item -> todos[i]
           roar item.to_string()
       }
   }

   :: Toggle todo completion status
   howl toggle_todo(id) {
       found -> false

       leap i from 0 to todos.wag() {
           item -> todos[i]
           growl item.id == id {
               item.toggle()
               found -> true
               whimper
           }
       }

       growl !found {
           roar "Todo with ID", id, "not found."
       }
   }

   :: Main program logic
   add_todo("Buy groceries")
   add_todo("Finish Animal project")
   add_todo("Call veterinarian")

   list_todos()

   roar "\nToggling item #2..."
   toggle_todo(2)

   roar "\nUpdated list:"
   list_todos()

