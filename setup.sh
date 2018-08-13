#!/bin/bash

factorydir="asciidoctor-stylesheet-factory"
stylesdir=$1
stylename=$2
[ -z ${stylename} ] && exit 0
[ -z ${stylesdir} ] && stylesdir=sass
[ -d ${stylesdir} ] || mkdir ${stylesdir}

# get stylesheet factory
[[ -d ${factorydir} ]] || git clone https://github.com/asciidoctor/asciidoctor-stylesheet-factory.git ${factorydir}
# generate CSS stylesheet
cp -R ${stylesdir} ${factorydir}/
cd ${factorydir} && compass compile ${stylesdir}/${stylename}.scss && cd ..
cp ${factorydir}/stylesheets/${stylename}.css ${stylesdir}/${stylename}.css

