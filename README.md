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
get_info(return_as_bytes=False) -> dict[str,any] | bytes
	# Returns server rules as a dict in key,value format
	# Pass return_as_bytes=True to return raw packet data instead of dict

get_server_name() -> str
	# Returns server name

get_short_code() -> str
	# Returns server short code (used to Direct Connect)

get_player_count() -> int
	# Returns online player count

get_story_progress() -> str
	# Returns story progress identifier

close() -> None
	# Closes socket when finished
```

Example:

```Python

from APyoticFactor import AF_ServerInfo

server_info = AF_ServerInfo('127.0.0.1', 27015)

server_rules = server_info.get_info()
print(f"Server Name: {server_rules["ServerName"]}")

server_info.close()
