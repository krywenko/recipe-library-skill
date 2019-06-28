from os.path import join, abspath, dirname
import os.path
import random
from adapt.tools.text.tokenizer import EnglishTokenizer
from mycroft.messagebus.client.ws import WebsocketClient
from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util import play_mp3
from mycroft.util.parse import fuzzy_match
from mycroft.util.parse import match_one
from mycroft.audio import wait_while_speaking
from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.context import *
import subprocess

class RecipeLibary(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        
    def initialize(self):
        
        #Register list of recipe titles that are held in a padatious entity
        self.register_entity_file("title.entity")
        self.process = None
        self.register_entity_file("titleshrimp.entity")
        self.process = None
        self.register_entity_file("titlecake.entity")
        self.process = None
        self.register_entity_file("titlecookie.entity")
        self.process = None
        self.register_entity_file("titlebread.entity")
        self.process = None
        self.register_entity_file("titlebreakfast.entity")
        self.process = None
        self.register_entity_file("titlechicken.entity")
        self.process = None
        self.register_entity_file("titlebeef.entity")
        self.process = None
        self.register_entity_file("titlepork.entity")
        self.process = None
        self.register_entity_file("titlevegan.entity")
        self.process = None  
        self.register_entity_file("titleslow.entity")
        self.process = None
        self.register_entity_file("titlesnack.entity")
        self.process = None
        self.register_entity_file("titleworld.entity")
        self.process = None        
        
              
        #Build recipe list
        self.slow_play_list = {
     
        }       
        self.snack_play_list = {
            'bacon dijon egg salad sandwich': join(abspath(dirname(__file__)), 'recipes/snack', 'bacon-dijon-egg-salad-sandwich'),    
        }        
        self.world_play_list = {
            'german rouladen': join(abspath(dirname(__file__)), 'recipes/world', 'german-rouladen'),
        }          
        self.beef_play_list = {
            'standing roast beef brined': join(abspath(dirname(__file__)), 'recipes/beef', 'standing-roast-beef-brined'),
        }       
        self.pork_play_list = {
     
        }        
        self.vegan_play_list = {
     
        }        
        
        self.cookies_play_list = {
            'peanut butter bars i': join(abspath(dirname(__file__)), 'recipes/cookies', 'peanut-butter-bars-i'),
        }        
        self.cake_play_list = {
            'tiramisu layer cake': join(abspath(dirname(__file__)), 'recipes/cake', 'tiramisu-layer-cake'),

        }        
        self.breakfast_play_list = {
            'classic waffles': join(abspath(dirname(__file__)), 'recipes/breakfast', 'classic-waffles'),

        }        
        self.bread_play_list = {
            'banana banana bread': join(abspath(dirname(__file__)), 'recipes/bread', 'banana-banana-bread'),
            
        }        
        
        self.chicken_play_list = {
            'simple whole roasted chicken': join(abspath(dirname(__file__)), 'recipes/chicken', 'simple-whole-roasted-chicken'),

        }
        self.shrimp_play_list = {
            'szechwan shrimp': join(abspath(dirname(__file__)), 'recipes/shrimp', 'szechwan-shrimp'),

        }
        self.play_list = {
            'chewy chocolate chip oatmeal cookies': join(abspath(dirname(__file__)), 'recipes', 'chewy-chocolate-chip-oatmeal-cookies'),
            'sourdough pancakes': join(abspath(dirname(__file__)), 'recipes', 'sourdough-pancakes'),    
            'impossible coconut pie ii': join(abspath(dirname(__file__)), 'recipes', 'impossible-coconut-pie-ii'),
            
        }
 ########################################
 ###### get recipes ###########       
    @intent_file_handler('pick.getrecipe.intent')
    def handle_pick_getrecipe(self, message):
        self.speak_dialog('pick.getrecipes')
        wait_while_speaking()
        title = message.data.get('group')
        
        if title == 'bread':
            self.speak('getting new bread recipes') 
            os.system("$HOME/mycroft-core/skills/recipe-library-skill/./bread_recipe") 
        if title == 'cookie':
            self.speak('getting new cookie recipe')
            os.system("$HOME/mycroft-core/skills/recipe-library-skill/./cookie_recipe")  
        if title == 'cake':
            self.speak('getting new cake recipes')
            os.system("$HOME/mycroft-core/skills/recipe-library-skill/./cake_recipe")
        if title == 'breakfast':
            self.speak('getting new breakfast recipes')
            os.system("$HOME/mycroft-core/skills/recipe-library-skill/./breakfast_recipe")            
        if title == 'chicken':
            self.speak('getting new chicken recipes')
            os.system("$HOME/mycroft-core/skills/recipe-library-skill/./chicken_recipe")
        if title == 'beef':
            self.speak('getting new beef recipes')
            os.system("$HOME/mycroft-core/skills/recipe-library-skill/./beef_recipe")  
        if title == 'shrimp':
            self.speak('getting new shrimp recipes')
            os.system("$HOME/mycroft-core/skills/recipe-library-skill/./shrimp_recipe")
        if title == 'vegan':
            self.speak('getting new vegan recipes') 
            os.system("$HOME/mycroft-core/skills/recipe-library-skill/./vegan_recipe")
        if title == 'snack':
            self.speak('getting new snack recipes') 
            os.system("$HOME/mycroft-core/skills/recipe-library-skill/./snack_recipe") 
        if title == 'slow cooker':
            self.speak('getting new slow cooker recipes')
            os.system("$HOME/mycroft-core/skills/recipe-library-skill/./slow-cooker_recipe") 
        if title == 'world':
            self.speak('getting new world recipes') 
            os.system("$HOME/mycroft-core/skills/recipe-library-skill/./world_recipe")      
        if title == 'pork':
            self.speak('getting new pork recipes') 
            os.system("$HOME/mycroft-core/skills/recipe-library-skill/./pork_recipe")             
            
            
              
        else:
           # return None
            self.speak('Finished download new recipes from all recipe  dot com')     
 ######################       
    @intent_file_handler('catrecipes.pick.intent')
    def handle_catrecipes_pick(self, message):
        wait_while_speaking()
        self.speak(' the catagories are: bread, Cakes, cookies,  breakfast, snack, slow cooker, chicken, beef, pork, shrimp,  vegan and  world . ')        
        
        
 #####snack############
    #Play random recipe from list
    @intent_file_handler('snackrecipes.pick.intent')
    def handle_snrecipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.snack_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.snackrecipe.intent')
    def handle_pick_snrecipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        title = message.data.get('titlesnack')
        score = match_one(title, self.snack_play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
            #return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.snackrecipes.intent')
    def handle_list_snrecipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.snack_play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))
        
        
              
