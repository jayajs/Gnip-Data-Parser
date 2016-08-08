'''
Created on Jan 25, 2016

@author: user
'''
import json
def flattenDict(d, result=None):
    '''
    Used to flatten a dictionary $ since json is nothing but a dict 
    $$$Unused ->Loss of information with usage.Do not use
    
    '''
    if result is None:
        result = {}
    for key in d:
        value = d[key]
        if isinstance(value, dict):
            value1 = {}
            for keyIn in value:
                value1[".".join([key,keyIn])]=value[keyIn]
                flattenDict(value1, result)
        elif isinstance(value, (list, tuple)):   
            for indexB, element in enumerate(value):
                if isinstance(element, dict):
                    value1 = {}
                    index = 0
                    for keyIn in element:
                        newkey = ".".join([key,keyIn])        
                        value1[".".join([key,keyIn])]=value[indexB][keyIn]
                        index += 1
                    for keyA in value1:
                        flattenDict(value1, result)   
        else:
            result[key]=value
    return result

fp = open("D:\\File\\MC\\Test_Nukes\\activities_201507120440_201507120450.json",'r')
for line in fp.readlines():
    #print line
    j = json.loads(line)
    print flattenDict(j)