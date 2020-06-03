from PIL import Image, ImageOps
from pathlib import Path
import os
import json
import re


MISC_IDS = {
    (220, 255, 166, 255): 200, #Invisible Wall (Boundary)
    (128, 128, 128, 255): 206, #Surface 0
    (100, 100, 100, 255): 206, #Surface 0
    (204, 186, 143, 255): 206, #Surface 0
    (204, 176, 143, 255): 206, #Surface 0
    (143, 186, 204, 255): 207, #Surface 1
    (143, 176, 204, 255): 207, #Surface 1
    (177, 204, 143, 255): 208, #Surface 2
    (177, 194, 143, 255): 208  #Surface 2
    #"": 253, #Invisible Wall (Structure)
    #"": 254, #Underwater Boundary
    #"": 255, #Zero G
    #"": 256, #Zero G (protected)
    #"": 257, #World Gen Must Contain Ocean Liquid
    #"": 258, #World Gen Must Not Contain Ocean Liquid
    #"": 240, #World Gen Must Contain Solid
}

MISC_BACKGROUND_IDS = {
    (255, 0, 220, 255):   199, #Magic Pink Brush
    (200, 200, 200, 255): 206, #Surface 0
    (255, 232, 178, 255): 206, #Surface 0
    (255, 222, 178, 255): 206, #Surface 0
    (178, 232, 255, 255): 207, #Surface 1
    (178, 222, 255, 255): 207, #Surface 1
    (222, 255, 178, 255): 208, #Surface 2
    (222, 245, 178, 255): 208, #Surface 2
    (32, 32, 32, 255):    198, #Fill with air
    (48, 48, 48, 255):    209  #Fill with air (Overwritable)
}

ANCHOR_IDS = {
    (85, 255, 0, 255):    201, #Player Start
    (120, 120, 120, 255): 202, #World Gen Must Contain Air
    (0, 0, 0, 255):       214, #World Gen Must Contain Air Background
    (255, 255, 255, 255): 215, #World Gen Must Contain Solid Background
    (255, 168, 0, 255):   210, #Red Connector
    (0, 255, 186, 255):   211, #Yellow Connector
    (168, 255, 0, 255):   212, #Green Connector
    (0, 38, 255, 255):    213  #Blue Connector
}

BIOME_OBJECT_IDS = {
    (34, 102, 0, 255):    204, #Biome Item
    (26, 77, 0, 255):     205  #Biome Tree
}


