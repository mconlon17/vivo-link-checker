"""
    link_checker.py: for each web page in VIVO, check the URL to see if
    it responds.  If it does not, add it to a log and generate subtraction
    RDF to remove the web page and its URL from VIVO.

    Version 0.0 MC 2013-11-27
    --  basic framing, find all broken links
    Verrion 0.1 MC 2013-11-28
    --  Works as expected
    Version 0.2 MC 2014-08-13
    --  Improve code formatting, datetime stamping of all output, eror handling,
        passes pylint

"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2013, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.2"

from datetime import datetime
from vivotools import rdf_header
from vivotools import rdf_footer
from vivotools import remove_uri
from vivotools import vivo_sparql_query
import urllib

query = """
SELECT ?uri ?w ?linkuri
WHERE {
  ?uri vivo:webpage ?w .
  ?w vivo:linkURI ?linkuri .
}
"""

status = {}
srdf = rdf_header()
print datetime.now(), "Start"
data = vivo_sparql_query(query)["results"]["bindings"]
print datetime.now(), "Links found = ", len(data)
i = 0
for item in data:
    i = i + 1
    if i % 500 == 0:
        print datetime.now(), i
    uri = item["uri"]["value"]
    weburi = item["w"]["value"]
    linkuri = item["linkuri"]["value"]
    try:
        code = urllib.urlopen(linkuri).getcode()
        if code == None:
            status["None"] = status.get("None", 0) + 1
        else:
            status[str(code)] = status.get(str(code), 0) + 1
    except IOError:
        print datetime.now(), "IOError", None, i, linkuri
        status["IOError"] = status.get("IOError", 0) + 1
        continue
    else:
        print datetime.now(), "Other Exception", None, i, linkuri
        status["Other Exception"] = status.get("Other Exception", 0) + 1
        continue
    if code <= 200 or code == 403 or code == 401:
        continue
    elif code == 404 or code == 410:
        print datetime.now(), "Remove", code, i, linkuri, "from", uri

        # Remove all facts about the web page and all references to
        # the web page

        sub = remove_uri(weburi)
        srdf = srdf + sub
    else:
        print datetime.now(), "Unknown code", code, i, linkuri

#    Print code frequencies

for key in sorted(status.keys()):
    print key, status[key]

#   Write out subtraction RDF

srdf = srdf + rdf_footer()
print srdf

#   All done

print datetime.now(), "Finished"
