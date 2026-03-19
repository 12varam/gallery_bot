In this project i'm gonna make a bot that saves these things: an images, the image's date and description.
The bot will be simple and i'm gonna use these libraries: aiogram, environs and psycopg2

The logic is like this:
 -- user creates a gallery and gives it a name;
 -- and before sending an image the user chooses to which gallery he/she wants to save the image;
 -- user sends an image and then user asks the user for description;
 -- user can choose: if the user types nodesc the bot makes the description "no description" and if not, the makes just saves the desc and says that the image was successfully saved.
 
 -- the user also can see all the image he/she has saved by writing /mygalleries and by clicking the gallery he/she can see all the images


And of course he/she can add/see/change/delete any gallery or image (or the image's description). So basically just common CRUD




ℹ️ To make the bot work you have to fill up the .env file, an example of it has given in the .env.example

I think I'll make a video-saver bot too.
Thanks for reading all of this, have a good day and good luck with coding!