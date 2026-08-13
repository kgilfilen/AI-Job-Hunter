# Core Architecture

This provides a roughly correct explanation of how web pages work. There are many minute details that are not quite right, but generally this offers a good explanation of today's complexity of websights. 

### First, a summary

the browser renders the react frontend handed to it by the vite web server on my laptop at port 5173 (or hosted in the cloud somewhere), which makes requests to our backend api, by contacting the Uvicorn web server on port 8000 (and actually Chrome uses various available temporary ports as needed) which accepts requests because it has our fastapi backend running. 

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
* Vite receives GET, and hands out React stuff, including Javascript and HTML to Chrome.
* Chrome receives that stuff, and loads it/executes it in the browser, rendering the web page, at least the initial parts. It tries to start with a section called "Needs Attention" (because we wrote it to), which actually needs some data from the database about what tasks we have due now.
* The JavaScript needs that data from the backend, and a function in it does a fetch in the react code (fetch still running on chrome): fetch "http://127.0.0.1:8000/applications/needs-attention"'
* Because of the fetch, chrome sends "GET /applications/needs-attention" to 127.0.0.1 on port 8000
* Port 8000 has another web server, Uvicorn, which runs our API backend code built from FastApi, and FastApi responds to endpoints as needed.
* Uvicorn receives the full HTTP communication from Chrome, and hands the HTTP GET to FastApi. 
* FastApi examines the HTTP request: "GET /applications/needs-attention", and it does in fact, have a route registered for "/applications/needs-attention" which expects a "GET", and therefore calls the python function for that with any parameters that might have been sent.
* The function calls our other python service code, including the application service, which retrieves data from our repository layer over the database. 
* FastApi turns the answer into HTTP for the return trip to chrome. 
* Uvicorn returns the HTTP response to chrome, to the frontend "fetch" that is updating the frontend with the new data on chrome.
* The updated react UI might have a new list of applications that need attention, or a text saying "No followups are currently due."
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