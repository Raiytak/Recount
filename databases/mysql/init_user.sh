#!/bin/bash
  
Q1="SOURCE init.sql;"
Q2="CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypass';"
Q3="GRANT ALL PRIVILEGES ON expenses.* TO myuser@localhost;"
Q4="FLUSH PRIVILEGES;"
SQL=$Q1$Q2$Q3$Q4
 
  
sudo mysql -e "$SQL"
