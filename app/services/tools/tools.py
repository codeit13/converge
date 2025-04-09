from datetime import datetime
import os
from typing import Annotated, Dict
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from pydantic import BaseModel, Field

from utils.helpers import error_handler, extract_json_from_string, publish_article
from config import settings


class ArticleFormat(BaseModel):
    title: str = Field(
        ...,
        description="SEO-optimized title of the generated article (70-80 characters)"
    )
    content: str = Field(
        ...,
        description="Complete markdown content of the generated article"
    )
    slug: str = Field(
        ...,
        description="URL-friendly slug derived from the title"
    )
    description: str = Field(
        ...,
        description="Meta description for SEO (150-160 characters)"
    )
    summary: str = Field(
        ...,
        description="Summarizes the content or serves as a teaser to encourage readers to visit the page"
    )
    keywords: list[str] = Field(
        ...,
        description="Primary and secondary keywords for SEO optimization"
    )
    tags: list[str] = Field(
        ...,
        description="Hugo taxonomies for article categorization"
    )
    categories: list[str] = Field(
        ...,
        description="Main categories for the article in Hugo"
    )


@tool
@error_handler
def generate_article(context: str, tool_call_id: Annotated[str, InjectedToolCallId],) -> Dict:
    """
    Generate a well-structured SEO-optimized article on the given context.

    Args:
        context: (string) The context which the article will be based on

    Returns:
        dict: A dictionary containing the article details in the correct format
    """
    article_prompt = [
        ("system", f"""
            You are an expert technical writer specializing in AI content with strong SEO optimization. Your task is to create an authoritative, insightful blog article that ranks well on search engines while delivering genuine technical value to a knowledgeable audience.

            ## Article Structure Requirements
            Create a well-structured markdown article with:
            1. A compelling, specific title that includes the primary keyword (70-80 characters)
            2. An executive summary/introduction (150-200 words) that hooks the reader and outlines what they'll learn
            3. A well-structured content hierarchy using proper heading tags (H2, H3, H4)
            4. Strategic keyword placement throughout the content
            5. A comprehensive table of contents for easy navigation
            6. A strong conclusion with actionable takeaways
            7. A related resources/further reading section
            8. 5-7 relevant FAQs addressing common questions about the topic
            9. Total word count between 1800-2500 words for comprehensive coverage

            ## Detailed Sectional Requirements
            
            ### Introduction Section
            - Begin with a technical hook that demonstrates expertise and establishes relevance
            - Clearly state the problem or challenge the article addresses
            - Include a brief overview of what readers will learn
            - End with a transition to the main content
            
            ### Main Content Sections
            - Organize content into logical H2 sections with descriptive headings
            - Further divide complex sections into H3 and H4 subsections
            - Include prerequisites or background knowledge needed (if applicable)
            - For implementation guides:
              * Break down into clear, numbered steps
              * Explain the purpose of each step
              * Include code examples with comments
              * Highlight potential issues or gotchas
              * Provide verification steps to ensure correct implementation
            
            ### Practical Application Section
            - Include real-world use cases and examples
            - Discuss industry applications or business implications
            - Provide benchmarks or performance expectations where relevant
            
            ### Limitations & Considerations Section
            - Address technical limitations honestly
            - Discuss ethical considerations or potential challenges
            - Include alternative approaches where applicable
            
            ### Conclusion
            - Summarize key points and insights
            - Provide actionable next steps for readers
            - End with a forward-looking statement about the technology
            
            ### FAQs Section
            - Include 5-7 specific, detailed questions and answers
            - Address common challenges, misconceptions, and advanced usage
            - Incorporate additional keywords naturally in this section
            
            ### Further Reading Section
            - Link to related resources, documentation, and research papers
            - Suggest next topics to explore

            ## Technical Content Elements
            - Use markdown tables for comparative analyses
            - Include properly formatted code blocks with syntax highlighting (```language)
            - Create bulleted or numbered lists for step-by-step explanations
            - Emphasize key technical terms with bold or italic formatting
            - Add internal linking opportunities to related technical concepts
            - Use math formulas with proper LaTeX notation when needed
            - Include callouts for important notes, warnings, or tips
            - Use Hugo shortcodes for enhanced dynamic content:
              * {{< highlight python >}}code{{< /highlight >}}
              * {{< figure src="/images/diagram.png" title="Diagram Title" >}}
              * {{< notice note >}}Important information{{< /notice >}}
              * {{< tabs >}}{{< tab "Tab 1" >}}Content{{< /tab >}}{{< /tabs >}}

            ## Diagrams and Visualizations
            - Suggest appropriate diagrams or flowcharts that would enhance understanding
            - Provide textual descriptions of what these diagrams should illustrate
            - Include Mermaid or PlantUML markup for generating diagrams when appropriate
            - It supports GoAT diagrams (ASCII) by using ```goat block 

            ## SEO Optimization Rules
            - Primary keyword in title, URL slug, first paragraph, and at least one H2
            - Secondary keywords naturally distributed throughout the content (especially in H3s)
            - Strategic internal linking suggestions to strengthen site architecture
            - External authoritative linking to enhance credibility
            - Meta description suggestion (150-160 characters) that includes primary keyword
            - Image alt text recommendations that include relevant keywords

            ## Quality Standards
            - Ensure technical accuracy and up-to-date information
            - Avoid jargon without explanation (unless targeting highly technical audience)
            - Use consistent terminology throughout
            - Provide sufficient context and background for complex concepts
            - Balance theoretical explanations with practical applications
            - Write in an authoritative but accessible voice
            - Include relevant statistics, research findings, or benchmark data

            ## Short codes for various content options in markdown
            - For Youtube video use {{{{< youtubeLite id="SgXhGb-7QbU" label="Blowfish-tools demo" params="controls=0&start=10&end=30&modestbranding=2&rel=0&enablejsapi=1"  >}}}}
            - For displaying a tweet use {{{{< x user="SanDiegoZoo" id="1453110110599868418" >}}}}
            - For displaying a badge use {{{{</* /badge */>}}}}
            - For displaying a button use {{{{</* button href="#button" target="_self" */>}}}}
            - For displaying a chart use {{{{< chart >}}}} type: 'bar', data: {{ labels: ['Tomato', 'Blueberry', 'Banana', 'Lime', 'Orange'], datasets: [{{ label: '# of votes', data: [12, 19, 3, 5, 3], }}] }} {{{{< /chart >}}}}   
            - For importing code from other sources like github gist use {{{{</* codeimporter url="rawpublicaccessiblefileurl" type="toml" startLine="11" endLine="18" */>}}}}
            - For using github link, use this github card {{{{</* github repo="nunocoracao/blowfish" */>}}}}
            - For math expressions, use katex language like this example: {{{{< katex >}}}} \(f(a,b,c) = (a^2+b^2+c^2)^3\)
            - For using mermaid diagrams use {{{{< mermaid >}} graph LR; A[Lemons]-->B[Lemonade]; B-->C[Profit] {{< /mermaid >}}}}


            ## Metadata
            Current Date: {datetime.now().strftime("%Y-%m-%d")}
            Current Time: {datetime.now().strftime("%H:%M:%S")}
            Target Audience: Technical professionals, AI enthusiasts, developers, data scientists
            Content Type: Technical explanation of a concept, implementation guide of a topic, industry analysis, or emerging technology overview
        """
         )
    ]

    llm = ChatOpenAI(
        api_key=settings.OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.7)

    llm = llm.with_structured_output(ArticleFormat)

    article_prompt.append(
        ("human", f"Generate an article for this context:\n{context}"))
    response: ArticleFormat = llm.invoke(article_prompt)

    response = response.model_dump()

    # Dir for storing blog markdown files (For Docker & Local)
    CONTENT_DIR = "/app/blog/content"
    if not os.path.exists(CONTENT_DIR):
        CONTENT_DIR = os.path.join(
            os.path.dirname(os.getcwd()), "blog", "content")

    # print(f"Content directory: {CONTENT_DIR}")

    if response.get('content'):
        articleLink = publish_article(CONTENT_DIR, response)
        response['link'] = articleLink

    return Command(
        update={
            "article": response,
            "messages": [
                ToolMessage(
                    f"Here's your generated article \n\n{response.get('content')}", tool_call_id=tool_call_id
                )
            ],
        }
    )

    # return {"article": response}
