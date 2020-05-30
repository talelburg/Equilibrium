![build status](https://travis-ci.org/talelburg/equilibrium.svg?branch=master)
![coverage](https://codecov.io/gh/talelburg/equilibrium/branch/master/graph/badge.svg)

# Equilibrium

Equilibrium is an implementation of a Brain-Computer Interface. 
<!-- 
See [full documentation](https://equilibrium.readthedocs.io/en/latest/).
-->

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

4. To jumpstart the whole system, you may run the dedicated script:
    ```shell script
    $ ./scripts/run-pipeline.sh
    ```
   This will run all components of the system locally on your computer. All that's left to do is upload!
  
   Note: This script assumes you have docker-compose (and, of course, docker) installed.

## Usage

The `equilibrium` packages provides the following functionality:

- ### The Client
    The client serves as the entrypoint for data into our system. It allows us to stream a mind sample
    from a given path over the network to a server at a given address.
    
    - #### API
        ```pycons
        >>> from equilibrium.client import upload_sample
        >>> host, port, path = "127.0.0.1", 8000, "sample.mind.gz"
        >>> upload_sample(host, port, path)
        ```
    - #### CLI
        ```shell script
        $ python -m equilibrium.client upload-sample -h "127.0.0.1" -p 8000 "sample.mind.gz"
        ```

- ### The Server
    The server listens on a given address, processes the data sent by the clients and publishes it. 
    When using the API, the exact meaning of 'publish' is up to you.
    
    The intent, and therefore the CLI's behaviour, is to publish to a message queue, 
    from which the data is available for consumption by all who subscribe to it. 
    
    - #### API
        ```pycons
        >>> from equilibrium.server import run_server
        >>> def publish(message):
        >>>     print(message)
        >>> host, port = "127.0.0.1", 8000 
        >>> run_server(host, port, publish)
        ```
    - #### CLI
        ```shell script
        $ python -m equilibrium.server run-server -h "127.0.0.1" -p 8000 -mq "rabbitmq://127.0.0.1:5672"
        ```
        The format for the url is very simple: `<mqscheme>://<mqhost>:<mqport>`.

- ### The Parser
    The parsers process the data in some fashion, and return results. The API allows one to run a
    parser once, directly on raw data, and receive the result.
    
    The CLI supports both that functionality and the functionality to let the parser run 
    indefinitely, subscribing to a message queue, processing incoming data and publishing 
    the result back to the queue.
    
    - #### API
        ```pycons
        >>> from equilibrium.parsers import run_parser
        >>> parser_name, raw_data = "pose", ...
        >>> run_parser(parser_name, raw_data)
        ```
    - #### CLI
        ```shell script
        $ python -m equilibrium.parsers parse "pose" "data.raw" > "pose.result"
      
        $ python -m equilibrium.parsers run-parser "pose" -mq "rabbitmq://127.0.0.1:5672"
        ```
        The format for the url is the same as before: `<mqscheme>://<mqhost>:<mqport>`.
    
    Our system ships with four built-in parsers.
    To add one of your own, follow these steps:
    1. Create a python module inside the `equilibrium.parsers` package. Its name must match the 
    name of your new parser (i.e. when invoked by name anywhere).
    2. Inside your new module, write your parser. A parser is either a function, which receives 
    the snapshot data and the path of a data directory to use, or a class, which has a `parse` method
    accepting those same two parameters. This parser must be decorated with 
    `ParsingManager.parses(parser_name)` - the `ParsingManager` class is implemented in 
    `equilibrium.parsers.parsing_manager`.
    3. (Optional) Add a directive to `docker-compose.yml` to build and start your new parser
    in its own container.
    
    For examples, check out the existing parsers: `pose`, `feelings`, `color_image` and `depth_image`.
        
- ### The Saver
    The saver's job is to receive processed data from the parsers and save it to a database.
    As with the parsers, there are two supported modes of behaviour.
    The API lets us save results for which we have the data.
     
    The CLI supports both that mode and a mode to let the save run indefinitely, 
    subscribing to a message queue and saving data received from it.
    
    - #### API
        ```pycons
        >>> from equilibrium.saver import Saver
        >>> database_url = "mongodb://127.0.0.1:27012"
        >>> saver = Saver(database_url)
        >>> topic, raw_data = "pose", ...
        >>> saver.save(topic, raw_data)
        ```
    - #### CLI
        ```shell script
        $ python -m equilibrium.saver save -d "rabbitmq://127.0.0.1:27017" "pose" "pose.result"
      
        $ python -m equilibrium.saver run-saver -d "rabbitmq://127.0.0.1:27017" -mq "rabbitmq://127.0.0.1:5672"
        ```
        The format for the urls is similar, and reminiscent of what we've seen: 
        
        - `<mqscheme>://<mqhost>:<mqport>`
        - `<dbscheme>://<dbhost>:<dbport>`

- ### The API
    Our system exposes a RESTful API. The following endpoints are supported:
    
    - `GET /users` - Returns the list of users (IDs and usernames).
    - `GET /users/<user_id>` - Returns the specified user's full details.
    - `GET /users/<user_id>/snapshots` - Returns the list of timestamps of snapshots 
    for the specified users.
    - `GET /users/<user_id>/snapshots/<timestamp>` - Returns the timestamp and available 
    results for the specified snapshot
    - `GET /users/<user_id>/snapshots/<timestamp>/<result_name>` - Returns the specified result from
    the specified snapshot. If the data is large, only metadate is sent, including a `data` field,
    which holds a url where the full (base64-encoded) data can be retrieved. 
    
    For all of this to function, there must be a server set up to serve this API. For that, we have
    the following: 
    
    - #### API
        ```pycons
        >>> from equilibrium.api import run_api_server
        >>> host, port, database_url = "127.0.0.1", 5000, "mongodb://127.0.0.1:27012" 
        >>> run_api_server(host, port, database_url)
        ```
    - #### CLI
        ```shell script
        $ python -m equilibrium.api run-server -h "127.0.0.1" -p 5000 -d "mongodb://127.0.0.1:27012"
        ```
        The format for the url is very predictable: `<dbscheme>://<dbhost>:<dbport>`.

- ### The CLI
    We provide a dedicated CLI to serve our API. This is very analogous to the API:
    
    ```shell script
    $ python -m equilibrium.cli get-users
    $ python -m equilibrium.cli get-user 1
    $ python -m equilibrium.cli get-snapshots 1
    $ python -m equilibrium.cli get-snapshot 1 2
    $ python -m equilibrium.cli get-result 1 2 pose
    ```
    All commands support the `-h` and `-p` flags to specify the API server's host and port, 
    respectively (the default are "127.0.0.1" and 5000, respectively).
    
    The `get-result` command supports the `-s` flag, which receives a path and saves the result's
    data to it.

- ### The GUI
    We also provide a `react`-based GUI to consume the data, which itself consumes the API.
    To enjoy this, we need a server to serve this GUI:
    
    - #### API
        ```pycons
        >>> from equilibrium.gui import run_server
        >>> host, port, api_host, api_port = "127.0.0.1", 5000, "127.0.0.1", 8080
        >>> run_server(host, port, api_host, api_port)
        ```
    - #### CLI
        ```shell script
        $ python -m equilibrium.gui run-server -h "127.0.0.1" -p 5000 -H "127.0.0.1" -P 8080
        ```
