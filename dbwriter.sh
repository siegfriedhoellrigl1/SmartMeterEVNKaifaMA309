#!/bin/bash

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

x="$(curl -q localhost 2>/dev/null)"

leistung=$(echo "$x" | grep Leistung | awk '{print $9;}' | cut -d' ' -f1-)
verbraucht=$(echo "$x" | grep Verbraucht | awk '{print $3;}')
eigespeist=$(echo "$x" | grep Eingespeist | awk '{print $2;}')
u_l1=$(echo "$x" | grep ^L1 | awk '{print $3;}' | cut -d 'V' -f1)
u_l2=$(echo "$x" | grep ^L2 | awk '{print $3;}' | cut -d 'V' -f1)
u_l3=$(echo "$x" | grep ^L3 | awk '{print $3;}' | cut -d 'V' -f1)



i_l1=$(echo "$x" | grep ^L1 | awk '{print $4;}' | cut -d 'A' -f1)
i_l2=$(echo "$x" | grep ^L2 | awk '{print $4;}' | cut -d 'A' -f1)
i_l3=$(echo "$x" | grep ^L3 | awk '{print $4;}' | cut -d 'A' -f1)

cosphi=$(echo "$x" | grep cosPhi | awk '{print $3;}')

#echo leistung=$leistung
#echo verbraucht=$verbraucht
#echo eigespeist=$eigespeist
#echo u_l1=$u_l1
#echo u_l2=$u_l2
#echo u_l3=$u_l3



#echo i_l1=$i_l1
#echo i_l2=$i_l2
#echo i_l3=$i_l3

#echo cosphi=$cosphi

echo "INSERT INTO TABELLENNAME (zeit, bezug, einspeisung, leistung, U_L1, U_L2, U_L3, I_L1, I_L2, I_L3, Leistungsfaktor) VALUES (utc_timestamp(), $verbraucht, $eigespeist, $leistung, $u_l1, $u_l2, $u_l3, $i_l1, $i_l2, $i_l3, $cosphi)" | mysql -hHOST -uUSER -pPASSWORT DATENBANKNAME

