from time import time, sleep
from random import seed
from random import randint
import os
import json
import signal
import sys
import datetime

import pytchat

import mc_api as mc

# TODO: Parse blockstate
# TODO: "X" joined the stream

rcon = mc.connect("localhost", "test", port=25576)
chat = pytchat.create(video_id="mTPaIkbMH8Q")
seed(int(time()))

MAIN_ALT = "CVFhyum"
LEFT_ALT = "Hamesh"
RIGHT_ALT = "MrsCVF"


def init_server():
    list_of_cmd = [
        f'setblock 0 4 -5 repeating_command_block{{Command:"execute at PortalHub run tp {RIGHT_ALT} ~-10 4 ~-20 facing entity PortalHub",powered:1b,auto:1b}} destroy',
        f'setblock -2 4 -5 repeating_command_block{{Command:"execute at PortalHub run tp {LEFT_ALT} ~10 4 ~-20 facing entity PortalHub",powered:1b,auto:1b}} destroy',
        f"whitelist on",
        f"whitelist add {MAIN_ALT}",
        f"whitelist add {RIGHT_ALT}",
        f"whitelist add {LEFT_ALT}",
        f"op {MAIN_ALT}",
        f"op {RIGHT_ALT}",
        f"op {LEFT_ALT}",
        f"give PortalHub saddle",
        f"give PortalHub pig_spawn_egg",
        f"time set noon",
        f"gamerule sendCommandFeedback false",
    ]

    for cmd in list_of_cmd:
        print(mc.post(cmd))


init_server()


def signal_handler(self, sig, frame):
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)


def get_player_pos(player: str) -> mc.BlockCoordinates:
    coords = mc.post(f"data get entity {player}")

    coords = coords[coords.find("Pos") :]
    coords = coords[: coords.find("]")]
    coords = coords[coords.find("[") + 1 :]
    coords = coords.split(",")

    try:
        x = float(coords[0][:-1])
        y = float(coords[1][:-1])
        z = float(coords[2][:-1])
    except ValueError:
        x = 0.0
        y = 0.0
        z = 0.0

    return mc.BlockCoordinates(x, y, z)


def center(text, scale=0):
    return mc._set_text(
        text,
        mc.BlockCoordinates(0, 0, 0),
        ["quartz"],
        "mixed",
        "east",
        mc.BlockHandler("replace"),
        scale,
        mc.Block("air"),
    )


def shoot_forward():

    list_of_cmd = [
        "execute at PortalHub run fill ~-1 ~-1 ~ ~1 ~-1 ~-140 minecraft:packed_ice",
        "execute at PortalHub run fill ~-1 ~ ~ ~-1 ~2 ~-140 minecraft:barrier",
        "execute at PortalHub run fill ~1 ~ ~ ~1 ~2 ~-140 minecraft:barrier",
        "execute at PortalHub run fill ~ ~2 ~ ~ ~2 ~-140 minecraft:barrier",
        "execute at PortalHub run data merge entity @e[type=pig,sort=nearest,limit=1] {Motion:[0.0d,0.0d,-8.0d]}",
    ]

    for cmd in list_of_cmd:
        mc.post(cmd)


DIRECTIONS = ["left", "right"]


def shoot_sideway():

    value = randint(0, 1)

    if value == 0:
        mc.post("execute at PortalHub run fill ~-100 ~-1 ~-1 ~ ~-1 ~1 minecraft:ice")
        mc.post(
            "execute at PortalHub run data merge entity @e[type=pig,sort=nearest,limit=1] {Motion:[-8.0d,0.0d,0.0d]}"
        )
    else:
        mc.post("execute at PortalHub run fill ~100 ~-1 ~-1 ~ ~-1 ~1 minecraft:ice")
        mc.post(
            "execute at PortalHub run data merge entity @e[type=pig,sort=nearest,limit=1] {Motion:[8.0d,0.0d,0.0d]}"
        )


