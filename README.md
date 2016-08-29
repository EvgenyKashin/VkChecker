# VkChecker

Simple script for scraping information about users' friends and followers in social network VK.
Script checks VK users from list and tell you about changing in his friends/followers list.

# Usage
You should create a file called private.py and set value of list VK_IDS with strings id. For example:
VK_IDS = ['123456', '234567']
You can run script from the shell or comand line: 'python scraper.py'. In ther first time script will download and save all needed info, after that you have to run this command manualy or automaticaly (preferably) every time, when you want to see changing friends.
The best way to do it is sheduled to run a script wia cron or smth similar. An interval between the run preferably 1 day.
After first run in the project folder will be created a folder called 'id' + vk_id. For example: 'id123456'. It contain all collected information. The most intresting are two files:

* last_result.txt - contain information about last changing
* log.txt - contain information about all changing