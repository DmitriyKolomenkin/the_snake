def solution (node, idx):
# Напишите код функции здесь.
    count = 0
    curr = node
    prev = None
    found = False
    while not found:
        if count == idx:
            found = True
        else:
            prev = curr
            curr = curr next_item
        count += 1
    if prev is None:
        node = curr.next_item
    else:
        prev.next_item = curr.next_item
    return node