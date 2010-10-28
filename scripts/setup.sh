#!/bin/bash

SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR
SCRIPT_DIR=$PWD
cd ..
ROOT_DIR=$PWD

echo "0: $0"
echo "SCRIPT_DIR: $SCRIPT_DIR"
echo "ROOT_DIR: $ROOT_DIR"

mkdir $ROOT_DIR/static
mkdir $ROOT_DIR/static/css
mkdir $ROOT_DIR/static/js

cd $SCRIPT_DIR
curl -L -o blueprint.tar.gz http://github.com/joshuaclayton/blueprint-css/tarball/master
tar xvzf blueprint.tar.gz
cd joshuaclayton-blueprint-css*
rm -rf $ROOT_DIR/static/css/blueprint
cp -R blueprint $ROOT_DIR/static/css
cd ..
rm blueprint.tar.gz
rm -rf joshuaclayton-blueprint-css*
#curl -L -o $ROOT_DIR/static/js/jquery.ui.menu.js http://github.com/jquery/jquery-ui/raw/0746f991155df8a833abbe6ac1fbdcf6c73217ec/ui/jquery.ui.menu.js
#curl -L -o $ROOT_DIR/static/css/jquery.ui.menu.css http://github.com/jquery/jquery-ui/raw/menu/themes/base/jquery.ui.menu.css
#curl -L -o $ROOT_DIR/static/css/fg.menu.css http://jquery-ui.googlecode.com/svn/branches/labs/fg-menu/fg.menu.css
#curl -L -o $ROOT_DIR/static/js/fg.menu.js http://jquery-ui.googlecode.com/svn/branches/labs/fg-menu/fg.menu.js
