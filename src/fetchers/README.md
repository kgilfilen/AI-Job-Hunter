# Fetchers Package

## Directory Overview

The **Fetchers** package is responsible for retrieving job-posting content from
external web pages and extracting deterministic information that can be obtained
directly from the page.

It converts unstructured HTML into a `FetchedJobPage` containing:

* readable page text
* page title
* canonical URL
* standard HTML metadata
* structured job metadata extracted from JSON-LD

The package does not perform AI parsing, candidate matching, scoring, resume
generation, database persistence, or application-management logic.

### Design Goals

* Isolate network and HTML-processing concerns from the rest of the application.
* Preserve useful page information before AI interpretation occurs.
* Extract structured metadata deterministically when the source page provides it.
* Produce a stable domain object for downstream parsing and analysis.
* Reject obviously invalid URLs before making network requests.
* Keep site-independent fetching separate from future site-specific integrations.

### Modules

| Module                      | Responsibility                                                       |
| --------------------------- | -------------------------------------------------------------------- |
| `web_fetcher.py`            | Fetches job pages and converts HTML into a `FetchedJobPage`.         |
| `job_metadata_extractor.py` | Extracts normalized job metadata from JSON-LD embedded in job pages. |

---

# web_fetcher.py

## Purpose

This module retrieves a job posting from an HTTP or HTTPS URL and converts the
returned HTML into a `FetchedJobPage`.

It performs deterministic preprocessing before the job is handed to downstream
AI-based parsing or analysis.

Conceptually:

```text
Job URL
    ↓
web_fetcher
    ↓
HTTP response / HTML
    ↓
visible text + page metadata + JSON-LD metadata
    ↓
FetchedJobPage
    ↓
downstream parsing / JobService
```

The fetcher is responsible for obtaining and normalizing source-page
information. It does not determine whether the candidate is qualified for the
job or interpret the meaning of job requirements.

---

## Public Interface

The primary public function is:

* `fetch_job_description()`

Additional reusable functions currently exposed by the module are:

* `validate_url()`
* `extract_visible_text()`

Metadata helper functions are internal implementation details:

* `_get_meta_content()`
* `_extract_metadata()`
* `_extract_canonical_url()`

---

## Inputs and Outputs

### `fetch_job_description(url)`

* Input: job-posting URL as a string
* Output: `FetchedJobPage`
* Side effect: performs an HTTP GET request
* Raises:

  * `ValueError` for invalid URL structure
  * `RuntimeError` when the HTTP request fails

The returned `FetchedJobPage` contains:

* originally requested URL
* extracted visible page text
* page title
* canonical URL when available
* selected HTML metadata
* structured `JobMetadata` derived from JSON-LD

The current fetch process sends a browser-like User-Agent and applies a request
timeout.

---

### `validate_url(url)`

Validates that the supplied URL:

* uses `http` or `https`
* contains a hostname

Invalid schemes raise `ValueError`.

A URL without a hostname also raises `ValueError`.

This validation occurs before any network request is attempted.

---

### `extract_visible_text(html)`

* Input: raw HTML string
* Output: normalized readable page text
* Side effects: none

The function parses the HTML and removes the following elements:

* `script`
* `style`
* `noscript`
* `svg`
* `nav`
* `footer`

Remaining page text is:

* extracted with newline separators
* stripped of surrounding whitespace
* reduced to non-empty lines
* joined using newline characters

The function extracts general visible page content. It does not currently
attempt to locate a job-board-specific job-description container.

---

## Page Metadata

`fetch_job_description()` extracts several useful pieces of deterministic
page-level metadata.

### Page Title

The contents of the HTML `<title>` element are retained when present.

### Canonical URL

The module looks for:

```html
<link rel="canonical" href="...">
```

If present and valid, the `href` value becomes the page's canonical URL.

### HTML Metadata

The following `<meta>` values are currently retained when available:

