## Coding test for Tails.com by Kieran Gray

### Running the application
To start:

`make install`
`make run`

This will:

    - build the application image
    - pull the postgresql image
    - start the postgresql and application containers
    - run the database population script

### Using the application

The application will be available at http://localhost:8000

There are 3 different view types:

    - list
    - map
    - api

They can each be accessed as follows:

    - http://localhost:5000/{view_type}/
    
    - http://localhost:5000/{view_type}/filter/?postcode={postcode}&radius={radius}


### Running the tests

`make test`

This will:
    - Run the linting checks
    - Run the unit tests

`make pytest` to run just the unit tests.

### Debugging the tests

Additionally there is a `make pytest-debug` command that can be used to run 
the tests with debugpy. This allows VSCode debugger to connect to the container 
for interactive debugging.

To attach to the debugger you need a configuration in your `.vscode/launch.json` file.

An example launch.json with Attach configuration:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Attach",
            "type": "python",
            "request": "attach",
            "port": 5678,
            "host": "localhost",
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/app/"
                }
            ],
        }
    ]
}
```