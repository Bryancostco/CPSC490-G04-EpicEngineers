Epic: #24, #29, #33 · Stories: Writing Documentation for Architecture
```mermaid 
flowchart TB
%% High-Level Archiecture Diagram: Figure 1. Data Flow Visualization



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



%% System Context Diagram: Figure 2. Dashboard user workflow, display of dashboard

    subgraph context ["System context"]
        direction LR
        User["Dashboard user"]
        System["Analytics system<br/>Database, analysis, results, and dashboard"]

        User -->|Views dashboard| System
        System -->|Presents results| User
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