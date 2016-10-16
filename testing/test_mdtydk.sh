#!/bin/bash

#script name: test_mdtydk.sh
#purpose: test MDT YDK API. 
#author: Yifeng Shen
#version: 1.0
#Create date:  2016-10-15
#Change history:

SCRIPTNAME="test_mdtydk.sh"
AWK="/usr/bin/awk"
DATE="/bin/date"
WC="/usr/bin/wc"
SORT="/usr/bin/sort"
UNIQ="/usr/bin/uniq"
GREP="/usr/bin/grep"
TEE="/usr/bin/tee"
PRINTF="/usr/bin/printf"

exitcode=0

timestamp=`$DATE '+%b%e %T' | $AWK -F '[: ]' '{print $1"-"$2"-"$3"-"$4}'`
TMPLOG="/tmp/tmplog"
goodcount=0
badcount=0
cat /dev/null > $TMPLOG

TESTPROFILE="./testprofile.txt"
MAINPGORAM=""
TESTNUMBER=""
INTERVAL=2
SINGLESENSOR=""
MULTIPLESENSOR=""
ROUTERIP=""
ACCESSPORT=""
USRNAME=""
PASSWD=""
ADDFAMILY=""
DESTGNAME=""
DESTGFREIX=""
SENSORPREFIX=""
DETINATIONLST=""
RMTPORT=""
LOG=""

function throwerror
{
	errorcode=$1
	MESSAGE=""
	case $errorcode in
	1)
	 MESSAGE="Error $errorcode: API client program does not exist"
	;;
	2)
	 MESSAGE="Error $errorcode: missing test number"
	;;
	3)
	 MESSAGE="Error $errorcode: missing test interval"
	;;
	4)
	 MESSAGE="Error $errorcode: missing senor path (single)"
	;;
	5)
	 MESSAGE="Error $errorcode: missing sensor path (multiple)"
	;;
	esac
	
	echo $MESSAGE
	exit $errorcode
}

function getvalues
{
	returncode=0
	
	
	return $returncode
}

getvalues
returncode=$?
if [[ $returncode > 0 ]]
  then
   throwerror $returncode
fi
