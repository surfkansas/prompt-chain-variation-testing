from distutils.core import setup
setup(
  name = 'pcvt',
  py_modules = ['pcvt'],
  install_requires=[
        'openai>=1.7.2',
        'python-dotenv>=1.0.0'
    ],
  description = 'pcvt is a simple command line implementation of prompt chain variation testing for OpenAI and Azure OpenAI',
  version = '0.1.108',
  author = 'Mark Sweat',
  author_email = 'mark@surfkansas.com',
  url = 'https://github.com/surfkansas/prompt-chain-variation-testing'
)