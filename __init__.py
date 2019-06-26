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

class RecipeLibary(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        
    def initialize(self):
        
        #Register list of recipe titles that are held in a padatious entity
        self.register_entity_file("title.entity")
        self.process = None
        
        #Build recipe list
        self.play_list = {
            'standing roast beef brined': join(abspath(dirname(__file__)), 'recipes', 'standing-roast-beef-brined'),
            'roast chicken dinner with gravy': join(abspath(dirname(__file__)), 'recipes', 'roast-chicken-dinner-with-gravy'),
            'chewy chocolate chip oatmeal cookies': join(abspath(dirname(__file__)), 'recipes', 'chewy-chocolate-chip-oatmeal-cookies'),
            'bacon dijon egg salad sandwich': join(abspath(dirname(__file__)), 'recipes', 'bacon-dijon-egg-salad-sandwich'),
            'sourdough pancakes': join(abspath(dirname(__file__)), 'recipes', 'sourdough-pancakes'),    
            'impossible coconut pie ii': join(abspath(dirname(__file__)), 'recipes', 'impossible-coconut-pie-ii'),
            'german rouladen': join(abspath(dirname(__file__)), 'recipes', 'german-rouladen'),
        }

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
        self.speak_dialog('recipe.found')
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
            return None
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

