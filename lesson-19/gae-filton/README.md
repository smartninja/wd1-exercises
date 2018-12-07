# About

GAE Filton Hotel Guestbook.

# Usage

1. Click on Download ZIP
2. Save on your disk and unzip
4. Build something nice ;)
5. Run the app with this command: `dev_appserver.py ./`
6. Open your browser and go to: `http://localhost:8080`

If GAE doesn't work for you on localhost, change the gae_env variable to False (in main.py) and run the main.py directly.

Instead of the Cloud Datastore, an SQLite database will be used. There's a fake ndb wrapper in utils so you don't have to 
change any code.

**Important:** The fake ndb wrapper only supports writing into the database at this point, no editing and deleting yet.