* `description`
* `og:title`
* `og:description`
* `og:site_name`

Missing metadata is omitted rather than represented by empty strings.

---

## Dependencies

This module depends on:

* `requests`
* `BeautifulSoup`
* `urllib.parse.urlparse`
* `FetchedJobPage`
* JSON-LD extraction provided by `job_metadata_extractor.py`

It has no direct dependency on:

* AI models
* candidate profiles
* scoring
* resume generation
* SQLite
* repositories
* Streamlit

---

## Behavioral Specifications

* Only HTTP and HTTPS URLs are accepted.
* URL validation occurs before the network request.
* HTTP request failures are translated into `RuntimeError`.
* HTTP error responses are rejected through `raise_for_status()`.
* HTML is parsed using BeautifulSoup.
* Non-content HTML elements are removed before visible text is returned.
* Empty lines are removed from extracted page text.
* Page metadata is included only when a usable string value exists.
* JSON-LD metadata extraction occurs from the original HTML.
* The requested URL is preserved separately from the canonical URL.
* The function returns a domain object rather than raw HTML or a Requests
  response object.

---

## Invariants

The module aims to guarantee:

* no network request for an obviously invalid URL
* preservation of the originally requested URL
* normalized visible text
* deterministic HTML metadata extraction
* separation between fetching and AI interpretation
* no candidate-specific or scoring behavior

---

## Error Behavior

### Invalid URL

`validate_url()` raises `ValueError` when:

* the scheme is not HTTP or HTTPS
* no hostname is present

### Network Failure

`requests.RequestException` and its subclasses are converted into:

```text
RuntimeError("Failed to fetch job description: ...")
```

The original exception is preserved as the exception cause.

Possible failures include:

* DNS errors
* connection failures
* request timeout
* HTTP error status
* redirects ending in failure

### HTML Parsing

Malformed HTML is handled according to BeautifulSoup's normal parsing behavior.

Missing titles, canonical URLs, metadata tags, or JSON-LD data do not themselves
cause an exception.

---

## Good Unit-Test Targets

* valid HTTP URL accepted
* valid HTTPS URL accepted
* unsupported URL scheme rejected
* URL without hostname rejected
* HTTP request receives expected timeout and headers
* network exception converted to `RuntimeError`
* HTTP error response converted to `RuntimeError`
* script/style/navigation elements removed from visible text
* blank lines removed from visible text
* page title extracted correctly
* missing page title handled correctly
* canonical URL extracted correctly
* missing canonical URL handled correctly
* standard metadata extracted correctly
* empty metadata values discarded
* `FetchedJobPage` populated correctly
* JSON-LD metadata forwarded into `FetchedJobPage`

---

## Possible Future Enhancements

* Centralize request timeout and header configuration.
* More precise job-description DOM extraction.
* Redirect and final-URL tracking.
* Retry behavior for temporary network failures.
* Site-specific fetchers for job boards requiring specialized handling.
* JavaScript-rendered page support where appropriate.
* Additional HTML metadata.
* Fetch diagnostics or response metadata.

---

## Overall Responsibility

`web_fetcher.py` provides the network boundary between an external job page and
the internal Career Manager domain.

Its job is to retrieve the page and transform its HTML into deterministic,
usable source information.

It deliberately does not decide what the job means or how well the candidate
matches it.

---

# job_metadata_extractor.py

## Purpose

This module extracts structured job facts from JSON-LD embedded in job-posting
HTML.

Many job sites publish machine-readable Schema.org `JobPosting` data inside:

```html
<script type="application/ld+json">
```

When that information is available, the application can obtain facts such as
job title, company, location, salary, and posting dates without asking an AI to
infer them from visible text.

Conceptually:

```text
HTML
    ↓
extract_json_ld()
    ↓
JSON-LD dictionaries
    ↓
find_job_posting()
    ↓
JobPosting object
    ↓
extract_job_metadata()
    ↓
JobMetadata
```

