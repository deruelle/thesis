#!/bin/bash

# Yum update
echo "-----------------------"
echo "Yum update"
sudo yum -y update
echo ""

# Get cantiere
echo "-----------------------"
echo "Clone cantiere"
rm -rf cantiere
git clone git://github.com/stormgrind/cantiere.git 
echo ""

# Place specs files
mkdir cantiere/specs
cp specs/* cantiere/specs/

# Place src files
mkdir cantiere/src
cp src/* cantiere/src/

# Build the RPM
cd cantiere/
rake rpm:all

# (Take a coffee!)

# Get back to the root
cd ..

# Create the repos for BoxGrinder
#createrepo cantiere/build/topdir/fedora/14/RPMS/i386
#createrepo cantiere/build/topdir/fedora/14/RPMS/x86_64/
createrepo cantiere/build/topdir/fedora/14/RPMS/noarch/

# Set-up AWS S3
sudo mkdir /root/.boxgrinder/
sudo mv config /root/.boxgrinder/ 

# Build the appliances
echo "-----------------------"
echo "Build the appliances"
sudo bash -c "export LIBGUESTFS_MEMSIZE=300; boxgrinder-build appliances/mobicents-sip-servlets.appl -p ec2 -d ebs --trace"
sudo bash -c "export LIBGUESTFS_MEMSIZE=300; boxgrinder-build appliances/mobicents-load-balancer.appl -p ec2 -d ebs --trace"

echo ""

