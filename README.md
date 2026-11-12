# WorldWanderer
AQA A-Level Computer Science NEA/Coursework Project.

A singleplayer, geoguessr-esque game, made using entirely free and open-source resources available online.

## How to use
**run app.py**. ignore all the other files, just run app.py.

## Important: Mapillary API Access Token
This game will not work without a valid Mapillary API access token.

This repository will not provide you with one, so you'll have to get one yourself.

To get one, go to https://www.mapillary.com/developer and click on "get an access token".

When registering the application:
- The following details do not matter:
    - Application Name
    - Description
    - Company Name
    - Company Website
    - Redirect URL
- **It is imperative, however, that you allow the application to:**
    - Read

Once you have the token, paste it into the file located at the following location (relative file path):
> (root directory)\storage\mapillaryaccesstoken.txt
Replace the example with it, then leave it alone; the game should work as normal after.
