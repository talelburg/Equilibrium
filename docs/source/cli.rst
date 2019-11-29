Equilibrium CLI Reference
=========================

The ``equilibrium`` package provides a command-line interface:

.. code:: bash

    $ python -m equilibrium [OPTIONS] [COMMAND] [ARGS]
    ...

The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).

To see its version, run:

.. code:: bash

    $ python -m equilibrium --version
    equilibrium, version 0.5.0

The ``upload`` Command
~~~~~~~~~~~~~~~~~~~~~~

The ``upload`` subcommand uploads a user's thought to the specified server

.. code:: bash

    $ python -m equilibrium upload [ADDRESS] [USER_ID] [THOUGHT]
    foo

The ``run`` Command
-------------------

To run the ``run`` command:

.. code:: bash

    $ python -m equilibrium run [SUBCOMMAND] [ARGS]

The ``server`` subcommand
~~~~~~~~~~~~~~~~~~~~~~

The ``server`` subcommand runs a server at the specified address, using the specified data directory.

.. code:: bash

    $ python -m equilibrium run server [ADDRESS] [DATA_DIR]

The ``web`` subcommand
--------------------

The ``web`` subcommand runs a web server at the specified address, using the specified data directory.

.. code:: bash

    $ python -m equilibrium run server [ADDRESS] [DATA_DIR]
