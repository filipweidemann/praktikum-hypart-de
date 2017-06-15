HypArt
======


Re-Implementation of the original HypArt.de using Python/Flask.


### 'Version-ing'
This app was written using Python 2.7.

### Modules and setting up your database
Here are some prerequisites if you actually decide to run/modify the app on your machine:

1. Get Python (obviously), using Homebrew or something else (just my personal preference).
`brew install python` - disclaimer: the command `python` will point to your Python 2.x installation,
while `python3` points to the Python 3.x installation. 
2. Get the Python framework 'Flask' - `pip install flask`.
3. Get 'WTForms' - `pip install wtforms`.
4. (technically, the following steps are optional) Get an SQL module; to get compatibility outta the box, use `pymysql` - it's what I used and you won't need to modify the code if you just use it as well.
5. Clone my database structure using the `hypart.sql` file which can be found in the main directory of this repo.
6. Configure your server to run at port `8889` - usually this should be default, but.. you know..

## How to launch this rocket
So, you're down to get this app started? 
Go ahead and `cd` into the `hypart/document_root` directory and cast a simple `python app.py` to your bash.
Done. The app is running locally on your machine.

To view the site, go to `localhost:5000/main`, `localhost:5000/main.sh` or `localhost:5000` - you'll get redirected,
but the actual landing page is at `/main` by default. If you didn't change anything and got a `root` database user, you should be good.

Oh, the debugger should be active, so if anything goes wrong you get the detailed error page to see what went wrong.

