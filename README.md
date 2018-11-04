# HBI-CargoTracker

## Overview
The CargoTracker project for HackBI utilizes the Python Flask framework to host a web-app. The Web-app displays the "Cargo" 
in transit and allows the user to not only view which shipments are in transit but the individual details of each shipment.

Another function is the ability for the framework to "Check-In" with containers as they reach port. When any smartphone scans 
the "attached" RFID card, a GET request is sent to the Flask server to update the status of the shipment in the database.

Furthermore, the Flask server is integrated to make an API call to the home.com API to find the most convenient & quickest route for the shipment to get to its final destination once removed from the ship. When the status of each shipment is called
the quickest truck route is calculated using the here.com API and the quickest time in minutes is displayed. 

## Flask Server
The Flask server is run on a Raspberry Pi with python 2.7. It utilizes a sqlite3 database to store information about all shipments. There is a second script to initialize the database and fill it with example values.

## Here.com API
The Home.com API is used to pull the quickest route between the two coordinate points for a truck without factoring in traffic. It also factors in the weight and height restrictions of a truck. It then interprets the JSON request specifically for the total trip time and returns this value to the status function.

## RFID Integration
To integrate the RFID card, the url: http://"ip":"port"/arrival/"Base64_encoded_name" is writen to the card. When the card is scanned by a phone, a GET request is sent to that URL, which causes the status variable of that specific shipment to be changed. 
