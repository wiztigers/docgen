#!/bin/bash

factorydir="asciidoctor-stylesheet-factory"
stylesdir=$1
stylename=$2
[ -z ${stylename} ] && exit 0
[ -z ${stylesdir} ] && stylesdir=sass
[ -d ${stylesdir} ] || mkdir ${stylesdir}

# asciidoctor & dependencies
gem install prawn -v 2.1.0
gem install asciidoctor # HTML generation
gem install asciidoctor-pdf --pre # PDF generation

# get stylesheet factory
gem install compass zurb-foundation # CSS stylesheets generation
[[ -d ${factorydir} ]] || git clone https://github.com/asciidoctor/asciidoctor-stylesheet-factory.git ${factorydir}
# generate CSS stylesheet
cp -R ${stylesdir} ${factorydir}/
cd ${factorydir}
shift
for stylename; do
  compass compile ${stylesdir}/${stylename}.scss
  cp stylesheets/${stylename}.css ../${stylesdir}/${stylename}.css
done
cd ..

# get the latest version of wkhtmltopdf and untar it
[[ -e wkhtmltox-0.12.4_linux-generic-amd64.tar.xz ]] || wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
tar xf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
