# LoL-Champion-Visualizer
Designed to display league of legends champion base attributes/statistics in a clean and easy to use and understand GUI.

The champion names and wallpaper is scraped from the main league of legends page: 
- https://na.leagueoflegends.com/en-us/champions/

The champion statistics and original rendering model is scraped from the fan made wiki: 
- https://leagueoflegends.fandom.com/wiki/


## Features
- Can search for new champions released for extra information or use the existing information that was collected
- Search seamlessly for champions using their name and high res icons for fast recognition.
- Look between champion visuals (includes the original rendering of the champion and their loading splash art)
- See champion attributes in a clean window with visuals to easily recognize what you're looking at.
  - attributes sorted by offense, defense, and ranges.


## How To Use
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


## Results



## Tools Used
- Selenium with chrome driver - for web scraping of websites
- Json - for dumping the data collected and accessing it easily later
- Urllib - for any page downloads of visuals needed
- Kivy - for the gui application to display the information collected
- Unittest - used for testing the application to make sure everything is running correctly.


## Upcoming Features in new versions
- For each champion, scrape their 3d skin model from: https://teemo.gg/model-viewer and display it in the skin window with the other renderings.
- Implement a window where you can view what champion has the highest stat for each attribute
- Update the visuals of the application window and make it sleeker.
