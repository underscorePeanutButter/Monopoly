import random

class Player:
    def __init__(self, name):
        self.name = name
        self.location = -1

        self.jailed = False
        
        self.balance = 1500
        self.properties = []

        self.utilities = 0
        self.railroads = 0

class Property:
    def __init__(self, name, colour, price, rent, mortgage, house_price, hotel_price):
        self.name = name
        self.colour = colour
        self.owner = None
        self.price = price

        self.rent = rent
        self.mortgage = mortgage
        self.house_price = house_price
        self.hotel_price = hotel_price

        self.houses = 0
        self.hotel = False

class Railroad:
    def __init__(self, name):
        self.name = name
        self.owner = None
        
        self.price = 200
        self.rent = [25, 50, 100, 200]
        self.mortgage = 100

class Utility:
    def __init__(self, name):
        self.name = name
        self.owner = None

        self.price = 150
        self.rent = [4, 10]

class Tile:
    def __init__(self, name, variant, data):
        self.name = name
        self.variant = variant

        self.data = data

class Card:
    def __init__(self, name, description):
        self.name = name
        self.description = description

roll = lambda a=2,b=12: random.randint(a, b)

def display_player_data(player):
    print(f"{player.name}")
    print("".join(["-" for i in range(len(player.name))]))

    print(f"Balance: M{player.balance}")
    if len(player.properties) > 0:
        print("Properties:\n - " + "\n - ".join(property.name for property in player.properties))
    else:
        print("Properties:\n  This player has no properties")

def display_property_data(property):
    print(f"{property.name}")
    print("".join(["-" for i in range(len(property.name))]))
    
    print(f"Colour: {property.colour}")
    if property.owner:
        print(f"Owner: {property.owner.name}")
        print(f"Number of houses: {property.houses}")
        print(f"Has a hotel? {property.hotel}")
        print(f"Current rent: M{property.rent[property.houses + int(property.hotel)]}")
    else:
        print(f"Owner: {property.owner}")
        print(f"Price: M{property.price}")
        print(f"Rent:\n  " + "\n  ".join(f"With {i} houses: M{property.rent[i]}" for i in range(len(property.rent) - 1)))
        print(f"  With a hotel: M{property.rent[-1]}")    
    print(f"House price: M{property.house_price}")
    print(f"Hotel price (with 4 houses): M{property.hotel_price}")

def display_railroad_data(railroad):
    print(f"{railroad.name}")
    print("".join(["-" for i in range(len(railroad.name))]))

    if railroad.owner:
        print(f"Owner: {railroad.owner.name}")
        print(f"Current rent: M{railroad.rent[railroad.owner.railroads - 1]}")
    else:
        print(f"Owner: {railroad.owner}")
        print(f"Price: M{railroad.price}")
        print(f"Rent:\n  " + "\n  ".join(f"With {i} other railroads: M{railroad.rent[i]}" for i in range(len(railroad.rent))))

def display_utility_data(utility):
    print(f"{utility.name}")
    print("".join(["-" for i in range(len(utility.name))]))

    if utility.owner:
        print(f"Owner: {utility.owner.name}")
        print(f"Current rent: M{utility.rent[utility.owner.utilities - 1]} * roll")
    else:
        print(f"Owner: {utility.owner}")
        print(f"Price: M{utility.price}")
        print(f"Rent:\n  " + "\n  ".join(f"With {i} other utilities: M{utility.rent[i]} * roll" for i in range(len(utility.rent))))

def do_purchase(player, property, roll=None):
    if property.owner and property.owner != player:
        if type(property) == Property:
            rent = property.rent[property.houses + int(property.hotel)]
        elif type(property) == Railroad:
            rent = property.rent[property.owner.railroads - 1]
        elif type(property) == Utility:
            rent = property.rent[property.owner.utilities - 1] * roll

        if player.balance - rent < 0:
            print(f"{player.name} has gone bankrupt! {property.owner.name} gets their property.")
            for p in player.properties:
                property.owner.properties.append(p)
                p.owner = property.owner
            property.owner.balance += player.balance
            players.remove(player)

        else:
            player.balance -= rent
            print(f"Paying M{rent} for rent")
            print()

    elif not property.owner:
        if player.balance >= property.price:
            buying_property = input("Would you like to buy this property? ").lower().startswith("y")
            print()

            if buying_property:
                property.owner = player
                player.properties.append(property)

                player.balance -= property.price
                print("Property purchased.")
            else:
                print("Property not purchased.")
                print()
                auction(property)

        else:
            print("You don't have enough money to purchase this property.")
            print()
            auction(property)

