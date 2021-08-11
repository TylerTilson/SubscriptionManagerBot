import random
import string
import datetime as dt
from datetime import datetime
import discord

from dateutil import parser

# CHANGE
serverID = "412819293122723841"

# CHANGE
roleID = "412822761560473610"

successImage = "https://projectimpact.io/images/verification.png"
errorImage = "https://projectimpact.io/images/incorrect.png"
notifImage = "https://projectimpact.io/images/notificatiobn.png"


def generateKey(days=30):
    key = ["IMPACT"]

    for i in range(3):
        section = ''.join(
            [random.choice(string.ascii_uppercase + string.digits) for n in range(5)])
        key.append(section)

    return ["-".join(key), days]


def calculateEndDate(days):
    endDate = datetime.now() + dt.timedelta(days=days)
    return endDate.strftime("%Y-%m-%d")


def isAdmin(ID, adminList):
    return ID in adminList


async def addSubRole(client, userData):
    servers = client.servers
    for server in servers:
        if (server.id == serverID):
            users = server.members
            for role in server.roles:
                if (role.id == roleID):
                    for user in users:
                        if user.id == userData.id:
                            await client.add_roles(user, role)


async def removeSubRole(client, user):
    servers = client.servers
    for server in servers:
        if (server.id == serverID):
            for role in server.roles:
                if (role.id == roleID):
                    await client.remove_roles(user, role)


def invalidKeyMessage():
    embed = discord.Embed(colour=discord.Colour(
        0xFE0000), description="It seems you have entered an invalid or already used membership key. Before contacting a staff member for futher assistance make sure that the key you entered is correct.")
    embed.set_author(name="Error", icon_url=errorImage)
    return embed


def validKeyMessage(endDate: str):
    embed = discord.Embed(colour=discord.Colour(
        0x2ccb6f), description="Welcome to Impact! Make sure to take advantage of our full array of features. Remember... you can renew your membership at any time using [this](http://wishlist-atc.fetchapp.com/sell/5b589d49) link!")
    embed.set_author(name="Success",
                     icon_url="https://projectimpact.io/images/verification.png")
    dateFormatted = endDate
    dt = parser.parse(dateFormatted)
    dateFormatted = dt.strftime("%B %d, %Y")
    embed.add_field(name="Current Membership End Date", value=dateFormatted)
    return embed


def customGenerateKeyMessage(days, customKey):
    embed = discord.Embed(colour=discord.Colour(
        0x2ccb6f), description="Custom membership key {} has been created and will last {} day(s).".format(customKey, days))
    embed.set_author(name="Success", icon_url=successImage)
    return embed


def notifyAdminActivateMessage(userID):
    embed = discord.Embed(colour=discord.Colour(
        0xF79321), description="<@{}> has activated their membership.".format(userID))
    embed.set_author(name="Notification", icon_url=notifImage)
    return embed


def notifyAdminDeactivateMessage(userID):
    embed = discord.Embed(colour=discord.Colour(
        0xF79321), description="<@{}>'s membership has expired.".format(userID))
    embed.set_author(name="Notification", icon_url=notifImage)
    return embed


def twoDayNotificationMessage():
    embed = discord.Embed(colour=discord.Colour(
        0xF79321), description="We would like to let you know that you have 48 hours remaining in Impact until your membership comes to an end. If you would like to renew please use [this](http://wishlist-atc.fetchapp.com/sell/5b589d49) link!")
    embed.set_author(name="Notification", icon_url=notifImage)

    return embed


def expiredMessage():
    embed = discord.Embed(colour=discord.Colour(
        0xF79321), description="We would like to let you know your membership has come to an end. If you would like to renew please use [this](http://wishlist-atc.fetchapp.com/sell/5b589d49) link!")
    embed.set_author(name="Notification", icon_url=notifImage)
    return embed


def deleteAllUsedKeysMessage():
    embed = discord.Embed(colour=discord.Colour(
        0x2ccb6f), description="All redeemed membership keys have been cleaned from the Database.")
    embed.set_author(name="Success", icon_url=successImage)
    return embed


def deleteAllKeysMessage():
    embed = discord.Embed(colour=discord.Colour(
        0x2ccb6f), description="All membership keys have been deleted from the Database.")
    embed.set_author(name="Success", icon_url=successImage)
    return embed


def removeUserMessage(userID):
    embed = discord.Embed(colour=discord.Colour(
        0x2ccb6f), description="<@{}> has been removed from the Member role and from the Database.".format(userID))
    embed.set_author(name="Success", icon_url=successImage)
    return embed


def renewMessage():
    embed = discord.Embed(colour=discord.Colour(
        0x2ccb6f), description="Click [here](payment_url) to start the renewal process!")
    embed.set_author(name="Success", icon_url=successImage)
    return embed


def main():
    pass


if __name__ == '__main__':
    main()
