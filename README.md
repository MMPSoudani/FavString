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
- each time a text message is created its weight is calculated
  - the weight is calculated by adding the ASCII number for each en/EN letters to the total
- logged in users can add text messages to their favorite list
- text messages can be opened to view the text message and watch who have added to their favorite
- logged in users can logout
