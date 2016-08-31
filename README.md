# VkChecker

This is a simple script for scraping information about users' friends and followers in social network VK.
The script checks VK users from the list and tell you about changing in his friends/followers list.

# Usage
Install the Python requirements with pip install -r requirements.txt.

You should create a file called private.py and set a value of list VK_IDS with strings id. For example:
VK_IDS = ['123456', '234567'].

You can run the script from the shell or command line: 
```
python scraper.py
```
In the first time script will download and save all needed info, after that you have to run this command manually or automatically (preferably) every time, when you want to see change in friends.

The best way to do it is scheduled to run a script via cron or smth similar. An interval between the run preferably a one day.
A folder called 'id' + vk_id will be created after first run in the project folder. For example: 'id123456'. It contain all collected information. The most interesting are two files:

* last_result.txt - contain information about last changing
* log.txt - contain information about all changing