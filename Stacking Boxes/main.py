# problem: given a list of boxes (length, width, height), and that one box can be stacked on top of
# another iff it's length and width are BOTH smaller, return the tallest possible stack.

'''
Prereqs
-=-=-=-=-=-=-=-=-=
- structure -> List[tuple(int,int,int)]
- reasonable number of boxes, runtime won't be an issue
- NOT allowed to rotate boxes
- correctness, then runtime

Initial Thoughts
-=-=-=-=-=-=-=-=-=
'''


def tallest_stack(boxes):
