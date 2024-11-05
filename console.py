ranks = ["yellow", "purple", "blue", "green"]
mats = [0, 0, 0, 0]

def matCnt(idx):
    global mats, ranks
    for i in range(idx, len(ranks)):
        while True:
            try:
                mats[i] = int(input(f"How many {ranks[i]} material today? "))
                break
            except ValueError: print("\nYou didn't input a number. Try again!")

def calc(idx, reqCnt):
    global mats, ranks
    temp = reqCnt
    print("\nResult:")
    for i in range(idx + 1, len(ranks)):
        if (temp * 3) <= mats[i]:
            print(f"\nYou are now enough on {ranks[i]} material."
                  f"You can now buy {temp * 3} on {ranks[i - 1]} material."
                  f"Craft all materials from {ranks[i - 1]} to {ranks[idx]} materials"
                  f"to get a total of {reqCnt} {ranks[idx]} material.\n")
            break
        else:
            temp = (temp * 3) - mats[i]
            print(f"{ranks[i]} material missing {temp} pieces".capitalize())
            if i == len(ranks) - 1:
                print(f"\nBro, you need {temp} in {ranks[i]} material lmao\n")

# Main
rankNeed = str()
while True:
    rankNeed = input("\nWhat rank material do you need?\n[yellow, purple, green] or [1, 2, 3]: ")
    if rankNeed.isdigit() and 1 <= int(rankNeed) <= 3:
        rankNeed = ranks[int(rankNeed) - 1]
        break
    elif rankNeed not in ranks:
        print("\nInvalid input. Try again!")
    else: break

print("\nEnter your current materials count:")
idxRank = ranks.index(rankNeed)
matCnt(idxRank)

while True:
    try:
        reqCnt = int(input(f"\nHow many {rankNeed} material do you need? "))
        break
    except ValueError: print("\nYou didn't input a number. Try again!")

while True:
    action = input(f"\nDo you want to keep your {rankNeed} material count at {reqCnt}, "
                   f"or deduct your current count ({reqCnt} - {mats[idxRank]})?\n"
                   "[stay, deduct, or press Enter to stay]: ")
    if action in ["stay", ""]:
        calc(idxRank, reqCnt)
        break
    elif action == "deduct":
        calc(idxRank, reqCnt - mats[idxRank])
        break
    else: print("\nInvalid input. Try again!")
