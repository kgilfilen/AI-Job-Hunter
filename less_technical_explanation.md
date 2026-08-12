# Core Architecture

### First, a summary

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

### That is to say...

* someone puts "http://localhost:5173" in the address bar of chrome
* chrome sends "GET" to port 5173, which has the Vite webserver running/listening
* Vite receives GET /applications/needs-attention, and says, “You're asking my web server for /applications/needs-attention.”
* Vite, which is running on NPM, and is therefore providing itself as a web server, hands out the frontend typescript when people ask for it. Vite receives the GET request, and therefore goes to that end point, and hands out the typescript that is there. 
* Chrome receives that typescript, and loads it in the browser, rendering the web page, at least the header and "needs-attention" section.
* The JavaScript is executing behind the scenes on chrome, and needs some data from the backend, and a function in it does a fetch in the react code (fetch still running on chrome): fetch "http://127.0.0.1:8000/applications/needs-attention"'
* Chrome sends "GET /applications/needs-attention" to 127.0.0.1 on port 8000
* Port 8000 has another web server, Uvicorn, running, which contains our API backend code (using python FastApi), and all of the endpoints we need.
* Uvicorn/FastApi examine the request: "GET /applications/needs-attention", and FastApi does in fact, have an endpoint called "/applications/needs-attention" which accepts a "GET", and calls the python function for that with any parameters that might have been sent.
* The function calls our other python backend code, including the application service, which retrieves data from our database. the function returns the data, through Uvicorn/FastApi, to the frontend "fetch" that is rendered/rendering the new data on chrome.
* The fresh react UI might have a new picklist of jobs, or a text saying "No followups are currently due."
* The complete trip therefore looks approximately like this:

```
bash
Person → Chrome → Vite → React files → Chrome executes React → fetch() → Uvicorn → FastAPI → Service → Repository → SQLite → Repository → Service → FastAPI → Uvicorn → Chrome → React → rendered webpage
```

### An important distinction is that there are two HTTP requests involved.

The first request obtains the frontend application:

Chrome → Vite :5173

The second request obtains the application data needed by that frontend:

React running inside Chrome → Uvicorn/FastAPI :8000

Vite serves the frontend. Uvicorn serves the backend API. React executes in the user's browser and connects the two from the user's point of view.