# Indian Railways Train Booking & Fare Engine

A lightweight, production-ready Full-Stack Web Application built using Python Flask and SQLite3 that simulates an Indian Railways train routing, fare calculation, and ticket generation system. The application features a dynamic relational database backend to handle multi-station train schedules, calculate precise travel distances across intersecting routes, and automatically generate detailed passenger tickets with assigned PNRs, random coach coordinates, and specific berth configurations.

 🚄 Key Features & System Logic

* **Smart Route Intersection Matrix:** Utilizes an optimized SQLite self-join query layout on station route sequences to instantly display valid train options running between selected origins and destinations, ensuring strict verification of chronological stop orders (`d.stop_order > s.stop_order`).
* **Dynamic, Multi-Tier Fare Calculator:** Implements real-time programmatic fare algorithms customized specifically by train profile types:
  * **Vande Bharat Express (20833):** Premium pricing structures adjusting dynamically across AC Chair Car (CC) and Executive Car (EC) brackets.
  * **Garib Rath Express (12739):** Economic all-3A specialized budget tiering.
  * **Express/Superfast Fleets (Godavari, Janmabhoomi, etc.):** Standardized scaling across Sleeper (SL), 3A, 2A, and 1A classes based on precise mileage distance differentials ($\Delta \text{distance}$).
* **Automated Ticket & Coach Allotment:** Seamlessly aggregates passenger manifest arrays from booking forms, executes math logic to tally total fares, and assigns randomized alpha-numeric coach prefixes matching structural Indian Railways configurations (e.g., `S` for Sleeper, `B` for 3A, `A` for 2A) alongside unique 10-digit PNR strings.

🛠️ Tech Stack & Architecture

* **Backend Framework:** Python 3 + Flask
* **Database Engine:** SQLite3 (Embedded structural storage)
* **Production Gateway:** Gunicorn WSGI HTTP Server
* **Frontend Design:** Semantic HTML5 + Custom CSS3 Layouts
