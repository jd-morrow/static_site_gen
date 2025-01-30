# 
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This method has not been implemented.")

    def props_to_html(self):
        if self.props == None:
            return ""
        prop_string = ""
        for prop in self.props:
            prop_string = prop_string + " " + prop + "=\"" + self.props[prop] + "\""
        return prop_string


    def __repr__(self):
         return f"HTMLNode(\"{self.tag}\", \"{self.value}\", {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        if value is None:
            raise ValueError("LeafNode must have a value")

    def to_html(self):
        if self.tag is None:
            return self.value
        elif self.props is not None:
            html_props = self.props_to_html()
            return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if children is None:
            raise ValueError("ParentNode must have at least one child node")
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        
    def to_html(self):
        html_children = ""
        for child in self.children:
            html_children = html_children + child.to_html()
        return f"<{self.tag}>{html_children}</{self.tag}>"