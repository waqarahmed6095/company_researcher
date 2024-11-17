from datetime import datetime
from langchain_core.messages import AIMessage
from langchain_anthropic import ChatAnthropic
from ..format_classes import ResearchState



class GenerateNode:
    def __init__(self):
        self.model = ChatAnthropic(
            model="claude-3-5-sonnet-20240620",
            temperature=0
        )
    def extract_markdown_content(self, content):
        # Strip out extra preamble or conversational text, retaining only Markdown.
        start_index = content.find("#")  # Find the start of the markdown sections
        if start_index != -1:
            return content[start_index:].strip()
        return content.strip()

    async def generate_report(self, state: ResearchState):
        report_title = f"Weekly Report on {state['company']}"
        report_date = datetime.now().strftime('%B %d, %Y')

        # prompt = f"""
        # You are an expert researcher tasked with writing a fact-based report on recent developments for the company **{state['company']}**. Write the report in Markdown format, but **do not include a title**:
        # Documents to Base the Report On:
        # {state['documents']}

        # """
        prompt = f"""
        You are an expert researcher tasked with writing a fact-based report on recent developments for the company **{state['company']}**. Write the report in Markdown format, but **do not include a title**. Each section must be written in well-structured paragraphs, not lists or bullet points.
        Ensure the report includes:
        - **Inline citations** as Markdown hyperlinks directly in the main sections (e.g., Company X is an innovative leader in AI ([LinkedIn](https://linkedin.com))).
        - A **Citations Section** at the end that lists all URLs used.

        ### Report Structure:
        1. **Executive Summary**:
            - High-level overview of the company, its services, location, employee count, and achievements.
            - Make sure to include the general information necessary to understand the company well including any notable achievements.

        2. **Leadership and Vision**:
            - Details on the CEO and key team members, their experience, and alignment with company goals.
            - Any personnel changes and their strategic impact.

        3. **Product and Service Overview**:
            - Summary of current products/services, features, updates, and market fit.
            - Include details from the company's website, tools, or new integrations.

        4. **Financial Performance**:
            - For public companies: key metrics (e.g., revenue, market cap).
            - For startups: funding rounds, investors, and milestones.

        5. **Recent Developments**:
            - New product enhancements, partnerships, competitive moves, or market entries.

        6. **Citations**:
            - Ensure every source cited in the report is listed in the text as Markdown hyperlinks.
            - Also include a list of all URLs as Markdown hyperlinks in this section.

        ### Documents to Base the Report On:
        {state['documents']}
        """

        messages = [("system", "Your task is to generate a Markdown report."), ("human", prompt)]

        try:
            # Invoke the model
            response = await self.model.ainvoke(messages)

            # Extract the Markdown content
            markdown_content = self.extract_markdown_content(response.content)

            # Add the title and date to the response
            full_report = f"# {report_title}\n\n*{report_date}*\n\n{markdown_content}"
            return {"messages": [AIMessage(content=f"Generated Report:\n{full_report}")], "report": full_report}
        except Exception as e:
            error_message = f"Error generating report: {str(e)}"
            return {
                "messages": [AIMessage(content=error_message)],
                "report": f"# Error Generating Report\n\n*{report_date}*\n\n{error_message}"
            }


    async def run(self, state: ResearchState):
        result = await self.generate_report(state)
        return result