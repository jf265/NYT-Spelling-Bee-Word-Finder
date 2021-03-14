# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 20:18:54 2020

@author: jafra
"""
#Import needed packages
import requests
import json
import pandas as pd

#Import English language dictionary in .json format
dict_en = requests.get('https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json')

#Checking status, 404 would be failed, 200 means success
if dict_en.status_code == 200:
    print("Dictionary downloaded successfully.")
else:
    print("Failed")
    
#Write requested .json file to disk and call it 'dict_en.json'
print("Writing .json file to disk, 'dict_en.json.")

dict_req = dict_en.json()
with open('dict_en.json', 'w') as f:
    json.dump(dict_req, f)

#Open dict_en.json file from disk and storing it in input_dict
print("Loading file from disk.")
input_dict = json.load(open('dict_en.json'))

#Define output_dict as a dataframe, define dict_words as a list
output_dict = pd.DataFrame()
dict_words = []

#Loop through (.items(), loops through key and value at the same time)
#dictionary containing two loop variables, 'majorkey' and 'value'
#Which represents the structure of the input_dict within the variable 
#input_dict, write whatever is in the majorkey loop variable to the empty list
#'dict_words'
print("Iterating through json to create data frame series.")
for majorkey, value in input_dict.items():
    dict_words.append(majorkey)
    
#Write series 'dict_words' to dataframce output_dict and calling column "Terms"
output_dict['Terms'] = pd.Series(dict_words)
print("Data frame written sucessfully.")
print("")

#Getting input letters from user & checking whether input was as intended

lets = input("Please provide the 6 letters around the center without spaces first and the center letter at the end, e.g. 'abcdefg': ")
l1 = lets[0]
l2 = lets[1]
l3 = lets[2]
l4 = lets[3]
l5 = lets[4]
l6 = lets[5]
l7 = lets[6]
print("Your letters are",l1,l2,l3,l4,l5,l6,"with the center letter",l7)
check = input("Is this correct? Type 'Yes' or 'No': ")

while check == "No":
    lets = input("Please provide the 6 letters around the center without spaces first and the center letter at the end, e.g. 'abcdefg': ")
    l1 = lets[0]
    l2 = lets[1]
    l3 = lets[2]
    l4 = lets[3]
    l5 = lets[4]
    l6 = lets[5]
    l7 = lets[6]
    print("Your letters are", l1, l2, l3, l4, l5, l6, "with the center letter", l7)
    check = input("Is this correct? Type 'Yes' or 'No': ")
else:
    print("Great, let's get the cheating going!")

#Generating list of the index and use it to re-order based on word length

dict_sort = []
dict_sort = output_dict['Terms'].str.len().sort_values().index
sorted_dict = output_dict['Terms'].reindex(dict_sort)

#Re-indexing based on new, descending order
sorted_dict = sorted_dict.reset_index(drop = True)
desc_dict = sorted_dict.sort_index(axis = 0, ascending = False)
desc_dict = desc_dict.reset_index(drop = True)

#Filtering descending file to only words witha length greater than 3
#Filtering out any words that do not contain the provided center letter

desc_dict_clean = pd.DataFrame()
no3 = []

for w in desc_dict:
    if len(w) > 3 and l7 in w:
        no3.append(w)
        
desc_dict_clean['Terms'] = pd.Series(no3)

#Writing cleaned and sorted dictionary to .csv and re-opening it

desc_dict_clean.to_csv('Desc_dict_clean.csv', index = False)
clean_dict = pd.read_csv('Desc_dict_clean.csv')

#Placing provided letters into a regex & using it to loop through clean_dict to
#find string matches

lets_re = ("["+lets+"]{4,}")
results = pd.DataFrame()
cheat = clean_dict.loc[clean_dict['Terms'].str.contains(lets_re)]

#Building list of letters that are not to be used to filter the list to only
#words that contain all the user-provided letters

abc = "abcdefghijklmnopqrstuvwxyz"
excl_list = []

#Looping through abc to find all letters that are to be excluded and add an
#'|' to the end of them to use them in a regex - '|' being 'or'
for ch in abc:
    if ch not in lets:
        excl_list.append(ch+"|")

#Formatting the resulting list to be usable by making it into one string, 
#rather than a tuple & removing the right-most '|' to complete the regex
excl_list_one = "".join(excl_list)
excl_list_final = excl_list_one[0:37]

#Using created exclusion list to filter the word list to only words that contain
#the user provided letters

results = cheat.loc[~cheat['Terms'].str.contains(excl_list_final)]

#Adding a column with word length and dropping a legacy index column

results['Word Length'] = results['Terms'].str.len()

#Outputting final results
print("")
print("Let this list of words bee yours:")
print("")
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(results)

