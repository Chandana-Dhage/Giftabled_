num=int(input("Enter a number: "))

if num < 2:
    print(num, "is not prime")
else:
    flag = True

    for i in range(2, num):
        if num%i == 0:
            print(num, "is divisible by", i)
            flag=False
            break

    if flag:
        print(num, "is prime")
    else:
        print(num, "is not prime")