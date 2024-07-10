def solve():
    in1 = 'aaaabbbbccccdddd'
    out1 = 'ccaccdabdbdbbada'
    in2 = 'abcdabcdabcdabcd'
    out2 = 'bcaadbdcdbcdacab'
    
    perms = []
    
    # Break in1 into chunks of four
    # We know it was shuffled in order, so we can generate possible permutations
    # ie: The first four A's have to be mapped to [2, 6, 13, 15], B's to ...
    in1_groups = in1[0:4], in1[4:8], in1[8:12], in1[12:16]
    
    # Find each possible permutation index
    for group in in1_groups:
        for i in range(4):
            perms.append(out1.index(group[i]))
            out1 = out1.replace(group[i], '_', 1)
     
    print(perms)
    # Now we have a list of possible permutations, can break into chunks of four and validate against in2
    perms = [perms[i:i+4] for i in range(0, len(perms), 4)]
    in2_groups = in2[0:4], in2[4:8], in2[8:12], in2[12:16]
    
    final_perm = []
    
    # Check each group of four in in2 against the possible permutations to find the correct one
    for i, group in enumerate(in2_groups):
        for j in range(4):
            for p in perms[i]:
                if out2[p] == group[j]:
                    final_perm.append(p)
    
    print(final_perm)
    
    # ???????????????? -> owuwspdgrtejiiud
    
    print(''.join(['owuwspdgrtejiiud'[p] for p in final_perm]))

perm = solve()
    
    