# Weather App CLI
*❗THIS PROJECT IS NO LONGER ACTIVELY MAINTAINED❗*
    
	- The EC2 instance that is responsible for making API calls is no longer in service, therefore, the only working version of this project now requires you to use the source code from the local-api branch and provide your own api key from https://www.weatherapi.com
    
	- ❗THE PRECOMPILED VERSION IN RELEASES IS NO LONGER SUPPORTED❗
## Description
This is a project I decided to create to learn more about using APIs and implementing web servers into projects. It is a pretty straightforward weather application intended for the command line. There are tons of weather apps and widgets with GUIs out there but I personally wanted a weather application with a customizable amount of detail that I could use to easily check the weather while I am working in the terminal. It uses weatherAPI.com for the weather data and to practice obscuring my api key, I set up an EC2 instance through AWS to host a web server that has the API key and makes the API call on the backend, returning the data to the front end for the user. This program is written pretty much entirely in Python on the front and backend.

The program is meant to be added to PATH so that it can be called from anywhere in the terminal, it also supports different command line arguments to specify input and customize output.

## Installation
### Windows
1. Download the exe file from the releases section of this repository
2. Add file to PATH by doing the following: 
    - Search "Environment variables" in the search box and click on "edit the system environment variables"
    - Click the button at the bottom that says "Environment Variables"
    - Under "User variables for `<YourUserName>` click on the variable called "Path"
    - While "Path" is highlighted, click the button that says "edit"
    - Click the button that says "New" 
    - Copy the path of the location where you installed this program and paste it into the empty box that shows up when you press "New"
3. Once the file is added to path you can run the program from anywhere in your terminal by typing the name of the program, "weather"!
    - Note: if you choose not to add the program to PATH, you will need to be in the directory you downloaded the program into in order to run it

### Mac
For right now you guys will need to clone the repo and have python installed to use this
1. Make sure you have Git and Python >= 3.12 installed
2. In the terminal run `git clone https://github.com/petervislocky/weatherApp`
3. Cd into the project directory and run `python main.py`
4. To create a working exe file (so you can use the program as intended), use pip to install pyinstaller, and in the project directory run `pyinstaller --onefile --name weather main.py`
5. Add the exe file to PATH and enjoy!

### Linux
Same deal as windows, compiled file is located in the releases tab. Either download the file into a directory already in $PATH or add a line into your .bashrc file adding the project to $PATH.

## Usage
Supports the `-l` or `--location` flag, use this option to specify the location to show the weather for. If not specified the program will just prompt you for the location.
`-m` or `--metric` flag converts all output units to metric, conversely the `-i` or `--imperial` flag is used for imperial units *however* imperial units is the default so this flag is unnecessary and is just there for clarity's sake. `-v` or `--verbose` flag is used for verbose output. And `f` or `--forecast` flag will display a 3 day forecast.
Hope you enjoy! And if you like it, leave a star ;)
