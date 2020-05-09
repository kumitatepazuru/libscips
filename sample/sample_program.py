import threading
import time

import libscips.signal
import sys


def th(name, goalie):
    sig = libscips.signal.player_signal(send_log=False, recieve_log=False,
                                        analysis_log=("hear", "unknown", "init", "error"))
    r = sig.send_init(name, log=True, goalie=goalie)
    if sig.msg_analysis(r)["type"] == "error":
        sys.exit(1)
    side = sig.msg_analysis(r)["value"][1]
    sig.send_move(-20, -20, log=True)

    ok = 0
    while True:
        r = sig.recieve_msg()
        # print(r)
        ans = sig.msg_analysis(r)
        if ans["type"] == "hear":
            if ans["contents"] == "kick_off_l" and side == "l":
                ok = 1
            elif ans["contents"] == "kick_off_l" and side == "r":
                ok = 0
            if ans["contents"] == "kick_off_r" and side == "r":
                ok = 1
            elif ans["contents"] == "kick_off_r" and side == "l":
                ok = 0
            if ans["contents"] == "play_on":
                ok = 1
            if ans["contents"][:4] == "goal":
                ok = 0
                sig.send_move(-20, -20, log=True)
        if ans["type"] == "see":
            see = sig.see_analysis(r, "b")
            if see is not None:
                # print(see)
                if float(see[1]) != 0.0:
                    sig.send_turn(see[1])
                else:
                    if ok == 1:
                        k = sig.see_analysis(r, ["g", "l" * (side == "r") + "r" * (side == "l")])
                        if float(see[0]) < 1:
                            if k is None:
                                sig.send_kick(50, 135, log=True)
                            else:
                                sig.send_kick(100, k[1], log=True)
                        else:
                            # print("a")
                            sig.send_dash(100)
            else:
                sig.send_turn(10)
        time.sleep(0.05)


for i in range(10):
    threading.Thread(target=th, args=["test1", False]).start()
threading.Thread(target=th, args=["test1", True]).start()
for i in range(10):
    threading.Thread(target=th, args=["test2", False]).start()
threading.Thread(target=th, args=["test2", True]).start()
