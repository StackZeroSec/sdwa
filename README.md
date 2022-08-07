# SDWA (Sitting Duck Vulnerable App)
Intentionally vulnerable web app, a starting point to learn the basis of web exploitation.

## Description

SDWA is the simplest vulnerable application, easy to install and easy to exploit.
Here you can be creative and test whatever you learn in your cybersecurity path, the application is strictly related
with the tutorials you can find to [StackZero](https://www.stackzero.net)

![SDWA Homepage](/images/sdwa.jpg)

## Getting Started

### Dependencies
The application needs only python3 and git installed on your OS and very few dependencies

* Flask
* Flask-Session
* Flask-SQLAlchemy

### Installing
The installation is very simple:
* Open your terminal and set your current working directory wherever you want to download the application.
* Clone the git repository by typing
```
git clone https://github.com/StackZeroSec/sdwa.git
```
* Change the directory with
```
cd sdwa
```
* Install all the dependencies with the following command:
```
pip install -r requirements.txt
```
* If you are starting the application for the first time or you want to reset the Database for SQLi:
```
rm db/vuln_db.sqlite
python db/setup_db.py
```
### Writeups
As I said in the description, all the Write-ups are in [StackZero](https://www.stackzero.net) in particular you can find:

* [XSS](https://www.stackzero.net/the-terrifying-world-of-cross-site-scripting-xss-part-2/)
* [Sqli](https://www.stackzero.net/learn-sql-injection-in-practice-by-hacking-vulnerable-application/)
* [Cmdi](https://www.stackzero.net/command-injection/)

### Executing program
Running the application is extremely easy, from the sdwa directory type:
```
flask run
```
Now you just have to open your browser at the address: 127.0.0.1:5000 and the application is ready to be exploited


## License

This project is licensed under the GPL3 License - see the LICENSE.md file for details

