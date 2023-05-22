
This is a simple chat-bot that uses the OpenAI ChatGPT API.


# Setup

Make sure you have python3 installed:

```
python3 --version
```

Create a virtual environment and install the dependencies:

### Linux/Mac:

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

### Windows:

```
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

# Configuration
Provide your own OpenApi key inside .env file
```
OPENAI_API_KEY=<<YOUR_API_KEY>>
```


# Running

To run just do the following:

### Linux/Mac:

```
. ./venv/bin/activate
python main.py
```

### Windows:

```
venv\Scripts\activate.bat
python main.py
```
