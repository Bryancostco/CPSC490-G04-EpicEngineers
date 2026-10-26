```mermaid 
flowchart TB
    subgraph architecture ["High-level architecture"]
        direction LR
        DB[("Snow Flake Database")]
        Analysis["Data analysis"]
        Results["Data results"]
        Dashboard["Dashboard display"]

        DB -->|Source data| Analysis
        Analysis -->|Produces| Results
        Results -->|Visualized in| Dashboard
    end

    classDef data fill:#eef2ff,stroke:#818cf8
    classDef processing fill:#f5f3ff,stroke:#a78bfa
    classDef presentation fill:#f0fdfa,stroke:#2dd4bf
    classDef actor fill:#fff7ed,stroke:#fb923c

    class DB,Results data
    class Analysis,System processing
    class Dashboard presentation
    class User actor

````