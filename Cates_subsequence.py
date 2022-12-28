#Hazelyn Cates
#Started 12/28/22
#This program finds the longest common subsequence between two DNA sequences

import re
import math
import time

def LC_substring(s1, s2, s1_len, s2_len, string_count1, string_count2):
    #the size of the table/matrix to store the results of the longest common suffix is size s1_len * s2_len:
    LC_suffix = [[0 for i in range(s1_len + 1)] for j in range(s2_len + 1)]  #initialize table to all zeros
    #print(LC_suffix)

    #time how long each function call takes:
    start_substring = time.perf_counter()

    #populate the table with values indicating if the strings match or not
    for i in range(0, s2_len + 1): #rows
        for j in range(0, s1_len + 1): #columns
            if i == 0 or j == 0:
                LC_suffix[i][j] = 0

            elif s1[j - 1] == s2[i - 1]: #meaning at index i-1 and index j-1 strings s1 and s2 match, respectively
                LC_suffix[i][j] = LC_suffix[i - 1][j - 1] + 1  #the value at index i,j in the matrix gets replaced
                                                               #by the value at the previous index plus 1 to indicate a match

            else:
                LC_suffix[i][j] = max(LC_suffix[i - 1][j], LC_suffix[i][j - 1])
                #if they're not equal or set to 0, this takes the max of the value in the LC_suffix table
                #between the value at the previous row on the same column (i-1, j) and the value on the same row
                #but previous column (i, j-1)
    #print(LC_suffix)

    #once the table has been generated, call the LC_suffix function to actually find the LC suffix and print the resulting LCS
    find_LC_suffix(LC_suffix, s1, s2, s1_len, s2_len, string_count1, string_count2, start_substring)


#Takes the table generated in "LC_substring" and the two strings being compared as arguments and prints out the resulting LCS
def find_LC_suffix(LC_suffix, s1, s2, s1_len, s2_len, string_count1, string_count2, start_time):
    #from the table generated by the above code, the length of the LCS is given by the last index in the table (bottom right value)
    LCS_length = LC_suffix[s2_len][s1_len]
    #print(LCS_length)

    LCS = [0 for i in range(0, LCS_length)]  #initialize an empty array the size of the substring to hold the LCS
    LCS[LCS_length - 1] = 0  #set the last index in the array to 0 (i.e. empty)
    comps = 0  #this records the number of comparisons needed to find the LCS

    #set lengths of strings
    m = s1_len
    n = s2_len

    #while neither string is empty, continue trying to find the longest common subsequence starting at the end of each string and working back
    #Finding the longest common suffix eventually culminates into the longest common subsequence
    while m > 0 and n > 0:
        #want to check if the two strings have the same character at a given index:
        if s1[m - 1] == s2[n - 1]:  #have to subtract 1 since the strings are indexed starting at 0
            LCS[LCS_length - 1] = s1[m - 1]  #since the LCS array is also indexed from 0, the last spot in its array,would be at the length of the subsequence minus 1
            m -= 1  #take 1 off the length of the first string
            n -= 1  #take 1 off the length of the second string
            LCS_length -= 1  #take 1 off the length of the size of the LCS since a match has been found
            comps += 1 #this indicates a comparison has been made

        #if the first string is longer than the second, then you can't do any comparisons and have to decrement m
        #and vice versa, decrement n.
        #The goal is to travel along the diagonal of values created in the DP table
        #Which is like a path that tells you which characters are in the LCS
        #So by comparing the numbers in the table, you can figure out which characters get included in the LCS

        #check if string 2 is longer than string 1
        elif LC_suffix[n - 1][m] > LC_suffix[n][m - 1]:
            n -= 1 #only decrement length of string 2
            comps += 1 #indicates a comparison has been made

        #in the case that string 1 is longer than string 2
        else:
            m -= 1 #only decrement length of string 1
            comps += 1 #indicates a comparison has been made

    #join all characters that make up the LCS
    LCS_final = "".join(LCS)
    LCS_length = LC_suffix[s2_len][s1_len] #determines its length from the DP table generated in LC_substring function

    #Calculating the total number of possible substring combinations between the two sequences (n!/m!(n-m)!):
    total_substrings = 0 #variable to hold all possible combinations, initialize to 0
    length1 = max(s1_len, s2_len) #this corresponds to "n" in the above formula
    length2 = min(s1_len, s2_len) #this corresponds to "m" in the above formula

    total_substrings = math.factorial(length1) // (math.factorial(length2) * math.factorial(length1-length2))
    total_substrings_SN = "{:.2e}".format(total_substrings) #express value in scientific notation
    #print(total_substrings_SN)

    end_substring = time.perf_counter()
    substring_time = end_substring - start_time

    #need to replace the write statements with print statements
    print("\nString %d: %s\n" % (string_count1+1, s1))
    print("String %d: %s\n" % (string_count2+1, s2))
    print("Length of string %d: %d\n" % (string_count1+1, s1_len))
    print("Length of string %d: %d\n" % (string_count2+1, s2_len))
    print("Longest common substring between strings %d and %d: %s\n" % (string_count1+1, string_count2+1, LCS_final))
    print("LCS length: %d\n" % LCS_length)
    print("Number of comparisons: %d\n" % comps)
    print("All possible substring combinations between strings %d and %d: %s combinations\n" % (string_count1+1, string_count2+1, total_substrings_SN))
    print("Execution time for finding LCS between strings %d and %d: %.2e seconds" % (string_count1+1, string_count2+1, substring_time))
    print("\n\n")


#MAIN: File input
print("Enter full name of text file:")
file_name = input()
open_file = open(file_name, "r")

print("How many DNA sequences are in your file?")
num = int(input())
#print(num)

sequence = [] #array to store the sequences from the input file
#print(sequence)

#get only the sequences out of the file and store them in an array
for line in open_file:
    #print(line.strip())
    #only want the sequence, not the label or the "=", so use regex
    line.upper() #put all letters to uppercase
    s = re.search(r'(\w+)$', line) #everything after the equals sign up to a new line

    if s:
            seq = s.group() #only want to extract the sequence from the line, not the whole line
            #check if sequence is valid
            if re.search(r'[^ATCG]', seq): #if any characters besides the 4 bases are present, it's NOT a valid sequence
                print("Input sequence is not valid. Please restart with valid sequences.")
                exit(1) #exit program
            else: #if sequence is valid:
                sequence.append(seq) #append each extraced sequence to the sequence array

#NOT DOING FILE INPUT IN THIS PROGRAM
#file to write results to, open in append mode
#results_file = open("output.txt", "a")

#to call the functoin to make sure all sequences aree being compared to each other by using a nested for loop:
for i in range(0, num):
    for j in range(i+1, num):
        LC_substring(sequence[i], sequence[j], len(sequence[i]), len(sequence[j]), i, j)


