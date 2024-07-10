# ?? dashes pain
# ?? cups effort
# 1 cup water
# 4 kg bread crumbs
# 26 ml hot canola oil
# 13 kg egg yolks
# 24 teaspoons all purpose spices
# 7 teaspoons herbs
# 26 kg flour
# 26 kg sliced chicken breasts
# 1 dashes salt
# 11 dashes pepper
# 7 dashes pride and joy
# 10 kg tomato sauce
# 14 g cheese
# 13 kg ham
# 2 g pasta sauce
# 6 dashes chilli flakes
# 5 kg onion
# 9 dashes basil
# 19 dashes oregano
# 10 dashes parsley
# 20 teaspoons sugar

import string

alphabet = string.ascii_uppercase

mapping = {
    'pain': '_',
    'effort': '_',
    'water': alphabet[1-1],
    'bread crumbs': alphabet[4-1],
    'hot canola oil': alphabet[26-1],
    'egg yolks': alphabet[13-1],
    'all purpose spices': alphabet[24-1],
    'herbs': alphabet[7-1],
    'flour': alphabet[26-1],
    'sliced chicken breasts': alphabet[26-1],
    'salt': alphabet[1-1],
    'pepper': alphabet[11-1],
    'pride and joy': alphabet[7-1],
    'tomato sauce': alphabet[10-1],
    'cheese': alphabet[14-1],
    'ham': alphabet[13-1],
    'pasta sauce': alphabet[2-1],
    'chilli flakes': alphabet[6-1],
    'onion': alphabet[5-1],
    'basil': alphabet[9-1],
    'oregano': alphabet[19-1],
    'parsley': alphabet[10-1],
    'sugar': alphabet[20-1]    
}

instructions = """# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Remove bread crumbs from 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Add hot canola oil to 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Remove egg yolks from 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Remove all purpose spices from 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Add herbs to 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Add flour to 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Remove sliced chicken breasts from 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Remove salt from 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Add pepper to 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Remove pride and joy from 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Add tomato sauce to 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Remove cheese from 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Remove ham from 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Add pasta sauce to 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Remove chilli flakes from 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Remove onion from 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Add basil to 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Add oregano to 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Add water to 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Add parsley to 1st mixing bowl.
# Add effort to 1st mixing bowl.
# Put water into 1st mixing bowl.
# Combine pain into 1st mixing bowl.
# Add sugar to 1st mixing bowl.
# Add effort to 1st mixing bowl.
"""

instructions = instructions.split("\n")
mixing_bowl = ""

for instruction in instructions:
    if instruction == "":
        continue
    instruction = instruction.removeprefix("# ")
    opcode = instruction.split(" ")[0]
    if opcode == "Put":
        ingredient = instruction.split("into 1st")[0].removeprefix("Put ").strip()
        mixing_bowl += mapping[ingredient]
    elif opcode == "Add":
        ingredient = instruction.split("to 1st")[0].removeprefix("Add ").strip()
        mixing_bowl += mapping[ingredient]
    elif opcode == "Combine":
        ingredient = instruction.split("into 1st")[0].removeprefix("Combine ").strip()
        mixing_bowl += mapping[ingredient]
    elif opcode == "Remove":
        ingredient = instruction.split("from 1st")[0].removeprefix("Remove ").strip()
        try:
            # Find latest occurence of ingredient and remove it
            mixing_bowl = mixing_bowl[::-1].replace(mapping[ingredient], "", 1)[::-1]
        except:
            pass

print("".join(mixing_bowl))
        

