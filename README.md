# recipe-library-skill

here is a recipe libary skill for mycroft-   it reads locally stored recipes scrapped from allrecipes website .   to extract new recipes favourite  from  allrecipe web site
 simplly run ./recipe  with the url of the recipe on allrecipe.com
 example 
 ./recipe https://www.allrecipes.com/recipe/230812/standing-roast-beef-brined/
 
 benifit of local stored recipes  is that you can modify download or add your own. to suit your pwn preference or correct any weird vocalization mycroft might have .  once a recipe has being downloaded it will not add another recipe of the same name to be installed
 update:
 you can now add recipes by catagory from allrecipe.com   through the mycroft  voice interface
  - beef, pork, chicken, vegan, cake, cookies, bread, snacks, breakfast .. etc
  to list catagories just say what are my recipe catagories 
  
   to do download reciped to the device by catagory 
    just say "download new bread recipe" and it will download the days top  bread recipes from allricipe .com
    
 to list recipes by catagory just say "list bread recipes"  
 
 to  have mycroft read out or display recipe - just say - bread recipe "banana bread"  and  it will find your banana bread recipe
 
 read random bread recipe - just say "random bread recipe"
 
 individual  recipe upload still work ie
 ./recipe https://www.allrecipes.com/recipe/230812/standing-roast-beef-brined/
 but to get acces to those use they are place in a favorite catagory :
 list my favorite recipes --- to list them
 favorite recipe  standing roast beef  -- to have it read out the recipe 
 or  random favorite recipe
 
 you need to install lynx  for recipe scraper to work
 
 update-
 you can now say  
 read ingredients- it will read the line by line after prompt  option are yes ( next line) repeat and continue  which reads at a slow pace contiously  throuh the list
 read directions- it will read the line by line after prompt  option are yes ( next line) repeat and continue  which reads at a slow pace contiously  throuh the each direction
 also email recipe.  you just need to adjust emil script to match you email setting ( test for google mail) and you can send to any address. later on i probably add option email to my email address or my wife or table  computer 
 
 currently  after download  recipe fore the first time per cat agory   you need to wait several minutes before it done  after that downloading recipes are much faster 
