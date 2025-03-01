## Week 1 Summary

**Exploration:**

*   Investigated open-source LLMs (specifically Llama) using the Ollama software.
*   Understood the core concept of LLMs: large language models trained on extensive datasets.

**LLM Landscape:**

*   **Closed-Source Frontier Models:** Identified examples like GPTs, Claude, Gemini, and others.
*   **Open-Source Frontier Models:** Identified examples like DeepSeek, Llama, and others.

**Open-Source vs. Closed-Source LLMs:**

| Feature             | Open-Source                                                                                                     | Closed-Source                                                                                              |
| ------------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Benefits**        | Data stays within your network; greater control and customization.                                            | No infrastructure management; more complex and potentially more powerful models; dedicated support.       |
| **Disadvantages**   | Requires building custom LLM inference infrastructure (more in-house work); models may be less effective (currently). | Potential privacy concerns (confidential data may be sent to their servers).                              |

## Project: Web Summarizer

**Description:**

*   Developed a web summarizer application using the Gemini LLM.

**Implementation:**

*   Utilized two data extraction services:
    *   Beautiful Soup (likely for static content).
    *   Selenium (likely for dynamic or JavaScript-rendered content).
*   Prompted the Gemini LLM with the extracted data.
*   The LLM then generated a summarized text output.

## Model Parameters

Model parameters are the weights and biases of a deep neural network. They are the learned values that define the model's behavior and knowledge. These parameters are adjusted during training to minimize the difference between the model's predictions and the actual values. The number of parameters is a key factor influencing the model's capacity to learn complex patterns. However, a larger number of parameters also necessitates a larger dataset to avoid overfitting.

*   **Weights:** Represent the strength of the connections between neurons in different layers.
*   **Biases:** Allow neurons to activate even when the input is zero, adding flexibility to the model.
*   **Training Process:**  Involves adjusting weights and biases to optimize the model's performance on a given task.

## Tokenizer

In earlier approaches, models were trained character by character. This method had limitations, such as the inability to capture semantic meaning at the word or phrase level, and increased computational complexity. Later, models were trained on whole words, which also presented challenges, like dealing with a very large vocabulary and handling out-of-vocabulary words. Now, text is broken down into tokens, which provides a balance between character-level and word-level approaches.

**Tokenization** is the process of splitting a text sequence into smaller units called tokens. These tokens can be words, subwords, or characters. Different tokenization algorithms exist, each with its own advantages and disadvantages:

*   **Word-Based Tokenization:** Simplest approach, splits text into words based on spaces and punctuation. Can lead to a very large vocabulary, and struggles with out-of-vocabulary words.
*   **Character-Based Tokenization:** Splits text into individual characters. Handles out-of-vocabulary words well, but loses semantic meaning at the word level.
*   **Subword Tokenization:** Aims to strike a balance between word-based and character-based tokenization. Splits words into smaller subword units based on frequency analysis. Common algorithms include:
    *   **Byte Pair Encoding (BPE):** Merges frequently occurring pairs of characters or subwords into a single token.
    *   **WordPiece:** Similar to BPE, but uses a likelihood-based approach to determine which subwords to merge.
    *   **Unigram Language Model:** Trains a unigram language model to determine the probability of each subword, and then selects the most probable subword segmentation.

**Rule of Thumb:**

*   1 token is approximately 4 characters (not words as you mentioned).
*   1 token is about 3/4 of a word.
*   1000 tokens ≈ 750 words.

**Importance of Tokenization:**

*   **Vocabulary Size:** Tokenization affects the size of the model's vocabulary, which impacts memory usage and computational efficiency.
*   **Handling Rare Words:** Subword tokenization helps handle rare words and out-of-vocabulary words by breaking them down into known subwords.
*   **Model Performance:** The choice of tokenization algorithm can significantly impact the model's performance on various natural language processing tasks.

