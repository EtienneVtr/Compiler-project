import re
class Node:
    next_id = 0 

    def __init__(self, value, children=None):
        self.id = Node.next_id
        Node.next_id += 1
        self.value = value
        self.children = children if children is not None else []
    def __repr__(self):
        return f"Node(value={self.value}, children={self.children})"

# operator precedence
precedence = {
    'or': (1, 'left'),
    'and': (2, 'left'),
    'not': (3, 'none'),
    '=': (4, 'none'),
    '/=': (4, 'none'),
    '>': (4, 'none'),
    '>=': (4, 'none'),
    '<': (4, 'none'),
    '<=': (4, 'none'),
    '+': (5, 'left'),
    '-': (5, 'left'),
    '*': (6, 'left'),
    '/': (6, 'left'),
    'rem': (6, 'left'),
    '- (unary)': (6, 'none'), 
    '.': (7, 'left')
}

# reorganize the AST
def rearrange_ast(node):
    if not node.children or node.value not in precedence:
        return node

    # for the minus unary operator
    if len(node.children) == 1:
        node.children[0] = rearrange_ast(node.children[0])
        return node

    # for the other operators
    left = rearrange_ast(node.children[0])
    right = rearrange_ast(node.children[1])

    # verify if the current operator has a lower precedence than the children
    current_precedence = precedence[node.value][0]
    left_precedence = precedence[left.value][0] if left.value in precedence else -1
    right_precedence = precedence[right.value][0] if right.value in precedence else -1

    # if the current operator has a lower precedence than the left child
    if precedence[node.value][1] == 'left' and current_precedence < left_precedence:
        new_node = Node(left.value, [node, left.children[1]])
        node.children = [left.children[0], right]
        return rearrange_ast(new_node)

    # if the current operator has a lower precedence than the right child
    if precedence[node.value][1] == 'right' and current_precedence < right_precedence:
        new_node = Node(right.value, [left, right.children[0]])
        node.children = [new_node, right.children[1]]
        return rearrange_ast(new_node)

    return node



def parse_graph_line(line):
    """ 
    Parse a line from the graph file and return the parent and child node names.
    """
    match = re.match(r"\t(.+):(\d+) --> (.+):(\d+);", line)
    if match:
        return match.groups()
    return None

def build_ast_from_graph(lines):
    """
    build an AST from the graph file lines and return the root node.
    """
    nodes = {}
    for line in lines:
        parsed_line = parse_graph_line(line)
        if parsed_line:
            parent_name, parent_id, child_name, child_id = parsed_line
            parent_id, child_id = int(parent_id), int(child_id)

            # create parent node if it doesn't exist
            if parent_id not in nodes:
                nodes[parent_id] = Node(parent_name)
            parent_node = nodes[parent_id]

            # create child node if it doesn't exist
            if child_id not in nodes:
                nodes[child_id] = Node(child_name)
            child_node = nodes[child_id]

            # add child node to parent node
            parent_node.children.append(child_node)
    # return the root node
    return nodes[0]

def print_ast_mermaid(node, output=[], prefix=""):
    """
    Mermaid generator for AST.
    """
    if prefix:
        output.append(f"\t{prefix} --> {node.value}:{node.id}")
    else:
        output.append(f"\t{node.value}:{node.id}")

    for i, child in enumerate(node.children):
        child_prefix = f"{node.value}:{node.id}"
        print_ast_mermaid(child, output, child_prefix)

    return output


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python operator.py [path_to_graph_file.txt]")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, 'r') as file:
        lines = file.readlines()

    ast = build_ast_from_graph(lines)
    rearranged_ast = rearrange_ast(ast)

    print("AST Graph in Mermaid format:")
    mermaid_graph = print_ast_mermaid(ast)
    print("graph TD;")
    for line in mermaid_graph:
        print(line)