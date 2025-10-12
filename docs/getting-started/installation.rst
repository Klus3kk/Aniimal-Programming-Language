Installation
============

This guide will help you set up the Animal language interpreter on your system.

Requirements
------------

- Go 1.21 or higher
- Git

Install via ``go install``
--------------------------

The quickest way to get the CLI is with Go's install command, which fetches the latest tagged version:

.. code-block:: bash

   go install github.com/animal-lang/animal/cmd/animal@latest

The binary is placed in ``$GOBIN`` (or ``$GOPATH/bin``). Make sure that directory is on your ``PATH`` so ``animal`` is available everywhere.

Installing from Source
----------------------

1. Clone the repository

   .. code-block:: bash

      git clone https://github.com/animal-lang/animal.git
      cd animal

2. Build the interpreter

   .. code-block:: bash

      go build -o animal ./cmd/animal

3. Verify the installation

   .. code-block:: bash

      ./animal --version

   The command prints the version that was just built.

Useful CLI Flags
----------------

Animal ships with a couple of helper flags to enhance development:

.. code-block:: bash

   animal --repl              # launch the interactive shell
   animal --time script.anml  # report execution time
   animal --debug script.anml # emit debug trace output

Pass ``--help`` to see every supported flag.

Platform Notes
--------------

Linux / macOS
^^^^^^^^^^^^^

- Ensure the binary is executable: ``chmod +x animal`` when building from source.
- Add ``$GOBIN`` to the ``PATH`` so ``animal`` is available in new shells.

Windows
^^^^^^^

- ``go install`` will place ``animal.exe`` in ``%GOBIN%``.
- After building from source you can move ``animal.exe`` anywhere on the ``PATH``.
