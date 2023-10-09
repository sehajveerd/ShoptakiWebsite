# Information of Important Folders/Files within the WEB Folder:
The Web folder has 3 flask apps:
  - Listing Service
  - Transaction Service
  - User Service

All 3 flask apps have some common and important folder/files. Below is their purpose:
 - ### Migrations
      - This folder contains all the migration scripts which are automatically generated when we run ```flask db init``` within the flask app's venv
 - ### Models
      - This folder holds all the information about the Table structure of the database in our Listing Services
      - Tables included : Properties, Property_Images, States, Projects(Refering the seed data naming convention here)
  - ### Seeds
      - This folder has python scripts to get the seed data when the ```flask seed``` commands are run in the venv
      - The scripts take the data from the DATASETS folder within this repo and adds them to the database
  - ### Utils
      - This folder is used to maintain the function which have a specific purpose
      - placing them in a separate folder allows for focused unit testing and easier maintenance
      - In this flask app, we have consumer.py and googlemaps.py scripts
  - ### .env
      - This is the file, where we configure our environment variables
  - ### .flaskenv
      - This file is ensure that our project is running in a development environment and not on production
  - ### app.py
      - This file is required to create the Flask app instance
      - Used to define the graphql endpoint
      - Configures the middleware to connect the frontend and backend.(In this project, we are currently using CORS middleware)
  - ### config.py
      - Mainly utilised to store secret keys or database connection information using the environment variables provided in the .env file
  - ### requirements.txt
      - Includes all the packages and their versions, that are necessary for this project
      - We need to run ```pip install -r requirements.txt``` within the venv of the flask app to get these installed
      - Please add any packages, which were not added to this file. But, are present in the project
  - ### Schema.py
      - This file defines the types, queries, mutations,resolvers - the overall structure of the GraphQL API
      - This is for defining the queries and mutations of graphql
      - Each query or mutation defined in the schema has a corresponding resolver function that specifies how to retrieve or manipulate the data.
