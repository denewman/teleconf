#!/bin/bash

#script name: test_pdt.sh
#purpose: test PDT API. 
#author: Yifeng Shen
#version: 1.0
#Create date:  2016-10-15
#Change history:

SCRIPTNAME="test_pdt.sh"
AWK="/usr/bin/awk"
DATE="/bin/date"
WC="/usr/bin/wc"
SORT="/usr/bin/sort"
UNIQ="/usr/bin/uniq"
HEAD="/usr/bin/head"
GREP="/bin/grep"
TEE="/usr/bin/tee"
PRINTF="/usr/bin/printf"
SLEEP="/bin/sleep"

exitcode=0

timestamp=`$DATE '+%b%e %T' | $AWK -F '[: ]' '{print $1"-"$2"-"$3"-"$4}'`
TMPLOG="/tmp/tmplog"
goodcount=0
badcount=0
cat /dev/null > $TMPLOG

TESTPROFILE="./testprofile.txt"
MAINPGORAM=""
TESTNUMBER=""
INTERVAL=""
#MDTSINGLEPATH=""
#MDTMULTIPATH=""
PDTSINGLEPATH=""
PDTMULTIPATH=""
POLICYGROUPPREFIX=""
POLICYPREFIX=""
POLICYVERSION=""
POLICYPOLLINTERVAL=""
POLICYDSTIP=""
PDTCOMMENT=""
PDTIDENT=""
PDTDES=""

ROUTERIP=""
ACCESSPORT=""
USRNAME=""
PASSWD=""
ADDFAMILY=""
#DESTGNAME=""
#DESTGPREFIX=""
#SENSORPREFIX=""
#SUBSCIPTPREFIX=""
#DETINATIONLST=""
#DENCODER=""
#DPROTOCOL=""
RMTPORT=""
LOG=""
PYTHON=""
#POLLINGINTERVAL=""
SUBID=""

function usage
{
   echo "
  Usage:  ./$SCRIPTNAME {-f <test profile>}

  Options:  

           -f: full path of testing profile, default is ./testprofile.txt
		   		   
	   -h: print script usage

  Examples:
	   ##default mode, all test parameters are saved in file ./testprofile.txt ##
	   ./$SCRIPTNAME
	   
           ##assume all the test parameters are saved in file /data/testprofile ##   
	   ./$SCRIPTNAME -f /data/testprofile 
   
   "
	
}
function throwerror
{
	errorcode=$1
	MESSAGE=""
	case $errorcode in
	1)
	 MESSAGE="Error $errorcode: missing API client program"
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
	6)
	 MESSAGE="Error $errorcode: missing router ip address"
	;;
	7)
	 MESSAGE="Error $errorcode: missing user name of router"
	;;
	8)
	 MESSAGE="Error $errorcode: missing password of router"
	;;
	9)
	 MESSAGE="Error $errorcode: missing SSH/Netconf port value"
	;;
	10)
	 MESSAGE="Error $errorcode: missing policy name prefix"
	;;
	11)
	 MESSAGE="Error $errorcode: missing policy group prefix"
	;;
	12)
	 MESSAGE="Error $errorcode: missing PDT destination ip address"
	;;
	13)
	 MESSAGE="Error $errorcode: missing destination group remote port"
	;;
	14)
	 MESSAGE="Error $errorcode: missing destination group encoding schema"
	;;
	15)
	 MESSAGE="Error $errorcode: missing destination group protocol value"
	;;
	16)
	 MESSAGE="Error $errorcode: missing address family information"
	;;
	17)
	 MESSAGE="Error $errorcode: missing script log file information"
	;;
	18)
	 MESSAGE="Error $errorcode: missing testing profile"
	;;
	19)
	 MESSAGE="Error $errorcode: unable to clean old configurations"
	;;
	20)
	 MESSAGE="Error $errorcode: missing python path"
	;;
	21)
	 MESSAGE="Error $errorcode: missing subscription prefix"
	;;
	22)
	 MESSAGE="Error $errorcode: missing telemetry polling interval"
	;;
	23)
	 MESSAGE="Error $errorcode: missing start subscription id"
	;;
	esac
	
	echo $MESSAGE
	exit $errorcode
}

