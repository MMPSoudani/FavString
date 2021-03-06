# FavString
## Overview
- This project is written using Django webframework
- To style the pages, tailwind css is used through its CDN link
- The project uses a custom User model without incorporating any Django User models
- Visitors can register as normal or super users
- Super users, can add a text message
  - all the added text messages will be displayed in the home page along side:
    - the name of the creator
    - the date it was created
    - its weight
    - number of people added it to their favorite
- each time a text message is created its weight is calculated through a signal
  - the weight is calculated by adding the ASCII number for each en/EN letters to the total
- logged in users can add text messages to their favorite list
- text messages can be opened to view the text message and watch who have added to their favorite
- logged in users can logout
## API
- created an api for all the models
- the api includes the methods GET, POST, PUT and DELETE for all the models
- can access the api using the localhost:8000/api/ url link
## Display
![Home Page](https://github.com/MMPSoudani/FavString/tree/favString/FavString/static/media/HomePage.png)<br>
![Login Page](https://github.com/MMPSoudani/FavString/tree/favString/FavString/static/media/LoginPage.png)<br>
![Register Page](https://github.com/MMPSoudani/FavString/tree/favString/FavString/static/media/RegisterPage.png)<br>
![Logout Page](https://github.com/MMPSoudani/FavString/tree/favString/FavString/static/media/LogoutPage.png)<br>
![Add String Page](https://github.com/MMPSoudani/FavString/tree/favString/FavString/static/media/AddStringPage.png)<br>
![String Page](https://github.com/MMPSoudani/FavString/tree/favString/FavString/static/media/StringPage.png)
