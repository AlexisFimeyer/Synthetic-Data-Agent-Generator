import os
import csv
import requests
import json
from prompts import *

# Function to read the CSV from the user
def read_csv(file_path):
    data = []
    with open(file_path, "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Function to save the generated data to a new CSV file
def save_to_csv(data, output_file, headers=None):
    mode = "w" if headers else "a"
    with open(output_file, mode, newline='') as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for row in csv.reader(data.splitlines()):
            writer.writerow(row)

# Function to get the list of available Ollama models
def get_ollama_models():
    try:
        response = requests.get(f"{os.getenv('OLLAMA_BASE_URL')}/api/tags")
        response.raise_for_status()
        models = response.json()['models']
        return models
    except requests.exceptions.RequestException as e:
        print(f"Error fetching models: {e}")
        return []

# Function to prompt the user to select an Ollama model
def prompt_user_for_model(models):
    if not models:
        print("No models available.")
        return None
    print("Available Ollama models:")
    for i, model in enumerate(models):
        print(f"{i + 1}. {model['name']}")
    choice = int(input("Select the model number you want to use: ")) - 1
    return models[choice]['model']

# Function to send requests to the local Ollama instance and process the streaming response
def send_request_to_ollama(prompt, model, max_tokens, temperature):
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "prompt": prompt
    }
    response = requests.post(f"{os.getenv('OLLAMA_BASE_URL')}/api/generate", json=payload, stream=True)
    response.raise_for_status()

    result_text = ""
    for line in response.iter_lines():
        if line:
            line_content = line.decode('utf-8')
            try:
                json_content = json.loads(line_content)
                result_text += json_content['response']
            except json.JSONDecodeError:
                continue
    return {"choices": [{"text": result_text}]}

# Function to give the sample data to the analyzer agent
def analyzer_agent(sample_data, model):
    prompt = ANALYZER_USER_PROMPT.format(sample_data=sample_data)
    response = send_request_to_ollama(prompt, model, 400, 0.1)
    return response["choices"][0]["text"]

# Function to give the analysis results and sample data to the generator agent
def generator_agent(analysis_result, sample_data, model, num_rows=30):
    prompt = GENERATOR_USER_PROMPT.format(
        num_rows=num_rows,
        analysis_results=analysis_result,
        sample_data=sample_data
    )
    response = send_request_to_ollama(prompt, model, 1500, 1)
    return response["choices"][0]["text"]

# Main function
def main():
    file_path = input("\nEnter the path to the CSV file: ")
    file_path = file_path.strip()
    desired_rows = int(input("Enter the number of rows you want to generate for the new dataset: "))

    # Get available models and prompt the user to select one
    models = get_ollama_models()
    selected_model = prompt_user_for_model(models)

    if not selected_model:
        print("No model selected. Exiting.")
        return

    sample_data = read_csv(file_path)
    sample_data_str = "\n".join([",".join(row) for row in sample_data])

    print("\nLaunching team Agents...")
    analysis_result = analyzer_agent(sample_data_str, selected_model)
    if not analysis_result:
        print("Analyzer agent failed. Exiting.")
        return

    print("\n### Analyzer Agent output: ###\n")
    print(analysis_result)
    print("--------------------------------------------------------------------------------------------------- \n\nGenerating new data...")

    output_file = "/app/data/new_dataset.csv"
    headers = sample_data[0]
    save_to_csv("", output_file, headers)

    batch_size = 30
    generated_rows = 0

    while generated_rows < desired_rows:
        rows_to_generate = min(batch_size, desired_rows - generated_rows)
        generated_data = generator_agent(analysis_result, sample_data_str, selected_model, rows_to_generate)
        if not generated_data:
            print("Generator agent failed. Exiting.")
            return
        save_to_csv(generated_data, output_file)
        generated_rows += rows_to_generate
        print(f"Generated {generated_rows} rows out of {desired_rows}")
        
    print(f"\nNew dataset generated and saved to {output_file}")

if __name__ == "__main__":
    main()
