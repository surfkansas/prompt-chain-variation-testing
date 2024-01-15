from distutils.core import setup
setup(
  name = 'pcvt',
  py_modules = ['pcvt'],
  entry_points = {
    'console_scripts': ['pcvt=pcvt.__main__:cli'],
  },
  install_requires=[
        'click>=8.1.7',
        'openai>=1.7.2',
        'python-dotenv>=1.0.0'
    ],
  description = 'pcvt is a simple command line implementation of prompt chain variation testing for OpenAI and Azure OpenAI',
  version = '0.0.108',
  author = 'Mark Sweat',
  author_email = 'mark@surfkansas.com',
  url = 'https://github.com/surfkansas/aws-ping-login'
)