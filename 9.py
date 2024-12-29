import random
import time
import sys

def loading_animation(duration=2, message="Caricamento"):
    animation = "|/-\\"
    idx = 0
    start = time.time()
    while time.time() - start < duration:
        print(f'\r{message} {animation[idx % len(animation)]}', end='')
        idx += 1
        time.sleep(0.1)
    print("\r" + " " * (len(message) + 2))

class Player:
    def __init__(self, name, player_class):
        self.name = name
        self.health = 100
        self.sanity = 100
        self.inventory = []
        
        classes = {
            "Sopravvissuto": {"str": 6, "agi": 6, "int": 6, "luck": 6},
            "Esploratore Urbano": {"str": 4, "agi": 8, "int": 6, "luck": 6},
            "Ricercatore del Paranormale": {"str": 3, "agi": 5, "int": 9, "luck": 7},
            "Vagabondo": {"str": 5, "agi": 5, "int": 5, "luck": 9}
        }
        
        self.stats = classes[player_class]
        self.player_class = player_class

class Zone:
    def __init__(self, name, description, danger_level, special_items=None):
        self.name = name
        self.description = description
        self.danger_level = danger_level
        self.special_items = special_items or []
        self.connected_zones = []

class Level9Map:
    def __init__(self):
        self.zones = {
            'suburb': Zone(
                'Quartiere Residenziale',
                'Case suburbane identiche si estendono all\'infinito. Alcune sembrano fuse tra loro in modo impossibile.',
                5,
                ['chiave arrugginita', 'foto sbiadita']
            ),
            'street': Zone(
                'Strade Deserte',
                'Strade asfaltate bagnate, coperte di foglie. Pozzanghere riflettono una luna che non esiste.',
                7,
                ['cartello stradale', 'pezzo di asfalto anomalo']
            ),
            'park': Zone(
                'Parco Abbandonato',
                'Giochi arrugginiti e altalene che si muovono da sole. La nebbia è più densa qui.',
                6,
                ['altalena rotta', 'giocattolo abbandonato']
            ),
            'fog_zone': Zone(
                'Zona Nebbiosa',
                'La nebbia è così densa che è difficile vedere oltre pochi metri. Si sentono strani rumori.',
                8,
                ['bussola impazzita', 'lanterna nebbiosa']
            ),
            'power_lines': Zone(
                'Zona Elettrica',
                'Linee elettriche si estendono nel buio. Alcuni lampioni lampeggiano in modo irregolare.',
                7,
                ['cavo elettrico', 'batteria anomala']
            ),
            'playground': Zone(
                'Area Giochi',
                'Un parco giochi inquietante con tubi bianchi luminescenti. Porta a Level 283.',
                6,
                ['gessetto colorato', 'pupazzo inquietante']
            ),
            'airport': Zone(
                'Aeroporto Abbandonato',
                'Un aeroporto emerge dalla nebbia. Le insegne luminose lampeggiano in modo sinistro.',
                9,
                ['biglietto aereo', 'badge sicurezza']
            )
        }
        self.connect_zones()

    def connect_zones(self):
        connections = {
            'suburb': ['street', 'park', 'fog_zone'],
            'street': ['suburb', 'power_lines', 'airport'],
            'park': ['suburb', 'playground', 'fog_zone'],
            'fog_zone': ['suburb', 'park', 'power_lines'],
            'power_lines': ['street', 'fog_zone', 'airport'],
            'playground': ['park'],
            'airport': ['street', 'power_lines']
        }
        
        for zone_name, connected_to in connections.items():
            for connection in connected_to:
                self.zones[zone_name].connected_zones.append(self.zones[connection])

