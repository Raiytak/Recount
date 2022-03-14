# Recount
[![Raiytak - recount](https://img.shields.io/static/v1?label=Raiytak&message=recount&color=blueviolet&logo=github)](https://github.com/Raiytak/Recount "Go to GitHub repo")
[![GitHub tag](https://img.shields.io/github/v/tag/Raiytak/Recount?include_prereleases=&sort=semver&color=blue)](https://github.com/Raiytak/Recount/tree/v0.1)
[![License](https://img.shields.io/badge/License-MIT-brightgreen)](#license)

Display your expenses on interactive dashboards!

![Screenshot from 2022-03-14 15-22-52](https://user-images.githubusercontent.com/52044172/158192160-43978b88-1006-40e4-8e1f-f11e18360bf8.png) 


# Presentation
The application uses python3, MySQL and dash. It should have an online version soon, open only for selected people ;) \
But you can also make it run on your personal laptop!

https://user-images.githubusercontent.com/52044172/158196182-bd84b827-b002-4b7b-82ec-3476df44510c.mp4


# Installation

## Install necessary tools
python => 3.8 necessary (see https://www.python.org/downloads/) \
A mysql db is needed by the application. See https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/ for installation (a docker should be released for that aspect soon).

## MySQL Configuration
Upload the `init.sql` file present in [database](https://github.com/Raiytak/Recount/blob/master/database/init.sql) into mysql:
```
mysql -u USER -p recount < PATH/TO/FILE/init.sql
```
Add a user `myuser` and grant him access to this new database:
```
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypass';
GRANT ALL PRIVILEGES ON database_name.table_name TO 'newuser'@'localhost';
FLUSH PRIVILEGES;
```
The user should match the description of the one defined in [default_configs.json](https://github.com/Raiytak/Recount/blob/sanity-cleaning-core/recount/config/default_configs.json)


## App installation
```
git clone https://github.com/Raiytak/Recount.git
cd Recount
pip install recount/
python -m birthday_calendar
```



