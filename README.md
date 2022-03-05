# ChatBuddy

## Description:
- This repository contains the files for the ChatBuddy website.
- It is written using Django webframework, HTML and Tailwindcss.
- The website uses four models
  - Profile
  - Topic
  - Room
  - Message
- The User model is modified to use email instead of username for authentication.
- The website provides the ability to create chat rooms with a spesific topic and allow the users to send messages in them.
- To style the website, Tailwindcss is used through its CDN link.

## Website Functionalities:
- User Login, Logout and Registration.
- Each time a user signs up, a profile is created through Django signals for that user.
- A profile contains
  - full name
  - birth date
  - bio
  - avatar
- Creating rooms with specific topic.
- The host of the room can modify or delete their room.
  - The modification include changing the room's title, topic and description.
- Sending messages within a room.
- The sender of a message, can modify or delete their message.
- The website provides a profile page which contains four sections:
  - Overview: display general info about a user - public access.
  - Activity: display rooms the user has created and rooms the user has participated in - public access.
  - Update: update profile info - restricted access.
  - Setting: change password or delete account - restricted access.
