from langchain_core.messages import SystemMessage, AIMessage
from functools import partial
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver

# Import research state class
from backend.classes.research_state import ResearchState, InputState, OutputState

# Import node classes
from backend.nodes import (
    InitialGroundingNode, 
    SubQuestionsNode, 
    ResearcherNode, 
    ClusterNode, 
    ManualSelectionNode, 
    EnrichDocsNode, 
    GenerateNode,
    EvaluationNode,
    PublishNode
)
from backend.utils.routing_helper import (
    route_based_on_cluster, 
    route_after_manual_selection, 
    should_continue_research,
    route_based_on_evaluation
)


class Graph:
    def __init__(self, company=None, url=None, output_format="pdf", websocket=None):
        # Initial setup of ResearchState and messages
        self.messages = [
            SystemMessage(content="You are an expert researcher ready to begin the information gathering process.")
        ]
        # Initialize ResearchState
        self.state = ResearchState(
            company=company, 
            company_url=url, 
            output_format=output_format, 
            messages=self.messages
        )
        # Initialize nodes as attributes
        self.initial_search_node = InitialGroundingNode()
        self.sub_questions_node = SubQuestionsNode()
        self.researcher_node = ResearcherNode()
        self.cluster_node = ClusterNode()
        self.manual_selection_node = ManualSelectionNode()  # Now an attribute
        self.curate_node = EnrichDocsNode()
        self.generate_node = GenerateNode()
        self.evaluation_node = EvaluationNode()
        self.publish_node = PublishNode()

        # Initialize workflow for the graph
        self.workflow = StateGraph(ResearchState, input=InputState, output=OutputState)

        # Add nodes to the workflow
        self.workflow.add_node("initial_grounding", self.initial_search_node.run)
        self.workflow.add_node("sub_questions_gen", self.sub_questions_node.run)
        self.workflow.add_node("research", self.researcher_node.run)
        self.workflow.add_node("cluster", partial(self.cluster_node.run, websocket=websocket))
        self.workflow.add_node("manual_cluster_selection", partial(self.manual_selection_node.run, websocket=websocket))
        self.workflow.add_node("enrich_docs", self.curate_node.run)
        self.workflow.add_node("generate_report", partial(self.generate_node.run, websocket=websocket))
        self.workflow.add_node("eval_report", self.evaluation_node.run)
        self.workflow.add_node("publish", self.publish_node.run)

        # Add edges to graph
        self.workflow.add_edge("initial_grounding", "sub_questions_gen")
        self.workflow.add_edge("sub_questions_gen", "research")
        self.workflow.add_edge("research", "cluster")
        self.workflow.add_conditional_edges("cluster", route_based_on_cluster)
        self.workflow.add_conditional_edges("manual_cluster_selection", route_after_manual_selection)
        self.workflow.add_conditional_edges("enrich_docs", should_continue_research)
        self.workflow.add_edge("generate_report", "eval_report")
        self.workflow.add_conditional_edges("eval_report", route_based_on_evaluation)

        # Set start and end nodes
        self.workflow.set_entry_point("initial_grounding")
        self.workflow.set_finish_point("publish")

        # Set up memory
        self.memory = MemorySaver()

    
    async def run(self, progress_callback=None):
        # Compile the graph
        graph = self.workflow.compile(checkpointer=self.memory)
        thread = {"configurable": {"thread_id": "2"}}

       
        # Execute the graph asynchronously and send progress updates
        async for s in graph.astream(self.state, thread, stream_mode="values"):
            if "messages" in s and s["messages"]:  # Check if "messages" exists and is non-empty
                message = s["messages"][-1]
                output_message = message.content if hasattr(message, "content") else str(message)

                if progress_callback and not getattr(message, "is_manual_selection", False):
                    await progress_callback(output_message)
    def compile(self):
    # Use a consistent thread ID for state persistence
        thread = {"configurable": {"thread_id": "2"}}
        
        # Compile the workflow with checkpointer and interrupt configuration
        graph = self.workflow.compile(
            checkpointer=self.memory
            # interrupt_before=["manual_cluster_selection"]
        )
        return graph