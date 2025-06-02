from research_team import research_team
from writer_team import writer_team

if __name__ == "__main__":
    topic = input("Enter the topic: ")
    key_points = input("Enter the key points: ")
    code_file_name = input("Enter the code file name: ")

    # 1. Research team - lead researcher and research strategist
    perplexity_research = research_team(topic, key_points)

    # 2.Writer team - writer and editor
    writer_team(perplexity_research, code_file_name)
