#!/bin/bash

factorydir="asciidoctor-stylesheet-factory"
stylesdir=$1

# asciidoctor & dependencies
gem install prawn -v 2.1.0
gem install asciidoctor # HTML generation
gem install asciidoctor-pdf --pre # PDF generation

# stylesheet factory
gem install compass zurb-foundation # CSS stylesheets generation
git clone https://github.com/asciidoctor/asciidoctor-stylesheet-factory.git ${factorydir}
# generate all CSS stylesheets
cp -R ${stylesdir} ${factorydir}/
cd ${factorydir} && compass compile && cd ..

# get the latest version of wkhtmltopdf and untar it
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
tar xf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
