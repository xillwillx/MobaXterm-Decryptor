![alt text](https://i.imgur.com/bUzFv0g.png)
## What's it do?
Decrypt stored [MobaXterm](https://mobaxterm.mobatek.net/) passwords from the commandline. Utilizes decryption classes from [HyperSine](https://github.com/HyperSine/how-does-MobaXterm-encrypt-password). I couldnt get his version working originally so rewrote some parts in order to understand what the code was doing. This script currently doesnt decode passwords encrypted with a masterpassword (option not available in free version of MobaXterm anyways).


## How to use?
Uses Python3 and you need pycryptodome installed. `pip3 install pycryptodome` 
```
Usage:

From inifile:
    MobaDecrypt.py Computer Username SessionP Hash

From Registry Password:
    MobaDecrypt.py Computer Username SessionP Hash Host/IP User
From Registry Credential:
    MobaDecrypt.py Computer Username SessionP Hash
```

In order to decode you'll need the local **hostname** and the current **username**. you get these from a command prompt or powershell prompt:

cmd.exe
```
echo %username% && echo %computername%
```
powershell.exe
```
$env:UserDomain;$env:ComputerName
```

The hashed passwords and connection history are stored in 2 places, an .ini file, or the registry. 

### Registry
or export the registry key from commandline

```
reg export HKEY_CURRENT_USER\Software\Mobatek mobaxterm.reg
```
In either the reg file you'll have a SessionP number and the Host/IP of the connection and the Username

MobaXterm creds are saved as *passwords* and *credentials* in:

|Type       |Registry Path                      |
|-----------|-----------------------------------|
|Credentials|`HKEY_CURRENT_USER\Software\Mobatek\MobaXterm\C`|
|Passwords  |`HKEY_CURRENT_USER\Software\Mobatek\MobaXterm\P`|


1. Credentials would look like:

   ```
   Name             Type        Data
   example.com      REG_SZ      root:bSj4VWbHezNH3tTY9Nil2RzJX57p7/S6KqMw8VsiT/WH+I8p03pqnInAu
   ```


2. Password would look like:

   ```
   Name                         Type        Data
   ssh22:root@45.32.110.171     REG_SZ      F0+wuBvbe9qPW6ypiOeYHTHhKdShRc/nXaM1Ky1jeTfw46TzQoSesX9buGm0WW36yP4lhH70ZCHZpEo4wLJhIl1
   ```
Credential Example:
```
MobaDecrypt.py DELLComputer Owner 165821882556840 bSj4VWbHezNH3tTY9Nil2RzJX57p7/S6KqMw8VsiT/WH+I8p03pqnInAu
```
Password Example:
```
MobaDecrypt.py ShadowSurface DoubleSine 165821882556840 F0+wuBvbe9qPW6ypiOeYHTHhKdShRc/nXaM1Ky1jeTfw46TzQoSesX9buGm0WW36yP4lhH70ZCHZpEo4wLJhIl1 45.32.110.171 root
```



### .ini File

Locate the MobaXterm.ini configuration file, usually in %MyDocuments%\MobaXterm folder. In the file locate the SessionP number under [Misc] , it'll look similar to SessionP=134452135324.  Passwords are under the [Passwords] section. Similar to  above you decrypt them. AFAIK you dont need the host/ip or user to decrypt
```
MobaDecrypt.py DELLComputer Owner 165821882556840 bSj4VWbHezNH3tTY9Nil2RzJX57p7/S6KqMw8VsiT/WH+I8p03pqnInAu
```
