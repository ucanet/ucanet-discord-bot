import discord
import socket
from ucanetlib import *

DISCORD_TOKEN = "YOUR_TOKEN" # Set to your Discord bot token
GUILD_ID = 000000000000000000 # Set to the Discord server id to operate in
CHANNEL_ID = 000000000000000000 # Set to the channel id to operate in

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)


def host_address(host_name):
        try:
                return socket.gethostbyname(host_name)
        except:
                return False

async def success_message(channel, title, text):
        discord_embed = discord.Embed(title=title, description=text, color=0x109319)
        discord_embed.set_footer(text = "Note: changes take 10+ minutes to propagate")
        await channel.send(embed = discord_embed)

async def error_message(channel, title, text):
        discord_embed = discord.Embed(title=title, description=text, color=0xFF3030)
        await channel.send(embed = discord_embed)

@client.event
async def on_ready():
        print(f'We have logged in as {client.user}')
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!help in DMs.'))

@client.event
async def on_message(message):
        arg_list = message.content.split(' ')

        if message.author == client.user:
                return

        if message.guild is None:
                if len(arg_list) > 0 and arg_list[0] == "!help":
                        discord_embed = discord.Embed(title="Help - Commands", description="The following is a list of commands available:", color=0x109319)
                        discord_embed.add_field(name="!help", value="shows command list", inline=False)
                        discord_embed.add_field(name="!list", value="displays a list of domains and subdomains you have registered", inline=False)
                        discord_embed.add_field(name="!set <domain name> <ip address>", value="registers an ip address to a domain/subdomain", inline=False)
                        discord_embed.add_field(name="!neocities <domain name> <Neocities site>", value="points the domain to a site hosted on neocities", inline=False)
                        discord_embed.add_field(name="!ddns <domain name> <ddns.net subdomain>", value="points the domain to a self-hosted site with a ddns.net sub-domain", inline=False)
                        discord_embed.add_field(name="!free <domain name> <free.nf site>", value="points the domain to a site hosted on free.nf", inline=False)
                        discord_embed.add_field(name="!check <domain name>", value="checks if domain is registered or not", inline=False)
                        await message.author.send(embed = discord_embed)

                if len(arg_list) > 1 and arg_list[0] == "!check":
                        if not find_entry(arg_list[1]):
                                if formatted_domain := format_domain(arg_list[1]):
                                        if not second_level(arg_list[1]):
                                                await success_message(message.author, 'Domain Available!', ":white_check_mark: This domain can be registered! :white_check_mark:\nGo to `#register-domain` to register this domain.")
                                        else:
                                                await error_message(message.author, 'Domain Check Failed', ':x: A subdomain cannot be checked solely. :x: Try a domain.')
                                else:
                                        await error_message(message.author, 'Domain Check Failed', ':x: Invalid domain format. :x: Try an example: ucanet.net')
                        else:
                                await error_message(message.author, ':x: Domain Taken.', ':lock: This domain is registered! :lock: Try using a different suffix (.co, .net, .org).')

                if len(arg_list) > 0 and arg_list[0] == "!list":
                        domain_list = user_domains(message.author.id)
                        if len(domain_list) > 0:
                                discord_embed = discord.Embed(title="Domain List", description="The following is a list of your registered domains:", color=0x109319)
                                domain_count = 0
                                for domain_name, current_ip in domain_list.items():
                                        current_label = "IP Address" if format_ip(current_ip) else "Neocities Site"
                                        if format_ip(current_ip) and current_ip == "0.0.0.0":
                                                current_ip = "(Not set)"
                                        domain_count += 1
                                        discord_embed.add_field(name=f'{domain_count}. {domain_name}', value=f'{current_label}: {current_ip}', inline=False)

                                await message.author.send(embed = discord_embed)
                        else:
                                await error_message(message.author, 'Domain List Failed', ':question: Looks like you do not have any registered domains! Go to `#register-domain` to register a domain.')

                if len(arg_list) > 2 and arg_list[0] == "!set":
                        if formatted_domain := format_domain(arg_list[1]):
                                if find_entry(formatted_domain):
                                        domain_list = user_domains(message.author.id)
                                        if formatted_domain not in domain_list.keys():
                                                if second_level(formatted_domain) and second_level(formatted_domain) in domain_list.keys():
                                                        pass
                                                else:
                                                        await error_message(message.author, 'IP Set Failed', ":x: This domain is not registered to your account. :x:\nType `!list` for a list of your registered domains/subdomains.")
                                                        return
                                        if formatted_ip := format_ip(arg_list[2]):
                                                if register_ip(formatted_domain, message.author.id, formatted_ip):
                                                        await success_message(message.author, 'IP Set Success', f':white_check_mark: You have successfully set the IP Address of `{formatted_domain}` :white_check_mark:' + "\nYou can revert this using the `!set <domain name> none` command.")
                                                else:
                                                        await error_message(message.author, 'IP Set Failed', ':x: You have reached the domain/subdomain limit of 20! :x:')
                                        else:
                                                await error_message(message.author, 'IP Set Failed', ':x: Invalid IP Address format. :x:')
                                else:
                                        await error_message(message.author, 'IP Set Failed', ":x: This domain does not exist. :x:\nType `!list` for a list of your registered domains/subdomains.")
                        else:
                                await error_message(message.author, 'IP Set Failed', ':x: Invalid domain format. :x:')

                if len(arg_list) > 2 and arg_list[0] == "!neocities":
                        if formatted_domain := format_domain(arg_list[1]):
                                if find_entry(formatted_domain):
                                        domain_list = user_domains(message.author.id)
                                        if formatted_domain not in domain_list.keys():
                                                if second_level(formatted_domain) and second_level(formatted_domain) in domain_list.keys():
                                                        pass
                                                else:
                                                        await error_message(message.author, 'Neocities Set Failed', ":x: This domain is not registered to your account. :x:\nType `!list` for a list of your registered domains/subdomains.")
                                                        return
                                        formatted_neo = format_domain(arg_list[2] + ".com")
                                        if formatted_neo and not second_level(formatted_neo):
                                                neocities_host = f"{arg_list[2].lower()}.neocities.org"
                                                if register_ip(formatted_domain, message.author.id, neocities_host):
                                                        await success_message(message.author, 'Neocities Set Success', f':white_check_mark: You have successfully pointed `{formatted_domain}` to a Neocities site :white_check_mark:' + "\nYou can revert this using the `!set <domain name> none` command.")
                                                else:
                                                        await error_message(message.author, 'Neocities Set Failed', ':x: You have reached the domain/subdomain limit of 20! :x:')
                                        else:
                                                await error_message(message.author, 'Neocities Set Failed', ':x: Invalid Neocities format. :x:')
                                else:
                                        await error_message(message.author, 'Neocities Set Failed', ":x: This domain does not exist. :x:\nType `!list` for a list of your registered domains/subdomains.")
                        else:
                                await error_message(message.author, 'Neocities Set Failed', ':x: Invalid domain format. :x:')

                if len(arg_list) > 2 and arg_list[0] == "!ddns":
                        if formatted_domain := format_domain(arg_list[1]):
                                if find_entry(formatted_domain):
                                        domain_list = user_domains(message.author.id)
                                        if formatted_domain not in domain_list.keys():
                                                if second_level(formatted_domain) and second_level(formatted_domain) in domain_list.keys():
                                                        pass
                                                else:
                                                        await error_message(message.author, 'ddns.net Set Failed', ":x: This domain is not registered to your account. :x:\nType `!list` for a list of your registered domains/subdomains.")
                                                        return
                                        formatted_neo = format_domain(arg_list[2] + ".com")
                                        if formatted_neo and not second_level(formatted_neo):
                                                neocities_host = f"{arg_list[2].lower()}.ddns.net"
                                                if register_ip(formatted_domain, message.author.id, neocities_host):
                                                        await success_message(message.author, 'Ddns Set Success', f':white_check_mark: You have successfully pointed `{formatted_domain}` to a ddns site :white_check_mark:' + "\nYou can revert this using the `!set <domain name> none` command.")
                                                else:
                                                        await error_message(message.author, 'Ddns Set Failed', ':x: You have reached the domain/subdomain limit of 20! :x:')
                                        else:
                                                await error_message(message.author, 'Ddns Set Failed', ':x: Invalid Neocities format. :x:')
                                else:
                                        await error_message(message.author, 'Ddns Set Failed', ":x: This domain does not exist. :x:\nType `!list` for a list of your registered domains/subdomains.")
                        else:
                                await error_message(message.author, 'Ddns Set Failed', ':x: Invalid domain format. :x:')

                print("arg_list:", arg_list)
                if len(arg_list) > 2 and arg_list[0] == "!free":
                        print("Command recognized")
                        if formatted_domain := format_domain(arg_list[1]):
                                print("Formatted domain:", formatted_domain)
                                if find_entry(formatted_domain):
                                        print("Domain exists in DB")
                                        domain_list = user_domains(message.author.id)
                                        if formatted_domain not in domain_list.keys():
                                                print("Checking subdomain ownership")
                                                if second_level(formatted_domain) and second_level(formatted_domain) in domain_list.keys():
                                                        print("Subdomain accepted")
                                                else:
                                                        print("Not owned - error returned")
                                                        await error_message(message.author, 'Freesites Set Failed', ":x: This domain is not registered to your account. :x:\nType `!list` for a list of your registered domains/subdomains.")
                                                        return
                                        print("Domain is allowed")
                                        formatted_neo = format_domain(arg_list[2] + ".com")
                                        print("Formatted neo:", formatted_neo)
                                        if formatted_neo and not second_level(formatted_neo):
                                                neocities_host = f"{arg_list[2].lower()}.free.nf"
                                                print("Registering", formatted_domain, "to", neocities_host)
                                                if register_ip(formatted_domain, message.author.id, neocities_host):
                                                        await success_message(message.author, 'Freesites Set Success', f':white_check_mark: You have successfully pointed `{formatted_domain}` to a Freesites site :white_check_mark:' + "\nYou can revert this using the `!set <domain name> none` command.")
                                                else:
                                                        await error_message(message.author, 'Freesites Set Failed', ':x: You have reached the domain/subdomain limit of 20! :x:')
                                        else:
                                                await error_message(message.author, 'Freesites Set Failed', ':x: Invalid Freesites format. :x:')
                                else:
                                        await error_message(message.author, 'Freesites Set Failed', ":x: This domain does not exist. :x:\nType `!list` for a list of your registered domains/subdomains.")
                        else:
                                await error_message(message.author, 'Freesites Set Failed', ':x: Invalid domain format. :x:')

                return




        if message.guild.id == GUILD_ID and message.channel.id == CHANNEL_ID:
                if len(arg_list) > 1 and arg_list[0] == "!register":
                        if not find_entry(arg_list[1]):
                                if formatted_domain := format_domain(arg_list[1]):
                                        if not second_level(arg_list[1]):
                                                if register_domain(formatted_domain, message.author.id):
                                                        await message.reply(f'<@{message.author.id}> has successfully registered `{formatted_domain}`!')
                                                        await success_message(message.author, 'Registration Successful.', f':white_check_mark: You have successfully registered `{formatted_domain}` :white_check_mark:' + "\nSet an ip address with the `!set <domain name> <ip address>` command.")

                                                        if initial_address := host_address(formatted_domain):
                                                                register_ip(formatted_domain, message.author.id, initial_address)

                                                        await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="domain registerer"))
                                                else:
                                                        await error_message(message.author, 'Registration Failed.', ':x: You have reached the domain/subdomain limit of 20! :x:')
                                        else:
                                                await error_message(message.author, 'Registration Failed.', ':x: A subdomain cannot be registered solely. :x: Try again later.')
                                else:
                                        await error_message(message.author, 'Registration Failed.', ':x: Invalid domain format. :x: Try again later.')
                        else:
                                await error_message(message.author, 'Registration Failed.', ":x: This domain already exists.\n\n:x: Use `!check <domain name>` in this private channel to check the ownership of a domain.")

                return


ucanetlib.init_library()
client.run(DISCORD_TOKEN)
