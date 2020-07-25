from inspire_hand_r import InspireHandR
import time
if __name__=='__main__':
    hand = InspireHandR()

    pos1,pos2,pos3,pos4,pos5,pos6 = [0]*6
    pos4 = 550
    hand.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
    start_time = time.time()
    while 1:
        time.sleep(0.1)
        current_time = time.time() - start_time
        if current_time > 5:
            start_time = time.time()
            if pos4 == 550:
                pos4 = 750
            else:
                pos4 = 550
        print(current_time,pos1,pos2,pos3,pos4,pos5,pos6)
        hand.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
        
        