class Level9Game:
    def __init__(self):
        self.entities = [
            {"name": "Smiler", "difficulty": 7},
            {"name": "Skin-Stealer", "difficulty": 8},
            {"name": "The Mangled", "difficulty": 9},
            {"name": "The Observer", "difficulty": 6},
            {"name": "Deathmoth", "difficulty": 5}
        ]
        
        self.items = [
            "torcia",
            "kit medico",
            "mappa strappata",
            "acqua almond",
            "radio rotta"
        ]

    def start(self):
        print("=== BACKROOMS: LEVEL 9 ===")
        loading_animation(2, "Inizializzazione Level 9")
        print("Ti risvegli in un'infinita area suburbana a mezzanotte...")
        name = input("Inserisci il tuo nome: ")
        
        print("\nScegli la tua classe:")
        print("1. Sopravvissuto (statistiche bilanciate)")
        print("2. Esploratore Urbano (+ agilità)")
        print("3. Ricercatore del Paranormale (+ intelligenza)")
        print("4. Vagabondo (+ fortuna)")
        
        classes = {
            "1": "Sopravvissuto",
            "2": "Esploratore Urbano",
            "3": "Ricercatore del Paranormale",
            "4": "Vagabondo"
        }
        
        choice = input("Seleziona (1-4): ")
        player = Player(name, classes[choice])
        loading_animation(1, "Generazione personaggio")
        
        self.game_loop(player)

    def encounter(self, player):
        entity = random.choice(self.entities)
        loading_animation(1, "Incontro entità")
        print(f"\nUn {entity['name']} ti sta attaccando!")
        
        player_power = (player.stats["str"] + player.stats["agi"] + player.stats["luck"]) / 3
        roll = random.randint(1, 20) + player_power
        
        if roll > entity["difficulty"] * 2:
            print("Sei riuscito a sfuggire all'entità!")
            player.sanity += 5
            return True
        else:
            damage = random.randint(10, 25)
            player.health -= damage
            player.sanity -= 10
            print(f"L'entità ti ha ferito! (-{damage} salute)")
            return False

    def game_loop(self, player):
        level_map = Level9Map()
        current_zone = level_map.zones['suburb']
        
        while player.health > 0 and player.sanity > 0:
            print(f"\nZona attuale: {current_zone.name}")
            print(f"Salute: {player.health} | Sanità Mentale: {player.sanity}")
            print("\nAzioni disponibili:")
            print("1. Esplora la zona")
            print("2. Cambia zona")
            print("3. Usa oggetto")
            print("4. Controlla inventario")
            print("5. Riposa")
            
            action = input("Cosa vuoi fare? ")
            
            if action == "1":
                result = explore_zone(player, current_zone)
                if result == "combat":
                    self.encounter(player)
            elif action == "2":
                current_zone = change_zone(current_zone)
            elif action == "3":
                if player.inventory:
                    print("\nOggetti disponibili:")
                    for i, item in enumerate(player.inventory):
                        print(f"{i+1}. {item}")
                    item_choice = int(input("Usa oggetto (numero): ")) - 1
                    if item_choice < len(player.inventory):
                        used_item = player.inventory.pop(item_choice)
                        loading_animation(1, "Utilizzo oggetto")
                        if used_item == "kit medico":
                            player.health += 30
                            print("Hai recuperato salute (+30)")
                        elif used_item == "acqua almond":
                            player.sanity += 20
                            print("Hai recuperato sanità mentale (+20)")
                else:
                    print("\nInventario vuoto!")
            elif action == "4":
                print("\nInventario:", ", ".join(player.inventory))
            elif action == "5":
                loading_animation(2, "Riposando")
                if random.random() < 0.3:
                    print("\nQualcosa ti ha disturbato durante il riposo!")
                    self.encounter(player)
                else:
                    player.health += 10
                    player.sanity += 5
                    print("\nTi sei riposato (+10 salute, +5 sanità)")
        
        if player.health <= 0:
            print("\nSei morto...")
        elif player.sanity <= 0:
            print("\nHai perso la ragione...")

def explore_zone(player, current_zone):
    loading_animation(1, f"Esplorando {current_zone.name}")
    print(f"\n{current_zone.description}")
    
    if random.random() < 0.3:
        found_item = random.choice(current_zone.special_items)
        print(f"\nHai trovato: {found_item}")
        player.inventory.append(found_item)
    
    if random.random() < (current_zone.danger_level / 10):
        return "combat"
    
    return "safe"

def change_zone(current_zone):
    print("\nZone connesse:")
    for i, zone in enumerate(current_zone.connected_zones):
        print(f"{i+1}. {zone.name} (Livello Pericolo: {zone.danger_level})")
    
    choice = int(input("\nScegli dove andare (numero): ")) - 1
    if 0 <= choice < len(current_zone.connected_zones):
        loading_animation(2, "Cambiando zona")
        return current_zone.connected_zones[choice]
    return current_zone

if __name__ == "__main__":
    game = Level9Game()
    game.start()