FIREWORK_LIST = [
    "{LifeTime:20,FireworksItem:{id:firework_rocket,Count:1,tag:{Fireworks:{Explosions:[{Type:0,Trail:1,Colors:[I;11743532],FadeColors:[I;11743532]}],Flight:1}}}}",
    "{LifeTime:20,FireworksItem:{id:firework_rocket,Count:1,tag:{Fireworks:{Explosions:[{Type:0,Trail:1,Colors:[I;15435844],FadeColors:[I;15435844]}],Flight:1}}}}",
    "{LifeTime:20,FireworksItem:{id:firework_rocket,Count:1,tag:{Fireworks:{Explosions:[{Type:0,Trail:1,Colors:[I;14602026],FadeColors:[I;14602026]}],Flight:1}}}}",
    "{LifeTime:20,FireworksItem:{id:firework_rocket,Count:1,tag:{Fireworks:{Explosions:[{Type:0,Trail:1,Colors:[I;4312372],FadeColors:[I;4312372]}],Flight:1}}}}",
    "{LifeTime:20,FireworksItem:{id:firework_rocket,Count:1,tag:{Fireworks:{Explosions:[{Type:0,Trail:1,Colors:[I;6719955],FadeColors:[I;6719955]}],Flight:1}}}}",
    "{LifeTime:20,FireworksItem:{id:firework_rocket,Count:1,tag:{Fireworks:{Explosions:[{Type:0,Trail:1,Colors:[I;8073150],FadeColors:[I;8073150]}],Flight:1}}}}",
    "{LifeTime:20,FireworksItem:{id:firework_rocket,Count:1,tag:{Fireworks:{Explosions:[{Type:0,Trail:1,Colors:[I;11743532,8073150,4312372,14602026,6719955,15435844],FadeColors:[I;11743532,8073150,4312372,14602026,6719955,15435844]}],Flight:1}}}}",
]


def shoot_firework(offset):
    value = randint(1, len(FIREWORK_LIST)) - 1
    mc.post(
        f"execute at PortalHub run summon firework_rocket ~-{11 + offset} ~{5 + offset / 2} ~-125 {FIREWORK_LIST[value]}"
    )
    mc.post(
        f"execute at PortalHub run summon firework_rocket ~{11 + offset} ~{5 + offset / 2} ~-125 {FIREWORK_LIST[value]}"
    )


def execute_at_cta():
    list_of_cmd = [
        "execute at PortalHub run fill ~-1 ~-1 ~ ~1 ~-1 ~-140 minecraft:packed_ice",
        "execute at PortalHub run fill ~-1 ~ ~ ~-1 ~2 ~-140 minecraft:barrier",
        "execute at PortalHub run fill ~1 ~ ~ ~1 ~2 ~-140 minecraft:barrier",
        "execute at PortalHub run fill ~ ~2 ~ ~ ~2 ~-140 minecraft:barrier",
        "execute at PortalHub run data merge entity @e[type=pig,sort=nearest,limit=1] {Motion:[0.0d,0.0d,-8.0d]}",
    ]

    for cmd in list_of_cmd:
        mc.post(cmd)


