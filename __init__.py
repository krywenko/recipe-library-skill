from os.path import join, abspath, dirname
import os.path
import random
from adapt.tools.text.tokenizer import EnglishTokenizer
from mycroft.messagebus.client.ws import WebsocketClient
from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util import nice_number
from mycroft.util.parse import fuzzy_match
from mycroft.util.parse import match_one
from mycroft.audio import wait_while_speaking
from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.context import *
import subprocess
from mycroft.util.parse import normalize
import re
import time


class RecipeLibrary(MycroftSkill):
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
        self.is_reading = False
        self.is_paused = False
        self.is_continue = False
        self.is_repeat = False 
        self.is_next = False
              
        #Build recipe list
        self.slow_play_list = {
            'refried beans without the refry': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'refried-beans-without-the-refry'),
            'slow cooker buffalo chicken sandwiches': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-buffalo-chicken-sandwiches'),
            'slow cooker italian beef for sandwiches': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-italian-beef-for-sandwiches'),
            'slow cooker texas pulled pork': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-texas-pulled-pork'),
            'its chili by george': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'its-chili-by-george'),
            'slow cooker pepper steak': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-pepper-steak'),
            'amazing pork tenderloin in the slow cooker': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'amazing-pork-tenderloin-in-the-slow-cooker'),
            'bbq pork for sandwiches': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'bbq-pork-for-sandwiches'),
            'easy slow cooker french dip': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'easy-slow-cooker-french-dip'),
            'slow cooker chicken stroganoff': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-chicken-stroganoff'),
            'slow cooker beef stroganoff i': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-beef-stroganoff-i'),
            'slow cooker beef stew i': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-beef-stew-i'),
            'slow cooker pulled pork': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-pulled-pork'),
            'slow cooker chicken tortilla soup': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-chicken-tortilla-soup'),
            'slow cooker chicken and dumplings': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-chicken-and-dumplings'),
            'awesome slow cooker pot roast': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'awesome-slow-cooker-pot-roast'),
            'simple slow cooked korean beef soft tacos': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'simple-slow-cooked-korean-beef-soft-tacos'),
            'papa funks campfire chili': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'papa-funks-campfire-chili'),
            'kefir yogurt sana': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'kefir-yogurt-sana'),
            'clean eating refried beans': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'clean-eating-refried-beans'),
            'busy day slow cooker taco soup': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'busy-day-slow-cooker-taco-soup'),
            'barbacoa style shredded beef': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'barbacoa-style-shredded-beef'),
            'bbq beef brisket sandwiches': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'bbq-beef-brisket-sandwiches'),
            'slow cooker mediterranean beef with artichokes': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-mediterranean-beef-with-artichokes'),
            'amazing ribs': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'amazing-ribs'),
            'mississippi pot roast': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'mississippi-pot-roast'),
            'slow cooker mac and cheese': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-mac-and-cheese'),
            'slow cooker beef pot roast': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-beef-pot-roast'),
            'melt in your mouth meat loaf': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'melt-in-your-mouth-meat-loaf'),
            'slow cooker corned beef and cabbage': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-corned-beef-and-cabbage'),
            'slow cooker salisbury steak': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-salisbury-steak'),
            'colleens slow cooker jambalaya': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'colleens-slow-cooker-jambalaya'),
            'slow cooker baby back ribs': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-baby-back-ribs'),
            'slow cooker chicken taco soup': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-chicken-taco-soup'),
            'zesty slow cooker chicken barbecue': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'zesty-slow-cooker-chicken-barbecue'),
            'slow cooker german potato salad': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'slow-cooker-german-potato-salad'),
            'outrageous warm chicken nacho dip': join(abspath(dirname(__file__)), 'recipes/slowcooker', 'outrageous-warm-chicken-nacho-dip'),
     
        }       
        self.snack_play_list = {
            'grilled marinated shrimp': join(abspath(dirname(__file__)), 'recipes/snack', 'grilled-marinated-shrimp'),
            'bacon wrapped smokies': join(abspath(dirname(__file__)), 'recipes/snack', 'bacon-wrapped-smokies'),
            'cocktail meatballs': join(abspath(dirname(__file__)), 'recipes/snack', 'cocktail-meatballs'),
            'playgroup granola bars': join(abspath(dirname(__file__)), 'recipes/snack', 'playgroup-granola-bars'),
            'coconut shrimp i': join(abspath(dirname(__file__)), 'recipes/snack', 'coconut-shrimp-i'),
            'sugar coated pecans': join(abspath(dirname(__file__)), 'recipes/snack', 'sugar-coated-pecans'),
            'hummus iii': join(abspath(dirname(__file__)), 'recipes/snack', 'hummus-iii'),
            'asian lettuce wraps': join(abspath(dirname(__file__)), 'recipes/snack', 'asian-lettuce-wraps'),
            'brown sugar smokies': join(abspath(dirname(__file__)), 'recipes/snack', 'brown-sugar-smokies'),
            'seven layer taco dip': join(abspath(dirname(__file__)), 'recipes/snack', 'seven-layer-taco-dip'),
            'artichoke spinach dip restaurant style': join(abspath(dirname(__file__)), 'recipes/snack', 'artichoke-spinach-dip-restaurant-style'),
            'hot artichoke and spinach dip ii': join(abspath(dirname(__file__)), 'recipes/snack', 'hot-artichoke-and-spinach-dip-ii'),
            'double tomato bruschetta': join(abspath(dirname(__file__)), 'recipes/snack', 'double-tomato-bruschetta'),
            'restaurant style buffalo chicken wings': join(abspath(dirname(__file__)), 'recipes/snack', 'restaurant-style-buffalo-chicken-wings'),
            'jalapeno popper spread': join(abspath(dirname(__file__)), 'recipes/snack', 'jalapeno-popper-spread'),
            'annies fruit salsa and cinnamon chips': join(abspath(dirname(__file__)), 'recipes/snack', 'annies-fruit-salsa-and-cinnamon-chips'),
            'guacamole': join(abspath(dirname(__file__)), 'recipes/snack', 'guacamole'),
            'easy ham and cheese appetizer sandwiches': join(abspath(dirname(__file__)), 'recipes/snack', 'easy-ham-and-cheese-appetizer-sandwiches'),
            'artichoke hearts gratin': join(abspath(dirname(__file__)), 'recipes/snack', 'artichoke-hearts-gratin'),
            'mexican style shrimp cocktail': join(abspath(dirname(__file__)), 'recipes/snack', 'mexican-style-shrimp-cocktail'),
            'amazing no cook spinach artichoke dip': join(abspath(dirname(__file__)), 'recipes/snack', 'amazing-no-cook-spinach-artichoke-dip'),
            'strawberry bruschetta': join(abspath(dirname(__file__)), 'recipes/snack', 'strawberry-bruschetta'),
            'baked buffalo chicken dip': join(abspath(dirname(__file__)), 'recipes/snack', 'baked-buffalo-chicken-dip'),
            'perfect crab stuffed mushrooms': join(abspath(dirname(__file__)), 'recipes/snack', 'perfect-crab-stuffed-mushrooms'),
            'easy rumaki with pineapple': join(abspath(dirname(__file__)), 'recipes/snack', 'easy-rumaki-with-pineapple'),
            'cucumber and olive appetizers': join(abspath(dirname(__file__)), 'recipes/snack', 'cucumber-and-olive-appetizers'),
            'mast o khiar': join(abspath(dirname(__file__)), 'recipes/snack', 'mast-o-khiar'),
            'baked ham and cheese party sandwiches': join(abspath(dirname(__file__)), 'recipes/snack', 'baked-ham-and-cheese-party-sandwiches'),
            'chilean pebre sauce': join(abspath(dirname(__file__)), 'recipes/snack', 'chilean-pebre-sauce'),
            'baked kale chips': join(abspath(dirname(__file__)), 'recipes/snack', 'baked-kale-chips'),
            'mouth watering stuffed mushrooms': join(abspath(dirname(__file__)), 'recipes/snack', 'mouth-watering-stuffed-mushrooms'),
            'skyline dip': join(abspath(dirname(__file__)), 'recipes/snack', 'skyline-dip'),
            'southern pimento cheese': join(abspath(dirname(__file__)), 'recipes/snack', 'southern-pimento-cheese'),
            'buffalo chicken dip': join(abspath(dirname(__file__)), 'recipes/snack', 'buffalo-chicken-dip'),
            'no bake energy bites': join(abspath(dirname(__file__)), 'recipes/snack', 'no-bake-energy-bites'),
            'delaware scrapple dip': join(abspath(dirname(__file__)), 'recipes/snack', 'delaware-scrapple-dip'),
            'watermelon fire and ice salsa': join(abspath(dirname(__file__)), 'recipes/snack', 'watermelon-fire-and-ice-salsa'),
            'bacon dijon egg salad sandwich': join(abspath(dirname(__file__)), 'recipes/snack', 'bacon-dijon-egg-salad-sandwich'),    
        }        
        self.world_play_list = {
            'artichoke spinach dip restaurant style': join(abspath(dirname(__file__)), 'recipes/world', 'artichoke-spinach-dip-restaurant-style'),
            'mexican rice ii': join(abspath(dirname(__file__)), 'recipes/world', 'mexican-rice-ii'),
            'roasted garlic cauliflower': join(abspath(dirname(__file__)), 'recipes/world', 'roasted-garlic-cauliflower'),
            'double tomato bruschetta': join(abspath(dirname(__file__)), 'recipes/world', 'double-tomato-bruschetta'),
            'shepherds pie vi': join(abspath(dirname(__file__)), 'recipes/world', 'shepherds-pie-vi'),
            'awesome sausage apple and cranberry stuffing': join(abspath(dirname(__file__)), 'recipes/world', 'awesome-sausage-apple-and-cranberry-stuffing'),
            'szechwan shrimp': join(abspath(dirname(__file__)), 'recipes/world', 'szechwan-shrimp'),
            'italian sausage soup': join(abspath(dirname(__file__)), 'recipes/world', 'italian-sausage-soup'),
            'basic crepes': join(abspath(dirname(__file__)), 'recipes/world', 'basic-crepes'),
            'curried coconut chicken': join(abspath(dirname(__file__)), 'recipes/world', 'curried-coconut-chicken'),
            'roasted brussels sprouts': join(abspath(dirname(__file__)), 'recipes/world', 'roasted-brussels-sprouts'),
            'annies fruit salsa and cinnamon chips': join(abspath(dirname(__file__)), 'recipes/world', 'annies-fruit-salsa-and-cinnamon-chips'),
            'braised balsamic chicken': join(abspath(dirname(__file__)), 'recipes/world', 'braised-balsamic-chicken'),
            'creamy au gratin potatoes': join(abspath(dirname(__file__)), 'recipes/world', 'creamy-au-gratin-potatoes'),
            'chicken marsala': join(abspath(dirname(__file__)), 'recipes/world', 'chicken-marsala'),
            'quinoa and black beans': join(abspath(dirname(__file__)), 'recipes/world', 'quinoa-and-black-beans'),
            'chicken cordon bleu ii': join(abspath(dirname(__file__)), 'recipes/world', 'chicken-cordon-bleu-ii'),
            'taco seasoning i': join(abspath(dirname(__file__)), 'recipes/world', 'taco-seasoning-i'),
            'baked ziti i': join(abspath(dirname(__file__)), 'recipes/world', 'baked-ziti-i'),
            'indian style chicken and onions': join(abspath(dirname(__file__)), 'recipes/world', 'indian-style-chicken-and-onions'),
            'chef johns chicken kiev': join(abspath(dirname(__file__)), 'recipes/world', 'chef-johns-chicken-kiev'),
            'spongy japanese cheesecake': join(abspath(dirname(__file__)), 'recipes/world', 'spongy-japanese-cheesecake'),
            'easy chorizo street tacos': join(abspath(dirname(__file__)), 'recipes/world', 'easy-chorizo-street-tacos'),
            'greek lemon chicken and potato bake': join(abspath(dirname(__file__)), 'recipes/world', 'greek-lemon-chicken-and-potato-bake'),
            'spaghetti cacio e pepe': join(abspath(dirname(__file__)), 'recipes/world', 'spaghetti-cacio-e-pepe'),
            'labneh lebanese yogurt': join(abspath(dirname(__file__)), 'recipes/world', 'labneh-lebanese-yogurt'),
            'summer berry compote': join(abspath(dirname(__file__)), 'recipes/world', 'summer-berry-compote'),
            'chicken stir fry': join(abspath(dirname(__file__)), 'recipes/world', 'chicken-stir-fry'),
            'bang bang chicken': join(abspath(dirname(__file__)), 'recipes/world', 'bang-bang-chicken'),
            'the best steak marinade': join(abspath(dirname(__file__)), 'recipes/world', 'the-best-steak-marinade'),
            'my favorite sesame noodles': join(abspath(dirname(__file__)), 'recipes/world', 'my-favorite-sesame-noodles'),
            'chinese pepper steak': join(abspath(dirname(__file__)), 'recipes/world', 'chinese-pepper-steak'),
            'omas rhubarb cake': join(abspath(dirname(__file__)), 'recipes/world', 'omas-rhubarb-cake'),
            'juicy roasted chicken': join(abspath(dirname(__file__)), 'recipes/world', 'juicy-roasted-chicken'),
            'chef johns chicken tikka masala': join(abspath(dirname(__file__)), 'recipes/world', 'chef-johns-chicken-tikka-masala'),
            'authentic german potato salad': join(abspath(dirname(__file__)), 'recipes/world', 'authentic-german-potato-salad'),
            'spicy thai basil chicken pad krapow gai': join(abspath(dirname(__file__)), 'recipes/world', 'spicy-thai-basil-chicken-pad-krapow-gai'),
            'authentic bangladeshi beef curry': join(abspath(dirname(__file__)), 'recipes/world', 'authentic-bangladeshi-beef-curry'),
            'traditional mexican guacamole': join(abspath(dirname(__file__)), 'recipes/world', 'traditional-mexican-guacamole'),
            'easy bulgogi korean bbq beef': join(abspath(dirname(__file__)), 'recipes/world', 'easy-bulgogi-korean-bbq-beef'),
            'german rouladen': join(abspath(dirname(__file__)), 'recipes/world', 'german-rouladen'),
        }          
        self.beef_play_list = {
            'shepherds pie vi': join(abspath(dirname(__file__)), 'recipes/beef', 'shepherds-pie-vi'),
            'rempel family meatloaf': join(abspath(dirname(__file__)), 'recipes/beef', 'rempel-family-meatloaf'),
            'debdoozies blue ribbon chili': join(abspath(dirname(__file__)), 'recipes/beef', 'debdoozies-blue-ribbon-chili'),
            'beef stew vi': join(abspath(dirname(__file__)), 'recipes/beef', 'beef-stew-vi'),
            'slow cooker pepper steak': join(abspath(dirname(__file__)), 'recipes/beef', 'slow-cooker-pepper-steak'),
            'italian spaghetti sauce with meatballs': join(abspath(dirname(__file__)), 'recipes/beef', 'italian-spaghetti-sauce-with-meatballs'),
            'burrito pie': join(abspath(dirname(__file__)), 'recipes/beef', 'burrito-pie'),
            'easy slow cooker french dip': join(abspath(dirname(__file__)), 'recipes/beef', 'easy-slow-cooker-french-dip'),
            'slow cooker beef stroganoff i': join(abspath(dirname(__file__)), 'recipes/beef', 'slow-cooker-beef-stroganoff-i'),
            'salisbury steak': join(abspath(dirname(__file__)), 'recipes/beef', 'salisbury-steak'),
            'slow cooker beef stew i': join(abspath(dirname(__file__)), 'recipes/beef', 'slow-cooker-beef-stew-i'),
            'sloppy joes ii': join(abspath(dirname(__file__)), 'recipes/beef', 'sloppy-joes-ii'),
            'easy meatloaf': join(abspath(dirname(__file__)), 'recipes/beef', 'easy-meatloaf'),
            'boilermaker tailgate chili': join(abspath(dirname(__file__)), 'recipes/beef', 'boilermaker-tailgate-chili'),
            'baked ziti i': join(abspath(dirname(__file__)), 'recipes/beef', 'baked-ziti-i'),
            'awesome slow cooker pot roast': join(abspath(dirname(__file__)), 'recipes/beef', 'awesome-slow-cooker-pot-roast'),
            'grilled steak tips with chimichurri': join(abspath(dirname(__file__)), 'recipes/beef', 'grilled-steak-tips-with-chimichurri'),
            'prime rib au jus with yorkshire pudding': join(abspath(dirname(__file__)), 'recipes/beef', 'prime-rib-au-jus-with-yorkshire-pudding'),
            'keema aloo ground beef and potatoes': join(abspath(dirname(__file__)), 'recipes/beef', 'keema-aloo-ground-beef-and-potatoes'),
            'tennessee meatloaf': join(abspath(dirname(__file__)), 'recipes/beef', 'tennessee-meatloaf'),
            'abuelas picadillo': join(abspath(dirname(__file__)), 'recipes/beef', 'abuelas-picadillo'),
            'the real deal korean beef ribs': join(abspath(dirname(__file__)), 'recipes/beef', 'the-real-deal-korean-beef-ribs'),
            'chicago inspired italian beef sandwich': join(abspath(dirname(__file__)), 'recipes/beef', 'chicago-inspired-italian-beef-sandwich'),
            'a minnesotans beef and macaroni hotdish': join(abspath(dirname(__file__)), 'recipes/beef', 'a-minnesotans-beef-and-macaroni-hotdish'),
            'carne asada marinade': join(abspath(dirname(__file__)), 'recipes/beef', 'carne-asada-marinade'),
            'spaghetti sauce with ground beef': join(abspath(dirname(__file__)), 'recipes/beef', 'spaghetti-sauce-with-ground-beef'),
            'chinese pepper steak': join(abspath(dirname(__file__)), 'recipes/beef', 'chinese-pepper-steak'),
            'brown sugar meatloaf': join(abspath(dirname(__file__)), 'recipes/beef', 'brown-sugar-meatloaf'),
            'chef johns stuffed peppers': join(abspath(dirname(__file__)), 'recipes/beef', 'chef-johns-stuffed-peppers'),
            'baked spaghetti': join(abspath(dirname(__file__)), 'recipes/beef', 'baked-spaghetti'),
            'meatball nirvana': join(abspath(dirname(__file__)), 'recipes/beef', 'meatball-nirvana'),
            'chef johns italian meatballs': join(abspath(dirname(__file__)), 'recipes/beef', 'chef-johns-italian-meatballs'),
            'beef stroganoff for instant pot': join(abspath(dirname(__file__)), 'recipes/beef', 'beef-stroganoff-for-instant-pot'),
            'hamburger steak with onions and gravy': join(abspath(dirname(__file__)), 'recipes/beef', 'hamburger-steak-with-onions-and-gravy'),
            'worlds best lasagna': join(abspath(dirname(__file__)), 'recipes/beef', 'worlds-best-lasagna'),
            'chef johns grilled mojo beef': join(abspath(dirname(__file__)), 'recipes/beef', 'chef-johns-grilled-mojo-beef'),
            'standing roast beef brined': join(abspath(dirname(__file__)), 'recipes/beef', 'standing-roast-beef-brined'),
        }       
        self.pork_play_list = {
            'italian breaded pork chops': join(abspath(dirname(__file__)), 'recipes/pork', 'italian-breaded-pork-chops'),
            'caramel apple pork chops': join(abspath(dirname(__file__)), 'recipes/pork', 'caramel-apple-pork-chops'),
            'italian sausage soup with tortellini': join(abspath(dirname(__file__)), 'recipes/pork', 'italian-sausage-soup-with-tortellini'),
            'brown sugar smokies': join(abspath(dirname(__file__)), 'recipes/pork', 'brown-sugar-smokies'),
            'absolutely ultimate potato soup': join(abspath(dirname(__file__)), 'recipes/pork', 'absolutely-ultimate-potato-soup'),
            'cheesy ham and hash brown casserole': join(abspath(dirname(__file__)), 'recipes/pork', 'cheesy-ham-and-hash-brown-casserole'),
            'slow cooker texas pulled pork': join(abspath(dirname(__file__)), 'recipes/pork', 'slow-cooker-texas-pulled-pork'),
            'colleens slow cooker jambalaya': join(abspath(dirname(__file__)), 'recipes/pork', 'colleens-slow-cooker-jambalaya'),
            'marinated baked pork chops': join(abspath(dirname(__file__)), 'recipes/pork', 'marinated-baked-pork-chops'),
            'super delicious zuppa toscana': join(abspath(dirname(__file__)), 'recipes/pork', 'super-delicious-zuppa-toscana'),
            'italian sausage soup': join(abspath(dirname(__file__)), 'recipes/pork', 'italian-sausage-soup'),
            'amazing pork tenderloin in the slow cooker': join(abspath(dirname(__file__)), 'recipes/pork', 'amazing-pork-tenderloin-in-the-slow-cooker'),
            'bbq pork for sandwiches': join(abspath(dirname(__file__)), 'recipes/pork', 'bbq-pork-for-sandwiches'),
            'bow ties with sausage tomatoes and cream': join(abspath(dirname(__file__)), 'recipes/pork', 'bow-ties-with-sausage-tomatoes-and-cream'),
            'slow cooker pulled pork': join(abspath(dirname(__file__)), 'recipes/pork', 'slow-cooker-pulled-pork'),
            'baked pork chops i': join(abspath(dirname(__file__)), 'recipes/pork', 'baked-pork-chops-i'),
            'boilermaker tailgate chili': join(abspath(dirname(__file__)), 'recipes/pork', 'boilermaker-tailgate-chili'),
            'delicious ham and potato soup': join(abspath(dirname(__file__)), 'recipes/pork', 'delicious-ham-and-potato-soup'),
            'spam fries with spicy garlic sriracha dipping sauce': join(abspath(dirname(__file__)), 'recipes/pork', 'spam-fries-with-spicy-garlic-sriracha-dipping-sauce'),
            'slow cooker carnitas': join(abspath(dirname(__file__)), 'recipes/pork', 'slow-cooker-carnitas'),
            'okinawa shoyu pork': join(abspath(dirname(__file__)), 'recipes/pork', 'okinawa-shoyu-pork'),
            'super easy pulled pork sandwiches': join(abspath(dirname(__file__)), 'recipes/pork', 'super-easy-pulled-pork-sandwiches'),
            'mushroom pork chops': join(abspath(dirname(__file__)), 'recipes/pork', 'mushroom-pork-chops'),
            'instant pot baby back ribs': join(abspath(dirname(__file__)), 'recipes/pork', 'instant-pot-baby-back-ribs'),
            'bucatini allamatriciana': join(abspath(dirname(__file__)), 'recipes/pork', 'bucatini-allamatriciana'),
            'cheesy ham and corn chowder': join(abspath(dirname(__file__)), 'recipes/pork', 'cheesy-ham-and-corn-chowder'),
            'sweet pork for burritos': join(abspath(dirname(__file__)), 'recipes/pork', 'sweet-pork-for-burritos'),
            'balsamic roasted pork loin': join(abspath(dirname(__file__)), 'recipes/pork', 'balsamic-roasted-pork-loin'),
            'chef johns stuffed peppers': join(abspath(dirname(__file__)), 'recipes/pork', 'chef-johns-stuffed-peppers'),
            'slow cooker baby back ribs': join(abspath(dirname(__file__)), 'recipes/pork', 'slow-cooker-baby-back-ribs'),
            'baked bbq baby back ribs': join(abspath(dirname(__file__)), 'recipes/pork', 'baked-bbq-baby-back-ribs'),
            'easy sausage gravy and biscuits': join(abspath(dirname(__file__)), 'recipes/pork', 'easy-sausage-gravy-and-biscuits'),
            'delaware scrapple dip': join(abspath(dirname(__file__)), 'recipes/pork', 'delaware-scrapple-dip'),
            'chef johns italian meatballs': join(abspath(dirname(__file__)), 'recipes/pork', 'chef-johns-italian-meatballs'),
            'worlds best honey garlic pork chops': join(abspath(dirname(__file__)), 'recipes/pork', 'worlds-best-honey-garlic-pork-chops'),
            'worlds best lasagna': join(abspath(dirname(__file__)), 'recipes/pork', 'worlds-best-lasagna'),
            'pineapple sticky ribs': join(abspath(dirname(__file__)), 'recipes/pork', 'pineapple-sticky-ribs'),
            'orange and milk braised pork carnitas': join(abspath(dirname(__file__)), 'recipes/pork', 'orange-and-milk-braised-pork-carnitas'),
     
        }        
        self.vegan_play_list = {
            'vegan brownies': join(abspath(dirname(__file__)), 'recipes/vegan', 'vegan-brownies'),
            'real hummus': join(abspath(dirname(__file__)), 'recipes/vegan', 'real-hummus'),
            'spiced pumpkin seeds': join(abspath(dirname(__file__)), 'recipes/vegan', 'spiced-pumpkin-seeds'),
            'ds famous salsa': join(abspath(dirname(__file__)), 'recipes/vegan', 'ds-famous-salsa'),
            'strawberry oatmeal breakfast smoothie': join(abspath(dirname(__file__)), 'recipes/vegan', 'strawberry-oatmeal-breakfast-smoothie'),
            'healthy banana cookies': join(abspath(dirname(__file__)), 'recipes/vegan', 'healthy-banana-cookies'),
            'spicy black bean vegetable soup': join(abspath(dirname(__file__)), 'recipes/vegan', 'spicy-black-bean-vegetable-soup'),
            'roasted garlic lemon broccoli': join(abspath(dirname(__file__)), 'recipes/vegan', 'roasted-garlic-lemon-broccoli'),
            'spicy bean salsa': join(abspath(dirname(__file__)), 'recipes/vegan', 'spicy-bean-salsa'),
            'black bean and corn salad ii': join(abspath(dirname(__file__)), 'recipes/vegan', 'black-bean-and-corn-salad-ii'),
            'spanish rice ii': join(abspath(dirname(__file__)), 'recipes/vegan', 'spanish-rice-ii'),
            'the best vegetarian chili in the world': join(abspath(dirname(__file__)), 'recipes/vegan', 'the-best-vegetarian-chili-in-the-world'),
            'hummus iii': join(abspath(dirname(__file__)), 'recipes/vegan', 'hummus-iii'),
            'refried beans without the refry': join(abspath(dirname(__file__)), 'recipes/vegan', 'refried-beans-without-the-refry'),
            'cranberry sauce': join(abspath(dirname(__file__)), 'recipes/vegan', 'cranberry-sauce'),
            'lentil soup': join(abspath(dirname(__file__)), 'recipes/vegan', 'lentil-soup'),
            'roasted brussels sprouts': join(abspath(dirname(__file__)), 'recipes/vegan', 'roasted-brussels-sprouts'),
            'quinoa and black beans': join(abspath(dirname(__file__)), 'recipes/vegan', 'quinoa-and-black-beans'),
            'guacamole': join(abspath(dirname(__file__)), 'recipes/vegan', 'guacamole'),
            'chai spice cheesecake': join(abspath(dirname(__file__)), 'recipes/vegan', 'chai-spice-cheesecake'),
            'vegan tomato soup': join(abspath(dirname(__file__)), 'recipes/vegan', 'vegan-tomato-soup'),
            'couscous with olives and sun dried tomato': join(abspath(dirname(__file__)), 'recipes/vegan', 'couscous-with-olives-and-sun-dried-tomato'),
            'steamed vegan rice cakes banh bo hap': join(abspath(dirname(__file__)), 'recipes/vegan', 'steamed-vegan-rice-cakes-banh-bo-hap'),
            'rice paper fake bacon': join(abspath(dirname(__file__)), 'recipes/vegan', 'rice-paper-fake-bacon'),
            'vegan zucchini noodles with chickpeas and zucchini blossoms': join(abspath(dirname(__file__)), 'recipes/vegan', 'vegan-zucchini-noodles-with-chickpeas-and-zucchini-blossoms'),
            'ultimate tofu breakfast burrito bowls': join(abspath(dirname(__file__)), 'recipes/vegan', 'ultimate-tofu-breakfast-burrito-bowls'),
            'vegan mug cake with pineapple and mint': join(abspath(dirname(__file__)), 'recipes/vegan', 'vegan-mug-cake-with-pineapple-and-mint'),
            'vegan potato soup': join(abspath(dirname(__file__)), 'recipes/vegan', 'vegan-potato-soup'),
            'vegan blueberry crisp': join(abspath(dirname(__file__)), 'recipes/vegan', 'vegan-blueberry-crisp'),
            'shanghai noodle salad': join(abspath(dirname(__file__)), 'recipes/vegan', 'shanghai-noodle-salad'),
            'instant pot roasted brussels sprouts': join(abspath(dirname(__file__)), 'recipes/vegan', 'instant-pot-roasted-brussels-sprouts'),
            'churros': join(abspath(dirname(__file__)), 'recipes/vegan', 'churros'),
            'briam greek baked zucchini and potatoes': join(abspath(dirname(__file__)), 'recipes/vegan', 'briam-greek-baked-zucchini-and-potatoes'),
            'greek lentil soup fakes': join(abspath(dirname(__file__)), 'recipes/vegan', 'greek-lentil-soup-fakes'),
            'strawberry banana breeze smoothie': join(abspath(dirname(__file__)), 'recipes/vegan', 'strawberry-banana-breeze-smoothie'),
            'chocolate banana sorbet': join(abspath(dirname(__file__)), 'recipes/vegan', 'chocolate-banana-sorbet'),
            'chilean pebre sauce': join(abspath(dirname(__file__)), 'recipes/vegan', 'chilean-pebre-sauce'),
            'zesty quinoa salad': join(abspath(dirname(__file__)), 'recipes/vegan', 'zesty-quinoa-salad'),
     
        }        
        
        self.cookies_play_list = {
            'oatmeal peanut butter cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'oatmeal-peanut-butter-cookies'),
            'zucchini brownies': join(abspath(dirname(__file__)), 'recipes/cookies', 'zucchini-brownies'),
            'the best lemon bars': join(abspath(dirname(__file__)), 'recipes/cookies', 'the-best-lemon-bars'),
            'classic peanut butter cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'classic-peanut-butter-cookies'),
            'chocolate chocolate chip cookies i': join(abspath(dirname(__file__)), 'recipes/cookies', 'chocolate-chocolate-chip-cookies-i'),
            'iced pumpkin cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'iced-pumpkin-cookies'),
            'peanut butter cup cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'peanut-butter-cup-cookies'),
            'soft oatmeal cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'soft-oatmeal-cookies'),
            'chewy chocolate chip oatmeal cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'chewy-chocolate-chip-oatmeal-cookies'),
            'beths spicy oatmeal raisin cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'beths-spicy-oatmeal-raisin-cookies'),
            'big soft ginger cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'big-soft-ginger-cookies'),
            'mrs siggs snickerdoodles': join(abspath(dirname(__file__)), 'recipes/cookies', 'mrs-siggs-snickerdoodles'),
            'easy sugar cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'easy-sugar-cookies'),
            'the best rolled sugar cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'the-best-rolled-sugar-cookies'),
            'award winning soft chocolate chip cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'award-winning-soft-chocolate-chip-cookies'),
            'best big fat chewy chocolate chip cookie': join(abspath(dirname(__file__)), 'recipes/cookies', 'best-big-fat-chewy-chocolate-chip-cookie'),
            'best brownies': join(abspath(dirname(__file__)), 'recipes/cookies', 'best-brownies'),
            'best chocolate chip cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'best-chocolate-chip-cookies'),
            'cornes de gazelle gazelle horns': join(abspath(dirname(__file__)), 'recipes/cookies', 'cornes-de-gazelle-gazelle-horns'),
            'easy chewy flourless peanut butter cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'easy-chewy-flourless-peanut-butter-cookies'),
            'lime bars': join(abspath(dirname(__file__)), 'recipes/cookies', 'lime-bars'),
            'chocolate cheesecake cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'chocolate-cheesecake-cookies'),
            'gluten free magic cookie bars': join(abspath(dirname(__file__)), 'recipes/cookies', 'gluten-free-magic-cookie-bars'),
            'spicy mexican hot chocolate cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'spicy-mexican-hot-chocolate-cookies'),
            'red velvet coconut biscotti': join(abspath(dirname(__file__)), 'recipes/cookies', 'red-velvet-coconut-biscotti'),
            'cardamom and espresso chocolate chip cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'cardamom-and-espresso-chocolate-chip-cookies'),
            'mini chocolate chip shortbread cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'mini-chocolate-chip-shortbread-cookies'),
            'coconut macaroons iii': join(abspath(dirname(__file__)), 'recipes/cookies', 'coconut-macaroons-iii'),
            'chef johns peanut butter cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'chef-johns-peanut-butter-cookies'),
            'chef johns lemon bars': join(abspath(dirname(__file__)), 'recipes/cookies', 'chef-johns-lemon-bars'),
            'chewy sugar cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'chewy-sugar-cookies'),
            'original nestle toll house chocolate chip cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'original-nestle-toll-house-chocolate-chip-cookies'),
            'cherry cheesecake brownies': join(abspath(dirname(__file__)), 'recipes/cookies', 'cherry-cheesecake-brownies'),
            'baklava pinwheel cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'baklava-pinwheel-cookies'),
            'brookes best bombshell brownies': join(abspath(dirname(__file__)), 'recipes/cookies', 'brookes-best-bombshell-brownies'),
            'best ever buckeye brownies': join(abspath(dirname(__file__)), 'recipes/cookies', 'best-ever-buckeye-brownies'),
            'grandmas lace cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'grandmas-lace-cookies'),
            'chocolate hazelnut spread no bakes': join(abspath(dirname(__file__)), 'recipes/cookies', 'chocolate-hazelnut-spread-no-bakes'),
            'lemon bars i': join(abspath(dirname(__file__)), 'recipes/cookies', 'lemon-bars-i'),
            'chef johns chocolate chip cookies': join(abspath(dirname(__file__)), 'recipes/cookies', 'chef-johns-chocolate-chip-cookies'),
            'refrigerator cookies iii': join(abspath(dirname(__file__)), 'recipes/cookies', 'refrigerator-cookies-iii'),
            'peanut butter bars i': join(abspath(dirname(__file__)), 'recipes/cookies', 'peanut-butter-bars-i'),
        }        
        self.cake_play_list = {
            'tres leches milk cake': join(abspath(dirname(__file__)), 'recipes/cake', 'tres-leches-milk-cake'),
            'chocolate cavity maker cake': join(abspath(dirname(__file__)), 'recipes/cake', 'chocolate-cavity-maker-cake'),
            'best carrot cake ever': join(abspath(dirname(__file__)), 'recipes/cake', 'best-carrot-cake-ever'),
            'dark chocolate cake i': join(abspath(dirname(__file__)), 'recipes/cake', 'dark-chocolate-cake-i'),
            'davids yellow cake': join(abspath(dirname(__file__)), 'recipes/cake', 'davids-yellow-cake'),
            'golden rum cake': join(abspath(dirname(__file__)), 'recipes/cake', 'golden-rum-cake'),
            'cake balls': join(abspath(dirname(__file__)), 'recipes/cake', 'cake-balls'),
            'sopapilla cheesecake pie': join(abspath(dirname(__file__)), 'recipes/cake', 'sopapilla-cheesecake-pie'),
            'extreme chocolate cake': join(abspath(dirname(__file__)), 'recipes/cake', 'extreme-chocolate-cake'),
            'black magic cake': join(abspath(dirname(__file__)), 'recipes/cake', 'black-magic-cake'),
            'sams famous carrot cake': join(abspath(dirname(__file__)), 'recipes/cake', 'sams-famous-carrot-cake'),
            'white chocolate raspberry cheesecake': join(abspath(dirname(__file__)), 'recipes/cake', 'white-chocolate-raspberry-cheesecake'),
            'one bowl chocolate cake iii': join(abspath(dirname(__file__)), 'recipes/cake', 'one-bowl-chocolate-cake-iii'),
            'simple white cake': join(abspath(dirname(__file__)), 'recipes/cake', 'simple-white-cake'),
            'double layer pumpkin cheesecake': join(abspath(dirname(__file__)), 'recipes/cake', 'double-layer-pumpkin-cheesecake'),
            'carrot cake iii': join(abspath(dirname(__file__)), 'recipes/cake', 'carrot-cake-iii'),
            'chantals new york cheesecake': join(abspath(dirname(__file__)), 'recipes/cake', 'chantals-new-york-cheesecake'),
            'too much chocolate cake': join(abspath(dirname(__file__)), 'recipes/cake', 'too-much-chocolate-cake'),
            'nutella cream cheese pound cake': join(abspath(dirname(__file__)), 'recipes/cake', 'nutella-cream-cheese-pound-cake'),
            'spiced orange olive oil cake': join(abspath(dirname(__file__)), 'recipes/cake', 'spiced-orange-olive-oil-cake'),
            'red velvet strawberry cake': join(abspath(dirname(__file__)), 'recipes/cake', 'red-velvet-strawberry-cake'),
            'plum kuchen': join(abspath(dirname(__file__)), 'recipes/cake', 'plum-kuchen'),
            'banana split cupcakes': join(abspath(dirname(__file__)), 'recipes/cake', 'banana-split-cupcakes'),
            'grandmas skillet pineapple upside down cake': join(abspath(dirname(__file__)), 'recipes/cake', 'grandmas-skillet-pineapple-upside-down-cake'),
            'slow cooker peach upside down cake': join(abspath(dirname(__file__)), 'recipes/cake', 'slow-cooker-peach-upside-down-cake'),
            'blueberry muffin cake': join(abspath(dirname(__file__)), 'recipes/cake', 'blueberry-muffin-cake'),
            'surprise inside independence cake': join(abspath(dirname(__file__)), 'recipes/cake', 'surprise-inside-independence-cake'),
            'lemon buttermilk pound cake with aunt evelyns lemon glaze': join(abspath(dirname(__file__)), 'recipes/cake', 'lemon-buttermilk-pound-cake-with-aunt-evelyns-lemon-glaze'),
            'lemon meringue cheesecake': join(abspath(dirname(__file__)), 'recipes/cake', 'lemon-meringue-cheesecake'),
            'classic strawberry shortcakes': join(abspath(dirname(__file__)), 'recipes/cake', 'classic-strawberry-shortcakes'),
            'coconut cream pound cake': join(abspath(dirname(__file__)), 'recipes/cake', 'coconut-cream-pound-cake'),
            'keto raspberry cheesecake': join(abspath(dirname(__file__)), 'recipes/cake', 'keto-raspberry-cheesecake'),
            'chocolate cupcakes': join(abspath(dirname(__file__)), 'recipes/cake', 'chocolate-cupcakes'),
            'quick lemon cheesecake': join(abspath(dirname(__file__)), 'recipes/cake', 'quick-lemon-cheesecake'),
            'banana cake vi': join(abspath(dirname(__file__)), 'recipes/cake', 'banana-cake-vi'),
            'omas rhubarb cake': join(abspath(dirname(__file__)), 'recipes/cake', 'omas-rhubarb-cake'),
            'sweetheart cupcakes': join(abspath(dirname(__file__)), 'recipes/cake', 'sweetheart-cupcakes'),
            'nannies hot milk sponge cake': join(abspath(dirname(__file__)), 'recipes/cake', 'nannies-hot-milk-sponge-cake'),
            'texas sheet cake v': join(abspath(dirname(__file__)), 'recipes/cake', 'texas-sheet-cake-v'),
            'no bake cheesecake flag cake': join(abspath(dirname(__file__)), 'recipes/cake', 'no-bake-cheesecake-flag-cake'),
            'tiramisu layer cake': join(abspath(dirname(__file__)), 'recipes/cake', 'tiramisu-layer-cake'),

        }        
        self.breakfast_play_list = {
            'french toast i': join(abspath(dirname(__file__)), 'recipes/breakfast', 'french-toast-i'),
            'christmas breakfast sausage casserole': join(abspath(dirname(__file__)), 'recipes/breakfast', 'christmas-breakfast-sausage-casserole'),
            'overnight blueberry french toast': join(abspath(dirname(__file__)), 'recipes/breakfast', 'overnight-blueberry-french-toast'),
            'pumpkin bread iv': join(abspath(dirname(__file__)), 'recipes/breakfast', 'pumpkin-bread-iv'),
            'monkey bread i': join(abspath(dirname(__file__)), 'recipes/breakfast', 'monkey-bread-i'),
            'banana pancakes i': join(abspath(dirname(__file__)), 'recipes/breakfast', 'banana-pancakes-i'),
            'spinach quiche': join(abspath(dirname(__file__)), 'recipes/breakfast', 'spinach-quiche'),
            'cheesy ham and hash brown casserole': join(abspath(dirname(__file__)), 'recipes/breakfast', 'cheesy-ham-and-hash-brown-casserole'),
            'pumpkin pancakes': join(abspath(dirname(__file__)), 'recipes/breakfast', 'pumpkin-pancakes'),
            'crustless spinach quiche': join(abspath(dirname(__file__)), 'recipes/breakfast', 'crustless-spinach-quiche'),
            'basic crepes': join(abspath(dirname(__file__)), 'recipes/breakfast', 'basic-crepes'),
            'buttermilk pancakes ii': join(abspath(dirname(__file__)), 'recipes/breakfast', 'buttermilk-pancakes-ii'),
            'fluffy french toast': join(abspath(dirname(__file__)), 'recipes/breakfast', 'fluffy-french-toast'),
            'waffles i': join(abspath(dirname(__file__)), 'recipes/breakfast', 'waffles-i'),
            'banana sour cream bread': join(abspath(dirname(__file__)), 'recipes/breakfast', 'banana-sour-cream-bread'),
            'moms zucchini bread': join(abspath(dirname(__file__)), 'recipes/breakfast', 'moms-zucchini-bread'),
            'downeast maine pumpkin bread': join(abspath(dirname(__file__)), 'recipes/breakfast', 'downeast-maine-pumpkin-bread'),
            'good old fashioned pancakes': join(abspath(dirname(__file__)), 'recipes/breakfast', 'good-old-fashioned-pancakes'),
            'breakfast pita pizza': join(abspath(dirname(__file__)), 'recipes/breakfast', 'breakfast-pita-pizza'),
            'french toast souffle': join(abspath(dirname(__file__)), 'recipes/breakfast', 'french-toast-souffle'),
            'honey nut granola': join(abspath(dirname(__file__)), 'recipes/breakfast', 'honey-nut-granola'),
            'ultimate tofu breakfast burrito bowls': join(abspath(dirname(__file__)), 'recipes/breakfast', 'ultimate-tofu-breakfast-burrito-bowls'),
            'favorite banana blueberry quick bread': join(abspath(dirname(__file__)), 'recipes/breakfast', 'favorite-banana-blueberry-quick-bread'),
            'herb sausage and cheese dutch baby': join(abspath(dirname(__file__)), 'recipes/breakfast', 'herb-sausage-and-cheese-dutch-baby'),
            'easy quiche': join(abspath(dirname(__file__)), 'recipes/breakfast', 'easy-quiche'),
            'puff pastry waffles': join(abspath(dirname(__file__)), 'recipes/breakfast', 'puff-pastry-waffles'),
            'black and blueberry muffins': join(abspath(dirname(__file__)), 'recipes/breakfast', 'black-and-blueberry-muffins'),
            'lolas horchata': join(abspath(dirname(__file__)), 'recipes/breakfast', 'lolas-horchata'),
            'strawberry banana breeze smoothie': join(abspath(dirname(__file__)), 'recipes/breakfast', 'strawberry-banana-breeze-smoothie'),
            'chef johns banana bread': join(abspath(dirname(__file__)), 'recipes/breakfast', 'chef-johns-banana-bread'),
            'baked ham and cheese party sandwiches': join(abspath(dirname(__file__)), 'recipes/breakfast', 'baked-ham-and-cheese-party-sandwiches'),
            'cheesy amish breakfast casserole': join(abspath(dirname(__file__)), 'recipes/breakfast', 'cheesy-amish-breakfast-casserole'),
            'fluffy and delicious pancakes': join(abspath(dirname(__file__)), 'recipes/breakfast', 'fluffy-and-delicious-pancakes'),
            'peanut butter banana smoothie': join(abspath(dirname(__file__)), 'recipes/breakfast', 'peanut-butter-banana-smoothie'),
            'easy sausage gravy and biscuits': join(abspath(dirname(__file__)), 'recipes/breakfast', 'easy-sausage-gravy-and-biscuits'),
            'summer garden crustless quiche': join(abspath(dirname(__file__)), 'recipes/breakfast', 'summer-garden-crustless-quiche'),
            'fluffy pancakes': join(abspath(dirname(__file__)), 'recipes/breakfast', 'fluffy-pancakes'),
            'on the farm scrambled eggs': join(abspath(dirname(__file__)), 'recipes/breakfast', 'on-the-farm-scrambled-eggs'),
            'classic waffles': join(abspath(dirname(__file__)), 'recipes/breakfast', 'classic-waffles'),

        }        
        self.bread_play_list = {
            'bazlama turkish flat bread': join(abspath(dirname(__file__)), 'recipes/bread', 'bazlama-turkish-flat-bread'),
            'grandma johnsons scones': join(abspath(dirname(__file__)), 'recipes/bread', 'grandma-johnsons-scones'),
            'homesteader cornbread': join(abspath(dirname(__file__)), 'recipes/bread', 'homesteader-cornbread'),
            'simple scones': join(abspath(dirname(__file__)), 'recipes/bread', 'simple-scones'),
            'sweet dinner rolls': join(abspath(dirname(__file__)), 'recipes/bread', 'sweet-dinner-rolls'),
            'golden sweet cornbread': join(abspath(dirname(__file__)), 'recipes/bread', 'golden-sweet-cornbread'),
            'banana muffins ii': join(abspath(dirname(__file__)), 'recipes/bread', 'banana-muffins-ii'),
            'jps big daddy biscuits': join(abspath(dirname(__file__)), 'recipes/bread', 'jps-big-daddy-biscuits'),
            'banana sour cream bread': join(abspath(dirname(__file__)), 'recipes/bread', 'banana-sour-cream-bread'),
            'amish white bread': join(abspath(dirname(__file__)), 'recipes/bread', 'amish-white-bread'),
            'grandmothers buttermilk cornbread': join(abspath(dirname(__file__)), 'recipes/bread', 'grandmothers-buttermilk-cornbread'),
            'clone of a cinnabon': join(abspath(dirname(__file__)), 'recipes/bread', 'clone-of-a-cinnabon'),
            'janets rich banana bread': join(abspath(dirname(__file__)), 'recipes/bread', 'janets-rich-banana-bread'),
            'moms zucchini bread': join(abspath(dirname(__file__)), 'recipes/bread', 'moms-zucchini-bread'),
            'downeast maine pumpkin bread': join(abspath(dirname(__file__)), 'recipes/bread', 'downeast-maine-pumpkin-bread'),
            'to die for blueberry muffins': join(abspath(dirname(__file__)), 'recipes/bread', 'to-die-for-blueberry-muffins'),
            'banana crumb muffins': join(abspath(dirname(__file__)), 'recipes/bread', 'banana-crumb-muffins'),
            'injera ethiopian teff bread': join(abspath(dirname(__file__)), 'recipes/bread', 'injera-ethiopian-teff-bread'),
            'brown butter pineapple corn muffins': join(abspath(dirname(__file__)), 'recipes/bread', 'brown-butter-pineapple-corn-muffins'),
            'dutch oven whole wheat bread': join(abspath(dirname(__file__)), 'recipes/bread', 'dutch-oven-whole-wheat-bread'),
            'strawberry bread': join(abspath(dirname(__file__)), 'recipes/bread', 'strawberry-bread'),
            'cloud bread with italian herbs': join(abspath(dirname(__file__)), 'recipes/bread', 'cloud-bread-with-italian-herbs'),
            'broa portuguese cornbread': join(abspath(dirname(__file__)), 'recipes/bread', 'broa-portuguese-cornbread'),
            'burger or hot dog buns': join(abspath(dirname(__file__)), 'recipes/bread', 'burger-or-hot-dog-buns'),
            'donut muffins': join(abspath(dirname(__file__)), 'recipes/bread', 'donut-muffins'),
            'chef johns blueberry muffins': join(abspath(dirname(__file__)), 'recipes/bread', 'chef-johns-blueberry-muffins'),
            'chef johns banana bread': join(abspath(dirname(__file__)), 'recipes/bread', 'chef-johns-banana-bread'),
            'best bread machine bread': join(abspath(dirname(__file__)), 'recipes/bread', 'best-bread-machine-bread'),
            'basic biscuits': join(abspath(dirname(__file__)), 'recipes/bread', 'basic-biscuits'),
            'homemade hamburger buns': join(abspath(dirname(__file__)), 'recipes/bread', 'homemade-hamburger-buns'),
            'chef johns buttermilk biscuits': join(abspath(dirname(__file__)), 'recipes/bread', 'chef-johns-buttermilk-biscuits'),
            'blueberry zucchini bread': join(abspath(dirname(__file__)), 'recipes/bread', 'blueberry-zucchini-bread'),
            'quick cinnamon rolls': join(abspath(dirname(__file__)), 'recipes/bread', 'quick-cinnamon-rolls'),
            'best keto bread': join(abspath(dirname(__file__)), 'recipes/bread', 'best-keto-bread'),
            'no knead artisan style bread': join(abspath(dirname(__file__)), 'recipes/bread', 'no-knead-artisan-style-bread'),
            'pizza on the grill i': join(abspath(dirname(__file__)), 'recipes/bread', 'pizza-on-the-grill-i'),
            'hawaiian banana nut bread': join(abspath(dirname(__file__)), 'recipes/bread', 'hawaiian-banana-nut-bread'),
            'banana banana bread': join(abspath(dirname(__file__)), 'recipes/bread', 'banana-banana-bread'),
            
        }        
        
        self.chicken_play_list = {
            'spicy garlic lime chicken': join(abspath(dirname(__file__)), 'recipes/chicken', 'spicy-garlic-lime-chicken'),
            'curried coconut chicken': join(abspath(dirname(__file__)), 'recipes/chicken', 'curried-coconut-chicken'),
            'angel chicken pasta': join(abspath(dirname(__file__)), 'recipes/chicken', 'angel-chicken-pasta'),
            'slow cooker chicken stroganoff': join(abspath(dirname(__file__)), 'recipes/chicken', 'slow-cooker-chicken-stroganoff'),
            'sweet sticky and spicy chicken': join(abspath(dirname(__file__)), 'recipes/chicken', 'sweet-sticky-and-spicy-chicken'),
            'roast sticky chicken rotisserie style': join(abspath(dirname(__file__)), 'recipes/chicken', 'roast-sticky-chicken-rotisserie-style'),
            'rosemary ranch chicken kabobs': join(abspath(dirname(__file__)), 'recipes/chicken', 'rosemary-ranch-chicken-kabobs'),
            'chicken enchiladas ii': join(abspath(dirname(__file__)), 'recipes/chicken', 'chicken-enchiladas-ii'),
            'braised balsamic chicken': join(abspath(dirname(__file__)), 'recipes/chicken', 'braised-balsamic-chicken'),
            'salsa chicken': join(abspath(dirname(__file__)), 'recipes/chicken', 'salsa-chicken'),
            'buffalo chicken dip': join(abspath(dirname(__file__)), 'recipes/chicken', 'buffalo-chicken-dip'),
            'slow cooker chicken tortilla soup': join(abspath(dirname(__file__)), 'recipes/chicken', 'slow-cooker-chicken-tortilla-soup'),
            'chicken marsala': join(abspath(dirname(__file__)), 'recipes/chicken', 'chicken-marsala'),
            'garlic chicken': join(abspath(dirname(__file__)), 'recipes/chicken', 'garlic-chicken'),
            'chicken cordon bleu ii': join(abspath(dirname(__file__)), 'recipes/chicken', 'chicken-cordon-bleu-ii'),
            'baked teriyaki chicken': join(abspath(dirname(__file__)), 'recipes/chicken', 'baked-teriyaki-chicken'),
            'slow cooker chicken and dumplings': join(abspath(dirname(__file__)), 'recipes/chicken', 'slow-cooker-chicken-and-dumplings'),
            'chicken pot pie ix': join(abspath(dirname(__file__)), 'recipes/chicken', 'chicken-pot-pie-ix'),
            'chicken divan casserole': join(abspath(dirname(__file__)), 'recipes/chicken', 'chicken-divan-casserole'),
            'moms fabulous chicken pot pie with biscuit crust': join(abspath(dirname(__file__)), 'recipes/chicken', 'moms-fabulous-chicken-pot-pie-with-biscuit-crust'),
            'roast chicken with thyme and onions': join(abspath(dirname(__file__)), 'recipes/chicken', 'roast-chicken-with-thyme-and-onions'),
            'tender italian baked chicken': join(abspath(dirname(__file__)), 'recipes/chicken', 'tender-italian-baked-chicken'),
            'slow cooker belgian chicken booyah': join(abspath(dirname(__file__)), 'recipes/chicken', 'slow-cooker-belgian-chicken-booyah'),
            'campbells easy broccoli and chicken skillet': join(abspath(dirname(__file__)), 'recipes/chicken', 'campbells-easy-broccoli-and-chicken-skillet'),
            'moroccan chicken tagine with caramelized pears': join(abspath(dirname(__file__)), 'recipes/chicken', 'moroccan-chicken-tagine-with-caramelized-pears'),
            'campbells chicken enchilada skillet': join(abspath(dirname(__file__)), 'recipes/chicken', 'campbells-chicken-enchilada-skillet'),
            'blackened chicken alfredo pizza': join(abspath(dirname(__file__)), 'recipes/chicken', 'blackened-chicken-alfredo-pizza'),
            'lemon chicken piccata': join(abspath(dirname(__file__)), 'recipes/chicken', 'lemon-chicken-piccata'),
            'slow cooker chicken taco soup': join(abspath(dirname(__file__)), 'recipes/chicken', 'slow-cooker-chicken-taco-soup'),
            'garlic roasted chicken and potatoes': join(abspath(dirname(__file__)), 'recipes/chicken', 'garlic-roasted-chicken-and-potatoes'),
            'spicy thai basil chicken pad krapow gai': join(abspath(dirname(__file__)), 'recipes/chicken', 'spicy-thai-basil-chicken-pad-krapow-gai'),
            'zesty slow cooker chicken barbecue': join(abspath(dirname(__file__)), 'recipes/chicken', 'zesty-slow-cooker-chicken-barbecue'),
            'bacon ranch chicken enchiladas': join(abspath(dirname(__file__)), 'recipes/chicken', 'bacon-ranch-chicken-enchiladas'),
            'beer can chicken': join(abspath(dirname(__file__)), 'recipes/chicken', 'beer-can-chicken'),
            'isaiahs pretzel fried chicken': join(abspath(dirname(__file__)), 'recipes/chicken', 'isaiahs-pretzel-fried-chicken'),
            'chicken parmesan': join(abspath(dirname(__file__)), 'recipes/chicken', 'chicken-parmesan'),
            'penne with chicken and asparagus': join(abspath(dirname(__file__)), 'recipes/chicken', 'penne-with-chicken-and-asparagus'),
            'steves roasted chicken soft tacos': join(abspath(dirname(__file__)), 'recipes/chicken', 'steves-roasted-chicken-soft-tacos'),
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
        
             ##########Next###############        
    @intent_file_handler('next.read.intent')
    def handle_next_read(self, message):
       self.is_next = True
         
       
        
          ##########Pause###############        
    @intent_file_handler('pause.read.intent')
    def handle_pause_read(self, message):
       self.is_paused = True
     
       
###############################         
        
        
         ##########Continue###############        
    @intent_file_handler('continue.read.intent')
    def handle_contin_read(self, message):
       self.is_continue = True
     
       
###############################        
     
              ##########repeat###############        
    @intent_file_handler('repeat.read.intent')
    def handle_repeat_read(self, message):     
       self.is_repeat = True     
        
        
###############################   
        ##########Stop###############        
    @intent_file_handler('stop.read.intent')
    def handle_stop_read(self, message):     
       self.is_reading = False

          
###############################      
        
    def stop(self):
        self.log.info('stop is called')
        if self.is_reading is True:
           self.is_reading = False
           return True
        else:
           return False       
      
        
             ############Directionss###########       
        
    @intent_file_handler('pick.directions.intent')
    def handle_pick_directions(self, message):
       self.is_reading = True              
       self.is_paused = True
       self.is_continue = False
       self.is_repeat = True

       filepath = open("recipe.dat","r")  
       path = filepath.read()
       #Recipe_str = os.popen("cat " + path + " |  sed -n '/^Directions/, $ p' | sed  '1d' ").read()
       Recipe_str = os.popen("$HOME/mycroft-core/skills/recipe-library-skill/./directions " + path).read()
       Rcnt = 0
        
       for  line in (Recipe_str.splitlines()):            
               if self.is_reading is False:                     
                   break
               else: 
                    if self.is_paused is True:                     
                       for x in range(100):
                           time.sleep(3)
                           if self.is_continue is True:
                                  self.is_continue = False
                                  self.is_paused = False
                                  break
                              
                           else:
                               if self.is_repeat is True:
                                  wait_while_speaking() 
                                  self.speak("{}".format(line), wait=True)
                                  time.sleep(3)
                                  self.is_repeat = False
                                  response = self.get_response('reed next line ')
                                  
                                  if response == 'yes':
                                     self.is_next = False 
                                     self.is_paused = True
                                     self.is_repeat = True
                                     break      
                                  if response == 'continue':
                                     self.is_next = False 
                                     self.is_paused = False
                                     self.is_repeat = True
                                     break  
                                  if response == 'repeat':
                                     self.is_repeat = True 
                                          
                               if self.is_next is True:
                                  wait_while_speaking() 
     
                                  self.is_next = False 
                                  self.is_paused = True
                                  self.is_repeat = True
                                  break                                
                           
                    else:                    
                        wait_while_speaking() 
               
                      
                        Rcnt = Rcnt+1
                        Rcnt_str = str(Rcnt)
                        file1 = open("Rcnt.dat","w")   
                        #cnt_int = str(cnt)
                        file1.write(Rcnt_str)
                        file1.close() 
                        self.speak("{}".format(line), wait=True) 
                        time.sleep(3)    
           
       
                      
       if self.is_reading is True:
          self.is_reading = False


        
        ############ingredients###########       
        
    @intent_file_handler('pick.ingredient.intent')
    def handle_pick_ingredients(self, message):
       self.is_reading = True             
       self.is_paused = True
       self.is_continue = False
       self.is_repeat = True       

       filepath = open("recipe.dat","r")  
       path = filepath.read()
       Recipe_str = os.popen("cat " + path + " |  sed -n '/^ Ingredients/,/^Directions/p;/^Directions/q' | sed  '1d;$d' | sed '$ a end of ingredient list'").read()
       Rcnt = 0
        
       for  line in (Recipe_str.splitlines()):            
               if self.is_reading is False:                     
                   break
               else: 
                    if self.is_paused is True:                     
                       for x in range(100):
                           time.sleep(3)
                           if self.is_continue is True:
                                  self.is_continue = False
                                  self.is_paused = False
                                  break
                              
                           else:
                               if self.is_repeat is True:
                                  wait_while_speaking() 
                                  self.speak("{}".format(line), wait=True)
                                  time.sleep(3)
                                  self.is_repeat = False
                                  response = self.get_response('next ingredient ')
                                  
                                  if response == 'yes':
                                     self.is_next = False 
                                     self.is_paused = True
                                     self.is_repeat = True
                                     break      
                                  if response == 'continue':
                                     self.is_next = False 
                                     self.is_paused = False
                                     self.is_repeat = False
                                     break  
                                  if response == 'repeat':
                                     self.is_repeat = True 
                                          
                               if self.is_next is True:
                                  wait_while_speaking() 

                                  self.is_next = False 
                                  self.is_paused = True
                                  self.is_repeat = True
                                  break                 
                    else:                      
                        wait_while_speaking() 
               
                      
                        Rcnt = Rcnt+1
                        Rcnt_str = str(Rcnt)
                        file1 = open("Rcnt.dat","w")   

                        file1.write(Rcnt_str)
                        file1.close() 
                        self.speak("{}".format(line), wait=True) 
                        time.sleep(3)    
           
       
                      
       if self.is_reading is True:
          self.is_reading = False
       
          
        
 ###############EMAILRecipe######################       
    @intent_file_handler('email.read.intent')
    def handle_email_read(self, message):
       self.speak('Sending recipe to your email')
       filepath = open("recipe.dat","r")  
       path = filepath.read()
        
       os.system("$HOME/mycroft-core/skills/recipe-library-skill/./email " + path )
       self.speak('done')
        
        
        
        
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
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  line = nice_number(normalize(line))
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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()
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
        print (self.file_system.path)
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.slow_play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()       
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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()
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
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()        
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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()            
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
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()        
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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()            
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
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()        
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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()        
            
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
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()        
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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()        
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
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()        
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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()        
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
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()        
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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()        
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
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()        
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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()        
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
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()        
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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()        
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
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()        
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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()        
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
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()        
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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()        
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
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()        
        with open(filepath) as fp:  
              for cnt, line in enumerate(fp):
                  regex = '({\d}* {\d}+\/{\d}+)' 
                  fraction = re.search(regex, line)
                  if not fraction:
                     self.speak("{}".format(line))
                     continue
                  formatted_line = re.sub(regex, extract_number(fraction.group(1)),  line)  
                  self.speak("{}".format(formatted_line))

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
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()        
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
    return RecipeLibrary()

