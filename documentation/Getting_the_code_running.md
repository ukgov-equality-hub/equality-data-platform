
[Equality Data Platform](../README.md) >
[Developer documentation](README.md) >
Getting the code running

# Getting the code running

Get the code:
* Clone this repo  
  If you're cloning with SSH / GitKraken, you want this link:  
  `git@github.com:cabinetoffice/equality-data-platform.git`

* Open the Folder in your IDE  
  Note: in Python, you don't need to open a "Solution" file (like you would in C#)

Get and edit the config files:
* Ask an existing developer for a copy of the files listed below and
  save them to the `equality-data-website` folder of your local repository
  (the files are git ignored, so they shouldn't get committed - **check this!**)
  * `.env`

Fetch the project dependencies:
* Open a Bash terminal in the folder `equality-data-website`

* Run `pip install -r requirements.txt`  
  This installs the Python dependencies

* Run `npm install`  
  This installs the Javascript dependencies

Build the CSS and JS:
* Open a Bash terminal in the `equality-data-website` folder

* Run `npm run build` to build the CSS and JS **once**

* Alternatively, run `npm run watch` to re-compile whenever you change your CSS and JS files

Build and run the website:
* Open a Bash terminal in the `equality-data-website` folder

* Run `./run_local.sh`

* The website should be visible at http://localhost:5000/  
