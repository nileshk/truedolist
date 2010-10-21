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

cd $SCRIPT_DIR
curl -L -o blueprint.tar.gz http://github.com/joshuaclayton/blueprint-css/tarball/master
tar xvzf blueprint.tar.gz
cd joshuaclayton-blueprint-css*
rm -rf $ROOT_DIR/static/css/blueprint
cp -R blueprint $ROOT_DIR/static/css
cd ..
rm blueprint.tar.gz
rm -rf joshuaclayton-blueprint-css*