function getvalues
{
	returncode=0
	
	##find the main API client programm##
	KEYWD="PDT_SSH"
	MAINPGORAM=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$MAINPGORAM" -o ! -f $MAINPGORAM ] 
	  then
	    returncode=1
		throwerror $returncode
	fi
	
	##find number of testings##
	KEYWD="TESTNUMBER"
	TESTNUMBER=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$TESTNUMBER" ] 
	  then
	    returncode=2
		throwerror $returncode
	fi
	
	##find testing interval##
	KEYWD="INTERVAL"
	INTERVAL=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$INTERVAL" ] 
	  then
	    returncode=3
		throwerror $returncode
	fi
	
	##find single sensor path for PDT##
	KEYWD="PDTSINGLEPATH"
	PDTSINGLEPATH=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$PDTSINGLEPATH" ] 
	  then
	    returncode=4
		throwerror $returncode
	fi
	
	##find multiple sensor paths for PDT##
	KEYWD="PDTMULTIPATH"
	PDTMULTIPATH=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$PDTMULTIPATH" ] 
	  then
	    returncode=5
		throwerror $returncode
	fi
	
	##find ip address of the router##
	KEYWD="ROUTERIP"
	ROUTERIP=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$ROUTERIP" ] 
	  then
	    returncode=6
		throwerror $returncode
	fi
	
	##find user name of the router##
	KEYWD="USRNAME"
	USRNAME=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$USRNAME" ] 
	  then
	    returncode=7
		throwerror $returncode
	fi
	
	##find password of the router##
	KEYWD="PASSWD"
	PASSWD=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$PASSWD" ] 
	  then
	    returncode=8
		throwerror $returncode
	fi
	
	##find access port of the router##
	KEYWD="SSHPORT"
	ACCESSPORT=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$ACCESSPORT" ] 
	  then
	    returncode=9
		throwerror $returncode
	fi
	
	##find prefix of policy name##
	KEYWD="POLICYPREFIX"
	POLICYPREFIX=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$POLICYPREFIX" ] 
	  then
	    returncode=10
		throwerror $returncode
	fi
	
	##find prefix of policy group name##
	KEYWD="POLICYGROUPPREFIX"
	POLICYGROUPPREFIX=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$POLICYGROUPPREFIX" ] 
	  then
	    returncode=11
		throwerror $returncode
	fi
	
	##find destination ip address##
	KEYWD="POLICYDSTIP"
	POLICYDSTIP=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$POLICYDSTIP" ] 
	  then
	    returncode=12
		throwerror $returncode
	fi
	
	##find remote port of destination group##
	KEYWD="RMTPORT"
	RMTPORT=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$RMTPORT" ] 
	  then
	    RMTPORT=2103
	fi
	
	##find PDT comment##
	KEYWD="PDTCOMMENT"
	PDTCOMMENT=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	
	##find PDT indentifier##
	KEYWD="PDTIDENT"
	PDTIDENT=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	
	##find protocol value under destination group##
	KEYWD="ADDFAMILY"
	ADDFAMILY=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$ADDFAMILY" ] 
	  then
	    returncode=16
		throwerror $returncode
	fi
	
	##find script log file##
	KEYWD="LOG"
	LOG=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$LOG" ] 
	  then
	    returncode=17
		throwerror $returncode
	fi
	
	##find python path##
	KEYWD="PYTHON"
	PYTHON=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$PYTHON" -o ! -f $PYTHON ] 
	  then
	    returncode=20
		throwerror $returncode
	fi
	
	##find PDT description##
	KEYWD="PDTDES"
	PDTDES=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	
	##find polling interval for telemetry ##
	KEYWD="POLICYPOLLINTERVAL"
	POLICYPOLLINTERVAL=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$POLICYPOLLINTERVAL" ] 
	  then
	    returncode=22
		throwerror $returncode
	fi
	
	##find policy version##
	KEYWD="POLICYVERSION"
	POLICYVERSION=`$GREP $KEYWD $TESTPROFILE | $HEAD -1 | $AWK '{print $NF}'`
	if [ ! -n "$POLICYVERSION" ] 
	  then
	    POLICYVERSION=1
	fi
	
	return $returncode
}

