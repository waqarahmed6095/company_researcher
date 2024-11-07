# Company Researcher Workflow with Tavily and AI Agents

This open-source **Company Research Tool** leverages Tavily’s advanced `search` and `extract` capabilities to automate in-depth company research. With a flexible, agent-driven process, it generates well-structured and comprehensive company reports, ideal for competitive intelligence, lead research, and GTM (Go-to-Market) analysis.

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Application](#running-the-application)
3. [Workflow Features](#workflow-features)
4. [Workflow Diagram](#workflow-diagram)
5. [Customization](#customization)
6. [Future Directions](#future-directions)

## Overview

This tool automates a **multi-stage workflow** to collect, organize, and analyze real-time data about target companies using Tavily’s search and extract functions. Designed for modularity, it can be adapted to various research tasks beyond company analysis, with simple modifications. 

### How It Works
1. **Initial Search and Ground Truth**: The workflow starts by establishing a baseline (or "ground truth") through Tavily’s `extract` tool on the primary company URL. This foundational information helps filter relevant data in later steps.
2. **Targeted Question Generation**: Based on the ground truth, the tool generates targeted questions that guide Tavily’s `search`, ensuring that only the most relevant and high-quality information is gathered.
3. **Research and Clustering**: Using Tavily’s `search`, documents are collected and organized into clusters based on relevance. AI-powered clustering ensures accuracy, especially in cases where multiple companies have similar names.
4. **Human-in-the-Loop Verification**: If clustering doesn’t automatically identify the correct information (e.g., no clear match to the input URL), a human-in-the-loop step allows manual selection of the right cluster.
5. **Data Enrichment**: The chosen cluster is enriched with further extraction from Tavily, adding depth and completeness to the data.
6. **Report Generation and Feedback Loop**: A structured report is generated and evaluated for completeness. If gaps are found, the workflow loops back to refine content until the report meets quality standards.
7. **Final Output**: The polished report is formatted and saved in the desired format (PDF or Markdown) for easy access and distribution.

## Getting Started

### Prerequisites

- **Python 3.11 or later**: [Python Installation Guide](https://www.tutorialsteacher.com/python/install-python)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/danielleyahalom/company_researcher.git
   cd company_researcher
   ```

2. **Set Up API Keys**:
   Configure your OpenAI and Tavily API keys as environment variables or place them in a `.env` file:

   ```bash
   export OPENAI_API_KEY={Your OpenAI API Key here}
   export TAVILY_API_KEY={Your Tavily API Key here}
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Open `app.py` and set the **company name**, **URL**, and optionally the **output format** (`pdf` or `markdown`). If `output_format` is omitted, it defaults to `pdf`.

   Here is an example configuration in `app.py`:

   ```python
   # app.py
   import asyncio
   from .graph import Graph

   async def main():
       # Initialize the Graph
       graph = Graph()

       # Set up the company name and URL
       company_name = "Tavily"  # Replace with the desired company name
       company_url = "https://tavily.com/"  # Replace with the desired company URL

       # Specify output format; defaults to "pdf" if not specified
       output_format = "pdf"  # Change to "markdown" if desired

       # Run the graph for the specified company, URL, and output format
       await graph.run(company=company_name, url=company_url, output_format=output_format)

   if __name__ == "__main__":
       asyncio.run(main())
   ```

2. Start the application:

   ```bash
   python -m backend.app
   ```

## Workflow Features

1. **User Input**: Define a **company name** and **URL** to kickstart the research.
2. **Ground Truth with Tavily Extract**: Establishes a baseline from the company’s main web domain, setting a “ground truth” for the research.
3. **Sub-question Generation**: Dynamically generates sub-questions that guide Tavily’s `search` for focused, high-quality information.
4. **AI-Driven Clustering**: Organizes retrieved documents by relevance, leveraging AI to ensure accuracy in cases of companies with similar names.
5. **Human-in-the-Loop for Cluster Selection**: Allows optional manual intervention if automatic clustering doesn’t yield a definitive match, improving the quality of the final data.
6. **Document Curation and Enrichment**: Further refines and enriches the data with detailed content, ensuring the report is robust.
7. **Report Generation and Evaluation**: Generates a structured, in-depth report with built-in evaluation, looping back to refine as necessary.
8. **Multi-format Output**: Saves the final report as a PDF or Markdown file, ready for distribution.

## Workflow Diagram

Below is a diagram of the workflow, highlighting Tavily’s `extract` and `search` at various stages, feedback loops, and human-in-the-loop elements for cluster selection.

![Workflow Diagram](path_to_workflow_diagram.png)  


## Customization

This tool’s modular structure makes it adaptable to a wide range of research applications. Here’s how you can customize it:

- **Modify Prompts**: Adjust the prompts in the sub-question generation and report generation steps to focus on different research aspects or areas.
- **Extend Workflow Nodes**: Add, remove, or modify nodes in the workflow to tailor the process to specific research requirements.
- **Adjust Output Formats**: Customize the output format or style (e.g., using a CSS file for PDF styling) to suit organizational or reporting needs.

## Future Directions

This project serves as a flexible foundation that can be adapted to various domains by tweaking prompts and parameters. Possible applications include:

- **Market Analysis**: Adapt for analyzing industry trends or competitor performance.
- **Lead Generation**: Use as an automated lead research tool to gather detailed profiles on prospective clients.
- **General Topic Research**: Apply the workflow to other fields, such as academic research or trend analysis in technology and business.
