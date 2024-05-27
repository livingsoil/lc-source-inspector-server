## Pull and run Selenium Standalone Image/Container for scraping
### ARM64 arch
```bash
$ docker pull seleniarm/standalone-chromium

$ docker run --rm -it -p 4444:4444 -p 5900:5900 -p 7900:7900 --shm-size 2g seleniarm/standalone-chromium:latest

```
### Other
```bash
$ docker pull selenium/standalone-chrome

$ docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:latest

```

If the Selenium container is running, Selenium UI will be served from http://localhost:4444/ui/


## Build and run the Flask API to handle the POST from lc-source-inspector frontend

