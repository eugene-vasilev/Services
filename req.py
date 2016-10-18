def request_conversion(command):
    separated = command.split(',',-1)
    lang=separated[-1]
    code_last_index = len(command)-len(separated[-1])-1
    code = command[0:code_last_index]

    data=(code,lang)
    return data
