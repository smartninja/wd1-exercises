# About

If Cloud SDK does not work on your computer, use this example. 

### libraries

First install the necessary libs: `pip install -r requirements.txt` (the `requests` library is added).

The `requests` library will help us fetch the data from the OpenWeatherMap API. This library is the equivalent of the 
`urlfetch` library on GAE.

### get the API key

In order to get the data from OpenWeatherMap you'll need to create an account there (`openweathermap.org/api`). Then 
create an API key in the dashboard and copy it into main.py.

### Running the app

Run main.py (right click in Pycharm on main.py and select Run). Or run it via command line: `python main.py`.