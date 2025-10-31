# src/ontology.py
class EntityRow:
    """
    VIBE-O'nun temel yapı taşı: Ontolojik kimlik + çoklu bağlam pozisyonu
    """
    def __init__(self, binary_id: str, name: str, namespace: str = "universal"):
        self.binary_id = binary_id          # 1.0.0.27
        self.name = name                    # "Penguin"
        self.namespace = namespace          # "universal", "brand", vs
        self.level = binary_id.count(".")   # Hiyerarşik derinlik
        self.functions = []                 # ["swims", "feathers"]
        self.positions = []                 # [{"x": 180, "context": "aquatic"}]
        self.parent_hint = ".".join(binary_id.split(".")[:-1])  # 1.0.0

    def add_function(self, func: str):
        if func not in self.functions:
            self.functions.append(func)

    def add_position(self, x: float, context: str, weight: float = 1.0):
        self.positions.append({
            "x": x,
            "context": context,
            "weight": weight
        })

    def __repr__(self):
        return f"Entity[{self.namespace}]({self.binary_id}, '{self.name}', pos={len(self.positions)})"