def auction(property):
    print("Auction")
    print("-------")
    
    current_bid = 0
    current_bidder = None

    dropped_players = []

    while True:
        if (len(players) - len(dropped_players) == 1 and current_bidder) or len(players) - len(dropped_players) == 0:
            break

        for player in players:
            print()
            if (len(players) - len(dropped_players) == 1 and current_bidder) or len(players) - len(dropped_players) == 0:
                break

            if player.balance < current_bid + 1:
                dropped_players.append(player)

            if player not in dropped_players:
                print(f"Player: {player.name}")
                print(f"Balance: M{player.balance}")
                print(f"Property: {property.name}")
                print(f"Current bid: M{current_bid}")
                if current_bidder:
                    print(f"Highest bid: {current_bidder.name}")
                print()
                print("1. + M1")
                
                if player.balance > current_bid + 10:
                    print("2. + M10")
                if player.balance > current_bid + 100:
                    print("3. + M100")
                print("4. Drop out")
                choice = input("What will you do? ")

                if choice == "1":
                    current_bid += 1
                    current_bidder = player
                elif choice == "2":
                    if player.balance >= current_bid + 10:
                        current_bid += 10
                        current_bidder = player
                    else:
                        print("You don't have enough money! Adding M1 instead.")
                        current_bid += 1
                        current_bidder = player
                elif choice == "3":
                    if player.balance >= current_bid + 100:
                        current_bid += 100
                        current_bidder = player
                    else:
                        print("You don't have enough money! Adding M1 instead.")
                        current_bid += 1
                        current_bidder = player
                else:
                    dropped_players.append(player)
                    print("You have dropped out.")

    print()
    
    if len(dropped_players) != len(players):
        print(f"{current_bidder.name} won the auction.")

        current_bidder.properties.append(property)
        current_bidder.balance -= current_bid
        property.owner = current_bidder

        print(f"M{current_bid} paid. Congratulations!")
    else:
        print(f"No one won the auction. {property.name} still available.")

community_chest_deck = []
chance_deck = []
free_parking_money = 0

board = [Tile("Go", "Special", "Go"),\
         Tile("Mediterranean Avenue", "Property", Property("Mediterranean Avenue", "Brown", 60, [2, 10, 30, 90, 160, 250], 30, 50, 50)),\
         Tile("Community Chest", "Draw", community_chest_deck),\
         Tile("Baltic Avenue", "Property", Property("Baltic Avenue", "Brown", 60, [4, 20, 60, 180, 360, 450], 30, 50, 50)),\
         Tile("Income Tax", "Payment", 200),\
         Tile("Reading Railroad", "Railroad", Railroad("Reading Railroad")),\
         Tile("Oriental Avenue", "Property", Property("Oriental Avenue", "Light Blue", 100, [6, 30, 90, 270, 400, 550], 50, 50, 50)),\
         Tile("Chance", "Draw", chance_deck),\
         Tile("Vermont Avenue", "Property", Property("Vermont Avenue", "Light Blue", 100, [6, 30, 90, 270, 400, 550], 50, 50, 50)),\
         Tile("Connecticut Avenue", "Property", Property("Connecticut Avenue", "Light Blue", 120, [8, 40, 100, 300, 450, 600], 60, 50, 50)),\
         Tile("Jail", "Special", "Jail"),\
         Tile("St. Charles Place", "Property", Property("St. Charles Place", "Pink", 140, [10, 50, 150, 450, 625, 750], 70, 100, 100)),\
         Tile("Electric Company", "Utility", Utility("Electric Company")),\
         Tile("States Avenue", "Property", Property("States Avenue", "Pink", 140, [10, 50, 150, 450, 625, 750], 70, 100, 100)),\
         Tile("Virginia Avenue", "Property", Property("Virginia Avenue", "Pink", 160, [12, 60, 180, 500, 700, 900], 80, 100, 100)),\
         Tile("Pennsylvania Railroad", "Railroad", Railroad("Pennsylvania Railroad")),\
         Tile("St. James Place", "Property", Property("St. James Place", "Orange", 180, [14, 70, 200, 550, 750, 950], 90, 100, 100)),\
         Tile("Community Chest", "Draw", community_chest_deck),\
         Tile("Tennessee Avenue", "Property", Property("Tennessee Avenue", "Orange", 180, [14, 70, 200, 550, 750, 950], 90, 100, 100)),\
         Tile("New York Avenue", "Property", Property("New York Avenue", "Orange", 200, [16, 80, 220, 600, 800, 1000], 100, 100, 100)),\
         Tile("Free Parking", "Special", "Free Parking"),\
         Tile("Kentucky Avenue", "Property", Property("Kentucky Avenue", "Red", 220, [18, 90, 250, 700, 875, 1050], 110, 150, 150)),\
         Tile("Chance", "Draw", chance_deck),\
         Tile("Indiana Avenue", "Property", Property("Indiana Avenue", "Red", 220, [18, 90, 250, 700, 875, 1050], 110, 150, 150)),\
         Tile("Illinois Avenue", "Property", Property("Illinois Avenue", "Red", 240, [20, 100, 300, 750, 925, 1100], 120, 150, 150)),\
         Tile("B&O Railroad", "Railroad", Railroad("B&O Railroad")),\
         Tile("Atlantic Avenue", "Property", Property("Atlantic Avenue", "Yellow", 260, [22, 110, 330, 800, 975, 1150], 130, 150, 150)),\
         Tile("Ventnor Avenue", "Property", Property("Ventnor Avenue", "Yellow", 260, [22, 110, 330, 800, 975, 1150], 130, 150, 150)),\
         Tile("Water Works", "Utility", Utility("Water Works")),\
         Tile("Marvin Gardens", "Property", Property("Marvin Gardens", "Yellow", 280, [24, 120, 360, 850, 1025, 1200], 140, 150, 150)),\
         Tile("Go to Jail", "Special", "Go to Jail"),\
         Tile("Pacific Avenue", "Property", Property("Pacific Avenue", "Green", 300, [26, 130, 390, 900, 1100, 1275], 150, 200, 200)),\
         Tile("North Carolina Avenue", "Property", Property("North Carolina Avenue", "Green", 300, [26, 130, 390, 900, 1100, 1275], 150, 200, 200)),\
         Tile("Community Chest", "Draw", community_chest_deck),\
         Tile("Pennsylvania Avenue", "Property", Property("Pennsylvania Avenue", "Green", 320, [28, 150, 450, 1000, 1200, 1400], 160, 200, 200)),\
         Tile("Short Line", "Railroad", Railroad("Short Line")),\
         Tile("Chance", "Draw", chance_deck),\
         Tile("Park Place", "Property", Property("Park Place", "Dark Blue", 350, [35, 175, 500, 1100, 1300, 1500], 175, 200, 200)),\
         Tile("Luxury Tax", "Payment", 100),\
         Tile("Boardwalk", "Property", Property("Boardwalk", "Dark Blue", 400, [50, 200, 600, 1400, 1700, 2000], 200, 200, 200))]

