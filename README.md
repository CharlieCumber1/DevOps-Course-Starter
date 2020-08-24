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

Additionally you will need to create a trello board with three lists with the following names (these are case sensitive):
1. Not Started
2. In Progress
3. Done

 You will need the identifier for the board. You can see the identifier by navigating to the trello board in a browser and adding '.json' to the url to view the raw JSON.

Within the .env file created by the setup script described above, you should add the values of the following variables:
```
TRELLO_KEY = your_personal_trello_api_key
TRELLO_TOKEN = your_personal_trello_api_secret_token
TRELLO_BOARD = trello_board_id
```

## Testing

The end to end tests require you have the firefox browser installed and that you download the corresponding version of the Geckodriver (check version compatability [`here`](https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html)):
* Download and install firefox from [`here`](https://www.mozilla.org/en-US/firefox/download/)
* Download Geckodriver from [`here`](https://github.com/mozilla/geckodriver/releases) and add the executable file to the root of the project.

Once the test setup requirments are completed, execute the tests by running:
```bash
$ pytest
```