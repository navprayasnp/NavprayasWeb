# NavprayasWeb
Official Website for Navprayas

 ## Contributing

 ### Git
Look up installation instructions [here](https://git-scm.com/downloads)

 - Configure git to use your name and email for all commits:

 `git config user.name "Your Name"`

 `git config user.email "you@domain.com"`

 - Use `--global` flag if you want it to be configured across system.

 ### Configuration

 1. Fork this repo using the `Fork` button near the top. This will create a copy of this repo in your account.
2. Clone the repo from **your** account.
3. Configure local copy to use another remote repo.
    - In the project repo execute: `git remote -v`. This will show a list of urls and remote name. Make sure it's **your** account's url.
    - Add another one: `git remote add upstream https://github.com/navprayasnp/NavprayasWeb.git`. This is the original repo's url. Verify using `git remote -v`. Now, there will two entries.

 ### Submit your changes:
1. Before making any changes, create a new branch: `git branch <branch_name>`. Then move into that branch: `git checkout <branch_name>`. Most of the time these two steps can be combined into one: `git checkout -b <branch_name>`.
2. Commit your changes after done. This is a tow step process: `git add <name1> <name2>`. names can be file names or directory names. Use `.` as name (`git add .`) to add all files/directories. Confirm all files have been added: `git status`. Now, commit: `git commit -m "some message"`.

 If no new files have been created, both steps can be combined: `git commit -am "some message`.
3. Push your changes to github. `git push origin master`
4. Create a pull request from github's ui. This will submit your branch to original owner's repo. He'll merge your changes.

 ### Get updated code:
Recall the `upstream` configuration. That will be used for this step.
1. Checkout master branch: `git checkout master`
2. Pull and merge changes from original repo's owner: `git pull upstream master`. Now you have updated code.

 NOTE: Never make changes in `master` branch. Before making change for the day, get updated code and update your current work in progress with same: Ensure you are in a work-in-progress branch, then, `git rebase master`. This will update your current branch with all upstream changes, and then apply your changes on top of that.

 ## Development setup

 ### VS Code: Recommended Editor

 - Install from [here](https://code.visualstudio.com/)
- Install python extension. [Instructions](https://marketplace.visualstudio.com/itemdetails?itemName=ms-python.python)
- Install [Editorconfig](https://editorconfig.org/) plugin. [Instructions](https://marketplace.visualstudio.com/itemdetails?itemName=EditorConfig.EditorConfig)
- Install django plugin. [Instructions](https://marketplace.visualstudio.com/itemdetails?itemName=batisteo.vscode-django)
- Install toml language plugin. [Instructions](https://marketplace.visualstudio.com/itemdetails?itemName=bungcip.better-toml)
- Install beautifier. [Instructions](https://marketplace.visualstudio.com/itemdetails?itemName=HookyQR.beautify)
- Configuration for VSCode (python specific):
```json
{
    "[python]": {
        "editor.rulers": [
            88
        ]
    },
    "emmet.triggerExpansionOnTab": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "beautify.language": {
        "js": {
            "type": [
                "javascript",
                "json",
                "jsonc"
            ],
            "filename": [
                ".jshintrc",
                ".jsbeautifyrc"
            ]
        },
        "css": [
            "css",
            "less",
            "scss"
        ],
        "html": [
            "htm",
            "html",
            "django-html"   // add this.
        ]
    }
}
 ```

 NOTE: Read about emmet [here](https://emmet.io/). This is an extremely handy tool for every web developer. Highly recommended.

 ### Python 3.7
Look up installation instructions [here](https://www.python.org/downloads/)

 To install Python 3.7 on Linux, you have to build the executable yourself if it is not provided by your systems package manager (which is the case if you use Ubuntu).
Read instruction [here](https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/#installing-python-3-7-on-ubuntu-from-source)

 ### Poetry
Read about Poetry [here](https://poetry.eustace.io/docs/)

 Install the `1.0.0a2` version.

 1. Get the installer.
    - On Unix systems execute: `curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py`
    - On Windows download the installer from: `https://github.com/sdispater/poetry/blob/master/get-poetry.py`

 2. Execute the command: `python get-poetry.py --version 1.0.0a2`

 3. Change configuraiton to create virtualenv in the project's folder (This is recommended).
    `poetry config settings.virtualenvs.in-project true`

 This will make poetry executable available to you. You can now manage an independent dev environment for this project.

 ### Install project dependencies:
Execute `poetry install` in the project's root folder.

 ### Activate virtualenv:
Execute `source .venv/bin/activate` (on unix systems) or `.venv\bin\activate.exe` (on windows). (Look up command for windows if this doesn't work)


 Add your name and email (as configured in git) in `pyprojects.toml` file. You are now ready to work
