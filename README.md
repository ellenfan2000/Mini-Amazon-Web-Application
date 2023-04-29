# ERSS-project-rf96-xc139

This project is a **Mini-Amazon System** with World warehouse and Delivery systems. Users can use the front interface to buy products, view orders and make comments. The project is separated into two parts. The front end is built using Python **Django** responsible for taking user requests. The back-use use **SQLAlchemy** to manage the database, and **Google protocol buffer** to communicate with World and UPS about package update and so on. The front-end and back-end also communicate through a socket.

To start the server, use: `sudo docker-compose up`

This will start both the backend and the front end. Only when the backend prompts "World Initialized!", can the user buy products, since that is the signal that all products are ready in the warehouse. 

## Features

Detail extra features please refer to *Feature_Specification.pdf* 

* A searchable catalog of products with nice pictures
* check the status of an order
* specify an address (i.e., (x,y) coordinates) for delivery.
* specify a UPS account name to associate the order with (optional).
* Provide the Tracking Number for the shipment
