
import os
from datetime import datetime
from ..utils.pdf_utils import generate_pdf_from_md
from ..format_classes import ResearchState

class PublishNode:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    async def markdown_to_pdf(self, markdown_content: str, output_path: str):
        try:  
            # Generate the PDF from Markdown content
            generate_pdf_from_md(markdown_content, output_path)
            print(f"PDF report generated at: {output_path}")
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {str(e)}")

    async def format_output(self, state: ResearchState):
        report = state["report"]
        output_format = state.get("output_format", "pdf")  # Default to PDF

        # Set up the directory and file paths
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_base = f"{self.output_dir}/{state['company']}_Weekly_Report_{timestamp}"
        
        if output_format == "pdf":
            pdf_file_path = f"{file_base}.pdf"
            await self.markdown_to_pdf(markdown_content=report, output_path=pdf_file_path)
            formatted_report = f"PDF report saved at {pdf_file_path}"
        else:
            markdown_file_path = f"{file_base}.md"
            with open(markdown_file_path, "w") as md_file:
                md_file.write(report)
            formatted_report = f"Markdown report saved at {markdown_file_path}"

        return {"messages": [{"role": "assistant", "content": "Final report formatted."}], "save_report": formatted_report}

    async def run(self, state: ResearchState):
        result = await self.format_output(state)
        return result
    
# import os
# from datetime import datetime
# from md2pdf.core import md2pdf
# from ..format_classes import ResearchState

# class PublishNode:
#     def __init__(self):
#         pass

#     async def markdown_to_pdf(self, markdown_content: str, output_path: str):
#         try:  
#             # Use md2pdf to generate PDF
#             md2pdf(output_path, md_content=markdown_content)
#             print(f"PDF report generated at: {output_path}")
#         except Exception as e:
#             raise Exception(f"Failed to generate PDF: {str(e)}")

#     async def format_output(self, state: ResearchState):
#         report = state["report"]
#         output_format = state.get("output_format", "pdf")  # Default to PDF

#         # Set up the directory and file paths
#         directory = "reports"
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#         timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#         file_base = f"{directory}/{state['company']}_Weekly_Report_{timestamp}"
        
#         if output_format == "pdf":
#             # Convert directly from Markdown to PDF
#             pdf_file_path = f"{file_base}.pdf"
#             await self.markdown_to_pdf(markdown_content=report, output_path=pdf_file_path)
#             formatted_report = f"PDF report saved at {pdf_file_path}"
#         else:
#             # If specified Markdown; just save the report text
#             markdown_file_path = f"{file_base}.md"
#             with open(markdown_file_path, "w") as md_file:
#                 md_file.write(report)
#             formatted_report = f"Markdown report saved at {markdown_file_path}"

#         return {"messages": [{"role": "assistant", "content": "Final report formatted."}], "save_report": formatted_report}

#     async def run(self, state: ResearchState):
#         result = await self.format_output(state)
#         return result