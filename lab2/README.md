# LLM Prompt Injection Lab 2

This is a Flask application that demonstrates prompt injection vulnerabilities. But this time with [Rebuff](https://github.com/protectai/rebuff) in place!


## Requirements

- Python 3.x
- Flask
- google-generativeai
- rebuff

## Side Note
You might have some trouble setting up Pinecone with Rebuff. Refer to this
[Github Issue](https://github.com/protectai/rebuff/issues/105)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/vicevirus/prompt-injection-lab
    ```

2. Change into the project directory:

    ```bash
    cd lab2
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Or just use the Dockerfile (remember to set the API Key first) :)

## Usage

1. Start the Flask application:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Exploit it!

## Known solution
None yet. It blocks most of my prompt injection. Though, I haven't tested much.

