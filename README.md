# Prompt Chain Variation Testing

Prompt Chain Variation Testing (PCVT) is a testing methodology for testing LLM prompts. It specifically is meant to address testing prompt *chains* in a scientific method by changing one component in the chain at the time and scoring results using an AI rubric prompt.

A sample notebook is provided in the `samples` folder to get you started. 

Full documentation will (hopefully) be added here in the near future. For now, this sample notebook should provide a jump start for those wishing to use this tool.

-- more here

## Installation

This `pcvt` tool can be installed via pip, directly from the GitHub repository:

```bash
pip install git+https://github.com/surfkansas/prompt-chain-variation-testing
```

In addition, you will likely want to install `jupyter` and `pandas` in order to have a better experience with the tool.

```bash
pip install jupyter pandas pyarrow
```

## Environment variables

To run the `pcvt` tool, you will need to set the following environment variables in a `.env` file in folder where you run your  jupyter notebook.

```

***When using OpenAI***
```
OPENAI_API_KEY=
```

***When using Azure OpenAI***
```
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
OPENAI_API_VERSION=
```


