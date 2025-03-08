from yaml import safe_load
from extractor.soup_extractor import SoupFetcher
from llms.gemini_llm  import GeminiSummarizer
from llms.schema import Links


def main():
    """
    Main function to fetch website data, summarize it using Gemini, and save the summary.
    """

    url = "https://www.anthropic.com/"
    fetcher = SoupFetcher(url)
    fetcher.fetch()
    with open('./configs/prompts.yml') as f:
        prompts = safe_load(f)

    example_links = [{"url": "https://example.com/article1", "title": "Article 1 Title"}, {"url": "https://example.com/explanation", "title": "Another example"}]
    p = prompts['links']
    system_prompt = p['system_prompt']
    user_prompt = p['user_prompt'].format(formatted_links=fetcher.links, example_links=example_links)


    gemini_llm = GeminiSummarizer(
        user_prompt, system_prompt, seed=42, max_output_tokens=1000, temperature=0.5, 
        response_mime_type= 'application/json', response_schema=list[Links]
    )
    summary = gemini_llm.summarize()

    contents = f"Langing Page Title: {fetcher.title}\nLanding Page Contents: {fetcher.body}\n\n"
    for a in summary.parsed:
        fetcher = SoupFetcher(a.url)
        if fetcher.fetch() is None:
            continue
        fetcher.fetch()
        contents += f"Title: {a.title}\nContents: {fetcher.body}\n\n"
    
    print(summary.parsed)

    system_prompt = prompts['summarizer']['system_prompt']
    user_prompt = prompts['summarizer']['user_prompt'].format(contents=contents)


        # Initializing GeminiSummarizer with specific parameters
    gemini_llm = GeminiSummarizer(user_prompt, system_prompt, seed=42, max_output_tokens=10000, temperature=0.5)
    summary = gemini_llm.summarize()

    # Save the summary to a markdown file.
    with open('../outputs/summary.md', 'w') as f:
        f.write(summary.text)


# Execute the main function when the script is run.
main()
