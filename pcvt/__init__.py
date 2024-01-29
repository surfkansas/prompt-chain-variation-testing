import os
import json

from openai import AzureOpenAI, OpenAI

class Test:
    def __init__(self):
        pass

    def run_test(self, results_path):
        print(f'\nRunning test: {self.name}')

        test_folder = os.path.join(results_path, self.name)
        os.makedirs(test_folder, exist_ok=True)

        if self.provider == 'openai':
            client = OpenAI()
        elif self.provider == 'azure':
            client = AzureOpenAI()

        for test_number in range(1, self.run_count + 1):
            test_file = os.path.join(test_folder, f'{test_number:04}.test.json')

            if os.path.isfile(test_file) == False:
                print(f'  Running test: {test_file}')

                params = {'messages': self.chain, **self.settings}

                results = client.chat.completions.create(**params)

                with open(test_file, 'w') as f:
                    f.write(results.model_dump_json(indent=4))

        print('Completed test run')

class Scoring:
    def __init__(self):
        pass

    def run_scoring(self, results_path):
        print(f'\nRunning scoring: {self.name}')

        if self.provider == 'openai':
            client = OpenAI()
        elif self.provider == 'azure':
            client = AzureOpenAI()

        system_prompt = 'You are an AI assistant tasked with scoring responses. You will be provided with a response and a rubric. Your task is to score the response based on the rubric.'
        
        if self.system_prompt is not None:
            system_prompt = self.system_prompt

        if self.abstract is not None:
            system_prompt += f'\n\nScoring abstract: {self.abstract}'

        system_prompt += '\n\nThe following values should be used for the scoring rubric:\n'

        for rubric_score in self.rubric:
            system_prompt += f'\n* {rubric_score}: {self.rubric[rubric_score]}'

        if self.grounding is not None:
            system_prompt += f'\n\nUse the following grounding content to evaluate the response against the rubric:\n\n{self.grounding}\n'

        system_message = {
            'role': 'system',
            'content': system_prompt
        }

        scoring_tool = {
            'type': 'function',
            'function': {
                'name': 'supply_score',
                'description': 'Supply a score for the response based on the rubric.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'score': {
                            'type': 'string',
                            'decription': 'The rubric score calculated for the response.'
                        },
                        'reason': {
                            'type': 'string',
                            'description': 'The reason for the score.'
                        }
                    },
                    'required': [ 'score' ]
                }
            }
        }

        for root, dirs, files, in os.walk(results_path):
            for file in sorted(files):
                if file.endswith('.test.json'):
                    test_file = os.path.join(root, file)
                    score_file = os.path.join(root, f'{file}.{self.name}.score.json')
                    
                    if os.path.isfile(score_file) == False:
                        print(f'  Running scoring for test: {test_file}...')

                        with open(test_file) as f:
                            test_data = json.load(f)

                        test_message = test_data['choices'][0]['message']

                        for message_key in list(test_message):
                            if test_message[message_key] is None:
                                del test_message[message_key]

                        chain = [system_message, test_message]

                        params = {
                            'messages': chain, 
                            'tools': [scoring_tool], 
                            'tool_choice': 'supply_score', 
                            'tool_choice': 'auto', 
                            **self.settings
                        }

                        results = client.chat.completions.create(**params)

                        with open(score_file, 'w') as f:
                            f.write(results.model_dump_json(indent=4))
        
        print('Completed scoring run')
                        

class Experiment:
    
    def __init__(self):
        pass

    def from_file(experiment_filename):
        experiment = Experiment()

        expriment_directory = os.path.dirname(experiment_filename)

        with open(experiment_filename) as f:
            experiment_definition = json.load(f)

        experiment.provider = experiment_definition['provider']
        experiment.settings = experiment_definition['settings']

        tests = {}

        for test_name in experiment_definition['tests']:
            test = Test()
            test.name = test_name
            test.run_count = experiment_definition['tests'][test_name]['run_count']
            
            if 'settings' in experiment_definition['tests'][test_name]:
                test.settings = experiment_definition['tests'][test_name]['settings']
            else:
                test.settings = experiment.settings

            if 'provider' in experiment_definition['tests'][test_name]:
                test.provider = experiment_definition['tests'][test_name]['provider']
            else:
                test.provider = experiment.provider

            chain = []  
            for chain_fragment in experiment_definition['tests'][test_name]['chain']:
                chain_filename = chain_fragment['file']
                chain_relative_filename = os.path.join(expriment_directory, chain_filename)
                with open(chain_relative_filename) as f:
                    chain_fragment_data = json.load(f)
                    chain_fragment_slice = chain_fragment_data[chain_fragment['start_index']:chain_fragment['start_index'] + chain_fragment['count']]
                    chain.extend(chain_fragment_slice)
            test.chain = chain

            tests[test_name] = test

        experiment.tests = tests

        scores = {}

        for score_name in experiment_definition['scoring']['scores']:
            score = Scoring()

            score.name = score_name
            score.provider = experiment_definition['scoring']['provider']
            score.settings = experiment_definition['scoring']['settings']
            score.system_prompt = experiment_definition['scoring']['scores'][score_name].get('system_prompt', None)
            score.abstract = experiment_definition['scoring']['scores'][score_name].get('abstract', None)
            score.rubric = experiment_definition['scoring']['scores'][score_name]['rubric']
            score.grounding = experiment_definition['scoring']['scores'][score_name].get('grounding', None)
            
            scores[score_name] = score

        experiment.scores = scores

        return experiment
    
    def run_tests(self, results_path):
                  
        for test_name in self.tests:
            self.tests[test_name].run_test(results_path)

    def run_scoring(self, results_path):
        
        for score_name in self.scores:
            self.scores[score_name].run_scoring(results_path)