## OpenAI o3-mini Release Summary (January 31, 2025)

OpenAI has released **o3-mini**, a new, cost-efficient reasoning model available in both ChatGPT and the API. It's a powerful and fast model with exceptional STEM capabilities (science, math, coding) while maintaining low cost and latency.

**Key Features and Updates:**

*   **Availability:**
    *   Available in ChatGPT and the API.
    *   ChatGPT Plus, Team, and Pro users have access immediately, with Enterprise access in February.
    *   Free plan users can try o3-mini in ChatGPT by selecting 'Reason' in the message composer or regenerating a response.
    *   Rolling out to select developers in API usage tiers 3-5.
*   **Capabilities:**
    *   Supports function calling, Structured Outputs, and developer messages.
    *   Supports streaming.
    *   Offers three reasoning effort options: low, medium, and high.
    *   Does *not* support vision capabilities (use o1 for visual reasoning).
    *   Works with search in ChatGPT to find up-to-date answers with links to relevant web sources (early prototype).
*   **Performance:**
    *   Optimized for STEM reasoning.
    *   With medium reasoning effort, matches o1's performance in math, coding, and science, while delivering faster responses.
    *   Testers preferred o3-mini's responses to o1-mini 56% of the time and observed a 39% reduction in major errors.
    *   Matches the performance of o1 on some of the most challenging reasoning and intelligence evaluations including AIME and GPQA.
    *   Outperforms o1-mini in knowledge evaluations across general knowledge domains.
    *   Faster performance and improved efficiency compared to o1-mini.
    *   24% faster response time than o1-mini in A/B testing.
*   **ChatGPT Integration:**
    *   Replaces o1-mini in the model picker for paid users.
    *   Triples the rate limit for Plus and Team users from 50 messages per day with o1-mini to 150 messages per day with o3-mini.
    *   Paid users can select o3-mini-high in the model picker for a higher-intelligence version.
    *   Pro users will have unlimited access to both o3-mini and o3-mini-high.
*   **Safety:**
    *   Trained using deliberative alignment to reason about human-written safety specifications.
    *   Significantly surpasses GPT-4o on challenging safety and jailbreak evaluations.
*   **Pricing:**
    *   The release emphasizes driving down the cost of intelligence, reducing per-token pricing by 95% since launching GPT-4.

In essence, o3-mini is presented as a faster, more cost-effective, and highly capable model, particularly strong in STEM fields, with improved safety measures and wider accessibility across different user tiers.
