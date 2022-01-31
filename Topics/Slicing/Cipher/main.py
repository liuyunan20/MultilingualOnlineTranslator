string = "no clouds here to spy on pets"
string_list = list(string)
decode_str = "".join(string_list[0::5])
print(decode_str[::-1])
