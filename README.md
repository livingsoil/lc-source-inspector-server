## create a custom network to enable communication between the Flask  and Selenium containers
```bash
docker network create selnet
```

## Pull Selenium Standalone from Docker Hub
### ARM64 arch
```bash
$ docker pull seleniarm/standalone-chromium

$ docker run --network=selnet --name selenium --rm -it -p 4444:4444 -p 5900:5900 -p 7900:7900 --shm-size 2g seleniarm/standalone-chromium:latest

```
### non-ARM64 
```bash
$ docker pull selenium/standalone-chrome

$ docker run --network=selnet --name selenium -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:latest

```

Check Selenium is running at http://localhost:4444/ui/


## Build and run the Flask API to handle the POST from lc-source-inspector frontend

```bash
docker compose up -d
```

Check Flask API service
```bash
curl localhost:8000
# Flask server running on port 8000
```


## Rebuild and run after code updates
```bash
docker compose up --build -d
```