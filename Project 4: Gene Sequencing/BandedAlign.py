def bandedAlign(seq1, seq2, max_len):
    d = 3
    k = 2*d+1
    #checks if strings are longer than max_len, then cuts them down
    n = max_len
    m = max_len
    if len(seq1) < max_len:
        n = len(seq1)
    if len(seq2) < max_len:
        m = len(seq2)
    seq1 = seq1[:n]
    seq2 = seq2[:m]
    #swap to make longer first and save bool in case they need to swap back
    swapped = False
    if len(seq1) < len(seq2):
        x = seq1
        seq1 = seq2
        seq2 = x
        swapped = True
    #check if strings are too different to compare
    if len(seq1)-len(seq2) > d:
        edit_distance = float('inf')
        seq1 = "No Alignment Possible"
        seq2 = "No Alignment Possible"
        return [edit_distance, seq1, seq2]

    #initialize table for dynamic programming
    table = []
    table2 = []
    for i in range(0,k): #O(n)
        table.append([])
        table2.append([])
        table[i] = [float('inf') for x in range(0, n+1)] #O(kn), occupies kn space
        table2[i] = ["" for x in range(0, n+1)] #O(kn), occupies kn space
    table[d][0] = 0
    table2[d][0] = "src"

    #populate first section (j=0) so the origin point doesn't get wiped by delete
    for i in range(d+1, k):
        table[i][0] = table[i-1][0] + 5
        table2[i][0] = "del"
    #populates table with edit distances and table 2 with corresponding edit types
    for j in range(1, n+1): #O(k)
        for i in range(0, k): #O(kn)
            #check conditions and set sub match
            if i+j-4 < len(seq1): #condition avoids checking out of bounds for sequences old: table[i][j-1] < float('inf')
                match = (seq1[i+j-4] == seq2[j-1])
                if match:
                    sub_match = table[i][j-1] - 3
                else:
                    sub_match = table[i][j-1] + 1
            else:
                sub_match = float('inf')
            #check conditions and set insert
            if i < k - 1:
                insert = table[i+1][j-1] + 5
            else:
                insert = float('inf')
            #check conditions and set delete
            if i > 0:
                delete = table[i-1][j] + 5
            else:
                delete = float('inf')

            #determin min from edit options, add min and edit type to tables
            if i == d and j == 0:
                pass
            else:
                min = insert
                type = "ins"
                if delete < min:
                    min = delete
                    type = "del"
                if sub_match < min:
                    min = sub_match
                    type = "s_m"
                table[i][j] = min
                table2[i][j] = type
    
    #in cases where strings are different lengths the true "corner" of the modified matrix is d + difference, n
    #if that would place it out of bounds, they are too different to compare, which is already taken care of
    dest = d + len(seq1) - len(seq2)

    #modifies strings to add dashes where there were insertions and deletions
    i = dest
    j = n
    type = table2[i][j]
    while type != "src": #O(n)
        if type == "s_m":
            j = j-1
        if type == "ins":
            j = j-1
            i = i+1
            seq1 = seq1[:j+i-3] + '-' + seq1[j+i-3:]
        if type == "del":
            i = i-1
            seq2 = seq2[:j] + '-' + seq2[j:]
        type = table2[i][j]

    #cuts edited strings down to 100 characters
    if len(seq1) > 100:
        seq1 = seq1[:100]
    if len(seq2) > 100:
        seq2 = seq2[:100]
    #swaps back if they were swapped in the beginning
    if swapped:
        x = seq1
        seq1 = seq2
        seq2 = x
        swapped = True
    edit_distance = table[dest][n]
    return [edit_distance, seq1, seq2]