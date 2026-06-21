from data_structures import LinkedList

def get_middle(head):
    if head is None:
        return head
    slow = head
    fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow

def sorted_merge(a, b, compare_func):
    if a is None:
        return b
    if b is None:
        return a

    if compare_func(a.data, b.data):
        head = a
        a = a.next
    else:
        head = b
        b = b.next

    current = head

    while a is not None and b is not None:
        if compare_func(a.data, b.data):
            current.next = a
            a = a.next
        else:
            current.next = b
            b = b.next
        current = current.next

    if a is not None:
        current.next = a
    else:
        current.next = b

    return head

def merge_sort_nodes(head, compare_func):
    if head is None or head.next is None:
        return head

    middle = get_middle(head)
    next_of_middle = middle.next
    middle.next = None

    left = merge_sort_nodes(head, compare_func)
    right = merge_sort_nodes(next_of_middle, compare_func)

    return sorted_merge(left, right, compare_func)

def merge_sort(linked_list, compare_func):
    """
    Sorts a LinkedList in place.
    compare_func(a, b) should return True if a comes before b in sorted order.
    """
    if linked_list.head is None or linked_list.head.next is None:
        return
    linked_list.head = merge_sort_nodes(linked_list.head, compare_func)
