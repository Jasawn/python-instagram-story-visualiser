# Instagram Story Visualiser

## Team Members
1) Lim Zhen Guang
2) Lam Wei Ern

## Tool Description
Currently, it is difficult for researchers to monitor large amounts of data, especially those that have a expiry element to them based on time (e.g., Instagram Story). It is also difficult for researchers to monitor events across the world and correlate data visually.

This tool uses an Instagram account to monitor the Instagram Story of a user-defined list of Instagram users. The tool will periodically scrape these users based on user-defined time intervals. During the scraping, it will download the media posted on the Instagram Story, along with any location tag in the Story. After the scraping, it will store the data in a json file which is read by the Front-end website that is hosted on Python Flask. The Python Flask website will display a map and a timeline slider. The map will contain pins that represent each Instagram Story that was scraped and contains location data. The timeline slider will allow the user to view Instagram Stories that were scraped for that day, allowing users to visualize stories on a map. Stories that were scraped but do not have location tag will also be displayed on the website. 

## Installation Guide:
1) Ensure that you minimally have Python version>=3.9.7
	1. git clone https://github.com/Jasawn/python-instagram-story-visualiser.git
	2. cd python-instagram-story-visualiser
	3. pip install -r requirements.txt

## Usage
Step 1: Run the following code
python gui.py
![image](https://user-images.githubusercontent.com/91773813/233845145-8b187318-78e3-4b72-9fd3-9ba922f7efa4.png)

Step 2: Copy the link as shown in the image above 'http://127.0.0.1:5000/ and paste into a browser (Preferably Chrome or Firefox) and the output will be as shown in the screenshot below
![image](https://user-images.githubusercontent.com/91773813/233845272-9b78d3c0-6705-4afb-9f2d-97c9a8a46393.png)
	
Step 3: Click on 'Click here to start new search' to begin Instagram Story Scraping with the defined list of users. After clicking on the 'Click here to start new search', the output will be as shown in the screenshot below.
![image](https://user-images.githubusercontent.com/91773813/233845422-c8522113-08ff-4451-9ba9-bb79c7eb70bd.png)

**NOTE:** Do provide valid Instagram account. Create a text file with predefined list of users specified inside the text file and save the file in the same directory as the code.
	
![image](https://user-images.githubusercontent.com/91773813/233845535-72cce24b-acaa-4e18-9a4b-f866d4f83c44.png)

Step 4: After entering the required information, click on 'Start Scraping...' and let it load. Initially, another browser will open another tab to attempt to login in Instagram. Next, the output will be as shown in the screenshot below.
![image](https://user-images.githubusercontent.com/91773813/233845635-19aa6a4b-7c9a-4499-a668-6dfbfa6a9bf2.png)
	
**NOTE: **While there will be a browser popup, you can minimise the browser and continue with your daily tasks.
	
Step 5: After the scraping has been completed, a 'data.json' file will be created in the directory and the content downloaded will be saved in /static directory. The browser will automatically reload and show the data scraped from the defined list of user as shown in the image below.
	
![image](https://user-images.githubusercontent.com/91773813/233845893-c1537fc4-14d5-4093-a090-8bb52b4df30b.png)
	
**NOTE: **Those stories that have a location tag will have a pin shown in the map. While those stories without location tag can be seen after clicking on the 'No Coordinates' button located near the timeline slider
	


	
	
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
	
