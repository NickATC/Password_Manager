# Password Manager
*Version 1.3   May 2019*

Here is a simple, **insecure, not hashed** but effective **Password Manager** built with a nice GUI (?) for a better user experience.  Use this code to learn how to link the database with the GUI.  Database file is full of comments... it was useful for me back then, it may help you!

I wanted to emulate other password managers, like keepass, but security is something I didn´t know how to handle, so I focused my project on learning GUI and database design. Since it was my second project and my second database, I didn´t know how to write proper SQL queries.  I think I have improved a lot since then.

You can create new entries (Title of account, user, password, website and notes).  You can even create a password from withing the manager, and you can open the website from within the manager... remember I wanted to do something like keepass.  You can also edit and delete entries, and you can select the entries that are already in the database to see the saved data.  Remember... this program is for learning porpuses, so security was not in my mind.

The GUI design was very elementary, writing a line of code per widget.  I have implemented OOP since then, but for learning the way I coded it was enough for me.

Comments and critics are welcome: email me (nicolastautiva.nt      at     gmail dot  com )

## Who is this for?
For anyone who wants to see in very simple terms how to make a GUI and how to link it to a database.
**This program is not for personal use...or use it at your own risk.  Remember that there is no security, so anyone can have access to the info in the database.

## Getting Started

1.  Download the repo.
2.  Run *main.py*
3.  On the menu there is a user guide.  Just 4 steps to create more secure passwords.

### Prerequisites

To run the program properly you need Python 3.7+ and you just need to install Pyperclip.

To install:
```
pip install pyperclip
```

You should be ready within seconds!

### Things to fix
There is a lot to fix, and there will be no fixes.  I have decided to move to C#, and the lessons learned with these "small" projects have helped me a lot.

## Authors

* **Nicolás Táutiva** - *Initial work* - [NickATC](https://github.com/NickATC)

## Acknowledgments

* Thanks to PurpleBooth article on how to create a good README [Here](https://gist.githubusercontent.com/PurpleBooth/109311bb0361f32d87a2/raw/824da51d0763e6855c338cc8107b2ff890e7dd43/README-Template.md) 
