## Smoke tests

pytest

python3 -m pytest -v

python3 -m pytest tests/unit -v

python3 src/main.py --help

python3 src/main.py --file examples/jobs/lead_qa_auto.txt

python3 src/main.py --url https://www.virtualvocations.com/job/senior-qa-engineer-3129270-i.html

python3 src/main.py --examples

docker compose run --rm it-job-hunter pytest