class MapData:
    def __init__(self, height, width):
        self.map_data = {
        "backgroundcolor":"#000000",
        "compressionlevel":-1,
        "editorsettings":
            {
            "export":
                {
                "target":"."
                }
            },
        "height":height,
        "infinite":False,
        "layers":[
                {
                "data":[],
                "height":height,
                "id":1,
                "name":"back",
                "opacity":0.5,
                "type":"tilelayer",
                "visible":True,
                "width":width,
                "x":0,
                "y":0
                }, 
                {
                "data":[],
                "height":height,
                "id":2,
                "name":"front",
                "opacity":1,
                "type":"tilelayer",
                "visible":True,
                "width":width,
                "x":0,
                "y":0
                }, 
                {
                "color":"#5555ff",
                "draworder":"topdown",
                "id":3,
                "name":"mods",
                "objects":[],
                "opacity":1,
                "type":"objectgroup",
                "visible":True,
                "x":0,
                "y":0
                }, 
                {
                "color":"#ff0000",
                "draworder":"topdown",
                "id":4,
                "name":"objects",
                "objects":[],
                "opacity":1,
                "type":"objectgroup",
                "visible":True,
                "x":0,
                "y":0
                }, 
                {
                "color":"#ffff00",
                "draworder":"topdown",
                "id":5,
                "name":"wiring - lights & guns",
                "objects":[],
                "opacity":1,
                "type":"objectgroup",
                "visible":True,
                "x":0,
                "y":0
                }, 
                {
                "color":"#ff0000",
                "draworder":"topdown",
                "id":6,
                "name":"monsters & npcs",
                "objects":[],
                "opacity":1,
                "type":"objectgroup",
                "visible":True,
                "x":0,
                "y":0
                }, 
                {
                "color":"#00ffff",
                "draworder":"topdown",
                "id":7,
                "name":"wiring - locked door",
                "objects":[],
                "opacity":1,
                "type":"objectgroup",
                "visible":True,
                "x":0,
                "y":0
                }, 
                {
                "draworder":"topdown",
                "id":8,
                "name":"outside the map",
                "objects":[],
                "opacity":1,
                "type":"objectgroup",
                "visible":True,
                "x":0,
                "y":0
                }, 
                {
                "draworder":"topdown",
                "id":9,
                "name":"anchors etc",
                "objects":[],
                "opacity":1,
                "type":"objectgroup",
                "visible":True,
                "x":0,
                "y":0
                }, 
                {
                "draworder":"topdown",
                "id":10,
                "name":"items",
                "objects":[],
                "opacity":1,
                "type":"objectgroup",
                "visible":True,
                "x":0,
                "y":0
                }],
        "nextlayerid":11,
        "nextobjectid":679,
        "orientation":"orthogonal",
        "renderorder":"right-down",
        "tiledversion":"1.3.5",
        "tileheight":8,
        "tilesets":[
            {
            "firstgid":1,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/materials.json"
            }, 
            {
            "firstgid":198,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/miscellaneous.json"
            }, 
            {
            "firstgid":222,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/liquids.json"
            }, 
            {
            "firstgid":250,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/supports.json"
            }, 
            {
            "firstgid":287,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-race\/generic.json"
            }, 
            {
            "firstgid":2271,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-race\/ancient.json"
            }, 
            {
            "firstgid":2434,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-race\/apex.json"
            }, 
            {
            "firstgid":2805,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-race\/avian.json"
            }, 
            {
            "firstgid":3110,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-race\/floran.json"
            }, 
            {
            "firstgid":3305,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-race\/glitch.json"
            }, 
            {
            "firstgid":3531,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-race\/human.json"
            }, 
            {
            "firstgid":3819,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-race\/hylotl.json"
            }, 
            {
            "firstgid":4051,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-race\/novakid.json"
            }, 
            {
            "firstgid":4115,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/crafting.json"
            }, 
            {
            "firstgid":4195,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/decorative.json"
            }, 
            {
            "firstgid":5636,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/door.json"
            }, 
            {
            "firstgid":5768,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/farmable.json"
            }, 
            {
            "firstgid":5843,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/furniture.json"
            }, 
            {
            "firstgid":6197,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/light.json"
            }, 
            {
            "firstgid":6655,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/other.json"
            }, 
            {
            "firstgid":6967,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/pot.json"
            }, 
            {
            "firstgid":7264,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/sapling.json"
            }, 
            {
            "firstgid":7265,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/spawner.json"
            }, 
            {
            "firstgid":7281,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/storage.json"
            }, 
            {
            "firstgid":7515,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/teleporter.json"
            }, 
            {
            "firstgid":7557,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/tools.json"
            }, 
            {
            "firstgid":7562,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/trap.json"
            }, 
            {
            "firstgid":7766,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-category\/wire.json"
            }, 
            {
            "firstgid":7988,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-type\/container.json"
            }, 
            {
            "firstgid":8273,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-type\/farmable.json"
            }, 
            {
            "firstgid":8351,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-type\/loungeable.json"
            }, 
            {
            "firstgid":8632,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-type\/noisy.json"
            }, 
            {
            "firstgid":8673,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/objects-by-type\/teleporter.json"
            }, 
            {
            "firstgid":8700,
            "source":"..\/..\/..\/..\/..\/..\/..\/Program Files (x86)\/Steam\/steamapps\/common\/Starbound\/assets\/_unpacked\/tilesets\/packed\/huge-objects.json"
            }],
        "tilewidth":8,
        "type":"map",
        "version":1.2,
        "width":width
        }


class StarboundObject:
    def __init__(self, gid, height, id, width, x, y, offset_x, offset_y):
        self.object_data = {
            "gid":gid,
            "height":height,
            "id":id,
            "name":"",
            "rotation":0,
            "type":"",
            "visible":True,
            "width":width,
            "x":x*8 + offset_x,
            "y":y*8 - offset_y + 8
        }


input_folder = os.path.dirname(os.path.realpath(__file__)) + "/input/"
output_folder = os.path.dirname(os.path.realpath(__file__)) + "/output/"
object_dir_path = os.path.dirname(os.path.realpath(__file__)) + "/objects/"

with open(os.path.dirname(os.path.realpath(__file__)) + "/object_sizes.json", 'r') as read_file:
    OBJECT_SIZES = json.load(read_file)

with open(os.path.dirname(os.path.realpath(__file__)) + "/object_offsets.json", 'r') as read_file:
    OBJECT_OFFSETS = json.load(read_file)

with open(os.path.dirname(os.path.realpath(__file__)) + "/tile_ids.json", 'r') as read_file:
    TILE_IDS = json.load(read_file)

