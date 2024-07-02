# Synthetic Data Generator using Ollama

This project leverages a locally running Ollama LLM to create synthetic data based on input CSV files. The process involves analyzing the provided data structure and generating new data rows that adhere to the identified patterns.

## Prerequisites

1. **Docker**: Ensure you have Docker installed on your machine.
2. **Ollama LLM**: Ensure Ollama is running on your host machine and accessible at port `11434`.

## Project Structure
```.
├── Dockerfile
├── agents.py
├── prompts.py
├── requirements.txt
├── data
│   └── example_data.csv
└── README.md
```

## Files

- **Dockerfile**: The Docker configuration file to build the container.
- **agents.py**: The main script for analyzing and generating data.
- **prompts.py**: Contains prompts used for the analysis and data generation.
- **requirements.txt**: Lists the dependencies required for the project.
- **data/**: Directory containing the input CSV file (`example_data.csv`).

## Prepare the Data
Ensure you have an input CSV file placed in the data directory. An example file example_data.csv is already provided.

## Build the Docker Image
Build the Docker image using the following command:
``
docker build -t synthetic-data-generator .
``
## Run the Docker Container
Run the Docker container with the volume mount to the data directory:
``
docker run -it --rm -v $(pwd)/data:/app/data synthetic-data-generator
``
## Follow the Prompts
When you run the container, follow the prompts to:

Enter the path to the CSV file that you saved in the `/app/data` folder(e.g., `example_data.csv`).
Enter the number of rows you want to generate for the new dataset.
Select the model number you want to use from the available Ollama models.
The generated data will be saved to new_dataset.csv in the data directory.