#####slowcooker############
    #Play random recipe from list
    @intent_file_handler('slowrecipes.pick.intent')
    def handle_slrecipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.slow_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.slowrecipe.intent')
    def handle_pick_slrecipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        title = message.data.get('titleslow')
        score = match_one(title, self.slow_play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
            return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.slowrecipes.intent')
    def handle_list_slrecipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.slow_play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))
        
        
                
#####world############
    #Play random recipe from list
    @intent_file_handler('worldrecipes.pick.intent')
    def handle_wrecipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.world_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.worldrecipe.intent')
    def handle_pick_wrecipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        title = message.data.get('titleworld')
        score = match_one(title, self.world_play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
            #return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.worldrecipes.intent')
    def handle_list_wrecipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.world_play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))
               
 
 #       
  #####beef############
    #Play random recipe from list
    @intent_file_handler('beefrecipes.pick.intent')
    def handle_Berecipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.beef_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.beefrecipe.intent')
    def handle_pick_Berecipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        title = message.data.get('titlebeef')
        score = match_one(title, self.beef_play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
           # return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.beefrecipes.intent')
    def handle_list_Berecipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.beef_play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))
        
        
              
#####pork############
    #Play random recipe from list
    @intent_file_handler('porkrecipes.pick.intent')
    def handle_precipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.pork_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.porkrecipe.intent')
    def handle_pick_precipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        title = message.data.get('titlepork')
        score = match_one(title, self.pork_play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
            #return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.porkrecipes.intent')
    def handle_list_precipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.pork_play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))
        
        
                
