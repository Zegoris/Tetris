for i in range(0, 100):
    for _ in range(0, 3):
        if len(str(i)) < 4:
            i = "0" + str(i)
    print("STRING " + i[0])
    print("DELAY 10")
    print("STRING " + i[1])
    print("DELAY 10")
    print("STRING " + i[2])
    print("DELAY 10")
    print("STRING " + i[3])
    print("DELAY 10")
    print("ENTER")
    print("DELAY 100")
    print()