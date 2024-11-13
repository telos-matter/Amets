# Amets &nbsp; ![DEVELOPMENT STATUS: finished](https://badgen.net/badge/DEVELOPMENT%20STATUS/finished/green)

During my 3rd semester in 2021/2022, we were tasked with
creating a website using Django that would help users learn
German. We took the idea a bit further and added a reddit / stackoverflow
like feature where users could ask questions and answer them and
share news and talk about them. All with a voting, replies and ranking system.

Here is a Youtube video showcasing the website:

[![Amets youtube showcase video](https://img.youtube.com/vi/HFxtubhgUoE/1.jpg)](https://www.youtube.com/watch?v=HFxtubhgUoE)

## How to run the project:
If you want to run the project locally, you can do so by following these steps:

1. Clone the repository
```console
$ git clone https://github.com/telos-matter/Amets.git
```

2. Make sure you have Django 4.0.3 or higher installed. You can check trough this command:
```console
$ python -m django --version
```
If you don't have Django installed, you can follow this official [tutorial](https://docs.djangoproject.com/en/5.1/intro/) which will guide you trough the installation and also happens to be a really good tutorial for Django basics as well. (I highly recommend it, it's how I learned Django.)

3. Navigate to the project folder and run the server
```console
$ cd Amets
$ python manage.py runserver
```
And that's that. The provided SQLite database should give you enough content to play around with the website.
