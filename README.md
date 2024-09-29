# FakeNewsDetector
A Chrome Extension to detect the fake news via AI

PennState - DS440 Capstone Project

The structure of this program:


```bash
├── FakeNewsDetector
│   ├── algorithms
│   │      ├── LSTM
│   │  	   │    ├──LSTM.ipynb
│   │ 	   │	├──testModel_LSTM.ipynb
│   │	   │	├──best_model.h5
│   │	   └── ... other algorithms
│   ├── dataset
│   │       ├── data_process.ipynb
│   │	    └── dataset.txt # The link of dataset
│   ├── plugin_frontend
│   └── ....
```



## How to use

## **KEEPITAPI (BACKEND)**

Deploying the selfhosted Django API-REST server.

### INSTRUCTIONS:

#### 1) Create a new python virtualenviromen.

> virtualenv [VIRTUAL_ENVIROMENT_NAME]  

#### 2) Activate the virtualenv 

> [VIRTUAL_ENVIROMENT_NAME]/Scripts/activate

#### 3) Install all the dependecies in requieriments.

> pip install requirement.txt 

#### 4) Run the server.

> python manage.py runserver

## **CHROME EXTENSION:**

Extension that connects to the selfhosted API.

#### 1)Open the Google Chrome browser.

#### 2)Visit the Extension's tab.

> chrome://extensions/

#### 3)Turn on the developer's mode.

#### 4)Click on the "load unpacked extensions" button and select the [chrome_extension] folder.
