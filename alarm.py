import time

# have to exit with ctrl c, after pressing q in shuffle
while True:
    curtime = time.localtime()
    # play at 7:01 am local on the 22nd
    if curtime.tm_hour >= 7 and curtime.tm_min > 0 and curtime.tm_mday == 22:
        import shuffle
    else:
        time.sleep(60)
