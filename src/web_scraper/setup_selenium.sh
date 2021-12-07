#!/bin/bash

curl https://chromedriver.storage.googleapis.com/95.0.4638.69/chromedriver_linux64.zip --output chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv ./chromedriver ./src/web_scraper/chromedriver

rm chromedriver_linux64.zip