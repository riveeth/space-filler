# Space Filler

---
`Space Filler` is an HTTP service built on FastAPI and Gradio for correcting missed spaces in input text. 
The service receives one text input with a length of less than 512 symbols and up to five missed spaces, 
and provides two outputs: the corrected sentence and a list of missed spaces positions.

---
## Installation

To install and run `space filler`, follow these steps:

1. Clone the repository using the following command:

```sh
git clone https://github.com/riveeth/space-filler.git
```

2. Navigate to the project directory:
```sh
cd space-filler
```

3. Create a virtual environment and install dependencies:
```sh
python3 -m venv .space_filler_venv
source .space_filler_venv/bin/activate
pip install -r requirements.txt
```
---
##  Usage
Start the application by executing the following command from the project directory:
```sh
python3 service/run.py
```
Open your web browser and navigate to http://localhost:8000. You should see the app running.

You can check the health of the service by visiting http://localhost:8000/healthcheck.
It will return `{"healthcheck":"OK"}` response if service is healthy. 
If there is an error or the service is not running, you may see an error message.

---
## Interface

![space_filler](https://user-images.githubusercontent.com/128361378/226759107-f04043fd-abe3-418f-813a-8bca2c9e813e.jpg)


Input the sentence in the `INPUT SENTENCE` field and click on the `Submit` button to retrieve the corrected 
sentence with the appropriate spacing. 

Some examples have already been provided for your convenience. 

You may also choose to activate the `Simplified Mode` feature, which will refrain from separating compound words that 
are recognized by the dictionary. For instance, when the `Simplified Mode` is enabled, the string `"searchbar"` will 
remain unchanged, but when disabled, it will be corrected to `"search bar"`.


---
## Dictionary

The algorithm used for space filling is dependent on word probabilities, and therefore requires 
a word corpus or a customized dictionary. Currently, 
the solution is based on 
["English Word Frequency"](https://www.kaggle.com/datasets/rtatman/english-word-frequency)
Kaggle dataset containing ~333k most commonly-used english words. Additional information regarding this approach and creating custom word probabilities dictionary may be 
found [here](https://github.com/riveeth/space-filler/blob/main/service/space_filler/create_custom_dict.py).

