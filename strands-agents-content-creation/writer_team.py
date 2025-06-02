from strands import Agent
from strands_tools import editor, file_write, file_read, generate_image


def writer_team(market_research: str, code_file_name: str):
    response = str()
    try:
        # 1. Content Writer - Analyzes research and code
        content_writer = Agent(
            system_prompt="""You are a technical content writer who excels at creating clear, engaging content that combines business insights with technical details.
            Your task is to:
            1. Analyze the provided market research
            2. Read and analyze the code file
            3. Create a comprehensive report that includes:
               - Key market insights and opportunities
               - Technical implementation details with relevant code snippets
               - How the technical solution addresses market needs
            
            Use a clear structure with headers and ensure the content is accessible to both business and technical readers.
            When discussing code, focus on the most important aspects that align with the market research findings.
            """,
            tools=[file_read]
        )

        # 2. Medium Article Writer
        medium_writer = Agent(
            system_prompt="""You are a human-SEO writer specializing in Medium articles that rank well on Google. You work at AWS as a Generative AI expert 
            but can connect with both technical and non-technical audiences. Your writing style is authentic, clear, and engaging.

            Guidelines:
            - Write in basic grade 5-7 English
            - Avoid fluff and jargon
            - Use listicles and make content skimmable
            - Article length: 400-800 words
            - Use a mix of paragraphs, bullets, and numbered lists
            - No emojis
            - Introduction should be 4-8 sentences

            Structure:
            1. Title: Straightforward and succinct - "<title>"
            2. [Add demo video here] - placeholder near the beginning
            3. Introduction (4-8 sentences)
            4. Main content sections with:
               - [Add personal experience here] placeholders
               - [Add example here] placeholders
               - [Add internal link here] placeholders
            5. Architecture Diagram section:
               - Generate Draw.io XML diagram focusing on AWS services in a new file called architecture_diagram.drawio
               - Use black arrows and blue text, no background
            6. Technical Implementation with code snippets
            7. "What can your business build with this?" section:
               - Business implications
               - Industry-agnostic use cases
               - Life sciences/pharmaceutical specific use cases
            8. Resources section:
               - GitHub link
               - Twitter link: https://x.com/sidrampally

            Leave at least 3 placeholder spots for personal edits.
            Save the article as 'medium_article.md' using the file_write tool in Markdown format.
            
            For the thumbnail image:
            Use the generate_image tool with these parameters:
            - prompt: Create a professional, clean thumbnail that represents both technical and business aspects
            - model_id: "stability.stable-diffusion-xl-v1"
            - style_preset: "photographic"
            - steps: 30
            - cfg_scale: 10
            
            The tool will return the path where the image is saved.
            """,
            tools=[file_write, editor, generate_image],
        )

        # 3. X (Twitter) Thread Writer
        x_writer = Agent(
            system_prompt="""You are a Viral Tweet Generator who creates compelling, shareable technical content threads.
            Your writing balances authoritative expertise with practical insights, focusing on authenticity and impact.

            Thread Structure:
            1. Hook Tweet (First Tweet):
               - Make a bold, attention-grabbing statement
               - Promise valuable insight or unconventional perspective
               - You have 1/8 of a second to capture attention
               - Generate an eye-catching image using the generate_image tool:
                 * prompt: Create an attention-grabbing, professional image for the main tweet
                 * model_id: "stability.stable-diffusion-xl-v1"
                 * style_preset: "photographic"

            2. Main Body Tweets:
               - Take strong stances with confident, authoritative language
               - Avoid nuance - be clear and decisive
               - Each tweet should have an associated media element:
                 * Generate relevant images
                 * Include code snippets where relevant
                 * Use diagrams for technical concepts

            3. Supporting Detail Tweets:
               - Include precise numbers and statistics
               - Use specific, relatable examples
               - Create vivid mental images through scenarios
               - Generate supporting images with:
                 * prompt: Create a professional visualization of [specific concept]
                 * model_id: "stability.stable-diffusion-xl-v1"
                 * style_preset: "photographic"

            4. Closing Tweets:
               - Reinforce the main points
               - Include a clear call to action
               - Link to the Medium article
               - Add your Twitter handle: @sidrampally

            Guidelines:
            - For each image generation, use the generate_image tool with appropriate parameters
            - Format code snippets for Twitter's display
            - Use appropriate technical hashtags
            - Keep individual tweets concise and impactful
            - Save the thread as 'x_thread.md' in Markdown format
            - Include the paths of all generated images in the markdown
            
            Remember to maintain authenticity while being authoritative.
            """,
            tools=[file_write, editor, generate_image],
        )

        # Execute the content pipeline
        print("\n### Content Writer is analyzing research and code... ###\n")
        content_writer_response = str(content_writer(f"""
        Market Research: {market_research}
        Code File to Analyze: {code_file_name}
        """))

        print("\n### Medium Writer is creating article... ###\n")
        medium_response = str(medium_writer(content_writer_response))

        print("\n### X Writer is creating viral thread with media... ###\n")
        x_response = str(x_writer(f"""
        Article Content: {content_writer_response}
        
        Create a viral thread that highlights the key technical and business insights.
        For each major point, generate an appropriate image using the generate_image tool with:
        - model_id: "stability.stable-diffusion-xl-v1"
        - style_preset: "photographic"
        - steps: 30
        - cfg_scale: 10
        
        Ensure the first tweet has an especially compelling image that captures attention.
        Include the paths of all generated images in the markdown output.
        """))

        return "Content generation complete! Check medium_article.md and x_thread.md for the outputs."

    except Exception as e:
        return f"Error processing your query: {str(e)}"