function printresult
{
	executedtest=$1
	passedtest=$2
	failedtest=$3
	
	timestamp=`$DATE '+%b%e %T' | $AWK -F '[: ]' '{print $1"-"$2"-"$3"-"$4}'`
	echo "$timestamp [$SCRIPTNAME] Summary: Total tests executed: $executedtest,\
 Passed: $passedtest, Failed: $failedtest" | $TEE -a $LOG

}

while getopts f:h: option
  do
    case $option in
    f)
	TESTPROFILE=$OPTARG
    ;;
    h)
    ;;
    esac	
  done
  
if [[ $1 == "-h" ]]
  then
    usage
	exit $exitcode
fi
##make sure the testing profile does exist##
if [ ! -f $TESTPROFILE ]
  then
	returncode = 18
	throwerror $returncode
fi
getvalues
returncode=$?
if [[ $returncode > 0 ]]
  then
   throwerror $returncode
fi

i=0

##remove the original configurations##
testreulst="NA"
timestamp=`$DATE '+%b%e %T' | $AWK -F '[: ]' '{print $1"-"$2"-"$3"-"$4}'`
echo "$timestamp [$SCRIPTNAME] removing old configure on $ROUTERIP started......" | $TEE -a $LOG
$PYTHON $MAINPGORAM --c=deletePDT --n=$ROUTERIP --u=$USRNAME --p=$PASSWD --pn=anything \
--pp=anything --dst=$POLICYDSTIP --pg=anything --rp=$ACCESSPORT --m=ssh --pv=$POLICYVERSION \
--pd=$PDTDES --pi=$PDTIDENT --pe=$POLICYPOLLINTERVAL --af=$ADDFAMILY --pc=$PDTCOMMENT \
--dp=$RMTPORT > $TMPLOG

timestamp=`$DATE '+%b%e %T' | $AWK -F '[: ]' '{print $1"-"$2"-"$3"-"$4}'`
if grep "Operation success" $TMPLOG 2>&1 > /dev/null
  then
    testresult="sucess!"
  else
	testresult="fail!"
fi
cat $TMPLOG >> $LOG
echo "$timestamp [$SCRIPTNAME] removing old configure on $ROUTERIP: $testresult" | $TEE -a $LOG
while [ $i -lt $TESTNUMBER ]
 do
  cat /dev/null > $TMPLOG
  testresult="NA"
  timestamp=`$DATE '+%b%e %T' | $AWK -F '[: ]' '{print $1"-"$2"-"$3"-"$4}'`
  i=`expr $i + 1`
  echo "$timestamp [$SCRIPTNAME] test ($i/$TESTNUMBER) started......" | $TEE -a $LOG
  POLICYNAME="$POLICYPREFIX$i"
  POLICYGROUPNAME="$POLICYGROUPPREFIX$i"
  if [[ $((i%2)) == 1 ]]
	then
	  SENSORPATH=$PDTSINGLEPATH
	else
	  SENSORPATH=$PDTMULTIPATH
  fi

 $PYTHON $MAINPGORAM --c=push --n=$ROUTERIP --u=$USRNAME --p=$PASSWD --pn=$POLICYNAME \
--pp="$SENSORPATH" --dst=$POLICYDSTIP --pg=$POLICYGROUPNAME --rp=$ACCESSPORT --m=ssh \
--pv=$POLICYVERSION --pd=$PDTDES --pi=$PDTIDENT --pe=$POLICYPOLLINTERVAL --af=$ADDFAMILY \
--pc=$PDTCOMMENT --dp=$RMTPORT > $TMPLOG 
 
  if grep "Operation success" $TMPLOG 2>&1 > /dev/null
    then
      testresult="pass"
	  goodcount=`expr $goodcount + 1`
    else
	  testresult="fail"
	  badcount=`expr $badcount + 1`
  fi 
  cat $TMPLOG >> $LOG
  timestamp=`$DATE '+%b%e %T' | $AWK -F '[: ]' '{print $1"-"$2"-"$3"-"$4}'`
  echo "$timestamp [$SCRIPTNAME] test ($i/$TESTNUMBER) completed. Result: $testresult" | $TEE -a $LOG
  $SLEEP $INTERVAL  
 done
 
 printresult $i $goodcount $badcount
 echo "script completed, all details are saved in $LOG"
