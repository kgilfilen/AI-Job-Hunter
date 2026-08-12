# Core Architecture

the browser renders the react frontend handed to it by the vite web server (at port 5173), which makes requests to our backend api, by contacting the uvicorn web server on port 80000 (actually various ports in the 58000 series) which accepts requests because it has our fastapi backend running. 

```
bash
Browser (chrome)
  ↓
Vite server
localhost:5173
  ↓
delivers React code
  ↓
Browser executes React
  ↓
React sends HTTP request
  ↓
Uvicorn
127.0.0.1:8000
  ↓
FastAPI
  ↓
our Python services/repositories/SQLite
```