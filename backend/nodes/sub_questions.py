from langchain_core.messages import AIMessage, SystemMessage
from ..format_classes import ResearchState, TavilySearchInput
from ..utils.utils import model

class SubQuestionsNode:
    def __init__(self) -> None:
        pass
     
    # Function to generate sub-questions based on initial search data
    async def generate_sub_questions(self, state: ResearchState):
        try:
            msg = "Generating sub-questions based on the initial search results...\n"
            
            if 'sub_questions_data' not in state:
                state['sub_questions_data'] = []
                
            # Prompt to generate detailed sub-questions
            prompt = f"""
            You are an expert researcher focusing on company analysis.
            Your task is to generate 5 to 6 specific sub-questions that will provide a thorough understanding of the company: '{state['company']}'.
            
            ### Key Areas to Explore:
            - **Company Background**: Include history, mission, headquarters location, and number of employees.
            - **Products and Services**: Focus on main offerings, unique features, and target customer segments.
            - **Market Position**: Address competitive standing, market reach, and industry impact.
            - **Financials**: Seek recent funding, revenue milestones, financial performance, and growth indicators.
            - **Reputation and Partnerships**: Explore public perception, major partnerships, and recent developments.

            Ensure these questions include specific inquiries about **number of employees**, **headquarters location**, and **revenue** as they are essential details for the report.
            
            Use the initial information provided from the company's website below to keep questions directly relevant to **{state['company']}**.

            Official URL: {state['company_url']}
            Initial Company Information:
            {state["initial_documents"]}
            
            Ensure questions are clear, specific, and well-aligned with the company's context.
            """
            
            # Use LLM to generate sub-questions
            messages = [SystemMessage(content=prompt)]
            sub_questions = await model.with_structured_output(TavilySearchInput).ainvoke(messages)
            msg += f"Generated {len(sub_questions.sub_queries)} sub-questions.\n"
        except Exception as e:
            msg = f"An error occurred during sub-question generation: {str(e)}"
        
        return {"messages": [AIMessage(content=msg)], "sub_questions": sub_questions, "initial_documents": state['initial_documents']}
            
    async def run(self, state: ResearchState):
        result = await self.generate_sub_questions(state)
        return result