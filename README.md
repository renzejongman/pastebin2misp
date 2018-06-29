# pastebin2misp

### Description
Pastebin2misp is a python package that allows for monitoring and scraping of pastes on pastebin of given authors.
It will periodically (if turned into a cron-job) check a list of pastebin-authors (provided by you), then check for new posts by those authors. If it finds any, it will scrape the text of that paste, parse Indicators of Compromise (IOCs) from them, add a new event in your MISP instance, add the IOCs as attributes and publish the event.

### Installation

1. Run **git clone https://github.com/renzejongman/pastebin2misp** in the folder you want to install it in
2. Populate the **usernames.conf**-file with the authors you want to follow. One username per line, no markup.
3. Populate **keys.py** with your MISPs URL and authentication key, the folder pat where you installed it and whether you want to receive email alerts.
4. Set up a cron-job to periodically run the script.
5. To run, type **python3 pastebin2misp.py**.

### First run & whenever you add a new author to usernames.conf

It's probably a good idea to change the command *alerts = True* in **keys.py** to *False* **before** you run the script for the first time, and whenever you add new authors to **usernames.conf**. The script pulls all historic pastes from those authors, which creates a lot of new events (and potentially alerts if set to True).
 
### Dependencies

* requests
* BeautifulSoup (bs4)
* pymisp

