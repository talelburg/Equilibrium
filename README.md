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

- `Sample`

    This is a function that returns a ``construct`` Struct to parse the sample format.
    When invoked with no argument, the Struct holds a list of all snapshots parsed.
    When invoked with an argument, it is assumed to be a processing hook, called on
    each snapshot as it is parsed. Each snapshot is then discarded (the list returned 
    is empty).
    
    ```pycon
    >>> from equilibrium import Sample
    >>> Sample().parse_file('sample.mind')
    Container(..., snapshots=ListContainer([Container(...)]))
    >>> Sample(hook).parse_file('sample.mind')
    Container(..., snapshots=ListContainer([]))
    >>> # hook was called on each snapshot 
    ```

- `upload_sample`

    This function uploads a user Sample to a server.

    ```pycon
    >>> from equilibrium import upload_sample
    >>> upload_sample(address=(HOST, PORT), sample_path="/path/to/sample/file")
    ```
 
- `Server`

    This is a class encapsulating the server.
    It can start listening by using the ``run`` method.
    The class also provides the ``parses`` decorator, to register parsers for 
    snapshot fields, and the ``parse`` method, to parse all supported fields of 
    specific snapshot.

    ```pycon
    >>> from equilibrium import Server
    >>> s = Server(port=PORT, data_dir="/path/to/data/dir")
    >>> s.run() # This accepts connections until interrupted
    >>> @Server.parse('fieldname')
    ... def parse_fieldname(directory, snapshot): # These are the parameters of a parser
    ...     pass
    >>> Server.parse(directory="/directory/of/snapshot", snapshot=SNAPSHOT) 
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

The CLI provides the `client` command, with the `run` subcommand:

```shell script
$ python -m equilibrium client run "127.0.0.1:5000" sample.mind
$
```

The CLI further provides the `server` command, with the `run` subcommand.

```shell script
$ python -m equilibrium server run 5000 /data
...
```

Finally, the CLI provides the `read` command:
```shell script
$ python -m equilibrium read sample.mind
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
