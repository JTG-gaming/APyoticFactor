# APyotic Factor

### A Python wrapper for querying server rules from an Abiotic Factor Dedicated Server

How to Use:
```Python
AF_ServerInfo(ip_address, port=27015)
	# Accepts server IP Address or Domain Name + Port (Default is 27015)
	# Returns AF_ServerInfo	object which contains the following Functions
```

Available Functions:
```Python
get_info(return_as_bytes=False)
	# Returns server rules as a dict in key,value format

get_server_name()
	# Returns server name as a string

get_short_code()
	# Returns short code as string (used to Direct Connect)

get_player_count()
	# Returns player count as integer

get_story_progress()
	# Returns story progress string

close()
	# Closes socket when finished
```

Example:

```Python

from APyoticFactor import AF_ServerInfo

server_info = AF_ServerInfo('127.0.0.1', 27015)

server_rules = server_info.get_info()
print(f"Server Name: {server_rules["ServerName"]}")

server_info.close()
