## IneryDB prototype python RPC API Dapp

### Pre-requirements

1. Active Node
    - You will need IP or DNS address of active server hosting inery blockchain protocol
    - Node must have API certificate for domain


2. Inery contract development toolkit
Steps for instalation could be found in cdt folder
    - Dependencies for cdt
    - Exported binnaries path to local enviroment


Value contracts represent databases on Inery blockchain.   

Contracts written in C++ are compiled into WASM (Web Assembly) and ABI(Application Binary Interface) files.   
WASM and ABI are connected with account on Inery Blockchain.  
In order to compile your contracts you will need inery cdt 

### Tips for using CLI 

 Step by step process on how to execute helper scripts. 

1. Open Terminal
    - navigate to IneryDB-v2 folder

2. Giving scripts the necessary permissions to run
    - give executable permission to all IneryDB scripts	
    - execute commands :
```sh
    chmod +x db_operation.py \
    chmod +x make_database.py
    chmod +x get_table.py
```
3. Execute Script
    - IneryDB scripts are called by executing command in terminal
        example : "./db_operation.py [option] [argument]".    
                

### Features 

Features that we are currently offering are creating databases and managing data on Inery blockchain.
Using RPC API for extremely fast response. Create database, tables, elements and use CRUD operations over them. 
Save Database content in json format. 

### Create on Inery blockchain 

Account on inery network will be required for contract database creation and deployment.   
You can create custom database with simple types with "make_database.py" script.   

example :  

```
$ python3 db_
Database name : db
How many tables?1
Enter name of table 1 : table1
How many elements should table consist : 1
What type is 1. element : string
Name of 1. element: name

inery-cpp version 1.7.0

Compiling...
action <crtable1> 
action <uptable1> 
action <dltable1>

Account : myacc
Privae key of an account : 5KHoGXZuEpqsfCe3mqHSQni1bUo4BrBbpbuUjxYfiHJU7eDzyeW

Contract Database db succesfully deployed to Inery network on account : myacc

```

### Manage your Data

1. Create table document instance
    - Usage: 

```
$ python3 db_operation.py --create 
Enter Account Name : myacc
Enter Private key of your account: 5KHoGXZuEpqsfCe3mqHSQni1bUo4BrBbpbuUjxYfiHJU7eDzyeW
Enter table : table1
Set name (string) : Peter

====================================================================================
#   myacc <= myacc::settable1        {"name":"Peter"}
====================================================================================

```

2. Get table content
- Usage :    
You will be asked to provide Account and Table name info.
```
$ python3 get_table
Account name : myacc
Table name : table1
``` 
 <strong> Content of table will be saved in table folder with ACCOUNT.TABLE.JSON name format </strong>
    

3. Update table element
- Usage : 

```
$ python3 db_operation.py --update
```

4. Delete table element
- Usage : 

```
$ python3 db_operation.py --delete
```