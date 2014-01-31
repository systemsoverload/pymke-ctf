# Level 0
## The backstory
Our enterprising young intern has looked around at the various authentication plugins for Flask and has deemed them all unworthy! His vastly superior solution is bound to be completely bullet-proof, if it weren't, Contoso Corp. would be at risk of losing their admin's super secret code.


## The challenge
This is a gray-box challenge, you have access to a COPY of the code running on a remote server somewhere, but not the DATA that is contained within. The copy of the application that may be cloned from here has some stub data to get you started. There is the assumption that you have valid login credentials for the remote server and that the admin is currently logged in.

Your mission, should you choose to accept it, is to login as a non-admin account and somehow get the web server to divulge the secret code to you.


## Installation
- git clone

- cd (cloned repo)

- mkdir env
- virtualenv env
- source env/bin/activate

- pip install -r requirements.txt
- python level00.py
