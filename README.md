![build status](https://travis-ci.org/talelburg/equilibrium.svg?branch=master)
![coverage](https://codecov.io/gh/talelburg/equilibrium/branch/master/graph/badge.svg)

# Equilibrium

An implementation of a Brain-Computer Interface. See [full documentation](https://equilibrium.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```shell script
    $ git clone git@github.com:talelburg/equilibrium.git
    ...
    $ cd equilibrium/
    ```

2. Run the installation script and activate the virtual environment:

    ```shell script
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [equilibrium] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:

    ```shell script
    $ pytest tests/
    ...
    ```

## Usage

The `equilibrium` packages provides the following functionality:

- `Thought`

    This class encapsulates the concept of a thought, allowing for easy 
    manipulation and representation of thoughts.

    In addition, it provides the `serialize` method to generate a compact 
    representation of a thought, and the `deserialize` class method to generate
    a thought object from such a compact representation.

    ```pycon
    >>> from equilibrium import Thought
    >>> # assume dt is a pre-existing datetime object precise to seconds
    >>> t = Thought(1, dt, "Hello")
    >>> t
    Thought(user_id=1, timestamp=datetime.datetime(...), thought='Hello')
    >>> t.serialize()
    b'\x01\x00\x00\x00\x00\x00\x00\x00...\x05\x00\x00\x00Hello'
    >>> Thought.deserialize(_)
    Thought(user_id=1, timestamp=datetime.datetime(...), thought='Hello')
    >>> Thought.deserialize(t.serialize()) == t
    True
    ```

- `upload_thought`

    This function uploads a user's thought to a server.

    ```pycon
    >>> from equilibrium import upload_thought
    >>> upload_thought(address=(HOST, PORT), user_id=1, thought="Hello")
    ```
 
- `run_server`

    This function starts a server that handles incoming connections,
    and stores their data.

    ```pycon
    >>> from equilibrium import run_server
    >>> run_server(address=(HOST, PORT), data_dir="/path/to/data/dir")
    ```

- `run_webserver`

    This function starts a web server, serving some data.

    ```pycon
    >>> from equilibrium import run_server
    >>> run_webserver(address=(HOST, PORT), data_dir="/path/to/data/dir")
    ```

The `equilibrium` package also provides a command-line interface:

```shell script
$ python -m equilibrium
equilibrium, version 0.1.0
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `upload` command:

```shell script
$ python -m equilibrium upload "127.0.0.1:5000" 1 Hello
$
```

The CLI further provides the `run` command, with the `server` and `web` subcommands.

```shell script
$ python -m equilibrium run server "127.0.0.1:5000" /data
^C
$ python -m equilibrium run web "127.0.0.1:5001" /data
...
```


Do note that each command's options should be passed to *that* command, so for
example the `-q` and `-t` options should be passed to `equilibrium`, not `run` or
`upload`.

```shell script
$ python -m equilibrium run -q ... # this doesn't work
ERROR: no such option: -q
$ python -m equilibrium -q upload ... # this does work
```
