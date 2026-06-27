# Division of Responsibilities

## Purpose

This document explains how AI assistance was used during the development of AI Job Hunter. It is intended to transparently describe which parts of the project were created through engineering decisions made by the project author and which parts benefited from AI-assisted implementation.

## Engineering Responsibilities (Human)

The overall architecture, direction, and engineering decisions for this project were made by the project author.

## Responsibilities included:

* Defining the overall project vision and goals.
* Choosing the application architecture.
* Determining which information should be extracted from job descriptions.
* Designing the domain model, including JobOpening, CandidateProfile, and FitAnalysis.
* Deciding to separate parsing from scoring.
* Choosing which features should be stored for future machine learning.
* Designing the testing strategy, including the separation of unit and integration tests.
* Reviewing generated code before incorporating it.
* Running the application repeatedly during development to understand behavior and validate execution paths.
* Debugging runtime errors, refining prompts, and improving parser quality.
* Making the final decisions regarding commits, refactoring, and project direction.

## AI Responsibilities

ChatGPT served as an engineering assistant rather than an autonomous software developer.

## AI assistance included:

* Suggesting software architecture improvements.
* Recommending project organization and directory structure.
* Drafting parser prompts for LLM-based information extraction.
* Generating boilerplate Python code for parsers, models, helper functions, and tests.
* Explaining Python language features and library usage.
* Assisting with debugging by interpreting error messages and proposing likely fixes.
* Suggesting unit and integration test cases.
* Recommending refactoring opportunities.
* Providing explanations of software engineering concepts, machine learning preparation, and design tradeoffs.

## Development Process

Development followed an iterative workflow:

2. Design the feature.
4. Discuss alternatives.
6. Generate or write an initial implementation.
8. Review every line of code.
10. Execute the code frequently.
12. Debug and refine.
14. Add or update automated tests.
16. Commit completed work to version control.

The author intentionally ran the application throughout development to understand execution flow rather than relying solely on generated code.

## Philosophy

The objective of this project was not to demonstrate that AI can replace software engineers.

Instead, the objective was to demonstrate how an experienced engineer can use AI to become more productive while maintaining responsibility for:

* architecture,
* correctness,
* testing,
* maintainability,
* and engineering judgment.

AI accelerated implementation. Human engineering guided the design.

## Future Direction

As the project evolves, additional AI capabilities may be incorporated into scoring, resume strategy, and machine learning experiments. The same development philosophy will continue:

* AI assists.
* The engineer designs, validates, and owns the system.

