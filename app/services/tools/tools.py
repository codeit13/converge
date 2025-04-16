from datetime import datetime
import os
import requests
from typing import Annotated, Dict, Optional
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
        ..., description="Primary and secondary keywords for SEO optimization (min: 2, max: 4)"
    )
    tags: list[str] = Field(
        ..., description="Hugo taxonomies for article categorization (min: 2, max: 4)"
    )
    categories: list[str] = Field(
        ..., description="Main categories for the article in Hugo (min: 2, max: 4)"
    )


class ResponseFormat(BaseModel):
    query_to_user: Optional[str] = Field(
        None, description="If you have any query/ question for the user, ask it here"
    )
    article: Optional[ArticleFormat] = Field(
        None,
        description="The article details in the correct format. If you don't have enough context, simply through null there"
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
            You are a highly skilled SEO-focused content creator with extensive experience in writing blog posts that not only rank well on search engines but also provide genuine value to readers. You have a strong understanding of technical subjects and can break down complex information into easily digestible formats while ensuring the content is structured properly in Markdown.

Your task is to write an SEO-ready blog post based on the context that will be provided to you. The context will include essential details and technical content elements that can enhance the post's richness and clarity. Make sure to structure the blog post effectively in Markdown format, including headings, lists, code snippets, and any other relevant elements to improve readability and SEO performance.

Here are the details you will need to consider while writing the blog post:

Context: __________
Target Keywords: __________
Target Audience: __________
Key Insights to Include: __________
Any specific technical elements required (e.g., code snippets, tables, etc.): __________
If you require any additional information or clarifications to create a comprehensive and valuable blog post, please ask the user for it.

            ## Metadata
            Current Date: {datetime.now().strftime("%Y-%m-%d")}
            Current Time: {datetime.now().strftime("%H:%M:%S")}
        """
         )
    ]

    llm = ChatOpenAI(
        api_key=settings.OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.7)

    llm = llm.with_structured_output(ResponseFormat)

    article_prompt.append(
        ("human", f"Generate an article for this context:\n{context}"))
    response: ResponseFormat = llm.invoke(article_prompt)

    response = response.model_dump()

    if response.get("message_to_user"):
        return response.get("message_to_user")
    else:
        # Dir for storing blog markdown files (For Docker & Local)
        article = response.get('article')
        if not article:
            return "I'm sorry, I don't have enough context to generate an article."

        CONTENT_DIR = "/app/blog/content"
        if not os.path.exists(CONTENT_DIR):
            CONTENT_DIR = os.path.join(
                os.path.dirname(os.getcwd()), "blog", "content")

        # print(f"Content directory: {CONTENT_DIR}")

        if article.get('content'):
            articleLink = publish_article(CONTENT_DIR, article)
            article['link'] = articleLink

        message = "Your article has been published"
        if article.get('link', None):
            message += f" at {article.get('link')}"
        else:
            message += f" with content {article.get('content', '')}"

        return Command(
            update={
                "articles": [article],
                "messages": [
                    ToolMessage(
                        message, tool_call_id=tool_call_id
                    )
                ],
            }
        )


@tool
@error_handler
def get_amazon_product_urls(query: str):
    """
    Get Amazon product URLs based on the given query.

    Args:
        query: (str) The search query for Amazon products

    Returns:
        str: JSON string containing the product URLs
    """
    payload = {'api_key': settings.SCRAPER_API_KEY,
               'query': query}
    response = requests.get(
        'https://api.scraperapi.com/structured/amazon/search', params=payload)

    response = response.text
    return response
