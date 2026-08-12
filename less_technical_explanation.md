# Core Architecture

This provides a roughly correct explanation of how web pages work. There are many minute details that are not quite right, but generally this offers a good explanation of today's complexity of websights. 

### First, a summary

the browser renders the react frontend handed to it by the vite web server on my laptop (or hosted in the cloud somewhere) at port 5173), which makes requests to our backend api, by contacting the uvicorn web server on port 8000 (and actually uses various available temporary ports as needed) which accepts requests because it has our fastapi backend running. 

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
* chrome sends "GET /" ('get the stuff for root') to port 5173, which has Vite webserver running/listening
* Vite receives GET, and hands out Javascript for our react frontend.
* Chrome receives that Javascript, and loads it in the browser, rendering the web page, at least the initial parts. It wants to start with a section called "Needs Attention".
* The JavaScript is executing behind the scenes on chrome, and needs some data from the backend, and a function in it does a fetch in the react code (fetch still running on chrome): fetch "http://127.0.0.1:8000/applications/needs-attention"'
* Chrome sends "GET /applications/needs-attention" to 127.0.0.1 on port 8000
* Port 8000 has another web server, Uvicorn, which runs our API backend code (using python FastApi), and all of the endpoints we need.
* Uvicorn/FastApi examine the request: "GET /applications/needs-attention", and FastApi does in fact, have an endpoint called "/applications/needs-attention" which accepts a "GET", and calls the python function for that with any parameters that might have been sent.
* The function calls our other python backend code, including the application service, which retrieves data from our database. the function returns the data, through Uvicorn/FastApi, to the frontend "fetch" that is updating the frontend with the new data on chrome.
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

## Actual division of labor

Vite SERVES the frontend.
Chrome EXECUTES the frontend.
React REQUESTS backend data.
Uvicorn SERVES the backend.
FastAPI ROUTES the API request.
Python services DO the business work.
Repositories ACCESS SQLite.