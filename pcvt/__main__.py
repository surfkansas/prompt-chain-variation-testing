import os
import json

import openai
import click
import dotenv

if os.path.isfile('.env'):
    dotenv.load_dotenv()

@click.group()
def cli():
    pass

@cli.command('run-experiment')
@click.option('-e', '--experiment', type=click.Path(),
    required=True,
    help='The JSON file that contains the experiment configuration.')
@click.option('-t', '--test-name', type=click.Path(),
    required=True,
    help='The name of the test to run.')
@click.option('-o', '--output', type=click.Path(),
    required=True,
    help='The output folder for the experiment.')
@click.option('-m', '--max-executions', type=int,
    help='The maximum number of executions to run.')
def run_experiment(experiment, test_name, output, max_executions):
    
    print()
    print(f'Running experiment: {experiment}')

    experiment_folder = os.path.dirname(experiment)

    with open(experiment) as f:
        experiment_data = json.load(f)

    test = experiment_data['tests'][test_name]
    
    print(f'  Runing test: {test_name}')

    chain = []

    for chain_fragment in test['chain']:
        chain_filename = chain_fragment['file']
        chain_relative_filename = os.path.join(experiment_folder, chain_filename)
        with open(chain_relative_filename) as f:
            chain_fragment_data = json.load(f)
            chain_fragment_slice = chain_fragment_data[chain_fragment['start_index']:chain_fragment['start_index'] + chain_fragment['count']]
            chain.extend(chain_fragment_slice)

    test_output = os.path.join(output, test_name)

    os.makedirs(test_output, exist_ok=True)

    provider = experiment_data['provider']

    if 'provider' in test:
        provider = test['provider']

    if provider == 'openai':
        client = openai.OpenAI()
    elif provider == 'azure':
        client = openai.AzureOpenAI()

    params = {'messages': chain}

    if 'settings' in experiment_data:
        for setting in experiment_data['settings']:
            params[setting] = experiment_data['settings'][setting]

    if 'settings' in test:
        for setting in test['settings']:
            params[setting] = test['settings'][setting]

    count = 0

    for test_number in range(1, test['run_count'] + 1):
        test_file = os.path.join(test_output, f'{test_number}.json')
        if os.path.isfile(test_file):
            print(f'    Test iteration {test_number} already exists.')
        else:
            print(f'    Running test iteration {test_number}...')

            results = client.chat.completions.create(**params)

            with open(test_file, 'w') as f:
                f.write(results.model_dump_json(indent=4))
            count += 1

        if max_executions is not None and count >= max_executions:
            print('Exiting, as maximum number of executions has been reached.')
            break

    print()


if __name__ == '__main__':
    cli()