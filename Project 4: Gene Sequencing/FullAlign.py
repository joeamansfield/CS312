def fullAlign(seq1, seq2, max_len):
    #checks if strings are longer than max_len, then cuts them down
    n = max_len
    m = max_len
    if len(seq1) < max_len:
        n = len(seq1)
    if len(seq2) < max_len:
        m = len(seq2)
    seq1 = seq1[:n]
    seq2 = seq2[:m]

    #initialize table for dynamic programming
    table = []
    table2 = []
    for i in range(0,n+1): #O(n)
        table.append([])
        table2.append([])
        table[i] = [0 for x in range(0, m+1)] #O(mn), occupies mn space
        table2[i] = ["" for x in range(0, m+1)] #O(mn), occupies mn space
    table2[0][0] = "src"
    for i in range(1,n+1): #O(n)
        table[i][0] = table[i-1][0] + 5
        table2[i][0] = "del"
    for j in range(1, m+1): #O(m)
        table[0][j] = table[0][j-1] + 5
        table2[0][j] = "ins"

    #populates table with edit distances and table 2 with corresponding edit types
    for i in range(1, n+1): #O(n)
        for j in range(1, m+1): #O(nm)
            match = (seq1[i-1] == seq2[j-1])
            insert = table[i][j-1] + 5
            delete = table[i-1][j] + 5
            if match:
                sub_match = table[i-1][j-1] - 3
            else:
                sub_match = table[i-1][j-1] + 1
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

    #modifies strings to add dashes where there were insertions and deletions
    i = n
    j = m
    type = table2[i][j]
    while type != "src": #O(n+m)
        if type == "s_m":
            i = i-1
            j = j-1
        if type == "ins":
            j = j-1
            seq1 = seq1[:i] + '-' + seq1[i:]
        if type == "del":
            i = i-1
            seq2 = seq2[:j] + '-' + seq2[j:]
        type = table2[i][j]
    
    edit_distance = table[n][m]

    #cuts edited strings down to 100 characters
    if len(seq1) > 100:
        seq1 = seq1[:100]
    if len(seq2) > 100:
        seq2 = seq2[:100]

    return [edit_distance, seq1, seq2]
    
