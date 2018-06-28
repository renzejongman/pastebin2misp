# pastebin2misp

### Description
Pastebin2misp is a python package that allows for monitoring and scraping of pastes on pastebin of given authors.
It will periodically (if turned into a cron-job) check a list of pastebin-authors (provided by you), then check for new posts by those authors. If it finds any, it will scrape the text of that paste, parse Indicators of Compromise (IOCs) from them, add a new event in your MISP instance, add the IOCs as attributes and publish the event.

### Installation

1. Press the green **download or clone button**, and save it in any folder.
2. Populate the **usernames.conf**-file with the authors you want to follow. One username per line, no markup.
3. Populate **keys.py** with your MISPs URL and authentication key.
4. Set up a cron-job to periodically run the script.
5. To run, type **python3 pastebin2misp.py**.

### First run

It's probably a good idea to change the command *misp.publish(event)* on line 102 (or so) of pastebin2misp.py into *misp.fast_publish(event)* **before** you run the script for the first time. Otherwise your users will be notified by email of every single paste being published as an event in MISP. If you want to review the events before publishing, remove the line altogether.
 
### Dependencies

* requests
* BeautifulSoup
* pymisp

