import connect
import shutter
import logging
import RPi.GPIO as GPIO


def main():
    global _shutDownEvent
    _shutDownEvent = threading.Event()
    signal.signal(signal.SIGINT, signal_handler)


    
    
 



# Execution or import
if __name__ == "__main__":
    # Logging setup
    logging.basicConfig(format="[%(asctime)s][%(module)s:%(funcName)s:%(lineno)d][%(levelname)s] %(message)s", stream=sys.stdout)
    log = logging.getLogger()

    print("\n[DBG] DEBUG mode activated ... ")
    log.setLevel(logging.DEBUG)
    #log.setLevel(logging.INFO)

    # Start executing
    main()


# The END - Jim Morrison 1943 - 1971
#sys.exit(0)