This module therefore forms part of the deterministic extraction layer of the
application.

---

## Public Interface

The primary functions are:

* `extract_json_ld()`
* `find_job_posting()`
* `extract_job_metadata()`

Internal normalization helpers are:

* `_clean_string()`
* `_extract_location()`
* `_extract_salary()`
* `_is_number()`
* `_format_number()`

---

## Inputs and Outputs

### `extract_json_ld(html)`

* Input: raw HTML
* Output: list of JSON-LD dictionaries
* Side effects: none

The function:

1. parses the HTML
2. finds `<script type="application/ld+json">` elements
3. ignores empty script blocks
4. attempts to parse each block as JSON
5. ignores malformed JSON
6. returns successfully parsed dictionary objects

Malformed or unusable JSON-LD does not cause extraction to fail.

The current implementation retains only JSON-LD blocks whose top-level parsed
value is a dictionary.

---

### `find_job_posting(blocks)`

* Input: JSON-LD dictionaries
* Output: first matching `JobPosting` dictionary, or `None`

The function recognizes a `JobPosting` in either:

```text
block["@type"] == "JobPosting"
```

or inside a JSON-LD:

```text
@graph
```

array.

The first matching job posting is returned.

---

### `extract_job_metadata(blocks)`

* Input: extracted JSON-LD dictionaries
* Output: `JobMetadata`
* Side effects: none

If no `JobPosting` object exists, the function returns an empty:

```python
JobMetadata()
```

When a job posting exists, the function attempts to populate:

* title
* company
* location
* employment type
* date posted
* valid-through date
* salary
* salary currency
* salary interval

Missing or malformed individual fields generally become `None` rather than
causing extraction to fail.

---

## Company Extraction

Company information comes from:

```text
hiringOrganization.name
```

The hiring organization must be represented as a dictionary and its name must
be a non-empty string.

Whitespace is removed from the beginning and end of the company name.

---

## Location Extraction

Location is derived from:

```text
jobLocation.address
```

The extractor currently uses:

* `addressLocality`
* `addressRegion`
* `addressCountry`

Available components are combined with commas.

For example:

```text
Denver, CO, US
```

When `jobLocation` is a list, the current implementation uses the first
location only.

Missing or invalid location structures produce `None`.

---

## Salary Extraction

Salary data comes from:

```text
baseSalary
```

The extractor supports several Schema.org-style representations.

### Direct Numeric Salary

Example conceptual structure:

```text
baseSalary:
    currency: USD
    value: 120000
```

Result:

```text
salary = "120000"
salary_currency = "USD"
salary_interval = None
```

### Salary Range

Conceptual structure:

```text
baseSalary:
    currency: USD
    value:
        minValue: 100000
        maxValue: 130000
        unitText: YEAR
```

Result:

```text
salary = "100000–130000"
salary_currency = "USD"
salary_interval = "YEAR"
```

### Single Structured Value

A numeric `value.value` is also supported.

### Partial Range

If only `minValue` or only `maxValue` exists, the available numeric value is
returned.

The current representation does not label a lone minimum or maximum as such;
only the numeric value is stored.

---

## Numeric Handling

`_is_number()` considers integers and floating-point values numeric.

Boolean values are deliberately excluded even though Python treats `bool` as a
subclass of `int`.

`_format_number()`:

* removes `.0` from whole-number floats
* retains decimal values when needed
* returns a string representation

Passing a nonnumeric value directly to `_format_number()` raises `TypeError`.

---

## String Normalization

`_clean_string()`:

* accepts strings only
* strips surrounding whitespace
* converts empty strings to `None`
* converts non-string values to `None`

This behavior is used throughout metadata extraction to prevent empty or
unexpected values from leaking into the domain model.

---

## Dependencies

This module depends on:

* `json`
* BeautifulSoup
* Python typing support
* `JobMetadata`

It has no dependency on:

* network requests
* AI
* candidate profiles
* parsing prompts
* scoring
* repositories
* databases
* UI code

---

## Behavioral Specifications

* Invalid JSON-LD blocks are ignored.
* Empty JSON-LD blocks are ignored.
* Only dictionary JSON-LD blocks are currently retained.
* The first discovered `JobPosting` is used.
* `JobPosting` objects may exist directly or inside `@graph`.
* Missing job metadata returns an empty `JobMetadata`.
* Missing individual metadata fields become `None`.
* Strings are stripped of surrounding whitespace.
* Empty strings become `None`.
* Boolean values are not treated as salary numbers.
* Whole-number salary values are rendered without a decimal suffix.
* Salary ranges use an en dash between minimum and maximum values.
* Extraction does not mutate the input JSON-LD structures.

---

## Invariants

The module aims to guarantee:

* deterministic metadata extraction
* graceful handling of absent metadata
* graceful handling of malformed JSON-LD
* normalized optional strings
* stable salary formatting
* independence from AI interpretation
* no network or persistence side effects

---

## Error Behavior

Malformed JSON inside JSON-LD script elements is silently ignored.

Unexpected or missing JSON-LD structures normally result in missing metadata
rather than exceptions.

`_format_number()` raises `TypeError` if directly passed a value that is not a
supported numeric type.

BeautifulSoup and standard Python errors otherwise propagate naturally.

---

## Good Unit-Test Targets

### JSON-LD Parsing

* valid JSON-LD dictionary extracted
* multiple JSON-LD blocks extracted
* empty JSON-LD ignored
* malformed JSON ignored
* non-dictionary top-level JSON behavior
* missing JSON-LD produces an empty list

### JobPosting Discovery

* top-level `JobPosting` discovered
* `JobPosting` inside `@graph` discovered
* unrelated JSON-LD ignored
* first matching `JobPosting` returned
* no job posting returns `None`

### Metadata Extraction

* empty `JobMetadata` returned when no posting exists
* title extraction
* company extraction
* employment type extraction
* posting-date extraction
* expiration-date extraction
* whitespace normalization
* malformed fields handled safely

### Location

* full city/region/country location
* partial location
* missing address
* location represented as a list
* empty location list
* multiple-location behavior

### Salary

* direct numeric salary
* integer salary
* decimal salary
* minimum/maximum salary range
* single structured salary
* minimum-only salary
* maximum-only salary
* currency extraction
* salary interval extraction
* boolean rejected as numeric salary
* malformed salary structure

---

## Possible Future Enhancements

* Support top-level JSON-LD arrays.
* Support multiple `JobPosting` objects explicitly.
* Preserve multiple job locations.
* Normalize country and region representations.
* Represent minimum-only and maximum-only salaries more explicitly.
* Normalize salary intervals.
* Support additional Schema.org job fields.
* Preserve raw structured metadata for debugging or auditing.
* Add metadata extraction diagnostics when malformed JSON-LD is encountered.

---

## Package Architectural Boundary

The Fetchers package sits before the application's probabilistic AI layer.

Where reliable structured facts are explicitly published by the source site,
the application should extract those facts deterministically rather than ask an
AI model to infer them.

For example:

```text
JSON-LD says:
    title = "Senior QA Engineer"
    company = "Example Corp"
    salary = "120000–140000"

             ↓

deterministic extraction

             ↓

JobMetadata
```

AI can later interpret what the responsibilities mean, whether the candidate's
experience satisfies them, and how the resume should respond.

The fetcher should not make those judgments.

---

## Overall Responsibility

The Fetchers package turns external job pages into reliable internal source
material.

`web_fetcher.py` owns retrieval and general HTML preprocessing.

`job_metadata_extractor.py` owns deterministic extraction of structured job
facts already published in the page.

Together they provide the source-data boundary between the public web and the
Career Manager's downstream parsing, analysis, and career-management layers.
