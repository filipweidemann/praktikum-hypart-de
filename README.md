HypArt
======


This had to be written in English, because PyCharm does not like German.
Sorry for that.

## Before you begin

## Fork this project
Please fork this project into your private area git(lab|hub) and invite the instructor to
your new forked python exercise project.

### Setting up your python environment
You only have to do this once on your system. This is about installing
python3 AND virtualenvwrapper. This is the preferred setup. You want this.

1. Have Python3.x (at least 3.5) ready. Best to be installed from
with homebrew or macports. Reach out for help if need it.
2. Install virtualenvwrapper via `pip3 install virtualenvwrapper`.
3. Export the path to your python3 binary by adding `export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3` to your `.profile` or `.bashrc`.
4. Don't forget to add `source /usr/local/bin/virtualenvwrapper.sh`
or `source /opt/local/bin/virtualenvwrapper.sh` to your `.profile` or `.bashrc`. **AFTER** the export statement from step 3. (The path depends on your choice to use homebrew or macports)  Again: Ask for help if needed.

### Creating a virtualenv (venv) for this exercise.
We are ready to go. Great. The last thing before starting coding is to create
a virtual environment for our exercise. What's that ?
It is a fresh sandbox in which you can install additional python software. If
you are no longer in need of that sandbox, you just throw it away. If you had
a bad dog in your sandbox: trash it and start anew.

On your console enter this: `mkvirtualenv hypart`

You will have some output like this.
```bash
$ mkvirtualenv hypart
Using base prefix ... bla bla bla... output output...
...
more lines with output.
...
(hypart) $
```
The new virtualenv is created and already activated. You can tell that by seeing the
name of your virtualenv in front of your $ prompt.

To enter your virtualenv the next time you will have to activate it. Open a new
terminal window and enter `lsvirtualenv`. TIP: by pressing the tab key you can
auto-complete your commands. Less typing.

On my system I have already some virtualenvs. My output shows:
```
$ lsvirtualenv
csimon
======
django1.10
==========
miwula
======
hypart
=====
```

To start working in the `hypart` virtualenv enter: `workon hypart` TIP: You can also use the
tab key for completing the name of your virtualenv. If you have multiple virtualenvs you can
press TAB twice to see a liste of your venvs to choose from.

```
$ workon hypart
(hypart) $
```

In our new venv we need a testing software for our exercise. Please install pytest with this
command:
```
pip install pytest
```
This is the way how new python applications or modules are installed into a venv.

Now we are ready to start the exercise.  Quite some work, but only for the first time setup.
Promised :-)

## You are up and running. What do do now:

Continue reading with `Aufgabe.txt`.
