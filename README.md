# pastebin2misp

### Description
Pastebin2misp is a python package that allows for monitoring and scraping of pastes on pastebin of given authors.
It will periodically (if turned into a cron-job) check a list of pastebin-authors (provided by you), then check for new posts by those authors. If it finds any, it will scrape the text of that paste, parse Indicators of Compromise (IOCs) from them, add a new event in your MISP instance, add the IOCs as attributes and publish the event.

### Installation

1. Run `git clone https://github.com/renzejongman/pastebin2misp` in the folder you want to install it in
2. install the dependencies (below)
3. Populate the `usernames.conf`-file with the authors you want to follow. One username per line, no markup.
4. Populate `keys.py` with your MISPs URL and authentication key (find it in your profile on your MISP instance), and whether you want to automatically publish - and if so alert on - the event.
5. Set up a cron-job to periodically run the script.
	* type: `sudo crontab -e`
	* add the following line (change the path for your installation): `0 * * * * /home/your-username/path/to/pastebin2misp/pastebin2misp.py` to run it every hour, on the hour.

6. To run, type `python3 pastebin2misp.py`.

### First run & whenever you add a new author to usernames.conf

It's probably a good idea to make sure `EMAIL_ALERTS` in `keys.py` is set to `False` **before** you run the script for the first time, and whenever you add new authors to **usernames.conf**. The script pulls all historic pastes from those authors, which creates a lot of new events (and potentially alerts if set to True).
 
### Dependencies

* requests:		`python3 -m pip install requests`
* BeautifulSoup:	`python3 -m pip install bs4`
* pymisp:		`python3 -m pip install pymisp`
* iocparser		`python3 -m pip install iocparser`

