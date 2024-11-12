# Company Researcher with Tavily and AI Agents

This open-source **Company Research Tool** leverages Tavily’s powerful `search` and `extract` capabilities to automate in-depth company research. The tool follows a structured, agent-driven workflow that dynamically curates and generates well-organized, comprehensive company reports, making it ideal for competitive intelligence, lead research, and Go-to-Market (GTM) analysis.

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

The Company Research Tool automates a **multi-stage workflow** for real-time company analysis. By integrating Tavily's `search` and `extract` capabilities with intelligent agents, this tool enables precise data collection, clustering, and curation of relevant information. It’s designed to be modular, making it easily adaptable to other research domains with minimal changes.

This workflow leverages Tavily's deep extraction and search functionalities in combination to gather both general context and targeted information. By utilizing feedback loops and human-in-the-loop verification, it ensures robust and accurate outputs, even in cases with companies that share similar names.

## How It Works

1. **Ground Truth Establishment**: The workflow begins by creating a foundational understanding of the company using Tavily’s `extract` tool on the primary URL. This "ground truth" guides subsequent steps.
2. **Sub-question Generation**: Based on the ground truth, targeted research questions are generated. These questions drive Tavily’s `search`, gathering focused, high-quality information.
3. **Research and Clustering**: Relevant documents are collected using Tavily’s `search`, then clustered by relevance. This clustering process organizes the data, especially useful when dealing with companies that have similar names.
4. **Human-in-the-Loop for Cluster Selection**: If clustering doesn’t yield an exact match to the target URL, manual review allows selection of the correct cluster to ensure accuracy.
5. **Data Enrichment**: The selected cluster undergoes further Tavily extraction, enriching the data to enhance completeness and reliability.
6. **Report Generation and Evaluation**: The curated data is used to generate a structured report, which is then evaluated for completeness. If gaps are found, a feedback loop prompts additional refinements.
7. **Output in Multiple Formats**: The final report can be exported as either a PDF or Markdown file, based on user preference.

## Getting Started

### Prerequisites

- Python 3.11 or later: [Python Installation Guide](https://www.tutorialsteacher.com/python/install-python)
- Tavily API Key - [Sign Up](https://tavily.com/)
- OpenAI API Key - [Sign Up](https://platform.openai.com/)


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

4. **Run the app**

```bash
python app.py
```

5. **Open the app in your browser**
```bash
http://localhost:8000
```

## Workflow Features

1. **User Input**: Define a **company name** and **URL** to initiate the research.
2. **Ground Truth Establishment with Tavily Extract**: Sets a foundational "ground truth" with Tavily `extact` from the main domain, helping to filter relevant information.
3. **Targeted Sub-question Generation**: Automatically generates sub-questions that guide Tavily’s `search` for specific, focused data.
4. **AI-Driven Clustering**: Clusters documents by relevance, using AI to manage cases where companies may have similar names.
5. **Human-in-the-Loop for Cluster Selection**: If clustering doesn’t produce a clear match, human intervention can select the appropriate cluster, ensuring data accuracy.
6. **Content Curation and Enrichment**: Refines the chosen cluster and enriches documents using Tavily `extract` for additional extraction, adding depth to the final report.
7. **Comprehensive Report Generation and Evaluation**: Builds a structured, detailed report with an evaluation step to ensure quality. Feedback loops allow refinement until completeness is achieved.
8. **Flexible Output Formats**: Generates the final report in PDF or Markdown format, ready for distribution.

## Workflow Diagram

Below is a diagram of the workflow, showing Tavily’s `extract` and `search` usage at various stages, feedback loops, and human-in-the-loop features.

![Workflow Diagram](path_to_workflow_diagram.png)

## Customization

This tool’s adaptable design enables it to serve various research applications. You can customize it in several ways:

- **Modify Prompts**: Tailor prompts in the question generation or report generation stages to suit different research needs.
- **Extend Workflow Nodes**: Add, remove, or adjust workflow nodes to focus on specific aspects of research or analysis.
- **Adjust Output Formats**: Customize the styling or format (e.g., via CSS for PDF styling) to match organizational needs.


## Future Directions

This project provides a flexible foundation for a wide range of research applications. By adjusting prompts and parameters, you can adapt it to suit different fields and needs. 
Potential applications include:

- **Market Analysis**: Adapt the workflow to analyze industry trends, competitive landscapes, or emerging technologies.
- **Lead Generation**: Use the tool to gather detailed profiles on prospective clients, identifying critical insights for business development.
- **Customizable Knowledge Bases**: Build ongoing research repositories for fields like law, finance, or medicine by continuously updating with new findings.

The adaptable structure of this workflow allows it to be tailored to any domain that requires structured, high-quality information gathering. As AI agents continue to evolve, this tool demonstrates how intelligent workflows, combined with robust data retrieval methods like Tavily’s `extract` and `search`, can revolutionize research and analysis across industries. 
