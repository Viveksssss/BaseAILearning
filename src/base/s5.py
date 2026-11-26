print("name is {0} ,age is {1}".format("bob",23))
print("{:>8}".format(12))


strings = ("puppy", "kitten", "puppy", "puppy", "weasel", "puppy", "kitten", "puppy")

counts = {}

# for kw in strings:
#     if kw not in counts:
#         counts[kw]=1
#     else :
#         counts[kw] += 1    
    
    
for kw in strings:
    counts[kw] = counts.setdefault(kw,0) + 1
    
print(counts)

nums = [1,2,3,4,5]
print(any( (i %2) for i in nums))
print(any( ( i>6 for i in nums)))