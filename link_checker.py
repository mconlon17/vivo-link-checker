"""
    link_checker.py: for each web page in VIVO, check the URL to see if
    it responds.  If it does not, add it to a log and generate subtraction
    RDF to remove the web page and its URL from VIVO.

    Version 0.0 MC 2013-11-27
    --  basic framing, find all broken links
    Verrion 0.1 MC 2013-11-28
    --  Works as expected

"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"
    
import vivotools as vt
from datetime import datetime
import urllib
import sys

query = """
SELECT ?uri ?w ?linkuri
WHERE {
  ?uri vivo:webpage ?w .
  ?w vivo:linkURI ?linkuri .
}
"""

status = {}
srdf = vt.rdf_header()
print datetime.now()
data = vt.vivo_sparql_query(query)["results"]["bindings"]
print "Links found = ",len(data)
i = 0
for item in data:
    i = i + 1
    if i % 500 == 0:
        print i
    uri = item["uri"]["value"]
    weburi = item["w"]["value"]
    linkuri = item["linkuri"]["value"]
    try:
        code = urllib.urlopen(linkuri).getcode()
        if code == None:
            status["None"] = status.get("None",0) + 1
        else:
            status[str(code)] = status.get(str(code),0) + 1
    except:
        print "No code",None,i,linkuri
        status["Exception"] = status.get("Exception",0) + 1
        continue
    if code == 200:
        continue
    elif code == 404 or code == 410:
        print "Remove",code,i,linkuri,"from",uri

        # Remove all facts about the web page and all references to
        # the web page
        
        sub = vt.remove_uri(weburi)
        srdf = srdf + sub
    else:
        print "Unknown code",code,i,linkuri
srdf = srdf + vt.rdf_footer()
print datetime.now()
for key in sorted(status.keys()):
    print key,status[key]
print srdf