def write_comment(
    name,
    msg,
    palette,
    user_name_palette,
    is_superchat=False,
    superchat_value="0",
    role=None,
):

    split_comment = []
    buff = ""
    count = 0
    for char in msg:

        if char.isspace() and count > 15:
            split_comment.append(buff)
            buff = ""
            count = 0
        elif count > 25:
            buff += char
            split_comment.append(buff)
            buff = ""
            count = 0
        else:
            buff += char

        count += 1
    else:
        split_comment.append(buff)
        split_comment.reverse()

    scale = 0

    zones = []
    pos = get_player_pos("portalhub")
    pos.z -= 140

    y = pos.y + 20

    y -= 3 * len(split_comment)

    if role == "cta":
        y -= 12
    if y < pos.y + 4:
        y = pos.y + 4

    for line in split_comment:

        instructions = center(line)
        zone = instructions["zone"]
        x_offset = (zone.pos2.x - zone.pos1.x) / 2

        coords = mc.BlockCoordinates(pos.x - x_offset, y * (scale + 1), pos.z)

        zone = mc.set_text(
            line,
            coords,
            style="mixed",
            palette=palette,
            scale=scale,
        )
        zones.append(zone)
        y += 6
    else:

        instructions = center(f"- {name} -")
        zone = instructions["zone"]
        x_offset = (zone.pos2.x - zone.pos1.x) / 2

        coords = mc.BlockCoordinates(pos.x - x_offset, y * (scale + 1), pos.z)
        zone = mc.set_text(
            f"- {name} -",
            coords,
            style="mixed",
            palette=user_name_palette,
            scale=scale,
        )
        zones.append(zone)

        if is_superchat and superchat_value != "0":
            y += 6

            instructions = center(superchat_value)
            zone = instructions["zone"]
            x_offset = (zone.pos2.x - zone.pos1.x) / 2

            coords = mc.BlockCoordinates(pos.x - x_offset, y * (scale + 1), pos.z)
            zone = mc.set_text(
                superchat_value,
                coords,
                style="uppercase",
                palette="red_sandstone",
                scale=scale,
            )

            y += 6

            instructions = center("Thanks for the donation!! <3")
            zone = instructions["zone"]
            x_offset = (zone.pos2.x - zone.pos1.x) / 2

            coords = mc.BlockCoordinates(pos.x - x_offset, y * (scale + 1), pos.z)
            zone = mc.set_text(
                "Thanks for the donation!! <3",
                coords,
                style="uppercase",
                palette="smooth_red_sandstone",
                scale=scale,
            )

        elif role == "mod":
            y += 6

            string = "* Stream Moderator *"

            instructions = center(string)
            zone = instructions["zone"]
            x_offset = (zone.pos2.x - zone.pos1.x) / 2

            coords = mc.BlockCoordinates(pos.x - x_offset, y * (scale + 1), pos.z)
            zone = mc.set_text(
                string,
                coords,
                style="uppercase",
                palette="red_sandstone",
                scale=scale,
            )
        elif role == "member":
            y += 6

            string = "* Channel Member *"

            instructions = center(string)
            zone = instructions["zone"]
            x_offset = (zone.pos2.x - zone.pos1.x) / 2

            coords = mc.BlockCoordinates(pos.x - x_offset, y * (scale + 1), pos.z)
            zone = mc.set_text(
                string,
                coords,
                style="uppercase",
                palette="red_sandstone",
                scale=scale,
            )
        elif role == "verified":
            y += 6

            string = "* Verified Youtuber *"

            instructions = center(string)
            zone = instructions["zone"]
            x_offset = (zone.pos2.x - zone.pos1.x) / 2

            coords = mc.BlockCoordinates(pos.x - x_offset, y * (scale + 1), pos.z)
            zone = mc.set_text(
                string,
                coords,
                style="uppercase",
                palette="red_sandstone",
                scale=scale,
            )
        elif role == "cta":
            y += 12
            x_offset = (
                -1 + len("Z: " + str("{:,}".format(int(pos.z)).replace(",", " "))) * 2
            )
            coords = mc.BlockCoordinates(pos.x - x_offset, y * (scale + 1), pos.z)
            zone = mc.set_text(
                "Z: " + str("{:,}".format(int(pos.z)).replace(",", " ")),
                coords,
                style="uppercase",
                palette="polished_blackstone",
                scale=scale,
            )
            y += 6
            x_offset = (
                -1 + len("X: " + str("{:,}".format(int(pos.x)).replace(",", " "))) * 2
            )
            coords = mc.BlockCoordinates(pos.x - x_offset, y * (scale + 1), pos.z)
            zone = mc.set_text(
                "X: " + str("{:,}".format(int(pos.x)).replace(",", " ")),
                coords,
                style="uppercase",
                palette="polished_blackstone",
                scale=scale,
            )

        return
        y += 8
        now = datetime.datetime.now()

        if now.minute == 59:

            time_left = str(60 - now.second)
            text = f"Stream ends in: {time_left} seconds"

            instructions = center(text)
            zone = instructions["zone"]
            x_offset = (zone.pos2.x - zone.pos1.x) / 2

            coords = mc.BlockCoordinates(pos.x - x_offset, y * (scale + 1), pos.z)

            zone = mc.set_text(
                text,
                coords,
                style="mixed",
                palette=["oak"],
                scale=scale,
            )

            zones.append(zone)

        else:

            time_left = str(60 - now.minute)
            text = f"Stream ends in: {time_left} minutes"

            instructions = center(text)
            zone = instructions["zone"]
            x_offset = (zone.pos2.x - zone.pos1.x) / 2

            coords = mc.BlockCoordinates(pos.x - x_offset, y * (scale + 1), pos.z)

            zone = mc.set_text(
                text,
                coords,
                style="mixed",
                palette=["oak"],
                scale=scale,
            )

            zones.append(zone)

    return zones


CTA_LIST = [
    "Like and subscribe for more interactive streams!",
]

CTA_SPACING = 100

BLACK_LIST = [
    "sus",
    "sussy",
    "baka",
    "impostor",
    "amogus",
    "among",
    "bakas",
    "amongus",
    "imposter",
    "uwu",
]

MESSAGE_COLOR = ["andesite"]

FORBIDDEN_BLOCKS = [
    "end_portal",
    "nether_portal",
    "end_gateway",
]

BLOCK_LIST = {}

path = os.path.dirname(os.path.abspath(__file__))
actual_path = f"{path}/mc_api/functions/block_list.json"

with open(actual_path) as f:
    BLOCK_LIST = json.load(f)

ITEM_LIST = {}

path = os.path.dirname(os.path.abspath(__file__))
actual_path = f"{path}/mc_api/setup/generated/reports/registries.json"

with open(actual_path) as f:
    dictionnary = json.load(f)
    ITEM_LIST = dictionnary["minecraft:item"]["entries"].keys()

