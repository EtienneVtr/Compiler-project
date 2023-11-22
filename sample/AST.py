from token_pcl import Token

class Node:
    def __init__(self, type:str):
        self.children:list['Node'] = []
        self.type:str = type
    def add_child(self, child:'Node') -> 'Node':
        if not isinstance(child, Node):
            child = Node(child)
        self.children.append(child)
        return self.children[-1]
    def nbr_children(self) -> int:
        return len(self.children)
    def rm_child(self) -> 'Node':
        return self.children.pop()
    def to_str(self) -> str:
        rtn = f"{self.type}: {', '.join([child.type for child in self.children])}"
        for child in self.children:
            if child.nbr_children():
                rtn += "\n" + child.to_str()
        return rtn
    def __str__(self) -> str:
        return self.to_str()
    def __repr__(self) -> str:
        if self.nbr_children() == 0:
            return self.type
        return f"{self.type}({', '.join([child.__repr__() for child in self.children])})"
class AST:
    def __init__(self):
        self.root = Node("FICHIER")
        self.cur = self.root
    def __str__(self):
        return self.root.__str__()
    def append(self, type:str) -> Node:
        self.cur.add_child(Node(type))
        return self.cur



if __name__=="__main__":
    ast = AST()
    ast.root.add_child(Node("a").add_child(Node("b")).add_child(Node("c")))
    print(ast)