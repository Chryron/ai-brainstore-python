# AI Brainstore Python

This is a proof-of-concept of a brain for an AI agent heavily inspired by [Mckay Wrigley](https://twitter.com/mckaywrigley/)'s [ai-brainstore](https://github.com/mckaywrigley/ai-brainstore) project.

This is a python port of the original project and it relies on the same high-level approach. The main difference is that this project does not use langchain or chroma. Instead I chose to learn and implement the vector database using [weviate](https://github.com/weaviate/weaviate-python-client), and borrowed some of the web-scraping and text summarization code from [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT).


## How It Works

Ask the agent a question.

If it knows the answer, then it will recall it from memory.

If it doesn't know the answer, then it will browse the web and learn about it.

As it learns, it will save its memories to its brain.

## Running Locally

**1. Clone Repo**

```bash
git clone https://github.com/Chryron/ai-brainstore-python
```

**2. Install Dependencies**

I use pipenv to manage dependencies, but you can use whatever you want.

### Installing pipenv
```bash
pip install pipenv
```
### Installing packages
```bash
cd ai-brainstore-python
pipenv install
pipenv shell
```

**3. Configure Settings**

Copy the .env.template file in the root of the repo and rename it to .env after you have filled in the values.

**4. Set up your Weviate Database**

This project uses a Weviate instance without authorization, hosted on Weviate Cloud Services (WCS) on the free tier. The [WCS quick-start guide](https://weaviate.io/developers/wcs/quickstart) should help you get started.

Note: The endpoint in your .env file should be the endpoint URL of your WCS instance.

**5. Run Script**

```bash
python main.py
```

**6. Use It**

You should now be able to interact with the agent via the terminal.
