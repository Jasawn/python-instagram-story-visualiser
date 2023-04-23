# Instagram Story Visualiser

## Team Members
1) Lim Zhen Guang
2) Lam Wei Ern

## Tool Description
Currently, it is difficult for researchers to monitor large amounts of data, especially those that have a expiry element to them based on time (e.g., Instagram Story). It is also difficult for researchers to monitor events across the world and correlate data visually.

This tool uses an Instagram account to monitor the Instagram Story of a user-defined list of Instagram users. The tool will periodically scrape these users based on user-defined time intervals. During the scraping, it will download the media posted on the Instagram Story, along with any location tag in the Story. After the scraping, it will store the data in a json file which is read by the Front-end website that is hosted on Python Flask. The Python Flask website will display a map and a timeline slider. The map will contain pins that represent each Instagram Story that was scraped and contains location data. The timeline slider will allow the user to view Instagram Stories that were scraped for that day, allowing users to visualize stories on a map. Stories that were scraped but do not have location tag will also be displayed on the website. 

## Installation Guide:
1) Ensure that you minimally have Python version>=3.9.7

	git clone https://github.com/Jasawn/python-instagram-story-visualiser.git
	cd /Jasawn
	pip install -r requirements.txt
	python gui.py

## Usage

## Additional Information
Pros:
- Instagram Story media is downloaded and stored locally so that they can be archived and collected for other purposes.
- Users are able to leave the application running unsupervised to collect information on stories and return at at future time to investigate the data.
- Application can use any profile to monitor accounts, and even monitor private profiles as long as the logged-in account is following the private account. This can allow operators to use the application to monitor profiles they do not typically have access to.

Cons:
- Application relies heavily on web scraping; a change in website layout will result in the app breaking.
- Currently only supports scraping of Instagram Stories.
- Instagram Stories must have a Location Tag, otherwise it will not be displayed on a map.
- Map is unable to auto-refresh once a scrape has completed

Roadmap:
- Figure out how to auto-refresh the map with updated data once scraping has completed.
- Look for other methods to monitor Instagram profiles and download the Instagram Story data.
- Allow monitoring of Tiktok stories, Snapchat, Facebook etc.
- Allow operators to create "Versions" of scraping, allowing customization of which users' stories to display on the map depending on the topic being investigated
- Provide graph/chart and perform some analytics on the amount of data collected and analyze trends
	
