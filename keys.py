#!/usr/bin/env python


## url and key for the MISP instance you want the pastes to be pushed to.
misp_url = ""
misp_key = ""

# the folder where you've installed pastebin2misp
path	 = ""

# whether or not to alert by email when a new event is created. Turn this to False whenever you add new users to usernames.conf, and when you run it for the first time, because it will import all the previous pastes from those new authors
alerting = True
