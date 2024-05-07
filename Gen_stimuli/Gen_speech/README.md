The main script for generating sentences in naturalistic speech was run in Text-to-speech (TTS) API in google cloud

## How to install the TTS and run the script:
Read the instructions fully before starting.

### Step 1 - Get a google cloud account
To run this script, you first need to go to [Link1](https://cloud.google.com/text-to-speech/?hl=en) to set up an account with Google Cloud.
It is has a free trial period lasting 90 days (as of April 2024), but requires credit card information to prove you're human.
It should automatically create a project, but if not, create a project.

### Step 2 - Activate your project
Activate your project by going to [Link2](https://console.cloud.google.com/apis/api/serviceusage.googleapis.com). If the link doesn't work, don't worry, just continue with the instructions. At some point you will get an error message telling you to activate your project with a link. Follow that link to activate your project. 

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
Go to [Link4](https://cloud.google.com/sdk/docs/install) for instructions to install the gcloud CLI. This step will differ depending on operating system. You might need to log into google when prompted. Then, close and open the console, and activate the environment again (using the second line in the code snippets from Step 2)

### Step 5 - Authenticate your credentials
In your environment, run the line `gcloud auth application-default login`. A browser window will open, where you need to log into your google account. This will authenticate your credentials. More information on this step can be found on [Link5](https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to).

### Step 6 - Enable the API on your project
In your environment, run the line `gcloud auth application-default set-quota-project <projectID>`. You can find the project ID by going to [Link6](https://console.cloud.google.com/welcome/) - it is listed on the page. For me, it's in the form of adjective-noun-numbers. 

This step will give you an error if your project has not been activated (Step 2). The error message includes a link. Follow that link to activate your project, then try this step again.

### Step 7 - Running your script
After all this is done, while still in the console and with the environment active, navigate to the folder where this script is saved (using `cd directory/of/script/`) and run it with the line
`python3 tts_sentenceGenerator.py`

Unfortunately, it will save all outputs in the same folder as the script is saved. 
Drag them over into the folder you want them in afterwards.


