from langchain_core.messages import AIMessage, SystemMessage
import asyncio
from datetime import datetime
from typing import List, Literal

from ..format_classes import ResearchState,DocumentClusters
from ..utils.utils import final_model


class ClusterNode:
    def __init__(self):
        pass

    async def cluster(self, state: ResearchState):
        company = state['company']
        company_url = state['company_url']
        initial_docs = state['initial_documents']
        documents = state.get('documents', {})
        
        msg = "Initiating clustering process to separate documents by associated company...\n"

        # Extract compnay domain from URL
        target_domain = company_url.split("//")[-1].split("/")[0]

        # Collect all retrieved documents without duplicates
        all_retrieved_urls = [{'url': url, 'content': doc.get('content', '')} for url, doc in documents.items()]

        # LLM prompt to categorize documents accurately
        prompt = f"""
            We conducted a search for a company called '{company}', but the results may include documents from other companies with similar names or domains.
            Your task is to categorize the retrieved documents by identifying which specific company they pertain to, using the initial company information as the "ground truth" to help distinguish the correct company.


            ### Target Company Information
            - **Company Name**: '{company}'
            - **Primary Domain**: '{target_domain}'
            - **Initial Context (Ground Truth)**: Information provided below should serve as a verification baseline to ensure relevance. Use it to confirm that the document content aligns directly with {company}.
            - **{initial_docs}**

            ### Retrieved Documents for Clustering
            Below are the retrieved documents, including URLs and brief content snippets:
            {[{'url': doc['url'], 'snippet': doc['content']} for doc in all_retrieved_urls]}

            ### Instructions
            - **Prioritize Domain Match**: Documents that contain '{target_domain}' should be included in the main cluster for '{company}'.
            - **Consider Aligned Third-Party Sources**: Documents from third-party domains can also be included in the '{company}' cluster if they strongly reference the target domain '{target_domain}' within their content or closely match the initial context of {company}.
            - **Separate Similar but Distinct Domains**: Documents from domains that resemble '{target_domain}', such as '{target_domain.replace('.com', '.io')}', should be placed in distinct clusters unless they explicitly reference the target domain and align with the company's context.

            ### Example Output Format
            {{
                "clusters": [
                    {{
                        "company_name": "Name of Company A",
                        "cluster": [
                            "http://example.com/doc1",
                            "http://example.com/doc2"
                        ]
                    }},
                    {{
                        "company_name": "Name of Company B",
                        "cluster": [
                            "http://example.com/doc3"
                        ]
                    }},
                    {{
                        "company_name": "Ambiguous",
                        "cluster": [
                            "http://example.com/doc4"
                        ]
                    }}
                ]
            }}

            ### Key Points
            - **Primary Domain Verification**: Documents containing '{target_domain}' should be grouped under '{company}'.
            - **Third-Party Documents**: Documents from other domains may belong to '{company}' if they directly reference '{target_domain}' within the content or match the initial company context.
            - **Handle Ambiguities Separately**: Place documents that do not clearly align in an "Ambiguous" cluster for further review.
        """




        # LLM call with structured output using DocumentClusters
        messages = [SystemMessage(content=prompt)]
        
        try:
            # Use the model's structured output with DocumentClusters format
            response = await final_model.with_structured_output(DocumentClusters).ainvoke(messages)
            clusters = response.clusters  # Access the structured clusters directly
        except Exception as e:
            msg += f"Error: {str(e)}\n"
            clusters = []


        # Summarize the results
        if not clusters:
            msg += "No valid clusters generated. Please check the document formats.\n"
        else:
            msg += "Clusters generated successfully:\n"
            for  idx, cluster in enumerate(clusters, start=1):
                msg += f"Company {idx}: {cluster.company_name} - URLs: {cluster.cluster}\n"
        
        return {"messages": [AIMessage(content=msg)], "document_clusters": clusters}
    
    # Define the function to choose the correct cluster as a conditional edge
    async def choose_cluster(self, state: ResearchState):
        company_url = state['company_url']
        clusters = state['document_clusters']

        # Attempt to automatically choose the correct cluster
        for cluster in clusters:
            # Check if any URL in the cluster starts with the company URL
            if any(url.startswith(company_url) for url in cluster.cluster):
                state['chosen_cluster'] = cluster
                msg = f"Automatically selected cluster for '{company_url}' as {cluster.company_name}."
                return {"messages": [AIMessage(content=msg)], "chosen_cluster": state['chosen_cluster']}

        # If no automatic match, indicate that manual selection is needed
        msg = "No automatic cluster match found. Please select the correct cluster manually."
        return {"messages": [AIMessage(content=msg)], "document_clusters": clusters, "chosen_cluster": None}

    async def run(self, state: ResearchState):
        cluster_result = await self.cluster(state)
        state['document_clusters'] = cluster_result['document_clusters'] 
        choose_cluster_result = await self.choose_cluster(state)
        result = {'chosen_cluster': choose_cluster_result['chosen_cluster']}
        result.update(cluster_result)
        return result
