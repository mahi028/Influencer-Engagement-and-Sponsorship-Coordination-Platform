#DESCRIPTION OF PROJECT 
 
In this day and age of social media, more and more Influencers and brands are collaborating online. This platform, SponserMe, helps both Brands as well as Influencers to collaborate easily, help Influencers monetize their content, let brands advertise their products and services by Influencers with high reach. It’s a platform where both, Brands and Influencers, can “Elevate their Brand and Empower their Influence”.
 
##TECHNOLOGIES USED 
 
•	Flask: Backend framework for building the web application. 
•	SQLAlchemy: ORM (Object-Relational Mapping) tool for database interactions. 
•	SQLite : Database management system for storing application data. 
•	HTML/CSS/JavaScript: Frontend technologies for user interface design and interactivity. 
•	Flask-Login: Extension for managing user sessions and authentication. 
•	Flask-WTForms: Provides flaskform for creating secure forms.
•	Bcrypt: Python library for hashing passwords
•	Datetime: Python library for handling date and time operations. 
•	UUID: Python library for generating unique ids.

 
##ARCHITECTURE 
 
Here, The app.py file contains the main code to run the application. /application is a module which contains all the files for app. The description of files inside application are as follows 
•	api.py – This file contains Activity Api for admin monitoring
•	Models.py – This contains DB Classes 
•	Validation.py – This contains error handling logic for API 
•	Templates – This contains all HTML templates for Admin, Auth, Influencer, Sponsor etc. 
•	form.py – This contains FlaskForm classes.
•	hash.py – Bcrypt hashing functions for password checking and hashing.
•	Static – This contains JS, CSS and image/upload files 
•	Controller – This module contain all the controller logic files for admin, influencer, sponsor, dashboard, auth etc.
o	auth.py - This file contains Authorization logic like login, signup.
o	admin.py - This file contains logic and routes for admins.
o	influencer.py - This file contains logic and routes for influencers.
o	sponser.py - This file contains logic and routes for sponsors.
o	dashboard.py – This file handles universal routes for all types of users.

 ![image](https://github.com/user-attachments/assets/1823c4b3-cae1-48f6-86b0-9cffbf860f80)

 
 
##FEATURES 
 
User Management: 
 
•	Registration and authentication for users (admin, sponsors and influencers). 
•	User roles (admin, sponsors and influencers) to control access and permissions. 
•	User profile management including personal details like name, email, profile img, etc. 
 



##Campaign and Post Management: 
 
•	Ability to create, update, delete privet and public campaigns.
•	Ability to create, update, delete privet and public posts.
•	Ability to like a post.
•	Ability to search for campaigns.
•	Feedback or suggestion for posts.
 
##Collab Request Management: 
 
•	Collaboration requests for campaigns.
•	Ability to negotiate budget.

##DB SCHEMA DESIGN 
 
The database schema consists of tables for users, roles, admin, sponsor, influencer, requests, campaign, posts. Each table contains relevant fields such as user details.

 ![image](https://github.com/user-attachments/assets/3156a61d-39ef-4f92-bea0-d2a975b897b4)

 