print("Monopoly\n")
number_of_players = int(input("How many players? "))

players = [Player(f"Player {i}") for i in range(number_of_players)]

while True:
    if len(players) == 1:
        break

    for player in players:
        if player.jailed:
            print("You're in jail!")
            if player.balance >= 50:
                is_paying = input("Would you like to pay M50 to get out? ")

                if is_paying.lower().startswith("y"):
                    player.balance -= 50
                    player.jailed = False
                else:
                    print("You're still in jail. :( Rolling for doubles...")
                    if roll(0, 31) == 0:
                        print("You did it! You're free!")
                        player.jailed = False
                    else:
                        print("You're still in jail.")

            else:
                print("You can't afford bail! Rolling for doubles...")
                if roll(0, 31) == 0:
                    print("You did it! You're free!")
                    player.jailed = False
                else:
                    print("You're still in jail.")
            print()

        if not player.jailed:
            print("Rolling dice...")
            spaces_to_move = roll()
            print(f"Moving {spaces_to_move} spaces...")
            print()

            new_location = player.location + spaces_to_move

            if new_location >= 40:
                new_location -= 40

            if (new_location < player.location):
                print(f"{player.name} passed go.")
                print()
                player.balance += 200

            player.location = new_location

            display_player_data(player)
            print()

            if type(board[player.location].data) == Property:
                display_property_data(board[player.location].data)
                print()

                do_purchase(player, board[player.location].data)
                
                if len(players) == 1:
                    break

            elif type(board[player.location].data) == Railroad:
                display_railroad_data(board[player.location].data)
                print()
                
                do_purchase(player, board[player.location].data)

                if len(players) == 1:
                    break

            elif type(board[player.location].data) == Utility:
                display_utility_data(board[player.location].data)
                print()

                do_purchase(player, board[player.location].data, spaces_to_move)

                if len(players) == 1:
                    break

            elif board[player.location].variant == "Special":
                if board[player.location].data == "Go":
                    print("You landed on go.")

                elif board[player.location].data == "Go to Jail":
                    player.jailed = True
                    player.location = 10
                    print("You've been arrested!")
                
                elif board[player.location].data == "Free Parking":
                    player.balance += free_parking_money
                    free_parking_money = 0
                    print(f"Free parking! You're collecting M{free_parking_money}!")

            elif board[player.location].variant == "Payment":
                print(f"You landed on {board[player.location].name}. You paid M{board[player.location].data}.")

                if player.balance < board[player.location].data:
                    print("You've gone bankrupt. Auction time!")
                    print()
                    auctioning_properties = player.properties
                    players.remove(player)
                    
                    if len(players) == 1:
                        break

                    for property in auctioning_properties:
                        auction(property)
                else:
                    player.balance -= board[player.location].data

                free_parking_money += board[player.location].data

        print()

print(f"{players[0].name} won the game!")
