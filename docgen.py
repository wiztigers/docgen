#!/usr/bin/env python

# alternative:
# #!/bin/sh
# """:"
# exec python $0 ${1+"$@"}
# """
# __doc__ = """Program description"""

import argparse
import mimetypes
from os import path
from sys import exit
import subprocess



def createParser():
	parser = argparse.ArgumentParser(description="HTML and PDF documentation generator")
	parser.add_argument('-v', '--verbose', help="verbose mode", action='store_true', default=False)
	parser.add_argument('-i', '--input', help="input file", nargs='?')
	parser.add_argument('-o', '--output',  help="output directory", nargs='?')
	parser.add_argument('-e', '--outdir',  help="output directory", nargs='?', default='doc')
	parser.add_argument('-a', '--html', help="generate html output using asciidoctor. This is the default.", action='store_true')
	parser.add_argument('-p', '--pdf',     help="generate pdf document. If input is a HTML file, wkhtmltopdf will be used. If not, asciidoctor-pdf will be.", action='store_true')
	parser.add_argument('-s', '--stylename', help="SASS stylesheet name", nargs='?')
	parser.add_argument('-d', '--stylesdir',  help="SASS stylesheets folder", nargs='?', default='sass')
	parser.add_argument('-k', '--linkstyle',    help="Link stylesheet in output", action='store_true', default=False)
	parser.add_argument('-m', '--macro', help="path to macro file", nargs='*', action='append', default=[])
	return parser



def isHTML(filename):
	mime = mimetypes.MimeTypes().guess_type(args.input)
	return (mime[0] is not None) and (mime[0].endswith('html'))

def addExtension(filename, suffix):
	res = path.splitext(path.basename(filename))[0]
	if not res.endswith('.'+suffix):
		res += '.'+suffix
	return res

def createHTMLCall(config):
	command = 'asciidoctor '+config.input
	if config.linkstyle:
		command += ' -a linkcss'
	if config.stylename is not None:
		command += ' -a stylesheet="'+config.stylename+'.css"'
	for macros in config.macro:
		for m in macros:
			command += ' -r '+m
	output = config.output
	if output is None:
		output = 'index'
	config.exported_html = path.join(config.outdir, addExtension(output,'html'))
	command += ' -o '+config.exported_html
	return command

def createPDFCall(config):
	command = 'asciidoctor-pdf '+config.input
	output = config.output
	if output is None:
		output = config.input
	config.exported_pdf = path.join(config.outdir, addExtension(output,'pdf'))
	command += ' -o '+config.exported_pdf
	return command

def createHTML2PDFCall(config):
	command = config.wkhtmltopdf_path
	command += '--enable-internal-links'
	command += '--enable-external-links'
	output = config.output
	if output is None:
		output = config.input
	config.exported_pdf = path.join(config.outdir, addExtension(output,'pdf'))
	command += ' '+config.exported_pdf
	return command



def call(command):
	if args.verbose: print('call [html]: '+command)
	try:
		child = subprocess.run(command+' 1>&2', shell=True, stderr=subprocess.PIPE, universal_newlines=True)
		errs = child.stderr
	except AttributeError: # os.python.version < 3.5
		child = subprocess.Popen(command+' 1>&2', shell=True, stderr=subprocess.PIPE, universal_newlines=True)
		outs, errs = child.communicate()
	if args.verbose: print('return code: '+str(child.returncode))
	if child.returncode is not 0:
		print(errs)
	return child.returncode



if __name__ == '__main__':
	parser = createParser()
	args = parser.parse_args()

	if not args.input:
		if args.verbose: print('No input file provided: nothing to do.')
		exit(0)

	html = isHTML(args.input)
	if not (args.html or args.pdf):
		if html:
			args.pdf = True
		else:
			args.html = True
	args.wkhtmltopdf_path = './wkhtmltox/bin/wkhtmltopdf'

	if args.html and not html:
		command = createHTMLCall(args)
		returncode = call(command)
		if returncode is not 0:
			exit(returncode)

	if args.pdf:
		if html:
			command = createHTML2PDFCall(args)
		else:
			command = createPDFCall(args)
		returncode = call(command)
		if returncode is not 0:
			exit(returncode)

