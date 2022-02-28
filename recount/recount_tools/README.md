# Birthday-Calendar
[![Raiytak - birthday-calendar](https://img.shields.io/static/v1?label=Raiytak&message=birthday-calendar&color=blueviolet&logo=github)](https://github.com/Raiytak/Birthday-Calendar "Go to GitHub repo")
[![GitHub tag](https://img.shields.io/github/tag/Raiytak/birthday-calendar?include_prereleases=&sort=semver&color=brightgreen)](https://github.com/Raiytak/birthday-calendar/releases/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen)](#license)

Interactive calendar to see and keep track of your family and friends' birthday!

![birthday calendar window](https://github.com/Raiytak/Birthday-Calendar/blob/master/assets/birthday_calendar.png?raw=true)

## Installation

python > 3.8 necessary (see https://www.python.org/downloads/)
```
git clone https://github.com/Raiytak/Birthday-Calendar.git
cd Birthday-Calendar
pip3 install -r requirements.txt
python3 -m birthday_calendar
```

## Save your birthdays!
To save your birthdays, you need a json file containing their info. An example is given below:
```
{
    "minimum": {
        "name": "Name",
        "lastname": "Lastname",
        "birthday": {
            "day": 12,
            "month": 12
        }
    },
    "julie": {
        "name": "Julie",
        "lastname": "Poiriet",
        "birthday": {
            "day": 30,
            "month": "march"
        }
    },
    "helloworld": {
        "name": "Hello",
        "lastname": "World",
        "birthday": {
            "day": 5,
            "month": "juillet",
            "year": 1997
        }
    }
}
```
You can download the example file here:
[birthdays.json](https://github.com/Raiytak/Birthday-Calendar/tree/master/assets/birthdays.json)
Then clic on the "Use File" button and select your file containing your info!

## Add / Remove a birthday
To __add a birthday__, add the information needed on the entries on the right and clic on "Add birthday", the identifier is optional (it is only required to differenciate two people with the same name and lastname).

To __remove a birthday__, you need to put its identifier (the name inside the parenthesis in the label of the birthday) next to the button "Remove", and then clic on it!

## Information
Using tkinter, it generates a calendar view on which you can add and delete birthdays.
You write the person's information (name, lastname, day and month) and it adds it to the list of birthdays.

The month can be an integer (1 - 12) or a name (february).
If the month is in a different language other than the english one, the app uses the googletranslation API to translate it.

A cache is created in the user folder (.birthday_calendar), to keep track of the translation and speed up the execution.