#####vegan############
    #Play random recipe from list
    @intent_file_handler('veganrecipes.pick.intent')
    def handle_vrecipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.vegan_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.veganrecipe.intent')
    def handle_pick_vrecipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        title = message.data.get('titlevegan')
        score = match_one(title, self.vegan_play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
            #return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.veganrecipes.intent')
    def handle_list_vrecipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.vegan_play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))
        
        
                
 ##       
  #####bread############
    #Play random recipe from list
    @intent_file_handler('breadrecipes.pick.intent')
    def handle_Brecipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.bread_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.breadrecipe.intent')
    def handle_pick_Brecipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        title = message.data.get('titlebread')
        score = match_one(title, self.bread_play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
            #return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.breadrecipes.intent')
    def handle_list_Brecipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.bread_play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))
        
        
              
#####breakfast############
    #Play random recipe from list
    @intent_file_handler('breakfastrecipes.pick.intent')
    def handle_brrecipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.breakfast_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.breakfastrecipe.intent')
    def handle_pick_brrecipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        title = message.data.get('titlebreakfast')
        score = match_one(title, self.breakfast_play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
            #return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.breakfastrecipes.intent')
    def handle_list_brrecipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.breakfast_play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))
        
        
                
#####cake############
    #Play random recipe from list
    @intent_file_handler('cakerecipes.pick.intent')
    def handle_Carecipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.cake_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.cakerecipe.intent')
    def handle_pick_Carecipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        title = message.data.get('titlecake')
        score = match_one(title, self.cake_play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
            #return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.cakerecipes.intent')
    def handle_list_Carecipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.cake_play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))
        
        
                
#####cookies############
    #Play random recipe from list
    @intent_file_handler('cookiesrecipes.pick.intent')
    def handle_Corecipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.cookies_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.cookiesrecipe.intent')
    def handle_pick_Corecipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        title = message.data.get('titlecookies')
        score = match_one(title, self.cookies_play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
            #return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.cookiesrecipes.intent')
    def handle_list_Corecipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.cookies_play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))
        
        
                
#####chicken############
    #Play random recipe from list
    @intent_file_handler('chickenrecipes.pick.intent')
    def handle_Crecipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.chicken_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.chickenrecipe.intent')
    def handle_pick_Crecipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        title = message.data.get('titlechicken')
        score = match_one(title, self.chicken_play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
            #return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.chickenrecipes.intent')
    def handle_list_Crecipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.chicken_play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))
        
        
        
#####SHRIMP############
    #Play random recipe from list
    @intent_file_handler('shrimprecipes.pick.intent')
    def handle_Srecipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.shrimp_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.shrimprecipe.intent')
    def handle_pick_Srecipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        titleshrimp = message.data.get('titleshrimp')
        score = match_one(titleshrimp, self.shrimp_play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
            #return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.shrimprecipes.intent')
    def handle_list_Srecipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.shrimp_play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))


##########FAV#############
    #Play random recipe from list
    @intent_file_handler('recipes.pick.intent')
    def handle_recipes_pick(self, message):
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  self.speak("{}".format(line))

    #Pick recipe by title
    @intent_file_handler('pick.recipe.intent')
    def handle_pick_recipe(self, message):
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        title = message.data.get('title')
        score = match_one(title, self.play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            with open(filepath) as fp:  
                  for cnt, line in enumerate(fp):
                      self.speak("{}".format(line))
        else:
           #find  return None
            self.speak('Sorry I could not find that recipe in my library')

    #List recipes in library
    @intent_file_handler('list.recipes.intent')
    def handle_list_recipes(self, message):
        wait_while_speaking()
        recipe_list = list(self.play_list.keys())
        print(recipe_list)
        self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))
    
    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

def create_skill():
    return RecipeLibary()

