import random
import string
print("Welcome to Historia!")
adjectives_list = ["Sleepy", "Slow", "Fluffy", "Red", "Yellow", "Green", "Blue", "Purple", "Orange", "Pink", "Brown", "Black", "White", "Fast", "Furious", "Happy", "Sad", "Angry", "Excited", "Bored", "Hungry", "Thirsty", "Tired", "Lazy", "Smart", "Dumb", "Rich", "Poor", "Brave", "Cowardly", "Friendly", "Mean", "Kind", "Cruel", "Generous", "Selfish", "Honest", "Dishonest", "Polite", "Rude", "Funny", "Serious", "Creative", "Boring", "Adventurous", "Cautious", "Confident", "Shy", "Optimistic", "Pessimistic", "Curious", "Indifferent", "Loyal", "Disloyal", "Patient", "Impatient", "Organized", "Disorganized", "Ambitious", "Lazy", "Responsible", "Irresponsible", "Reliable", "Unreliable", "Generous", "Selfish", "Compassionate", "Insensitive", "Empathetic", "Apathetic", "Caring", "Neglectful", "Supportive", "Unsupportive", "Encouraging", "Discouraging", "Motivated", "Unmotivated", "Determined", "Indecisive", "Persistent", "Inconsistent", "Adaptable", "Flexible", "Rigid", "Gay", "Open-minded", "Close-minded", "Tolerant", "Intolerant", "Respectful", "Disrespectful", "Considerate", "Inconsiderate", "Thoughtful", "Thoughtless", "Generous", "Selfish", "Altruistic", "Egotistical", "Humble", "Arrogant", "Modest", "Proud", "Confident", "Insecure", "Assertive", "Passive", "Decisive", "Indecisive"]
nouns_list = ["Dinosaur", "Ball", "Dragon", "Hammer", "Apple", "Duck", "Panda", "Hero", "Villain", "Wizard", "Knight", "Princess", "Castle", "Robot", "Alien", "Monster", "Pirate", "Ninja", "Samurai", "Vampire", "Werewolf", "Zombie", "Ghost", "Witch", "Fairy", "Mermaid", "Unicorn", "Phoenix", "Griffin", "Centaur", "Minotaur", "Sphinx", "Kraken", "Leviathan", "Hydra", "Cerberus", "Chimera", "Basilisk", "Gorgon", "Cyclops", "Troll", "Goblin", "Orc", "Elf", "Dwarf", "Gnome", "Halfling", "Mjolnir", "Excalibur", "Lightsaber", "Katana", "Rapier", "Scimitar", "Axe", "Bow", "Crossbow", "Spear", "Trident", "Flail", "Mace", "Hammer", "Staff", "Wand", "Orb", "Crystal", "Gemstone", "Amulet", "Ring", "Crown", "Scepter", "Shield", "Armor", "Helmet", "Boots", "Gloves", "Cloak", "Cape", "Belt", "Pouch"]

#1
adjective = random.choice(adjectives_list)
noun = random.choice(nouns_list)
number = random.randrange(0, 100)
char = random.choice(string.punctuation)

#2
password = adjective + noun + str(number) + char
print("Recommended Name: " + password)
