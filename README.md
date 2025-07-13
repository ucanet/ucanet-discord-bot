# ucanet-discord-bot
A discord bot for managing ucanet domains

For more info about the project, visit [ucanet.net](https://ucanet.net)

## Full Description
This repo contains the code to the python Discord bot used to register and manage ucanet domains. Unless you're operating a separate registry, you probably will not end up running this bot yourself.

## Commands
Command                                    | Context          | Description
-------------------------------------------|------------------|-------------
!register {domain name}                    | #register-domain | Registers a vacant domain name to the requested Discord user.
!help                                      | DMs              | Displays command list.
!list                                      | DMs              | Displays a list of domains and subdomains you have registered.
!set {domain name} {ip address}            | DMs              | Registers an ip address to a domain/subdomain.
!neocities {domain name} {neo cities site} | DMs              | Points the domain to a site hosted on Neocities.
!ddns {domain name} {ddns.net domain name} | DMs              | Points the domain to a self-hosted site with a ddns.net domain name.
!free {domain name} {freesites site}       | DMs              | Points the domain to a site hosted on Freesites.
!check {domain name}                       | DMs              | Checks if domain is registered or not.

## License
[AGPL-3.0 license](https://github.com/ucanet/ucanet-discord-bot/blob/main/LICENSE)
