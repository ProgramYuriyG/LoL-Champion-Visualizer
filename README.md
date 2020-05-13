# LoL-Champion-Visualizer
Designed to display league of legends champion base attributes/statistics in a clean and easy to use and understand GUI.

The champion names and wallpaper is scraped from the main league of legends page: 
- https://na.leagueoflegends.com/en-us/champions/

The champion statistics and original rendering model is scraped from the fan made wiki: 
- https://leagueoflegends.fandom.com/wiki/


## Table Of Contents:

- <a href="#features">Features</a> </br>
- <a href="#how_to">How To Use</a> </br>
- <a href="#results">Results</a> </br>
- <a href="#tools_used">Tools Used</a> </br>
- <a href="#upcoming_features">Upcoming Features</a> </br>


<h2 id="features">Features</h2>

- Can search for new champions released for extra information or use the existing information that was collected
- Search seamlessly for champions using their name and high res icons for fast recognition.
- Look between champion visuals (includes the original rendering of the champion and their loading splash art)
- See champion attributes in a clean window with visuals to easily recognize what you're looking at.
  - attributes sorted by offense, defense, and ranges.


<h2 id="how_to">How To Use</h2>

*In a later version this will be streamlined and will be launched using a simple .exe file*

Commands to execute for the GUI environment:
- python -m pip install --upgrade pip wheel setuptools virtualenv
- python -m virtualenv kivy_venv
- kivy_venv\Scripts\activate
- python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
- python -m pip install kivy_deps.gstreamer==0.1.*
- python -m pip install kivy==1.11.1
- pip install selenium

In the new built environment run: 

- python -m lolChampionVisualizer

This will now launch the whole folder as a module and the application will launch


<h2 id="results">Results</h2>

### Choose What Data To Use
![](/applicationImages/startingScreen.png)
### Search For Champions
![](/applicationImages/searchScreen_base.png)
### Specific Search
![](/applicationImages/searchScreen_ja.png)
### Jarvan IV Statistics
![](/applicationImages/jarvan_defense.png)
![](/applicationImages/jarvan_ranges.png)
### Ahri Statistics
![](/applicationImages/ahri_offense.png)


<h2 id="tools_used">Tools Used</h2>

- Selenium with chromedriver - For web scraping of websites
- Json - For dumping the data collected and accessing it easily later
- Urllib - For any page downloads of visuals needed
- Kivy - For the gui application to display the information collected
- Unittest - For testing the application to make sure everything is running correctly.


<h2 id="upcoming_features">Upcoming Features For New Versions</h2>

- For each champion, scrape their 3d skin model from: https://teemo.gg/model-viewer and display it in the skin window with the other renderings.
- Implement a window where you can view what champion has the highest stat for each attribute
- Add more options to search by in the search window
- Update the visuals of the application window and make it sleeker.
