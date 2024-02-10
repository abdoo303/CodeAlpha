############### task 1

import wonderwords

rw = wonderwords.RandomWord();

w = rw.word(word_max_length=10,word_min_length=2)
n = len(w)
ind = 0
print(f"The word has {n} letters")
trials = 0
while ind < n :
    print("Enter the current letter")
    c = input()
    trials+=1
    if c == w[ind]:
        print("Correct, what a genius!")
        ind+=1
    else: print("Try again.")
print("\nCongrats, you did it!",f"\ntotal trials is {trials}")

