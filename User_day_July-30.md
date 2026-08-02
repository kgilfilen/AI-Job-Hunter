# Put on your user hat!!

"If I were unemployed and using this every morning, what would annoy me?"

## Parsing real job posts

I am still doing regular job applications.


## Check job scores--would I have scored this job this way?


## Read explanations given


## Generate resumes for good jobs


## Compare two similar but different jobs


## Re-run the same job


## Gorilla tests


# Bugs


# Confusing


# Slow


# Ideas

We need to add current usage for the app and tests to the Readme.

# Missing skills I have, but teh tool does not know about. They should be added to the list, or added as an alias to an item that is already there.

"API testing",

"Regression testing",

"Functional testing",

"Integration testing",

"Test automation",

"Java",

"REST Assured",

"Database validation",

"CI/CD",

"AI agent workflows",

"Design patterns",

"QA",

"Automation architecture",

"Software Quality Assurance",

"SQL",

"UI testing",

"OOP",

"Agile",

"Test case management",

"Test automation",

"Selenium WebDriver",

"qTest",

"Postman",

"SDET",

"AI-driven automation",

"Playwright"

## BUG

### Title truncated during parsing

**Expected title:**

Senior Software Development Engineer in Test

**Actual title:**

Senior Software Development Engineer

**Impact:**

The parsed title changes the job classification from SDET to general software development. This could distort fit scoring, duplicate detection, résumé recommendations, and later job-history searches.

**Potential cause:**

The parser matched a shorter, familiar title phrase before considering the full title text.

**Expected behavior:**

Preserve the complete explicit title when the posting provides one, including suffixes such as:

- in Test
- Quality Engineering
- Test Automation
- Platform Engineering
- Data Engineering


## Observation

A complete copied job description identified the employer as Applied Systems, but processing the Virtual Vocations URL did not.

## Impact

The job-board page’s fetched visible text did not contain the employer evidence available in the complete posting. The parser therefore could not identify the hiring company.

## Potential Improvement

Rich URL processing should inspect page metadata, structured data, headers, embedded content, and outbound employer links in addition to visible text. Preserve the job board separately from the hiring company.

## Classification

URL extraction limitation / future feature

## Added

* Added parse_job_opening_file() wrapper.
* Moved parser regression tests to tests/test_data/job_descriptions.
* Added employment-type normalization with deterministic fallback.
* Added regression tests for company detection and title normalization.
* Verified JSON serialization is correct.
* Identified URL job-board limitation (Virtual Vocations vs. full employer posting).