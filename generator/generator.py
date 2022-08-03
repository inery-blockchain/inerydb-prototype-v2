#!/usr/bin/python3
#todo implement solution for adding vector as a type and dictinary(map)
import os, subprocess


def generateTableDictinary(contractName) :
    dic = dict()
    numOfTables = int(input("How many tables?")) 
    c = 0
    while c < numOfTables : 
        #todo make enum for types (string, int)
        currentTable = f"$table{c+1}"
        dic[currentTable] = {}
        # make sure contractName and tableName have diffrent names
        while True:
            x = input(f"Enter name of table {c+1} : ")
            if x == contractName :
                print("Table and Database must have different names")
                continue
            else :
                break
        
        dic[currentTable]["name"] = x
        dic[currentTable]["elements"] = []

        numElem = int(input("How many elements should table consist?\n"))
        j=0
        while j < numElem :
            x = {f"$type{j+1}": input(f"What type is {j+1}. element\n"), f"$name{j+1}" : input(f"Name of {j+1}. element\n")}
            dic[currentTable]["elements"].append(x)
            j+=1
        c+=1
    return dic

def generateStructures(contractName) :

    dic = generateTableDictinary(contractName)


    constructor=f'''#include <inery/inery.hpp>
#include <string>

using namespace inery;
using namespace std;

class [[inery::contract("{contractName}")]] {contractName} : public contract {"{"}
    public:
        using contract::contract;
        {contractName}(name reciever, name code, datastream<const char*> ds ) : contract(reciever, code, ds) {"{"}{"}"}

'''
    try: 
        os.mkdir(f'generator/contracts/{contractName}')
    except :
        pass

    code = open(f'generator/contracts/{contractName}/{contractName}.cpp', 'w+')

    code.write(constructor)
    
    id = '\t\tuint64_t\tid;\n'
    end = '\t\tuint64_t primary_key() const {return id; }\n\t};\n'

    element = '\t\t$type\t$name;\n'

    cnt =0
    for i in dic :
        table = dic[i]["name"]
        name = f'\tstruct [[inery::table("{table}")]] {table} {"{"}\n'
        typedef = f'\ttypedef inery::multi_index<"{table}"_n, {table}> table_inst{cnt};\n\n'

        code.write(name + id)
        
        for j in range(len(dic[i]["elements"])) :
            t = dic[i]["elements"][j][f'$type{j+1}']
            n = dic[i]["elements"][j][f'$name{j+1}']
            currentElement = element.replace('$type', t).replace('$name', n)
            code.write(currentElement)
        code.write(end + typedef)
        cnt+=1

    # ACTIONS 
    
    # parameter list
    # todo prebaci ovu unutrasnju petlju pravljenja liste elemenata u petlju kreiranja funkcije
    parametersList = []
    parametersList2 = []
    for m in dic :
        parameters = ''
        for j in range(len(dic[m]["elements"])) : 
            y = dic[m]["elements"][j][f'$type{j+1}']
            z = dic[m]["elements"][j][f'$name{j+1}']
            if len(dic[m]["elements"]) > j+1 :
                parameters += y + ' ' + z + ', '
            else :
                parameters += y + ' ' + z

        parametersList.append(f'({parameters})')
        parametersList2.append(f'(uint64_t id, {parameters})')

    # currently deployed create and update funcs

    # action syntax parts and assebly
    pom = 0
    for tbl in dic :
        table = dic[tbl]["name"]

        declareCr = f'\n\t[[inery::action]] void cr{table} {parametersList[pom]} {"{"}\n'
        declareUp = f'\n\t[[inery::action]] void up{table} {parametersList2[pom]} {"{"}\n'
        declareDl = f'\n\t[[inery::action]] void dl{table} (uint64_t id) {"{"}\n'
    
        table_instance = f'\t\ttable_inst{pom}  {table}(get_self(), get_self().value);\n'
        
        itr = f'\t\tauto itr = {table}.find(id);\n'
        check = f'\t\tcheck(itr != {table}.end(), "No entity with that id ");\n'

        modify = f'\t\t{table}.modify(itr, get_self(), [&](auto &row){"{"}\n'        
        emplace = f'\t\t{table}.emplace(get_self(), [&](auto &row){"{"}\n'
        delete = f'\t\t{table}.erase(itr);'
        
        id = f'\t\t\trow.id = {table}.available_primary_key();\n'

        element = '\t\t\trow.$name = $name;\n'
        
        close = '\t\t});\n\t}'

        # write for create action
        code.write(declareCr + table_instance + emplace + id)
        for e in range(len(dic[tbl]["elements"])) : 
            code.write(element.replace('$name', dic[tbl]["elements"][e][f"$name{e+1}"]))
        code.write(close)
        # write for update action
        code.write(declareUp + table_instance  + itr + check + modify)
        for e in range(len(dic[tbl]["elements"])) : 
            code.write(element.replace('$name', dic[tbl]["elements"][e][f"$name{e+1}"]))
        code.write(close)
        # write for delete action
        code.write(declareDl + table_instance + itr + check + delete + '\n\t}')

        pom+=1
    
    code.write('\n};')
    code.close()
  

    
    



