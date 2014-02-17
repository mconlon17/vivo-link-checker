# VIVO web link checker

This little python script finds all the URLs for web pages referenced in
your VIVO and checks each one.  The types of errors encountered are
tabulated and for web pages producing 404 (page not found) and 410 (Page 
gone) errors, substration RDF is generated tat can be used to remove these
web pages from your VIVO.  Running the link checker regularly will result
in fewer 404 errors for users of your VIVO.

## Example

The university of Florida VIVO references over 17,000 external web pages.
Many of these are links to the university course catalog -- we link each 
course to a course description in the on-line catalog, and many others
are links to PubMed Central full text versions of papers represented in VIVO.
Additional pages are reference for web sites of organizations and people.

When the link checker was run on UF VIVO on Monday, February 17, 2014, the
following results were obtained:

Links found = 17461
