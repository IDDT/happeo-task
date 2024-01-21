# happeo-task
Take home assignment for Happeo that implements a hate speech detection API and a single page web app for testing. Under the hood it runs on a pretrained LLM constraining its output for further processing. It's able to classify the user text among several types of hate speech and provide a short comment with reasoning. Further development may include suggesting the corrected version of user text to convey similar meating with toxicity stripped away.


### Run locally with Docker
Build and run as a Docker container. Make sure to have at least 8GB of free RAM.
```bash
docker build --tag hs-detector --target prod .
docker run -p 5000:5000/tcp --name hs-detector hs-detector:latest
```


### Run locally with venv
```bash
# Download model weights
wget -O temp/model.gguf $(grep -oP 'https://huggingface.co/[^"]+' Dockerfile)
# Create virtual environment and install dependencies.
python3 -m venv .venv && source .venv/bin/activate
pip3 install -U pip wheel
pip3 install -r requirements.txt
# Run the webserver.
FLASK_APP=src flask run
```


### Web GUI
Simple user interface to test the service is available at [http://127.0.0.1:5000](http://127.0.0.1:5000).


### API Endpoints
##### Analyze text for hate speech
```bash
curl -X POST http://127.0.0.1:5000/api/analyze -H "Content-Type: application/json" -d '{"text": "Your text goes here."}'
>>> {"comment":"No hate speech was detected in the given text.","labels":[]}
```
##### View history of analyzed texts
```bash
curl http://127.0.0.1:5000/api/history?limit=10
>>> [{"comment":"No hate speech was detected in the given text.","created_at":1705854943,"labels":[],"text":"Your text goes here."}, ...]
```
##### Export analysis history as CSV
```bash
curl -o export.csv http://127.0.0.1:5000/api/export
```


### Architecture
```
.
├── Dockerfile
├── README.md
├── requirements.txt
├── src
│   ├── config.py           # various configurables
│   ├── database.py         # database adapter
│   ├── __init__.py         # Flask web server & route definitions
│   ├── llm.py              # LLM adapter
│   ├── static              # static assets for web UI
│   │   ├── cutestrap.css
│   │   └── script.js
│   └── templates
│       └── index.html      # web UI single page app
└── temp
    └── model.gguf          # quantized Mistral-7B-Instruct-v0.2
```


### Improvements
- Initial prompt can be cached to speed up processing.
- Best to use asyncronously due to high latency (for ex. attach to a queue).
- Throughput is lacking - to be hosted on a GPU machine.
- For production, the persistent database should be considered.
- Mouting SQLite to a NFS volume is also an option.
- Add unit tests.
