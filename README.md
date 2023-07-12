# Real-Estate-Backend
ETL and backend services for real-estate-ai project

![Python](https://img.shields.io/badge/Python-3.9-blueviolet)
![Framework](https://img.shields.io/badge/Framework-Flask-red)

## Repo Directory
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
## To run the project in your local system

1. Clone this repository in your local system.
2. Install [requirements.txt]([https://github.com/yugu-yg/rest-api-in-flask/blob/master/requirements.txt](https://github.com/Shoptaki/real-estate-be/blob/main/requirements.txt)) file with the command `pip install -r requirements.txt`.
3. Build docker images and run in port 5000
4. Go to your browser and visit `http://127.0.0.1:5000/`
