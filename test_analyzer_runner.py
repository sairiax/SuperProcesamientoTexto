"""
Quick test script to verify AnalyzerRunner works correctly.
"""

from procesamientotexto.analyzers.analyzer_runner import AnalyzerRunner
from procesamientotexto.models.text_document import TextDocument


def main():
    # Create a sample document
    text = """
    This is a great test document! It contains some positive words like excellent and amazing.
    We want to verify that the analyzer runner works correctly.
    The text should be analyzed for frequency, language, sentiment, and readability.
    """

    doc = TextDocument(content=text.strip())

    # Create and run the analyzer
    runner = AnalyzerRunner()
    results = runner.analyze(doc)

    # Print results
    print("=" * 60)
    print("ANALYZER RUNNER TEST RESULTS")
    print("=" * 60)

    print("\n1. FREQUENCY ANALYSIS:")
    print(f"   Total Words: {results['total_words']}")
    print(f"   Top 5 Words: {list(results['top_words'].items())[:5]}")
    print(f"   Most Common Length: {results['most_common_length']}")

    print("\n2. LANGUAGE DETECTION:")
    print(f"   Language: {results['language']}")
    print(f"   Confidence: {results['confidence']}")

    print("\n3. SENTIMENT ANALYSIS:")
    print(f"   Sentiment: {results['sentiment']}")
    print(f"   Score: {results['score']}")
    print(f"   Positive Words: {results['pos_count']}")
    print(f"   Negative Words: {results['neg_count']}")

    print("\n4. READABILITY ANALYSIS:")
    print(f"   Avg Sentence Length: {results['avg_sentence_length']}")
    print(f"   Avg Word Length: {results['avg_word_length']}")
    print(f"   Complexity: {results['complexity']}")

    print("\n" + "=" * 60)
    print("✓ All analyzers executed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
