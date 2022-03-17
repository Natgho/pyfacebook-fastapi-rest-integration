# Use-Case Facebook Integration
## How to Run Project
```shell
pip install -r requirements.txt
uvicorn api:app --reload  
```
### Using with Docker:
```shell
docker build -t usecase-facebook-integration .
docker run -d --name usecase-facebook-integration -p 0.0.0.0:8080:80 usecase-facebook-integration
```
Open your browser at http://localhost:8080  
### Using with Docker-compose:
```shell
docker-compose up -d
```
Open your browser at http://localhost:8080