FORBIDDEN_ENTITIES = [
    "wither",
    "ender_dragon",
    "hoglin",
    "zoglin",
    "shulker",
    "player",
    "item",
    "falling_block",
    "area_effect_cloud",
]

ENTITY_LIST = {}

path = os.path.dirname(os.path.abspath(__file__))
actual_path = f"{path}/mc_api/setup/generated/reports/registries.json"

with open(actual_path) as f:
    dictionnary = json.load(f)
    ENTITY_LIST = dictionnary["minecraft:entity_type"]["entries"].keys()

prev_zone = []
msg_index = 0
username_buffer = {}
start = time()

while chat.is_alive():

    for c in chat.get().sync_items():

        msg_index += 1

        if msg_index % CTA_SPACING == 0:
            print(msg_index)

            write_comment(
                "* Stream *",
                CTA_LIST[int(msg_index / CTA_SPACING) % len(CTA_LIST)],
                ["brick"],
                ["smooth_sandstone"],
                role="cta",
            )
            shoot_forward()
            mc.post(
                "execute at PortalHub run particle minecraft:end_rod ~ ~15 ~-100 30 10 10 0 3000 force"
            )

            sleep(3)
            mc.post(
                'execute as @e[type=pig,limit=1,sort=nearest] at @s run summon leash_knot ~ ~ ~ {Tags:["Centre"]}'
            )
            mc.post("tp @e[type=pig,limit=1,sort=nearest] @e[tag=Centre,limit=1]")
            mc.post("kill @e[tag=Centre]")
            sleep(2)

        if int(time() - start) > 30:
            username_buffer = {}
            start = time()
        elif c.author.name in username_buffer.keys():
            if (
                c.type in ["superChat", "superSticker", "newSponsor"]
                or c.author.isChatOwner
            ):
                pass
            else:
                continue
        else:
            username_buffer[c.author.name] = True

        shoot_forward()

        if (
            "ender_dragon" in c.message
            or "ender dragon" in c.message
            or "enderdragon" in c.message
        ):
            mc.post(f"disguiseplayer {LEFT_ALT} ender_dragon")
            mc.post(f"disguiseplayer {RIGHT_ALT} ender_dragon")
        elif "wither" in c.message:
            mc.post(f"disguiseplayer {LEFT_ALT} wither")
            mc.post(f"disguiseplayer {RIGHT_ALT} wither")

        index = 0
        new_message = []
        exploded = False
        boom_index = 0
        blocks = False
        mobs = False
        items = False
        pos = get_player_pos("PortalHub")
        for word in c.message.split(" "):

            if word.lower() in ["bees!", "bees"]:
                word = "bee"

            if f"minecraft:{word.lower()}" in BLOCK_LIST:

                blocks = True

                if word in FORBIDDEN_BLOCKS:
                    new_message.append(word)
                    continue

                index += 4

                if word == "air":
                    continue

                additional_info = '"}'
                if "piston" in word:
                    additional_info = (
                        '",Properties:{facing:"up"}},TileEntityData:{facing:1}'
                    )

                elif "observer" in word:
                    additional_info = '",Properties:{facing:"down"}}'

                elif "furnace" in word or "dispenser" in word:
                    additional_info = '",Properties:{facing:"south"}}'

                elif "hopper" in word:
                    additional_info = '",Properties:{facing:"down"}}'

                cmd = f'execute at PortalHub run summon minecraft:falling_block {pos.x + 6} {pos.y + 10 + index} {pos.z - 100} {{BlockState:{{Name:"minecraft:{word}{additional_info},Time:1}}'
                mc.post(cmd)

                cmd = f'execute at PortalHub run summon minecraft:falling_block {pos.x - 6} {pos.y + 10 + index} {pos.z - 100} {{BlockState:{{Name:"minecraft:{word}{additional_info},Time:1}}'
                mc.post(cmd)

            elif f"minecraft:{word.lower()}" in ENTITY_LIST:

                if word in FORBIDDEN_ENTITIES:
                    new_message.append(word)
                    continue

                index += 4
                mobs = True

                cmd = f"execute at PortalHub run summon {word} {pos.x + 6} {pos.y + 10 + index} {pos.z - 100}"
                mc.post(cmd)

                cmd = f"execute at PortalHub run summon {word} {pos.x - 6} {pos.y + 10 + index} {pos.z - 100}"
                mc.post(cmd)

            elif f"minecraft:{word.lower()}" in ITEM_LIST:
                index += 4
                items = True

                cmd = f'execute at PortalHub run summon item {pos.x + 6} {pos.y + 10 + index} {pos.z - 100} {{Item:{{id:"{word}",Count:1b}}}}'
                mc.post(cmd)

                cmd = f'execute at PortalHub run summon item {pos.x - 6} {pos.y + 10 + index} {pos.z - 100} {{Item:{{id:"{word}",Count:1b}}}}'
                mc.post(cmd)

            elif word.lower() in ["explode", "boom"]:
                boom_index += 4
                exploded = True
                if not exploded:
                    mc.post(
                        f"execute at PortalHub run particle minecraft:explosion ~ ~15 ~-140 30 10 10 0 500 force"
                    )
                mc.post(
                    f"execute at PortalHub run summon tnt {pos.x - 13} {pos.y + 8 + boom_index} {pos.z - 100} {{Fuse:{20 + boom_index * 4}}}"
                )
                mc.post(
                    f"execute at PortalHub run summon tnt {pos.x + 13} {pos.y + 8 + boom_index} {pos.z - 100} {{Fuse:{20 + boom_index * 4}}}"
                )
                new_message.append(word)

            elif word.startswith("[") and word.endswith("]") and len(word) < 20:
                word = word.strip("[")
                word = word.strip("]")
                try:
                    mc.post(f"disguiseplayer {LEFT_ALT} player {word}")
                    mc.post(f"disguiseplayer {RIGHT_ALT} player {word}")
                except:
                    print("failed to set head")
                if len(c.message.split(" ")) == 1:
                    new_message.extend(["Changed the player skin to: " + word])

            elif word in ["firework", "fireworks"]:
                index += 4
                shoot_firework(index)
                new_message.append(word)

            else:
                if word.replace(".", "").lower() in BLACK_LIST:
                    new_message.append("CENSORED >:(")
                else:
                    new_message.append(word)
        else:
            list_of_true = 0
            for element in [mobs, blocks, items]:
                if element:
                    list_of_true += 1

            if list_of_true > 1 and len(new_message) == 0:
                new_message.append("Spawned some stuff!")
            elif mobs == True and len(new_message) == 0:
                new_message.append("Spawned some entities!")
            elif blocks == True and len(new_message) == 0:
                new_message.append("Spawned some blocks!")
            elif items == True and len(new_message) == 0:
                new_message.append("Spawned some items!")

            new_message = " ".join(new_message)

        if c.type in ["superChat", "superSticker"] or c.author.isChatOwner:
            prev_zone = write_comment(
                c.author.name,
                new_message,
                ["purpur"],
                ["dark_prismarine"],
                is_superchat=True,
                superchat_value=c.amountString
                if c.type in ["superChat", "superSticker"]
                else "0",
                role="owner" if c.author.isChatOwner else None,
            )
            mc.post(
                "execute at PortalHub run particle minecraft:end_rod ~ ~15 ~-100 30 10 10 0 3000 force"
            )
            shoot_firework(4)
            shoot_firework(8)
            shoot_firework(12)
            shoot_firework(16)
        elif c.type == "newSponsor":
            prev_zone = write_comment(
                c.author.name,
                "Thanks for becoming a channel member!",
                ["purpur"],
                ["dark_prismarine"],
            )
            mc.post(
                "execute at PortalHub run particle minecraft:end_rod ~ ~15 ~-100 30 10 10 0 3000 force"
            )
        elif c.author.isChatModerator:
            prev_zone = write_comment(
                c.author.name, new_message, MESSAGE_COLOR, ["warped"], role="mod"
            )
        elif c.author.isChatSponsor:
            prev_zone = write_comment(
                c.author.name, new_message, MESSAGE_COLOR, ["crimson"], role="member"
            )
        elif c.author.isVerified:
            prev_zone = write_comment(
                c.author.name,
                new_message,
                MESSAGE_COLOR,
                ["red_nether_brick"],
                role="verified",
            )
        else:
            prev_zone = write_comment(
                c.author.name, new_message, MESSAGE_COLOR, ["blackstone"]
            )

        if c.type == "superChat":
            sleep(10)
        elif (
            c.author.isChatSponsor
            or c.author.isChatModerator
            or c.author.isVerified
            or c.author.isChatOwner
        ):
            sleep(4)

        if msg_index % 200 == 0 or ("sideway" in c.message and c.author.isChatOwner):
            shoot_sideway()
            sleep(3)
        else:
            sleep(1)

        continue
        now = datetime.datetime.now()
        if now.minute == 0:
            shoot_forward()

            write_comment(
                "* Stream *",
                "Thank you everyone for participating! I'm going to create the next experiment now :) See you soon!",
                ["smooth_sandstone"],
                ["smooth_quartz", "polished_blackstone"],
            )

            exit()
