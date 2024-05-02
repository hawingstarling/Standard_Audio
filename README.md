
# Introduce
This is a project about Apple Music for playing music locally and developed in the Python programming language.
# Introduce Website
- Intruduce Website: [Apple Music](https://hawingstarling.github.io/MusicWeb/)
# Setting up a development enviroment
## Downloading the project
Requirement
- Python3 (Download from https://www.python.org/downloads/)
- Install XAMPP
- Import the `musicplayer.sql` file into MySQL

Clone the respository with following:

    $ git clone https://github.com/hawingstarling/Standard_Audio.git
    $ cd Standard_AudioMusic
## Install
### For Window
1. You can download the latest version of Python from the official Python website at [Install python3.10 or higher version](https://www.python.org/downloads/)
2. Download pip [pip](https://pip.pypa.io/en/stable/installation/)
3. Install necessary libraries 
```sh
$ venv\Scripts\Activate
$ pip install -r requirements.txt
```

### For linux
1. If python is not in your system
```sh
$ sudo apt update
$ sudo apt install python3.10
```

3. If pip is not installed, use the following command to install pip
```sh
$ sudo apt-get install python-pip
```
4. Next, run this command to install the libraries:
```sh
$ source venv\bin\activate
$ pip install -r requirements.txt
```
# Feature
1. Song Control
	-   Add songs from local music library using MP3 files.
	-   Delete songs.
	-   Add songs to playlists.
	-   Skip to next or previous song.
	-   Search Song
2. Playlist managerment
	-   Create playlists.
	-   Add songs to playlists.
	-   Delete playlists.
	-   Edit playlists (e.g., change song order, rename playlist).
# Run the application
After installing Python and the necessary libraries, you can run the application. Open Command Prompt or Terminal and navigate to the directory that contains the application's source code.

Run the following command to start the application:

    python main.py
# Download report latex
[Report OSSD Latex](https://www.overleaf.com/8423719863hdngctfjpsfj#f5c11b)
