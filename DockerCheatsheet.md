Right now, the app runs on job descriptions we manually put in the examples directory. 
It should run on job descriptions pulled from opportunities found in searches, when we get past MVP.
We are running the job hunter in docker for easier deployment/use by recruiters. And it looks good. And, what doesn't run in Docker in 2026?


# AI Job Hunter - Docker Commands

## Build the Docker image

```bash
docker build -t ai-job-hunter .
```

Rebuild from scratch (ignore cache):

```bash
docker build --no-cache -t ai-job-hunter .
```

---

## List Docker images

```bash
docker images
```

or

```bash
docker images ai-job-hunter
```

---

## Run the application

Uses the API key from your local `.env` file.

```bash
docker run --rm --env-file .env ai-job-hunter
```

Equivalent explicit command:

```bash
docker run --rm --env-file .env ai-job-hunter python -m src.main
```

---

## Run the test suite

```bash
docker run --rm \
    --env-file .env \
    ai-job-hunter \
    python -m pytest -v
```

---

## Mount the output directory

Persist generated JSON files to the host machine.

```bash
docker run --rm \
    --env-file .env \
    -v "$(pwd)/examples/output:/app/examples/output" \
    ai-job-hunter
```

---

## Run an interactive shell inside the container

```bash
docker run --rm -it ai-job-hunter bash
```

If `bash` isn't available:

```bash
docker run --rm -it ai-job-hunter sh
```

---

## Remove the image

```bash
docker rmi ai-job-hunter
```

---

## Verify Docker installation

```bash
docker --version
```

---

## Verify Docker is working

```bash
docker run hello-world
```

---

## View running containers

```bash
docker ps
```

---

## View all containers (including exited)

```bash
docker ps -a
```

---

## Clean up unused Docker resources

```bash
docker system prune
```

Add `-a` to remove unused images as well.

```bash
docker system prune -a
```
