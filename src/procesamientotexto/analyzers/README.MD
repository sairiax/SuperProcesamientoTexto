
src/procesamientotexto/analyzers/
├── AnalyzerRunner.py       # Orchestrator (summary report)
└── core/
    ├── base.py         # Abstract Base Class
    ├── word_counter.py # Basic word/frequency counts
    ├── frequency_analyzer.py # Top words/N-grams
    ├── language_detector.py # Language heuristic
    ├── sentiment_analyzer.py # Keyword-based sentiment
    └── readability_analyzer.py # Text complexity metrics