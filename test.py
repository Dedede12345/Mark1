
typed = ['sdfsadf', 'adfdsafcv']
import json
# while len(typed) == 0 or typed[-2:] != ['\n'] * 2:
#
#     try:
#         typed.append(line:=input(f"{'Enter text: ' * (len(typed) == 0)}") + '\n')
#
#     except EOFError:
#         break

while True:

    try:
        line = input("Do you want to save those links? [y/n]")
        if line == 'y':
            with open('datafile.json', 'w') as file:
                json.dump(typed, file)
                break
        if line == 'n':
            # print('adsfasdfasdfasdfafdsf')
            break
        else:
            print('asdfasdfasdf')
            continue

    except EOFError:
        break

# with open('datafile.json', 'r'):
#     json.load()

