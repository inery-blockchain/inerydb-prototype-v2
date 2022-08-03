from api.cline import Cline
from generator.generator import generateStructures
import os, subprocess


# Create Contract    
contractName = input("Database name : ")
generateStructures(contractName)

try :
    output = subprocess.check_output(["inery-cpp","--version"])
    print(output.decode())
except :
    print('No compiler found\n, check .bashrc if path to bin is exported and sourced')

# Compile contract
print("Compiling...")
path = os.path.join(os.getcwd(), f'generator/contracts/{contractName}/')
os.system(f'inery-cpp {path}{contractName}.cpp -o {path}/{contractName}.wasm ')

# Connect contract with account
account = input("Account : \n")
pri_key = input("Privae key of an aaccount : \n")

wasm = contractName + '.wasm'
wasm = os.path.join(path, wasm)

abi = contractName + '.abi'
abi = os.path.join(path, abi)



a = Cline()
a.set_code(account, "owner", wasm, pri_key)
a.set_abi(account, "owner", abi, pri_key)






