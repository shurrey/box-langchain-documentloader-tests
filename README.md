# Box Langchain DocumentLoader Test

This repo contains DocumentLoader tests in a number of scenarios using the developer token authentication method. 
* [Single file](document_loader_test_scripts/test_one_-_file.py)
* [Multiple files](document_loader_test_scripts/test_multiple_files.py)
* [All files in a folder](document_loader_test_scripts/test_folder.py)

It also enables tests for mutiple authentication methods:
* [Developer token](document_loader_test_scripts/test_folder.py) - used by the above tests
* [JWT with service account](document_loader_test_scripts/test_jwt_eid.py) - tests with a folder
* [JWT as user](document_loader_test_scripts/test_jwt_user.py) - tests with a folder
* [Client credentials grant with service account](document_loader_test_scripts/test_ccg_eid.py) - tests with a folder
* [Client credentials grant as user](document_loader_test_scripts/test_ccg_user.py) - tests with a folder

Finally, it provides both a Jupyter notebook and a script for testing the Box File Search Tool as part of a LangGraph agent.
* [Jupyter notebook](Test%20BoxFileSearchTool.ipynb) - to run locally, you must [install Jupyter notebooks](https://jupyter.org/install).
* [Test script](tool_test_scripts)/test_box_filesearch_tool.py

> [!IMPORTANT]  
> Until we merge the Box DocumentLoader with langchain, you will need to clone the langchain fork [here](https://github.com/shurrey/langchain) and run it locally to test.

## Prepare langchain repo for use locally
To prepare the langchain fork for use locally, you will need to follow these steps. These steps assume you have git and python installed and available at the commandline.

1. In your directory of choosing in the command prompt or terminal on your local machine, run `git clone https://github.com/box-community/langchain.git`.
2. Navigate to the langchain code package, by running `cd langchain/libs/core`
3. Install all dependencies by running `pip install -e .`
4. Navigate to the langchain package, by running `cd ../langchain`
5. Install all dependencies by running `pip install -e .`
6. Navigate to the langchain text-splitters package, by running `cd ../text-splitters`
7. Install all dependencies by running `pip install -e .`
Navigate to the langchain community package, by running `cd ../community`
8. Install all dependencies by running `pip install -e .`
9. Make note of the path. It will be something like `/Users/shurrey/local/langchain/libs/community`. You will need this as we set up these tests.

## Prepare the test suite for use

Now that we have langchain ready to use locally, we can now set up the tests to run. The test scripts rely on two key components, the environment files located in the [config](config) folder and the [box search](box_search.py) object.

The environment files are use to configure the tests to work. 

File | Purpose | Required
---+---+---
[.openai.env.template](.openai.env.template) | Configure openai API key | Yes
[.box.env.template](.box.env.template) | Configure Box-specific fields like file and folder ids | Yes
[.token.env.template](.token.env.template) | Configure developer token auth | Only for token tests
[.jwt.env.template](.jwt.env.template) | Configure JWT auth | Only for JWT tests
[.ccg.env.template](.ccg.env.template) | Configure CCG Auth | Only for CCG tests

The [box search](box_search.py) object enables a "real-life" scenario after the test scripts load the appropriate Documents from Box. box_search provides a two methods, `train_ai` and `box_search`.

The `train_ai` method accepts the documents return from the BoxLoader as an argument. It then does several things with those documents. First, it splits the documents into logical chunks using langchains `RecursiveCharacterTextSplitter`. It then takes those chunks of text, converts them to OpenAI embeddings and commits them to a local Chroma vector store. Finally, it instantiates a `ChatOpenAI` as the llm of choice, creates an `LLMChainExtractor` as a compressor, and uses it and Chroma as a `ContextualCompressionRetriever`. 

Many thanks to [HTMLFiveDev](https://www.youtube.com/@htmlfivedev) for their [video](https://www.youtube.com/watch?v=_zdpmxpH7S0), on which this object is based.

OK, assuming you have completed the steps above to get the langchain fork installed and prepped, let's get this started.

1. In your terminal, clone this repository to your local machine by running `git clone https://github.com/shurrey/box-langchain-documentloader-tests.git`. **This should not be inside of the langchain directory**.
2. Change directories to the project by running `cd box-langchain-documentloader-tests`. Open the folder in your favorite editor.
3. Remember that file path from prepping the langchain fork? Edit [requirements.txt](requirements.txt) and replace `file:///Users/shurrey/local` with the path to your langchain directory. You should now have entries for the core, langchain, text_splitters, and community modules that look like `file:///YOUR_PATH/langchain/libs/community`.
4. In the config directory, copy the environment templates to new files, for example, copy `.box.env.template` to `.box.env`. You must have `.box.env`, `.openai.env`, and whichever auth modes you plan to use. Open the newly created files, and add your values. 
5. Install the libraries you need. I recommend using a virtual environment. Follow [these instructions](https://virtualenv.pypa.io/en/latest/installation.html) to install it. Once installed, you can create a virtual environment at the command line in the root directory of this application by running `virtualenv .venv`.
6. Once you complete that step, you can activate your virtual environment at the commandline by running `source .venv/bin/activate`. This should change your command line prompt and prepend it with `(.venv)`.
7. Now you can install your dependencies at the commandline in the root directory of this application by running `pip install -r requirements.txt`.
5. You should now be all set to run the tests. Each test has a variable called `prompt`, which you can set based on the file(s) or folder you choose. It will be asked to OpenAI, so you will get a real answer based on the file(s) you provide. 

To run the tests, you can either use the tools provided by your development environment, or from the command line, run `python TEST_NAME.py` where TEST_NAME is the file name of the test you wish to run. For example, to test one file, you can run `python test-one-file.py`.