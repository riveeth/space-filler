# space-filler 


---



## Installation

To install and run space-filler, follow these steps:

- Clone this repository:

```sh
git clone https://github.com/riveeth/space-filler.git
```

- Navigate to the project directory:
```sh
cd space-filler
```

- Create a virtual environment and install dependencies:
```sh
python3 -m venv .space_filler_env
source .space_filler_env/bin/activate
pip install -r requirements.txt
```
---
##  Usage
Start the app by running the following command from project directory:
```sh
python3 service/run.py
```
Open your web browser and go to http://localhost:8000. You should see the app running.

You can check the health of the service by visiting http://localhost:8000/healthcheck.
It will return `{"healthcheck":"OK"}` response if service is healthy. 
If there is an error or the service is not running, you may see an error message.