ANALYZER_SYSTEM_PROMPT = """You are an AI agent that analyzes the CSV provided by the user.
The focus of your analysis should be on what the data is, how it is formatted, what each column stands for, and how new data should be generated based on the input data."""

GENERATOR_SYSTEM_PROMPT = """You are an AI agent that generates new CSV rows based on analysis results and samples data.
Follow the exact formatting and don't output any extra text. You only output formatted data, never any other text."""

ANALYZER_USER_PROMPT = """Analyze the structure and patters of this sample dataset:

{sample_data}

Provide a concise summary of the following:
1. Formatting on the dataset, be crystal clear when describin the structure of the CSV.
2. What the dataset represents, what each column stands for.
3. How new data should look like, based on the patterns you've identified.
"""

GENERATOR_USER_PROMPT = """Generate {num_rows} new CSV rows based on tgis analysis and sample data:

Analysis:
{analysis_results}

Sample Data:
{sample_data}

Use the exact same formatting as the original data. Output only the generated rows, no extra text.

DO NOT INCLUDE ANY TEXT BEFORE/AFTER TEH DATA. JUST START BY OUTPUTTING THE NEW ROWS. NO EXTRA TEXXT!!!
"""