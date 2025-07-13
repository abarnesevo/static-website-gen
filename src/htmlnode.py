class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props != None:
            keys = self.props.keys()
            values = self.props.values()
            parsed_props = ""
            for i in range(len(keys)):
                parsed_props = parsed_props + f' {keys[i]}="{values[i]}"'
            return parsed_props

    def __repr__(self):
        return f"HTMLNode: {self.tag}, {self.value}, {str(self.children)}, {str(self.props)}"

    def __eq__(self,node):
        return self.tag == node.tag and self.value == node.value and self.children == node.children and self.props == node.props

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super(LeafNode, self).__init__()
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if not self.value:
            raise ValueError
        
        elif not self.tag:
            return self.value

        else:
            prop = ""
            if self.props:
                key = list(self.props.keys())
                val = list(self.props.values())
                prop = f' {key[0]}="{val[0]}"'
            return f"<{self.tag}{prop}>{self.value}</{self.tag}>" 

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super(ParentNode, self).__init__()
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError("tags required for parent node")
        elif not self.children:
            raise ValueError("children required of parent node")
        else:
            children = ""
            for i in self.children:
                children = children + i.to_html()
            prop = ""
            if self.props:
                key = list(self.props.keys())
                val = list(self.props.values())
                prop = f' {key[0]}="{val[0]}"'
            return f"<{self.tag}{prop}>{children}</{self.tag}>" 


