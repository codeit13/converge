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
        description="Title of the generated article"
    )
    content: str = Field(
        ...,
        description="Markdown content of the generated article"
    )
    slug: str = Field(
        ...,
        description="Slug of the generated article"
    )
    keywords: list[str] = Field(
        ...,
        description="Keywords of the generated article"
    )
    link: str = Field(
        ...,
        description="Link of this published article"
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
            Create a markdown-formatted blog post with:
            1. A compelling, specific title that includes the primary keyword (70-80 characters)
            2. A well-structured content hierarchy using proper heading tags (H2, H3, H4)
            3. A URL-friendly slug derived from the title
            4. Strategic keyword placement throughout the content
            5. Total word count between 1500-2500 words for comprehensive coverage

            ## Content Quality Guidelines
            - Begin with a technical hook that demonstrates expertise and establishes relevance
            - Include code examples, mathematical formulas, or technical diagrams where appropriate
            - Break down complex AI concepts into digestible explanations without oversimplification
            - Support claims with referenced research papers, technical documentation, or industry benchmarks
            - Incorporate practical applications and real-world implications of the technology
            - Address potential limitations, ethical considerations, or technical challenges
            - End with forward-looking insights and actionable takeaways

            ## Technical Formatting Elements
            - Use markdown tables for comparative analyses
            - Include properly formatted code blocks with syntax highlighting
            - Create bulleted or numbered lists for step-by-step explanations
            - Emphasize key technical terms with bold or italic formatting
            - Add internal linking opportunities to related technical concepts

            ## SEO Optimization Rules
            - Primary keyword in title, first paragraph, and at least one H2
            - Secondary keywords naturally distributed throughout the content
            - Meta description suggestion (150-160 characters)
            - Image alt text recommendations that include relevant keywords
            - Internal and external linking strategy suggestions

            ## Metadata
            Current Date: {datetime.now().strftime("%Y-%m-%d")}
            Current Time: {datetime.now().strftime("%H:%M:%S")}
            Target Audience: Technical professionals, AI enthusiasts, developers, data scientists
            Content Type: Technical explanation, industry analysis, or emerging technology overview
        """
         )
    ]

    llm = ChatOpenAI(
        api_key=settings.OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.5)

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

    print("Current working dir: ", os.getcwd())
    print(f"Content directory: {CONTENT_DIR}")

    if response.get('content'):
        # print("got response.get('content')")
        articleLink = publish_article(CONTENT_DIR, response)
        print("********************* article link ********************: ", articleLink)
        response['link'] = articleLink

    return Command(
        update={
            "article": response,
            "messages": [
                ToolMessage(
                    "Successfully generated the article", tool_call_id=tool_call_id
                )
            ],
        }
    )

    # return {"article": response}
