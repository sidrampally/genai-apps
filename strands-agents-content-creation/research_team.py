import os

from dotenv import load_dotenv
from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.tools.mcp import MCPClient
from strands_tools import swarm

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")


def research_team(topic, key_points):
    response = str()
    try:
        perplexity_mcp_server = MCPClient(
            lambda: stdio_client(
                StdioServerParameters(
                    command="docker",
                    args=[
                        "run",
                        "-i",
                        "--rm",
                        "-e",
                        "PERPLEXITY_API_KEY",
                        "mcp/perplexity-ask",
                    ],
                    env={"PERPLEXITY_API_KEY": PERPLEXITY_API_KEY},
                )
            )
        )

        with perplexity_mcp_server:
            # Initialize Strands Agent with agent_graph
            tools = perplexity_mcp_server.list_tools_sync()
            lead_researcher = Agent(
                system_prompt="""
                You are a senior research analyst trained in high-depth content discovery and synthesis.
                Specifically:
                                - Key Trends and Insights
                                - Top use cases
                                - What’s currently happening in the industry or niche?
                                - Are there stats, frameworks, or case studies worth referencing?
                                - Popular Opinions vs. Expert Takes
                                - What are people saying on social platforms or forums?
                                - Are there any contrarian, expert-backed, or field-tested perspectives?
                                - Data, Stats, or Real Examples
                                - Include any performance benchmarks, studies, or business use cases
                                - Source Links or Summarized Citations
                                - If quoting or citing, include the origin (author, source, link)
                                You can do web search to gather more information.
                """,
                tools=tools + [swarm],
            )

            chief_strategist = Agent(
                system_prompt="""You are a senior research strategist trained in high-depth content discovery and synthesis.
                Your role is to explore authoritative sources, trends, case studies, and opinion patterns related to a specific topic or query.
                You always prioritize factual accuracy, real-world examples, and strategic relevance over surface-level summaries.
                Your insights are designed to inform downstream content agents who will create long-form posts, thought leadership, or campaign assets based on your research.
                Do not write final posts or content. Your output should consist of organized, useful findings that serve as a research base.
                """,
                tools=tools,
            )

            print("\n### Research Analyst is working! ###\n")

            researcher_response = str(lead_researcher(f"Use a swarm of 2 agents to conduct deep research on the topic: {topic}. You should focus more on the key points: {key_points}."))
            
            print("\n### Chief Strategist is working! ###\n")

            response = str(chief_strategist(researcher_response))

        if len(response) > 0:
            return response

        return "I apologize, but I couldn't properly analyze your question. Could you please rephrase or provide more context?"

    # Return specific error message for English queries
    except Exception as e:
        return f"Error processing your query: {str(e)}"
