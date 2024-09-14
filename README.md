# Multi-tenant Saas authentication system
Api's for handling multi-tenant saas backend operations for handling the below scenarios.
- Creating a user and assigning a role for him in a organization.
- Inviting members from different organizations.
- Updating and deleting the role of the members in the organization.
- Sending alert mails for each action performed.
- Retrieving number of users based on organization and roles with filters such as from and to date.

## DB design


![Database Schema](https://github.com/iamLUCISTAR/AuthService/blob/master/Screenshot%202024-09-14%20at%2012.14.31%20PM.png?raw=true)


## Code

Two scripts were written for two functionalities.
- First script to authenticate with Gmail API services and fetch emails from Gmail.
- Second script to generate rule actions that needs to be applied on stored emails and then apply the actions for filtered emails.

Code respository is defined in the below structure ,

- dockerfiles
- src
  - config
  - dao
  - entity
  - manager
  - script

## Setup

1. Create a python virtual environment (venv) and install the required packages mentioned in the requirements.txt file.
    ```{console}
   python -m venv venv
   source venv/bin/activate && pip install -r requirements.txt
   ```
2. Setup the python path
    ```{console}
   export PYTHONPATH=$PYTHONPATH:./
   ```
3. Setup and run the database server in the local. MySql engine is hosted in this implementation using docker compose.
    ```{console}
   docker-compose -f <path_to_docker_file> up -d 
   ```
3. Execute the below scripts to simulate the rule engine flow.
    ```{console}
    python3 src/script/mail_loader.py --clear True --limit 10
    ```
    ```{console}
    python3 src/script/operations_executor.py --json <path/to/jsonfile/>
    ```

## Author

- [Sharath Bhadrinath](https://github.com/iamLUCISTAR)