with open(os.path.dirname(os.path.realpath(__file__)) + "/object_ids.json", 'r') as read_file:
    OBJECT_IDS = json.load(read_file)

with open(os.path.dirname(os.path.realpath(__file__)) + "/object_flipped_ids.json", 'r') as read_file:
    OBJECT_FLIPPED_IDS = json.load(read_file)


def add_data(ids, tiles, new_map, x, y):
    for key, value in ids.items():
        if tiles == value:

            if tiles in OBJECT_SIZES:
                object_size = OBJECT_SIZES[tiles]

            if tiles in OBJECT_OFFSETS:
                object_offset = OBJECT_OFFSETS[tiles]
            
            new_object = StarboundObject(key, object_size[1], new_map.map_data.get("nextobjectid"), object_size[0], x, y, object_offset[0], object_offset[1])
            new_map.map_data.get("layers")[3].get("objects").append(new_object.object_data)
            new_map.map_data["nextobjectid"] += 1
            new_map.map_data.get("layers")[1].get("data").append(0)
            new_map.map_data.get("layers")[0].get("data").append(199)
            break


def convert():
    dungeon_file = Path(input('Please input the path to your .dungeon file: '))

    for file in os.listdir(input_folder):
        current_image = Image.open(input_folder + file)
        new_map = MapData(current_image.height, current_image.width)

        for y in range(0, current_image.height):
            for x in range(0, current_image.width):
                pixel = current_image.getpixel((x,y))

                if pixel in MISC_IDS:
                    new_map.map_data.get("layers")[1].get("data").append(MISC_IDS.get(pixel))
                    new_map.map_data.get("layers")[0].get("data").append(199)

                elif pixel in MISC_BACKGROUND_IDS:
                    new_map.map_data.get("layers")[0].get("data").append(MISC_BACKGROUND_IDS.get(pixel))
                    new_map.map_data.get("layers")[1].get("data").append(0)

                elif pixel in ANCHOR_IDS:
                    new_anchor = StarboundObject(ANCHOR_IDS.get(pixel), 8, new_map.map_data.get("nextobjectid"), 8, x, y, 0, 0)
                    new_map.map_data.get("layers")[8].get("objects").append(new_anchor.object_data)
                    new_map.map_data["nextobjectid"] += 1
                    new_map.map_data.get("layers")[1].get("data").append(0)
                    new_map.map_data.get("layers")[0].get("data").append(199)

                else:
                    with open(dungeon_file, 'r') as read_file:
                        fixed_json = ''.join(line for line in read_file if not line.startswith("    //"))
                        data = json.loads(fixed_json)

                    for tiles in data["tiles"]:
                        if "brush" in tiles:
                            value = tiles["value"]

                            if pixel == (value[0], value[1], value[2], value[3]):
                                if "npc" not in str(tiles["brush"]) and "stagehand" not in str(tiles["brush"]):

                                    if tiles["brush"][1][1] in TILE_IDS:
                                        if "foreground" in tiles["comment"]:
                                            new_map.map_data.get("layers")[1].get("data").append(TILE_IDS.get(tiles["brush"][1][1]))
                                            new_map.map_data.get("layers")[0].get("data").append(199)
                                            break

                                        elif "background" in tiles["comment"]:
                                            new_map.map_data.get("layers")[0].get("data").append(TILE_IDS.get(tiles["brush"][1][1]))
                                            new_map.map_data.get("layers")[1].get("data").append(0)
                                            break

                                        else:
                                            new_map.map_data.get("layers")[1].get("data").append(TILE_IDS.get(tiles["brush"][1][1]))
                                            new_map.map_data.get("layers")[0].get("data").append(199)
                                            break

                                    elif "right" in tiles["comment"]:
                                        add_data(OBJECT_IDS, tiles["brush"][1][1], new_map, x, y)
                                        break

                                    elif "left" in tiles["comment"]:
                                        add_data(OBJECT_FLIPPED_IDS, tiles["brush"][1][1], new_map, x, y)
                                        break

                                    else:
                                        add_data(OBJECT_IDS, tiles["brush"][1][1], new_map, x, y)
                                        break

                                else:
                                    new_map.map_data.get("layers")[1].get("data").append(0)
                                    new_map.map_data.get("layers")[0].get("data").append(199)
                                    break

        new_file_name = os.path.splitext(file)
        with open(output_folder + new_file_name[0] + ".json", "w") as write_file:
            json.dump(new_map.map_data, write_file, indent=4)


if __name__ == '__main__':
    convert()