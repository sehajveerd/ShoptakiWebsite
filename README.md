# Real-Estate-Backend
ETL and backend services for real-estate-ai project

![Python](https://img.shields.io/badge/Python-3.9-blueviolet)
![Framework](https://img.shields.io/badge/Framework-Flask-red)

## Folder structure
```
- web/          // Web server implemented in Flask
  - user-service/
  - listing-service/
      - app/
        - models/
        - resolvers/
        - __init__.py
        - config.py
      - migrations/
      - .env
      - .flaskenv
      - requirements.txt
      - Dockerfile
  - portfolio-service/
  - crowdfunding-service/
- datasets/
- etl/          // ETL implementation scripts
- k8s/
  - cluster/  // Kubernetes cluster manifests
  - helm/     // Helm charts and Kubernetes manifests
- script/       // additional scripts for deployment automation
- .gitignore
- README.md
```
## Getting Started

1. Clone this repository to your local system
   
```
git clone git@github.com:Shoptaki/real-estate-ai-be.git
```

2. Create virtual environments

To set up a virtual environment for this project, we’ll first install `virtualenv` with `pip`:
   
```
pip install virtualenv
```

Then, we’ll create a virtual environment named `venv` and activate it:

```
virtualenv venv
source venv/bin/activate
```
  
3. Install dependencies
   
Navigate to web/listing service folder and install dependencies for listing service.
   
```
pip install -r requirements.txt
```

4. Set up your environment variables in the .env file

5. Migrate the database

Run the following commands to set up the database and seed all the data.
   
```
flask db upgrade
flask seed all
```

6. Start the flask server in the development environment
   
```
flask run
```

7. Navigate to `localhost:5000/graphql` for the GraphQL interface
