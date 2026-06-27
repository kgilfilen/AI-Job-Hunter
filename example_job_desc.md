NOTE: this is an example of parsing a job description after day 4. It is a C++ Developer position that matches me somewhat, but it has been ten years since I looked at C++, and it has changed signficantly in that time. This scores the job at 60, and suggests to consider it. 

```
bash
--- Processing dev_II_cpp.txt ---
Fit Analysis:
{
    "overall_score": 60,
    "recommendation": "Consider",
    "strengths": [
        "Matches remote preference: remote"
    ],
    "concerns": [],
    "notes": []
}
Job Opening:
{
    "source_file": "dev_II_cpp.txt",
    "title": "Software Development Engineer II, Search",
    "company": "Mapbox",
    "location": "Mapbox US; Mapbox Germany; Mapbox Helsinki",
    "remote_status": "remote",
    "employment_type": "full-time",
    "security_clearance_required": false,
    "security_clearance_level": null,
    "required_skills": [
        "C++",
        "Memory management",
        "Multithreading",
        "Systems programming",
        "Python",
        "Scripting",
        "Performance optimization",
        "CPU optimization",
        "Memory optimization",
        "Data structures",
        "Algorithms",
        "Binary data formats",
        "Data compression",
        "Zstd",
        "Delta updates",
        "Search algorithms",
        "Offline search",
        "Embedded systems",
        "Mobile development",
        "Data processing pipelines",
        "System telemetry",
        "Technical design"
    ],
    "preferred_skills": [
        "Data Compression",
        "Zstd",
        "Delta Updates",
        "Mapping",
        "Navigation",
        "Automotive",
        "Machine Learning",
        "Geospatial Data Analysis",
        "Open Source",
        "Data Analysis"
    ],
    "responsibilities": [
        "Design and optimize on-device search algorithms",
        "Develop core offline search engine functionality",
        "Implement tile compression and delta update pipelines",
        "Integrate offline data processing pipelines with cloud search systems",
        "Collaborate with R&D and backend teams",
        "Support automotive customers and partners with integration challenges",
        "Monitor system telemetry and analyze performance tradeoffs",
        "Define technical roadmaps and scope complex offline search features",
        "Write technical design documents for offline search capabilities"
    ],
    "salary_range": null,
    "notes": [],
    "parser_metadata": {
        "title": {
            "confidence": 0.99,
            "evidence": "Software Development Engineer II, Search",
            "warning": null
        },
        "company": {
            "confidence": 0.99,
            "evidence": "Mapbox is the leading real-time location platform",
            "warning": null
        },
        "location": {
            "confidence": 0.95,
            "evidence": "Location\nMapbox US; Mapbox Germany; Mapbox Helsinki",
            "warning": "Multiple official locations are listed; location type is Remote and was not treated as the physical location."
        },
        "remote_status": {
            "confidence": 1.0,
            "evidence": "Location Type\nRemote",
            "warning": null
        },
        "employment_type": {
            "confidence": 1.0,
            "evidence": "Employment Type\nFull time",
            "warning": null
        },
        "security_clearance": {
            "confidence": 0.99,
            "evidence": "",
            "warning": null
        },
        "required_skills": {
            "confidence": 0.92,
            "evidence": "Important traits require strong proficiency in C++ with memory management, multi-threading, and systems-level programming; experience with Python or scripting; performance optimization in CPU, memory, and latency constrained environments; familiarity with data structures, algorithmic efficiency, and binary data formats. Responsibilities include optimizing core search algorithms for on-device execution, implementing tile compression such as Zstd and delta update pipelines, integrating data processing pipelines, monitoring system telemetry, and writing technical design documents.",
            "warning": null
        },
        "preferred_skills": {
            "confidence": 0.94,
            "evidence": "Familiarity with data structures, algorithmic efficiency, and binary data formats (experience with data compression like Zstd or delta update mechanisms is a strong plus). Nice to Have Traits: Prior experience in the mapping, navigation, or automotive industry. Knowledge of machine learning techniques for geospatial data analysis. Contributions to open-source geospatial or data analysis projects.",
            "warning": null
        },
        "responsibilities": {
            "confidence": 0.96,
            "evidence": "The role includes designing, coding, and optimizing on-device search algorithms, owning offline data delivery systems, integrating pipelines across teams, supporting automotive partners, monitoring telemetry, and defining roadmaps and technical designs.",
            "warning": null
        }
    }
}
Saved: examples/output/dev_II_cpp.json
Saved: examples/output/dev_II_cpp_fit.json
```
