#Error Handleing to confirm Inteded and Permissible indexs are valid
    #pull both columns (inteded and permissible)
    #splice lists together
    #for each num in list:
        #if protospacerstring[num] != 'a':
            #yell at user

#Sub char intended edit index for G
    #pull intended column
    #create new searchstring where searchString = (protospacerstring[intended] = G)
    #add searchString to MasterArray

#Create all variations of searchString with permissible index
    #pull permissble indexs
    #generate all variations of searchString with G at permissible indexes
        #???? come back
    #add all created variations to MasterArray
    
#check whether read is forward or Reversed:
    #if reversed then take reversed compliment of all sequences in Master Array:
    #for seq in MasterArray:
        #for char in seq:
            #if a then g
            #elif g then a
            #elif c then t
            #elif t then c
        #reverse seq

#convert alleles table to csv

#pull any line that matches an index of the MasterArray
