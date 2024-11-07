from langchain_core.messages import AIMessage
from ..format_classes import ResearchState

class ManualSelectionNode:
    async def manual_cluster_selection(self, state: ResearchState):

    # Allows the user to manually select the correct cluster if it wasn't determined automatically.
   
        clusters = state['document_clusters']
        msg = "Multiple clusters were identified. Please review the options and select the correct cluster for the target company.\n\n"
        print("Enter '0' if none of these clusters match the target company.\n")

        while True:
            try:
                # Prompt user for input
                selected_cluster_index = int(input("Enter the number of the correct cluster: ")) - 1

                # Handle '0' for rerun
                if selected_cluster_index == -1:
                    chosen_cluster = None
                    msg += "No suitable cluster found. Trying to cluster again.\n"
                    break
                # Validate selection within cluster bounds
                elif 0 <= selected_cluster_index < len(clusters):
                    chosen_cluster = clusters[selected_cluster_index]
                    msg += f"You selected cluster '{chosen_cluster.company_name}' as the correct cluster."
                    break
                else:
                    print("Invalid choice. Please enter a number corresponding to the listed clusters or '0' to re-cluster.")
            
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        return {"messages": [AIMessage(content=msg)], "chosen_cluster": chosen_cluster}

    async def run(self, state: ResearchState):
        result = await self.manual_cluster_selection(state)
        return result