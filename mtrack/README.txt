mtrack adapt the blockchain technology to track the buy and sell of a medicine.

mtrack allows the consumer to trace the item's original productor and all the
intermediate distributor of the item. 


HOW TO RUN
===========
Requirement to install
1. python with conda
  https://www.anaconda.com/download/ 
2. nodejs 
  https://nodejs.org/en/download/ 

After you install python and npm, unzip mtrack
1. start the server
open a command window in mtrack folder and run the following commands
  $> cd server
  $> conda create -f environment.yaml
  $> activate xsign
  $> python server.py

2. start the client  
open another command window in mtrack folder and run the following commands
  $> cd client\mtrackApp 
  $> npm install 
  $> ng serve --open
This will open the client webpage in the browser.
