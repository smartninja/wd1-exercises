# Exercise 15.1: Put your Fakebook project in your web app

- Install the dependencies: `pip install requirements.txt`
- Run the main.py file
- Go to `http://127.0.0.1:8080/templates/fakebook.html` to see the fakebook HTML page

--

## How to run webapp2 without GAE

> Note: This will only work on localhost. You will not be able to deploy this code on Google App Engine.

If you can't get GAE to run on your computer, you can still use the webapp2 Python framework without GAE. This is a step-by-step tutorial on how to do it.

### Step 1: Create new PyCharm project

Open PyCharm and click on **Create New Project**.

![PyCharm Create New Project Window](https://storage.googleapis.com/smartninja/pycharm-create-new-project-1543538360.png)

### Step 2 (optional): Create a virtual environment

In the next step define the project path and optionally create a virtual environment.

![Create a virtual environment](https://storage.googleapis.com/smartninja/pycharm-venv-path-1543538516.png)

### Step 3: Install PIP libraries

Now that you've started a new project, open the Terminal tab (below) and install **three** PIP libraries with the following commands:

- `pip install WebOb`
- `pip install Paste`
- `pip install webapp2`

`webapp2` is the Python framework we'll use and it needs `WebOb` in order to work correctly. `Paste` is a HTTP server that we'll use to run our website on our computer.

![Install libraries via PIP](https://storage.googleapis.com/smartninja/install-pip-libs-1543538743.png)

### Step 4: Create main.py

Create a file called `main.py` in the root of your project.

Then add the following code in it:

``` python
import webapp2
from paste import httpserver


# handlers
class MainHandler(webapp2.RequestHandler):
    def get(self):
        return self.response.write('Hello, SmartNinja!')
	
	
# URLs
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
	
	
# run the server
def main():
    httpserver.serve(app, host='127.0.0.1', port='8080')
	
	
if __name__ == '__main__':
    main()
```

### Step 5: Run your web app

Now you can finally run your new web app! Right-click on `main.py` and select **Run 'main'**.

![Run main.py](https://storage.googleapis.com/smartninja/run-main-pycharm-1543538963.png)

### Step 6: See your web app in browser

A new window will open in your PyCharm below. Click on the [http://127.0.0.1:8080](http://127.0.0.1:8080) link and your 
web app will open in the browser.

### Step 7: Make some changes

Change "Hello, SmartNinja!" into something else, for example "Hello, Your Name!". When you do this change, you'll have 
to reload **both** `main.py` and your browser to see the changes. 

Click on the green curved arrow to reload `main.py`:

![Reload app](https://storage.googleapis.com/smartninja/pycharm-reload-app-1543539316.png)

### Congrats

That's it! You've successfully set up a localhost web app. :)
