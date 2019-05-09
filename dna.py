from collections import namedtuple

"""
This program is an implementation of a solution to the following
ACM ICPC proglem https://mausa17.kattis.com/problems/longlongstrings
"""
Insert = namedtuple('I', ['i', 'v'])
Delete = namedtuple('D', ['i'])

"""
Converts the program to its canonical form by ordering
the program into increasing inserts followed by decreasing deletes
and then removing NOP insert/delete pairs
"""
def canonize(prog):
    order(prog)
    return minimize(prog)

"""
Order performs a pseudo bubble sort of the program
while preserving statement semantics
"""
def order(prog):
    need_update = True

    while need_update:
        need_update = False

        for i1 in range(len(prog) - 1):
            i2 = i1 + 1

            if update(prog, i1, i2):
                need_update = True

"""
Transforms
    D(1), I(1,'a') -> I(1,'a'), D(2)
    D(1), I(2,'a') -> I(3,'a'), D(1)
    D(2), I(1,'a') -> I(1,'a'), D(3)

    I(1,'a'), I(1, 'b') -> I(1,'b'), I(2,'a')
    D(1), D(2) -> D(3), D(1)
"""
def update(prog, i1, i2):
    left = prog[i1]
    right = prog[i2]

    if type(left) == Insert:
        if type(right) == Insert:
            if right.i <= left.i:
                prog[i1] = right
                prog[i2] = Insert(left.i + 1, left.v)
                return True
            else:
                return False
        else:
            return False
    else:
        if type(right) == Insert:
            if left.i <= right.i:
                prog[i1] = Insert(right.i + 1, right.v)
                prog[i2] = left
            else:
                prog[i1] = right
                prog[i2] = Delete(left.i + 1)
            return True
        else:
            if left.i <= right.i:
                prog[i1] = Delete(right.i + 1)
                prog[i2] = left
                return True
            else:
                return False

"""
Removes redundant insert/delete pairs

I(1,'a')
I(2,'b')
D(1)

I(1,'b')
"""
def minimize(prog):
    for i in range(len(prog)):
        if type(prog[i]) == Delete:
            first_del = i
            break
    else:
        return

    left = 0
    right = len(prog) - 1

    while left < first_del and right >= first_del:
        if prog[left].i == prog[right].i:
            slicer(prog, left, right)
            left += 1
            right -= 1
        elif prog[left].i < prog[right].i:
            left += 1
        else:
            right -= 1

    return [stmt for stmt in prog if stmt is not None]


def slicer(prog, insert, delete):
    prog[insert] = None
    prog[delete] = None

    for i in range(insert+1, delete):
        prog[i] = decrement(prog[i])

def decrement(stmt):
    if stmt == None:
        return None

    if type(stmt) == Insert:
        return Insert(stmt.i - 1, stmt.v)
    else:
        return Delete(stmt.i - 1)
    

p0 = [
    Delete(i=1),
    Delete(i=2)
]

p1 = [
    Delete(i=1),
    Delete(i=2)
]

print("Original")
print(p0)
print(p1)
print()

p0_can = canonize(p0)
p1_can = canonize(p1)

print()

print("Canonized")
print(p0_can)
print(p1_can)

print("Equivalent")
print(p0_can == p1_can)