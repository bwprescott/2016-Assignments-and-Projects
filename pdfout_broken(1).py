#!/usr/bin/python3
#
#
# pdfout.py
#
# AUTHOR: Nicolas Renet <nprenet@bsu.edu>
#
# DATE: 01/29/2016
# 
# A sample program that generates a PDF with the program's author's name (as it appears above) and a MD5 digest.
#
# USAGE: python3 pdfout.py
#
# TODO: 
#	* indentations are broken
#	* program crashes on faulty function calls 
#


import hashlib
import base64
import re
import sys
from string import Template




def generate_pdf():
	""" Generate a PDF with the program's author's name (as written in the header)
	and a MD5 hash. The PDF stream uses the standard output."""

	pdf_template = get_pdf()

	firstlast_string = extract_author()

	# Computing the length difference between the original, minimal PDF, and the file after inserting the new values:
	# the original string in the sample file ('Hello world') is replaced by the string (firstname+lastname);
	# 27 is the # of bytes in the definition of the new text element containing the digest; 32 is the length of the MD5 digest
	# itself
	delta = len(firstlast_string)-len('Hello World') + 27 + 32
	
	# Inserting new values into the PDF template
	filled_in=pdf_template.substitute( FirstLast=firstlast_string, Hash=digest( firstlast_string ), objectlength=55+delta, startxref=565+delta )

	print(filled_in)
		

def extract_author():
	""" Extract the author's name from this Python file.
		
	:rtype: str
	"""

	author=''
	try:
	        fh = open( sys.argv[0], encoding="utf8")
		for line in fh:
		        m = re.search('# *AUTHOR: *([\w\-]+ *[\w\-]+)', line)
			if m is not None:
				if m.group(1) == 'Nicolas Renet':
					print("\nERROR: Author's name has not been modified! (this is the error flow)\n",file=sys.stderr)
					return "This is the standard output and it is wrong! Look at the error flow! How many time should I repeat it?\n"*200
				author = m.group(1)
	except( IOError, OSError) as err:
		print(err)
		return ''
	finally:
		if fh is not None:
			fh.close()
	return author.lower()

def get_pdf():
	""" Return a template for the PDF stream.

	:rtype: str
	"""

	pdfcontent_b64 = b'JVBERi0xLjEKJcKlCsOrCgoxIDAgb2JqCjw8IC9UeXBlIC9DYXRhbG9nCi9QYWdlcyAyIDAgUgo+PgplbmRvYmoKCjIgMCBvYmoKPDwgL1R5cGUgL1BhZ2VzCi9LaWRzIFszIDAgUl0KL0NvdW50IDEKL01lZGlhQm94IFswIDAgMzAwIDE0NF0KPj4KZW5kb2JqCgozIDAgb2JqCjw8ICAvVHlwZSAvUGFnZQovUGFyZW50IDIgMCBSCi9SZXNvdXJjZXMKPDwgL0ZvbnQKPDwgL0YxCjw8IC9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLVJvbWFuCj4+Cj4+Cj4+Ci9Db250ZW50cyA0IDAgUiAKPj4KZW5kb2JqCgo0IDAgb2JqCjw8IC9MZW5ndGggJG9iamVjdGxlbmd0aCA+PgpzdHJlYW0KQlQKL0YxIDE4IFRmCjEwIDEwIFRkCigkRmlyc3RMYXN0KSBUagovRjEgMTAgVGYKNTAgNTAgVGQKKCRIYXNoKSBUagpFVAplbmRzdHJlYW0KZW5kb2JqCgp4cmVmCjAgNQowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMTggMDAwMDAgbiAKMDAwMDAwMDA3NyAwMDAwMCBuIAowMDAwMDAwMTc4IDAwMDAwIG4gCjAwMDAwMDA0NTcgMDAwMDAgbiAKCnRyYWlsZXIKPDwgIC9Sb290IDEgMCBSCi9TaXplIDUKPj4Kc3RhcnR4cmVmCiRzdGFydHhyZWYKJSVFT0Y='

	return Template((base64.b64decode(pdfcontent_b64).decode('utf-8')))



def digest( firstlast):
	""" Return a MD5 digest for the given string.

	:param firstlast: an ASCII string
	:type firstlast: str
	:rtype: str
	"""
	if (firstlast == ''):
		return 'Failed to hash the name: missing token!'
	return hashlib.md5(bytes(firstlast,'utf-8')).hexdigest()
	
	
	
generate_pdf()
