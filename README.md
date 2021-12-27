# drinkbot
A bartending machine that utilizes a raspberry pi and flask to make a webserver pour your drinks for you

This program requires a custom built device, including a raspberry pi, 6 peristaltic pumps, silicon tubing, an 8 port relay, and a power supply with a step down module.

In order to run it, simply run the drinkbot.py file on the raspberry pi, and it will start the flask web server. Navigate to the website (The raspberry pi's local IP generally)
and you should see the drink ordering screen. Many settings can be adjusted in the settings tab, which is password protected. The login credentials can be changed in the 
corresponding python file.

In the settings the drink names can be changed, the pumps can be primed or purged, and more.

The Web Server uses bootstrap, as well as some custom CSS, and HTML for individual pages as well as the overall color changing background.
