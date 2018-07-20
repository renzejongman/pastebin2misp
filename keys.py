## keys.py: config file for pastebin2misp.py

## url and key for the MISP instance you want the pastes to be pushed to.
MISP_URL 		= ""
MISP_KEY 		= ""

# whether or not to alert by email when a new event is created. Turn this to False whenever you add new users to usernames.conf, and when you run it for the first time, because it will import all the previous pastes from those new authors
PUBLISH_EVENTS		= True
EMAIL_ALERTS		= False

