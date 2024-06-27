# STIMULI GENERATION USER MANUAL

author: samuelmull

The main script for generating sentences in naturalistic speech is **01_TTS_sentenceGenerator.py**    
It is run using the google cloud Text-to-speech (TTS) API. This text will explain how to do that (as of June 2024)

## How to install the TTS API and run the script:

**Read the instructions fully before starting.**  
If you don't understand certain terms, don't worry. Just follow the instructions as best as you can.

### Step 1 - Get a google cloud account

To run this script, you first need to go to [Link1](https://cloud.google.com/text-to-speech/?hl=en) to set up an account with Google Cloud.  
It is has a free trial period lasting 90 days (as of April 2024), but requires credit card information to prove you're human.  
It should automatically create a project, but if not, create a project.  

### Step 2 - Activate your project

Activate your project by going to [Link2](https://console.cloud.google.com/apis/api/serviceusage.googleapis.com) . If the link doesn't work, don't worry, just continue with the instructions. At some point, you will get an error message telling you to activate your project. Follow the link in the error message to activate your project. 

### Step 3 - Install the python client

Once you have created (and maybe activated) your project, open a terminal and install the python client by running the following code taken from [Link3](https://cloud.google.com/python/docs/reference/texttospeech/latest) :   

Linux / Mac:   
```
python3 -m venv <your-env>
source <your-env>/bin/activate
pip install google-cloud-texttospeech
```

Windows:  
```
py -m venv <your-env>
.\<your-env>\Scripts\activate
pip install google-cloud-texttospeech
```

### Step 4 - Install the gcloud CLI

Go to [Link4](https://cloud.google.com/sdk/docs/install) for instructions to install the gcloud CLI. This step will differ depending on operating system. You might need to log into google when prompted. Then, close and re-open the console, and activate the environment again (= run the second line in the code snippets from *Step 3*)

### Step 5 - Authenticate your credentials

In your environment, run the line `gcloud auth application-default login`. A browser window will open, where you need to log into your google account again. This will authenticate your credentials. 

If this doesn't work, try running the line `./google-cloud-sdk/bin/gcloud init` or just `gcloud init`, and then run the above line again.  
For more information on this step, visit [Link5](https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to) .

### Step 6 - Enable the API on your project

In your environment, run the line `gcloud auth application-default set-quota-project <projectID>` with your projectID. You can find the project ID by going to [Link6](https://console.cloud.google.com/welcome/) - it is listed on the page. For me, it's in the form of adjective-noun-6numbers. 

This step will give you an error if your project has not been activated (*Step 2*). The error message includes a link. Follow that link to activate your project, then try this step again.

### Step 7 - Running your script

After all this is done, while still in the console and with the environment active, navigate to the folder where this script is saved (using `cd directory/of/script/`) and run it with the line `python3 01_TTS_sentenceGenerator.py`

Unfortunately, it will save all outputs in the same folder as the script is saved. The **.gitignore** file in the folder of the script will ensure that no files ending in **.wav** will be pushed to github.

Move the generated audio- and textfiles over into the folder you want them in afterwards. The easiest way to do this is with the script [**files_move.py**](../utils/files_move.py)
