class StoryNode:
    def __init__(self, name: str):
        self.name = name
        self.children: list[StoryNode] = []

def start_story(node: StoryNode):
    choice = input(f'''
    choose an action
    ----------------
    1) {node.children[0].name}
    2) {node.children[1].name}
    3) {node.children[2].name}
    ''')
    start_story(node.children[int(choice)-1])

if __name__ == "__main__":
    story = StoryNode("Story")
    story.children = [
        StoryNode("A"),
        StoryNode("B"),
        StoryNode("C")]
    start_story(story)








