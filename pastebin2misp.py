#!/usr/bin/env python3
## Description:         Pulls IOCs from pastes from monitored authors and adds them to MISP as events with attributes.
## Author:              Renze Jongman
## Date:                28 June 2018
## Instructions:        populate the usernames.conf-file with the username of pastebin-authors you want to follow, 
##                      populate the keys.py file with your misp-url and your auth-key, then set up a cron job to 
##                      check periodically for new posts. 
##                      Tip: on the first run, change 'self.misp.publish(event)' on line 102 to 'self.misp.fast_publish(event)',
##                      That will prevent everyone from receiving tons of emails on the firts run.

import logging, requests, bs4, re, shelve, os
from pymisp     import PyMISP
from keys       import misp_url, misp_key, path, alerting
from iocparser  import IOCParser


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.debug("Starting the Pastebin scraper.")
parsedPaste     = []
usernames       = []
toScrape        = []
os.chdir(path)

try:
    shelfFile   = shelve.open('knownpastes')
    knownPastes = shelfFile['knownPastes']
    shelfFile.close()
    logging.debug("Imported a grand total of {} previously imported pastes.".format(len(knownPastes)))
except:
    logging.warning("Failed to import known pastes.")
    knownPastes = []

f = open('usernames.conf')
for i in f:
    i = i.strip('\n')
    usernames.append(i)
    logging.debug("Added username {}.".format(i))
f.close()
logging.debug(usernames)


class paste:
    # class for each individual paste.

    def __init__(self, URI, title, username):
        self.URI    = URI
        self.title  = "OSINT - {} - {}".format(title, username)
        self.author = username

    def scrape(self):
        res         = requests.get(self.URI)
        res.raise_for_status()
        soup        = bs4.BeautifulSoup(res.text, "html.parser")
        self.code   = soup.textarea.getText()
        logging.debug("scraped full code of {}. It has a total of {} characters.".format(self.URI, len(self.code)))

    def iocs(self):
        parseObject = IOCParser(self.code)
        self.iocs   = (parseObject.parse())
        logging.debug("parsed {} IOC's from paste: {}".format(len(self.iocs), self.title))
        #logging.debug("for example: the first IOC is a {}, and has value {}".format(self.iocs[0].kind, self.iocs[0].value))



class generateEvents():
    # generates a seperate event for every paste with more than 1 parsed IOC, after initialising a connection with the MISP instance.

    def __init__(self, paste):
        self.paste  = paste
        self.url    = misp_url
        self.key    = misp_key


    def initMISP(self):
        self.misp   = PyMISP(self.url, self.key, False, 'json', debug=True)

    def addEvents(self):
        for i in range(len(self.paste)):
            if len(self.paste[i].iocs) != 0:
                logging.debug("Paste: {}, # of IOCs: {}. Creating an event.".format(self.paste[i].title, len(self.paste[i].iocs)))
                event   = self.misp.new_event(distribution=2, analysis=2, info=self.paste[i].title)
                self.misp.add_internal_link(event, self.paste[i].URI, category="External analysis")
                self.misp.add_tag(event, "Type:OSINT")
                self.misp.add_tag(event, 'osint:source-type="pastie-website"')
                self.misp.add_tag(event, 'OSINT')
                self.misp.add_tag(event, 'tlp:white')

                for j in range(len(self.paste[i].iocs)):
                    if self.paste[i].iocs[j].kind   == "IP":
                        self.misp.add_ipsrc(event, self.paste[i].iocs[j].value)
                    elif self.paste[i].iocs[j].kind == "uri":
                        self.misp.add_url(event, self.paste[i].iocs[j].value)
                    elif self.paste[i].iocs[j].kind == "md5":
                        self.misp.add_hashes(event, md5=self.paste[i].iocs[j].value)
                    elif self.paste[i].iocs[j].kind == "sha1":
                        self.misp.add_hashes(event, sha1=self.paste[i].iocs[j].value)
                    elif self.paste[i].iocs[j].kind == "sha256":
                        self.misp.add_hashes(event, sha256=self.paste[i].iocs[j].value)
                    elif self.paste[i].iocs[j].kind == "CVE":
                        #self.misp.add_object(event, 63, self.paste[i].iocs[j].value)
                        pass
                    if self.paste[i].iocs[j].kind   == "email":
                        self.misp.add_email_src(event, self.paste[i].iocs[j].value)
                self.misp.publish(event, alert=alerting)






def pasteRegex():
    return(re.compile(r'^[/][a-zA-Z0-9]{8}$'))

def scrapePosts(username):
    logging.debug("Starting the scrape.")
    res=requests.get('https://pastebin.com/u/{}'.format(username))
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    elems = soup.find_all(href=pasteRegex())
    logging.debug('gross number of links found: {}'.format(len(elems)))
    logging.debug("Deleting first ten results, because they are links to settings, messages and the new pastes on the rigt sidebar.")
    for i in range(10):
        #deletes links to settings, messages, and public pastes on the right sidebar.
        del elems[0]
    logging.debug("Found {} net posts for user {}".format(len(elems), username))
    for i in range(len(elems)):     
        postTitle   = elems[i].getText()
        postURI     = 'https://pastebin.com{}'.format(elems[i].attrs['href'])

        if postURI in knownPastes:
            logging.debug("{} was seen before. Not queuing for scraping.".format(postURI))
        else:
            logging.debug("{} is a new paste! Queued for scraping.".format(postURI))
            parsedPaste.append(paste(postURI, postTitle, username))
            knownPastes.append(postURI)
    shelfFile                   = shelve.open('knownpastes')
    shelfFile['knownPastes']    = knownPastes
    shelfFile.close()
    return(parsedPaste)


def findNewPastes(usernames):
    for i in range(len(usernames)):
        toScrape = (scrapePosts(usernames[i]))
    return(toScrape)

newPastes = findNewPastes(usernames)
logging.debug("Found {} new pastes.".format(len(newPastes)))
for i in range(len(newPastes)):
    newPastes[i].scrape()
    newPastes[i].iocs()
x = generateEvents(newPastes)
x.initMISP()
x.addEvents()
