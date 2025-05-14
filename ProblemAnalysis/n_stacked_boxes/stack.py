class Stack: 
    def __init__(self, boxes):
        self.boxes = boxes
    
    def is_splittable(self):
        return self.boxes != 1
