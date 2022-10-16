#!/bin/bash
  
Q1="CREATE DATABASE IF NOT EXISTS depenses;"
Q2="GRANT USAGE ON *.* TO myuser@localhost IDENTIFIED BY 'mypass';"
Q3="GRANT ALL PRIVILEGES ON depenses.* TO myuser@localhost;"
Q4="FLUSH PRIVILEGES;"
SQL="${Q1}${Q2}${Q3}${Q4}"
 
  
mysql -uroot -proot -e "$SQL"
