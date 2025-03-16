# Evaluation App Setup Guide for macOS

This guide will help you set up and run the Evaluation App on your Mac, even if you have no technical background. Just follow these steps in order.

## 1. Install Visual Studio Code

VS Code is a free editor we'll use to view and run the code:

1. Go to [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Click the big blue "Download Mac Universal" button
3. Once downloaded, open the downloaded file (it should be in your Downloads folder)
4. Drag the VS Code icon to the Applications folder when prompted
5. Go to your Applications folder and double-click Visual Studio Code to open it
6. If you get a security warning saying "macOS cannot verify the developer", click "Open" (you may need to right-click and select "Open" the first time)

## 2. Install Python

Our app needs Python to run:

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click the big "Download Python 3.x.x" button (the exact version number doesn't matter as long as it's Python 3)
3. Once downloaded, open the installer file
4. Follow the installation wizard, keeping all default options
5. Make sure the "Add Python to PATH" checkbox is selected before clicking "Install Now"

## 3. Install Git

Git is needed to download the project from GitHub:

1. Go to [https://git-scm.com/download/mac](https://git-scm.com/download/mac)
2. Click the link to download the latest installer
3. Once downloaded, open the installer and follow the instructions
4. Keep all default options during installation

## 4. Clone the Repository

Now let's get the project files from GitHub:

1. Open VS Code
2. Click on "Terminal" in the top menu
3. Select "New Terminal"
4. A terminal panel will open at the bottom of VS Code
5. In the terminal, type the following command and press Enter:

```bash
cd ~/Desktop
```

6. Now type the following command to download the project (replace the URL with the actual GitHub repository URL):

```bash
git clone https://github.com/your-organization/evaluation-app.git
```

7. Once completed, type:

```bash
cd evaluation-app
```

This will navigate into the project folder.

## 5. Create a Virtual Environment

A virtual environment keeps your project's packages separate from other Python projects:

```bash
# In the terminal, run:
python -m venv .env
```

If you see an error, try using `python3` instead:

```bash
python3 -m venv .env
```

## 6. Activate the Virtual Environment

```bash
# In the terminal, run:
source .env/bin/activate
```

You should now see `(.env)` at the beginning of your terminal prompt.

## 7. Install Required Packages

```bash
# In the terminal, run:
pip install streamlit pyyaml matplotlib seaborn plotly
```

This might take a minute or two to complete. If you see an error with `pip`, try using `pip3` instead.

## 8. Run the App

```bash
# In the terminal, run:
cd src
streamlit run app.py
```

The app should automatically open in your default web browser. If it doesn't, you can copy the URL shown in the terminal (usually something like http://localhost:8501) and paste it into your browser.

## Stopping the App

When you're done using the app:

1. Go back to the VS Code terminal
2. Press `Ctrl+C` to stop the app
3. Type `deactivate` and press Enter to exit the virtual environment

## Restarting the App Later

If you close VS Code and want to restart the app later:

1. Open VS Code
2. Open the `evaluation-app` folder (File → Open Folder, then navigate to the folder on your Desktop)
3. Open a new terminal (Terminal → New Terminal)
4. Run:
```bash
source .env/bin/activate
cd src
streamlit run app.py
```

## Troubleshooting

### "Command not found" errors
If you see "command not found" when trying to run Python or pip commands, try using `python3` instead of `python` and `pip3` instead of `pip`.

### Permission issues
If you see a "permission denied" error, you may need to add `sudo` before your command, like this:
```bash
sudo pip install streamlit pyyaml matplotlib seaborn plotly
```
You'll be asked for your computer password.

### Git isn't recognized
If your computer says it doesn't recognize the `git` command, you may need to install the Xcode Command Line Tools. Try this command:
```bash
xcode-select --install
```
Follow the prompts to install, then try the git command again.

### Browser doesn't open automatically
If the app doesn't open in your browser automatically, manually open your browser and go to:
```
http://localhost:8501
```

### Other issues
If you encounter any other problems, try closing VS Code completely and restarting your computer, then try again from step 4.