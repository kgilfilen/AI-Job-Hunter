# Deterministic Software and Probabilistic Intelligence

Traditional software is largely deterministic. Given the same inputs and the same state, it follows defined rules and should produce the same result.

AI, particularly a large language model, is different. It provides probabilistic intelligence. Rather than simply executing a fixed set of rules, it interprets information, weighs possibilities, recognizes patterns, and produces a judgment or response.

The AI Career Manager deliberately uses both.

## Deterministic Software: The Rules We Can Guarantee

Some parts of the Career Manager should never depend on an AI making a judgment.

When a job is saved, the application assigns it an ID. When the original job description is stored, it should remain unchanged. A SHA-256 hash calculated from the same text should always produce the same hash. Database operations, serialization, artifact naming, validation, and duplicate-detection rules should behave predictably.

These are software guarantees.

If the system asks, "Have I already stored a job with this exact description hash?" there is little benefit in asking an AI. Ordinary software can answer the question precisely, quickly, cheaply, and repeatedly.

## Probabilistic Intelligence: The Questions That Require Judgment

Other questions are much harder to express as fixed rules.

Consider a job description asking for "strong experience designing automated testing strategies across complex distributed systems."

Does the candidate's previous experience satisfy that requirement?

There may be no exact keyword match. Evidence might be scattered across several jobs, projects, and skills. The answer requires interpreting what the employer means and comparing it with what the candidate has actually done.

That is where probabilistic intelligence becomes valuable.

The AI can parse an unstructured job description into structured information, interpret requirements, compare them with the CandidateProfile, identify strengths and gaps, recommend resume changes, and generate a tailored resume. The result is not a mathematical certainty. It is an informed judgment based on evidence and context.

## Why the Combination Matters

A good AI application does not replace ordinary software with AI.

It puts each kind of computation where it belongs.

The Career Manager therefore has a useful architectural boundary:

Deterministic software provides the structure and guarantees. Probabilistic intelligence provides interpretation and judgment.

For example, AI may decide that a candidate appears to be a strong match for a position. But deterministic software should decide where that analysis is stored, which job ID it belongs to, whether required fields exist, and whether the application has already processed that job.

The AI can say, "I think this means X."

The software can say, "If X is accepted, these rules will always be followed."

That separation makes an AI application more reliable, testable, understandable, and maintainable. It also captures an important lesson from building the AI Career Manager: AI should reduce repetitive intellectual work without replacing engineering discipline.

The most powerful system is not AI instead of conventional software. It is conventional software providing a dependable foundation on which probabilistic intelligence can safely operate.