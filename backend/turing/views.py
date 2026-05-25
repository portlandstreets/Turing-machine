from rest_framework.decorators import api_view
from rest_framework.response import Response

def parse_rules(raw_code):
    transitions = {}
    for line in raw_code.splitlines():
        clean_line = line.strip()
        if not clean_line or clean_line.startswith(";"):
            continue
        parts = clean_line.split()
        if len(parts) == 5:
            # key: (state, current_symbol) -> value: (new_sym, direction, new_state)
            transitions[(parts[0], parts[1])] = (parts[2], parts[3].upper(), parts[4])
    return transitions

@api_view(['POST'])

    data = request.data
    tape_dict = data.get('tape', {}) 
    head = int(data.get('head', 0))
    state = str(data.get('state', '0'))
    blank = str(data.get('blank', '_'))
    code = str(data.get('code', ''))

    transitions = parse_rules(code)

    if state == "HALT":
        return Response({"tape": tape_dict, "head": head, "state": state, "halted": True})


    current_symbol = tape_dict.get(str(head), blank)
    key = (state, current_symbol)


    if key not in transitions:
        return Response({"tape": tape_dict, "head": head, "state": "HALT", "halted": True})

    new_sym, direction, new_state = transitions[key]
    

    tape_dict[str(head)] = new_sym

    state = new_state

    if direction == "R":
        head += 1
    elif direction == "L":
        head -= 1

    return Response({
        "tape": tape_dict,
        "head": head,
        "state": state,
        "halted": False
    })