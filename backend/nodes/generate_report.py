import tldextract
from datetime import datetime
from langchain_core.messages import AIMessage, SystemMessage
from ..format_classes import ResearchState, QuotedAnswer
from ..utils.utils import final_model

class GenerateNode:
    def __init__(self):
        pass
    async def generate_report(self, state: ResearchState):
            # Define a consistent title and subtitle format
        report_title = f"Weekly Report on {state['company']}"
        report_date = datetime.now().strftime('%B %d, %Y')

        prompt = f"""
            You are an expert researcher tasked with writing a fact-based report on recent developments for the company **{state['company']}**. Format the report in Markdown with the following sections only, without adding a title or subtitle. Only include the section content.

            ### Report Structure:
            1. **Executive Summary**:
            - Provide a high-level overview of the company and the service it provides, where it is located, and the number of employees.
            - Make sure to include the general information necessary to understand the company well including any notable achievements.

            2. **Leadership and Vision**:
            - Highlight the **CEO** and other key team members, especially if their experience aligns with the company’s strategic goals.
            - Mention key personnel changes, such as new hires or departures in pivotal roles, and their anticipated impact on the company’s strategy.
            - Include quotes or statements from leadership to reflect their vision if available.

            3. **Product and Service Overview**:
            - Summarize current products/services, focusing on unique features, market fit, and recent updates.
            - Highlight product specifics, particularly from the original company website, including new tools, integrations, or feature updates.
            - Mention customer impact metrics if available, such as satisfaction scores or adoption rates.

            4. **Financial Performance**:
            - For public companies, summarize key metrics like **revenue growth, market cap, and stock performance**.
            - For startups, emphasize **funding rounds, key investors, and revenue milestones**.
            - Note any recent shifts in financial strategy, such as a focus on profitability or R&D investment.

            5. **Recent Developments**:
            - Outline any product enhancements, strategic partnerships, or other significant initiatives.
            - Include competitive moves, such as market entries or client acquisitions, and how **{state['company']}** is positioned in response.

            ### Initial Company Information:
            This section contains information directly from the company's website:
            {state['initial_documents']}

            ### Documents to Base the Report On:
            {state['documents']}
            """

            # Invoke model for report generation
        messages = [SystemMessage(content=prompt)]
        response = await final_model.with_structured_output(QuotedAnswer).ainvoke(messages)
            
            # Assemble the final report with a consistent title and date
        full_report = f"# {report_title}\n\n*{report_date}*\n\n" + response.answer

            # Append citations only if needed, formatted separately from the main report
        if response.citations:

            full_report += "\n\n### Citations\n"
            for citation in response.citations:
                domain_name = tldextract.extract(citation.source_id).domain.capitalize()  # Extract and capitalize the domain name
                full_report += f"- [{domain_name}]({citation.source_id}): \"{citation.quote}\"\n"

            # Return the report with the title, subtitle, and content
        return {"messages": [AIMessage(content=f"Generated Report:\n{full_report}")], "report": full_report}

    async def run(self, state: ResearchState):
        result = await self.generate_report(state)
        return result