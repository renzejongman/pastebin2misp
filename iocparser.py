#!/usr/bin/env python3
## IOCParser: scrapes IOC's from freetext.

import re, logging, argparse
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

class IOC:
    # a simple class with a value for the type (kind) of IOC and the actual value of the IOC.
    
    def __init__(self, kind, value):
        self.kind   = kind
        self.value  = value

def check(kind):
    f       = open(kind, "r")
    y     = []      
    for line in f:
        y.append(line.rstrip())
    f.close()
    return("|".join(y)[:-1])
    return str(y)


class IOCParser:
    # takes a text and returns IOCs found in that text as a list of IOC-objects.
 



    ipRegex         = ["IP",        re.compile(r'(([0-9]{1,3}\.){3}[0-9]{1,3})')]
    uriRegex        = ["uri",       re.compile('\\b((http.\\/\\/)?[a-zA-Z0-9]{2,}[\\.](?:' + check("tlds") + ')[\\S]*)\\b', re.I)]
    md5Regex        = ["md5",       re.compile(r'\b(([a-f0-9]{32}\b|\b[A-F0-9]{32}))\b')]
    sha1Regex       = ["sha1",      re.compile(r'\b(([a-f0-9]{40}\b|\b[A-F0-9]{40}))\b')]
    sha256Regex     = ["sha256",    re.compile(r'\b(([0-9a-z]{64}\b|\b[0-9A-Z]{64}))\b')]
    CVERegex        = ["CVE",       re.compile(r'\b((CVE[\-]?[0-9]{4}\-[0-9]{3,6}))\b')]
    emailRegex      = ["email",     re.compile(r'\b(([a-zA-Z0-9\+\_\-]+[@][a-zA-Z0-9\+\_\-]+[.][a-zA-Z]{2,6}))\b')]
    fileRegex       = ["filename",  re.compile('(([a-zA-Z0-9\\.-_])+[\\.](' + check("extensions") + '))\\b', re.I)]



    def __init__(self, text):
        self.text = re.sub(r"\[\.\]",r".", text)
        self.text = re.sub(r'hxxp',r'http',self.text)



    def parse(self):
        iocs = []
        regexes = [self.ipRegex, self.uriRegex, self.md5Regex, self.sha1Regex, self.sha256Regex, self.CVERegex, self.emailRegex, self.fileRegex]
        for i in range(len(regexes)):
            logging.debug("Now scanning for {}s".format(regexes[i][0]))
            rule    = []
            rawRule = regexes[i][1].findall(self.text)

            for x in range(len(rawRule)):
                rule.append(rawRule[x][0])
           
            for j in range(len(rule)):
                iocs.append(IOC(regexes[i][0], rule[j]))
                logging.debug("Adding {} as a {}".format(rule[j], regexes[i][0]))

        for i in range(len(iocs)):           
            logging.debug("IOC-type: {}\t\tIOC-value: {}".format(iocs[i].kind, iocs[i].value))    
        logging.info("Found {} IOCs.".format(len(iocs)))
        return(iocs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IOC-parser extracts Indicators of Compromise (IOC) from a given plaintext source and exports them to a simple .csv-file.")

    parser.add_argument('-s', '--source', metavar='inputfilename',
                        dest='source', action='store', required=True,
                        help='the sourcefile you want to scrape IOCs from.')

    parser.add_argument('-o', '--output', metavar='outputfilename',
                        dest='destination', action='store', required=True,
                        help='the filename you want to save to. something.csv would make the most sense.')

    args = parser.parse_args()
    logging.info("Starting IOCParser.")
    
    f = open(args.source, "r")
    logging.info("opened {} for IOC-parsing.".format(args.source))
    resultsObject = IOCParser(f.read())
    results = resultsObject.parse()
    f.close()    
    logging.info("Read and closed {}.".format(args.source))

    g = open(args.destination, "w")
    logging.info("Opened {} to safe results.".format(args.destination))
    for i in range(len(results)):
        g.write("{},{}\n".format(results[i].kind, results[i].value))
    g.close()
    logging.info("Closed {}.".format(args.destination))
    logging.info("FInishing IOCParser.")
    logging.debug(check("extensions"))





#a = IOCParser(theText)
#print(a.parse())


