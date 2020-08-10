# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On macOS and Linux
```bash
$ source setup.sh
```
### On Windows (Using Git Bash)
```bash
$ source setup.sh --windows
```

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Configuration

### Trello
In order to use the app with your Trello account you will need to create an API key and token with the [`instructions here`](https://trello.com/app-key). 

Additionally you will need to create a trello board with two lists to group pending and completed tasks. You will need the identifiers for the board and two lists. You can see the identifiers by navigating to the trello board in a braowser and adding '.json' to the url to view the raw JSON.

You need to create a file in the root directory called "trello_config.py" with the following variables:
```
KEY = 'API key'
TOKEN = 'API token'
BOARD = 'Board ID'
PENDING = 'Pending list ID'
DONE = 'Done list ID'
```