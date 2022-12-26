# Recount
[![Raiytak - recount](https://img.shields.io/static/v1?label=Raiytak&message=recount&color=blueviolet&logo=github)](https://github.com/Raiytak/Recount "Go to GitHub repo")
[![GitHub tag](https://img.shields.io/github/v/tag/Raiytak/Recount?include_prereleases=&sort=semver&color=blue)](https://github.com/Raiytak/Recount/tree/v0.1)
[![License](https://img.shields.io/badge/License-MIT-brightgreen)](#license)

## Display your expenses on interactive dashboards!

![Screenshot from 2022-03-14 15-22-52](https://user-images.githubusercontent.com/52044172/158192160-43978b88-1006-40e4-8e1f-f11e18360bf8.png) 


# Presentation
The application should have an online version soon, open only for selected people ;) \
But you can also make it run on your personal laptop!


https://user-images.githubusercontent.com/52044172/158196182-bd84b827-b002-4b7b-82ec-3476df44510c.mp4



# Languages and tools
<div>
  <a href="https://www.python.org/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" title="Python" alt="Python" width="40" height="40"/>
  <a/>&nbsp;
  <a href="https://dash.plotly.com/">
    <img src="https://images.plot.ly/logo/new-branding/plotly-logomark.png" title="Dash" alt="Dash" width="40" height="40"/>
  <a/>&nbsp;
  <a href="https://reactjs.org/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/react/react-original-wordmark.svg" title="React" alt="React" width="40"/>
  <a/>&nbsp;
  <a href="https://www.mysql.com/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/mysql/mysql-original-wordmark.svg" title="MySQL"  alt="MySQL" width="50" height="50"/>
  <a/>&nbsp;
  <a href="https://git-scm.com/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/git/git-original.svg" title="Git" alt="Git" width="40" height="40"/>
  <a/>&nbsp;  
  <img src="https://github.com/devicons/devicon/blob/master/icons/css3/css3-plain-wordmark.svg"  title="CSS3" alt="CSS" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/html5/html5-original.svg" title="HTML5" alt="HTML" width="40"/>
</div>

# Installation

## Install necessary tools
python => 3.7 necessary (see https://www.python.org/downloads/) \
A mysql db is needed by the application. See https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/ for installation (a docker should be released for that aspect soon).


## App installation
```
git clone https://github.com/Raiytak/Recount.git
cd Recount
pip install -r recount/requirements.txt
```

After that, we will create and instanciate the necessary folders and files:
```
python -m recount.src.accessors --initiate-folders
```
You should check on your home folder (~ for Linux), a `.recount` folder should have been created. It is this file that the app will use.
You should modify the default password in `.recount/config/sql.config` to ensure some security.
You can also configure it while launching the application by providing information to the script. See `python -m recount -h` for that.


## MySQL Configuration
Upload the `init.sql` file present in [database](https://github.com/Raiytak/Recount/blob/master/database/init.sql) into mysql:
```
mysql -u root -p recount < databases/mysql/init.sql
```
This will create the necessary database and tables. You have to use the ROOT of your MySQL for this process.


Add a user and grant him access to this new database.
Its information have to match the one written in `.recount/config/sql.config`.
```
CREATE USER 'recount_admin'@'localhost' IDENTIFIED BY 'mypass';
GRANT ALL PRIVILEGES ON recount.* TO 'recount_admin'@'localhost';
FLUSH PRIVILEGES;
```
The name and password used SHOULD BE DIFFERENT from the default ones.

To ensure that the configuration is working, you can do `python -m recount.src.database --test`


## App configuration
To configure the database credentials and values used by Recount, you can set them via 2 possibilities:
-1: via command line
```
python -m recount --dbname recount-1 --dbuser recount-administrator
```
-2: by editing manually the config file, which is located at `~/.recount/config/sql.config`


## App launch
```
python -m recount --launch
```
Once running, you can access it through your browser by typing `localhost:8050`

Other option: Run with Gunicorn
`python -m gunicorn 'recount.app:createRecountServer()'`
