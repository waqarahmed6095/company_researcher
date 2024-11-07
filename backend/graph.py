import os
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph

# Import research state class
from .format_classes.research_state import ResearchState

# Import node classes
from .nodes import (
    InitialSearchNode, 
    SubQuestionsNode, 
    ResearcherNode, 
    ClusterNode, 
    ManualSelectionNode, 
    CurateNode, 
    GenerateNode,
    EvaluationNode,
    PublishNode
)
from .nodes.routing_helper import (
    route_based_on_cluster, 
    route_after_manual_selection, 
    should_continue_research,
    route_based_on_evaluation
)



class Graph:
    def __init__(self) -> None:   
        pass
    async def run(self, company: str, url: str):
                  # Initial message setup
        messages = [
            SystemMessage(content="You are an expert researcher ready to begin the information gathering process.")
        ]
        # Initialize ResearchState with provided company and URL
        state = ResearchState(company=company, company_url=url, messages=messages)

        # Initialize nodes
        initial_search_node = InitialSearchNode()
        sub_questions_node = SubQuestionsNode()
        researcher_node = ResearcherNode()
        cluster_node = ClusterNode()
        manual_selection_node = ManualSelectionNode()
        curate_node = CurateNode()
        generate_node = GenerateNode()
        evaluation_node = EvaluationNode()
        publish_node = PublishNode()

        # Define Research State Graph
        workflow = StateGraph(ResearchState)

        # Add nodes to graph
        workflow.add_node("initial_search", initial_search_node.run)
        workflow.add_node("sub_questions_gen", sub_questions_node.run)
        workflow.add_node("research", researcher_node.run)
        workflow.add_node("cluster", cluster_node.run)
        workflow.add_node("manual_cluster_selection", manual_selection_node.run)
        workflow.add_node("curate", curate_node.run)
        workflow.add_node("generate_report", generate_node.run)
        workflow.add_node("eval_report", evaluation_node.run)
        workflow.add_node("publish", publish_node.run)
        
        

        # Set up edges
        workflow.add_edge("initial_search", "sub_questions_gen")
        workflow.add_edge("sub_questions_gen", "research")
        workflow.add_edge("research", "cluster")

        workflow.add_conditional_edges("cluster", route_based_on_cluster)
        workflow.add_conditional_edges("manual_cluster_selection", route_after_manual_selection)
        workflow.add_conditional_edges("curate", should_continue_research)
        workflow.add_edge("generate_report", "eval_report")
        workflow.add_conditional_edges("eval_report", route_based_on_evaluation)

        # Set start and end nodes
        workflow.set_entry_point("initial_search")
        workflow.set_finish_point("publish")

        # Compile the graph
        graph = workflow.compile()
       

        # Initial message setup
        messages = [
            SystemMessage(content="You are an expert researcher ready to begin the information gathering process.")
        ]

        # Asynchronous execution of the graph
        async for s in graph.astream(state, stream_mode="values"):
            message = s["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()



