import sqlite3
from typing import Dict, List
from passlib.context import CryptContext
import re


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Encryption Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utils

# Hashing function
def hash(password):
    return pwd_context.hash(password)

# Compare Hashes function
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) 

# DB Manipulation

def get_from_db(query:str,fetchType:str,data = None):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    
    if fetchType == 'one':
        result = cur.execute(query,data).fetchone()
    elif fetchType == 'many':
        result = cur.execute(query,data).fetchmany()
    elif fetchType == 'all' and data:
        result = cur.execute(query,data).fetchall()
    elif fetchType == 'all' and data is None:
        result = cur.execute(query).fetchall()
    con.close()
    
    return result

def add_to_db(query: str,data):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute(query,data)
    
    con.commit()
    con.close()
    
    return data
    
def delete_from_db_by_id(table_name: str,_id):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    
    cur.execute("DELETE FROM {} WHERE id=?".format(table_name),(str(_id),))
    
    con.commit()
    con.close()
    
    return "Entry from {} deleted!".format(table_name)

def update_entry_in_db_by_id(table_name: str,set_query: str ,_id: int):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    
    q = "UPDATE {} SET {} WHERE id=?".format(table_name,set_query)
            
    cur.execute(q,(str(_id),))
    
    con.commit()
    con.close()
    
    return "Entry from {}, with Id: {} updated!".format(table_name,str(_id))

def update_entry_in_db_custom(table_name: str,set_query: str ,_searchCol: str, _searchColValue):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    
    q = "UPDATE {} SET {} WHERE {}=?".format(table_name,set_query, _searchCol)
            
    cur.execute(q,(str(_searchColValue),))
    
    con.commit()
    con.close()
    
    return "Entry from {}, with {}: {} updated!".format(table_name,_searchCol,str(_searchColValue))

def return_set_query_string(data):
    filtered_data = {k:v for k,v in data.items() if v is not None}
    q = ''
    for k,v in filtered_data.items():
        if k != list(filtered_data)[-1]:
            if type(v) == str:
                v = check_for_quote(v)
                q += k + '=' +"'"+v+"'"+',' + ' '
            else:
                q += k + '=' + str(v)+',' + ' '
        else:
            if type(v) == str:
                v = check_for_quote(v)
                q += k + '=' +"'"+v+"'"
            else:
                q += k + '=' + str(v)
    return q

def obj_to_dict(obj):
    obj_dict = vars(obj)
    del obj_dict['_sa_instance_state']
    return obj_dict

def check_for_quote(string: str) -> str:
    if "'" in string:
        string_list = string.split("'") 
        result = ''
        for subString in string_list:
            if subString != string_list[-1]:
                result += subString + "'" + "'"
            else:
                result += subString
        return result
    return string

def dict_to_tuple(list_dict: dict):
    tuple_list = []
    for k,v in list_dict.items():
        tuple_list.append(v)
        
    return tuple(tuple_list)

def cleanNullTerms(d):
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = cleanNullTerms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean

def check_email(email:str) -> bool:
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False