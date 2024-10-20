def log_info(input):
    if type(input) == list:
        for something in input:
            print(something)
    else:
        print(input)


def log_newline():
    print("------------------------------------------------------------------------------------------------------------------------------")