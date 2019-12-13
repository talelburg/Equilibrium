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

The ``client`` Command
~~~~~~~~~~~~~~~~~~~~~~

This command groups enables usage of the client functionality of the package. To run it:

.. code:: bash

    $ python -m equilibrium client [SUBCOMMAND] [ARGS]

The ``run`` Subcommand
----------------------

The ``run`` subcommand instructs the client to stream the given sample to the given server.
``SAMPLE_PATH`` must exist, and must be a file.

.. code:: bash

    $ python -m equilibrium upload [ADDRESS] [SAMPLE_PATH]
    ...

The ``server`` Command
~~~~~~~~~~~~~~~~~~~

To run the ``server`` command:

.. code:: bash

    $ python -m equilibrium server [SUBCOMMAND] [ARGS]

The ``run`` Subcommand
-------------------------

The ``run`` subcommand runs a server to listen on the specified port, using the specified data directory.
``DATA_DIR`` must exist, and must be a directory.

.. code:: bash

    $ python -m equilibrium server run [PORT] [DATA_DIR]

The ``read`` Command
----------------------

The ``read`` command parses the file at the given path, and prints information regarding the sample encoded in it.
``SAMPLE_PATH`` must exist, and must be a file.

.. code:: bash

    $ python -m equilibrium read [SAMPLE_PATH]
