import sys
import libscips.player
import threading


def th(name, goalie):
    sig = libscips.player.player_signal(send_log=False, recieve_log=True,
                                        analysis_log=("hear", "unknown", "init", "error"))
    r = sig.send_init(name, log=True, goalie=goalie)
    if sig.msg_analysis(r)["type"] == "error":
        sys.exit(1)
    sig.send_move(-20, -20, log=True)
    while True:
        sig.recieve_msg()


for i in range(10):
    threading.Thread(target=th, args=["test1", False]).start()
threading.Thread(target=th, args=["test1", True]).start()
for i in range(10):
    threading.Thread(target=th, args=["test2", False]).start()
threading.Thread(target=th, args=["test2", True]).start()