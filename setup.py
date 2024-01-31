from distutils.core import setup
setup(
  name = 'pcvt',
  packages = ['pcvt'],
  install_requires=[
        'openai>=1.7.2',
        'python-dotenv>=1.0.0'
    ],
  description = 'pcvt is a tool to scale-test small changes to a chat prompt chain for OpenAI and Azure OpenAI GPT backends',
  version = '0.1.108',
  author = 'Mark Sweat',
  author_email = 'mark@surfkansas.com',
  url = 'https://github.com/surfkansas/prompt-chain-variation-testing'
)