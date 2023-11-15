from token import Token

class Node:
    def __init__(self, type:str):
        self.children:list['Node'] = []
        self.type:str = type
    def add_child(self, child:'Node') -> 'Node':
        self.children.append(child)
        return self
    def nbr_children(self) -> int:
        return len(self.children)
    def rm_children(self) -> 'Node':
        return self.children.pop()
    def __str__(self) -> str:
        if self.nbr_children() == 0:
            return self.type
        else:
            return f"{self.type}({', '.join([child.__str__() for child in self.children])})"
class AST:
    def __init__(self):
        self.root = Node("FICHIER")
    def __str__(self):
        return self.root.__str__()


if __name__=="__main__":
    ast = AST()
    ast.root.add_child(Node("a").add_child(Node("b")).add_child(Node("c")))
    print(ast.root)