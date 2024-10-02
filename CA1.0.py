from IPython.display import clear_output
import random
import sys

print("You enter a castle with 10 (easy mode) floors to overcome and win.")

mnstrNumDiff = 5
mnstrHp = 10
mnstrAtt = 2

meXp = 1
meXpRcv = 0
meHp = 30
meHpStart = meHp
meHpHeal = 2
meAtt = 6
strength_boost = 5  # Strength potion boost
meAblt = ["attack", "defend", "strength", "healing","dodge"]

defend_counter = 0  # Counter for tracking defend action duration
strength_active = False  # To check if the strength potion is active

# Function for using the strength potion
def use_strength_potion():
    global meAtt, strength_active
    if not strength_active:  # Activate potion only if it's not already active
        meAtt += strength_boost
        strength_active = True
        print(f"You drank a Strength Potion! Your attack is increased by {strength_boost}. Current Attack: {meAtt}")
    else:
        print("You already used a Strength Potion on this floor!")

# Function for resetting strength potion effect
def reset_strength_potion():
    global meAtt, strength_active
    if strength_active:  # Only reset if the potion was used
        meAtt -= strength_boost
        strength_active = False
        print(f"The Strength Potion effect has worn off. Your attack is back to normal: {meAtt}")

# Function for defending (reduces damage by half for 2 turns)
def use_defense(nowMnstrAtt):
    global defend_counter
    defend_counter = 2  # Set defense to last for 2 rounds
    print("You defend! The monster's damage will be halved for the next 2 turns.")
    
# Function to apply damage, halving it if defense is active
def apply_damage(nowMnstrAtt):
    global meHp, defend_counter
    if defend_counter > 0:
        reduced_damage = nowMnstrAtt // 2
        print(f"Defense active! Monster's attack is reduced to {reduced_damage}.")
        meHp -= reduced_damage
        defend_counter -= 1  # Decrease defense counter each turn
    else:
        meHp -= nowMnstrAtt
    print(f"Monster attacks! Your HP is now {max(meHp, 0)}.")
    print()
    
def use_healing():
    global meHp, meHpStart, meHpHeal
    meHp += meHpHeal
    if meHp > meHpStart:
        meHp = meHpStart
    print(f"After healing by {meHpHeal}, your Hp now is {meHp}")
    
def use_dodge():
    dodge_chance = 0.3  # 30% chance to dodge
    if random.random() <= dodge_chance:
        print("You dodged the attack!")
        return True
    else:
        print("You failed to dodge!")
        return False

for i in range(1, 11):  # 10 floors
    print(f"This is the {i} floor")
    print(f"Your ability:\nHP = {meHp}\tAtt = {meAtt}\tXp = {round(meXp, 2)}")
    
    # Reset strength potion effect at the start of each floor
    reset_strength_potion()
    
    mnstrNum = random.randint(1, mnstrNumDiff)
    print(f"There are {mnstrNum} monsters")
    
    for a in range(mnstrNum):
        mnstrHpDiff = random.randint(1, i * 2)
        mnstrAttDiff = random.randint(i, mnstrAtt + i)
        nowMnstrHp = mnstrHp + mnstrHpDiff * 2
        nowMnstrAtt = mnstrAtt + mnstrAttDiff
        print(f"You meet the {a+1}th monster, it has {nowMnstrHp} HP and {nowMnstrAtt} attack damage")

        while nowMnstrHp > 0 and meHp > 0:  # Combat continues while monster and player have HP
            action = input(f"What do you want to do? {meAblt}: ").lower()

            if action == "attack" or action == "a":
                nowMnstrHp -= meAtt
                print(f"You make {meAtt} damage!")
                print(f"Now, the monster's HP is {max(nowMnstrHp, 0)}")
            elif action == "defend" or action == "d": 
                use_defense(nowMnstrAtt)  # Activate defense for 2 rounds
            elif action == "strength" or action == "s":
                use_strength_potion()  # Use strength potion
            elif action == "heal" or action == "h":
                use_healing()
            elif action == "dodge" or action == "dod":
                if use_dodge():
                    continue
            elif action == "q":
                sys.exit("GAME QUIT BY CODE")
            else:
                print("Invalid action. Please choose 'attack', 'defend', or 'strength'.")
                continue  # Ask again if invalid action
            
            # Monster attacks if it is still alive
            if nowMnstrHp > 0:
                apply_damage(nowMnstrAtt)  # Apply damage, check if defense is active

            # Check if the player or monster is dead
            if meHp <= 0:
                print("You have been defeated! Game over!")
                break
            elif nowMnstrHp <= 0:
                print("You defeated the monster!")
                # Gain XP or any other post-combat rewards
                meXpRcv = round(random.uniform(0.1, 0.24), 2)  # Round XP rewards
                meXp = round(meXp + meXpRcv, 2)  # Round and update the total XP
                print(f"You earn {meXpRcv} XP! Your current XP: {meXp}.")
                break
        
        if meHp <= 0:
            break  # Stop the game if player HP is zero or less
    
    if meHp <= 0:
        break  # Exit the floor loop if player HP is zero or less
    
    input("You finished this floor, press 'Enter' to go to the next floor...")
    clear_output(wait=True)

if meHp > 0:
    print("Congratulations, you completed the adventure!")
