# Gimothy
Git Identity Manager (GIM) is short for Gimothy. A tool for managing multiple git identities.

## Gimothy makes managing multiple Github identities easy

Lots of Github accounts? Do you need separate ones for work, personal projects or software contracting? Your friend Gimothy is here to help!

Gimothy is lightweight, written in Python and Python is also Gimothy's only dependancy. 

Gimothy is open source and at around 100 lines of Python, Gimothy is very easy to audit! Seriously, go do it! Don't just blindly run code that you find on GitHub!

## Install

Setting Gimothy up is easy! Just copy gim.py to a directory in your $PATH and create a gim.json configuration file in ~/.local/gim/gim.json. See the included gim.example.json for the format of this file.

### 1) Create the Gimothy configuration directory and template

`$mkdir -p ~/.local/gim/gim.json`
`$cp gim.example.json ~/.local/gim/gim.json`

### 2) Edit the configuration

`$[vim/nano/kate/code/editor of your choosing] ~/.local/gim/gim.json`

If you need to generate additional ssh keys (so that you can have one for each account) see this [article in the GitHub docs.](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

### 3) Put Gimothy somewhere in your $PATH

Put gim.py somewhere in your $PATH and make it executable. ~/.local/bin is often a good place. Optionally, also rename gim.py to remove the Python extension:

`$cp gim.py ~/.local/bin/gim`
`$chmod +x ~/.local/bin/gim`

## Running Gimothy

Navigate to the project you want to use Gimothy in and initialize it for use with Gimothy.

`$gim --gim-init`

Now whenever you want to use a git command, simply replace git with gim:

`$gim status`

Initializing a project with Gimothy leaves a .gim file in the project drirectory, so you may wish to add this file to you .gitignore:

`$echo .gim >> .gitignore`