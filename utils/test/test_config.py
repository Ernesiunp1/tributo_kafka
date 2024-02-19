import sys
import anfler.util.config.cfg as cfg

if __name__ == '__main__':
    # Must be full path or located in working directory
    if len(sys.argv)>1:
        cfg.load(sys.argv[1])
    else:
        cfg.load("config.json")

    print(cfg.get("L1A.L1A_2"))
    # test2

    # Key "db" doesn exist, use value "XX"
    print(cfg.get("db","XX",return_default=True))
    # XX

    # add more config
    cfg.load("config2.json")
    print(cfg.get("L1C"))
    # {'L1C_1': 'aaa', 'L1AC_2': '1'}

    print(cfg.get("L1B"))
    # {'L1B_1': 1, 'L1B_2': {'L2B': {'L2B_1': {'L3B_1': 1, 'L3B_2': 2}}}, 'L1B_3': 'asas'}
    cfg.load("config3.json")
    print(cfg.get("L1B"))
    # {'L1B_1': 1, 'L1B_2': {'L2B': {'L2B_1': {'L3B_3': 'NUEVO'}}}}

