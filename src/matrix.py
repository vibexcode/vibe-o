# src/matrix.py
"""
VIBE-O Dinamik Ontoloji Matrisi
- Anlamsal X ekseni hizalaması
- Çoklu pozisyon yönetimi
- Kuvvet tabanlı (force-based) dinamik
"""

import math
from typing import List, Dict, Any
from .ontology import EntityRow

class VibeOMatrix:
    def __init__(self, width: float = 1000.0):
        self.width = width  # X ekseni sınırsız ama başlangıç aralığı
        self.entities: Dict[str, EntityRow] = {}
        self.gravity_factor = 0.01
        self.repulsion_factor = 0.5

    def add_entity(self, entity: EntityRow):
        """Entity’i matrise ekle"""
        self.entities[entity.binary_id] = entity

    def semantic_distance(self, a: EntityRow, b: EntityRow) -> float:
        """İki entity arasındaki anlamsal uzaklık"""
        # Fonksiyon benzerliği
        if not a.functions or not b.functions:
            return 1.0
        
        set_a = set(a.functions)
        set_b = set(b.functions)
        intersection = set_a & set_b
        union = set_a | set_b
        jaccard = len(intersection) / len(union) if union else 0
        return 1.0 - jaccard

    def update_positions(self, iterations: int = 50):
        """
        Tüm entity’lerin X pozisyonlarını anlamsal çekim/itme kuvvetlerine göre güncelle
        """
        for _ in range(iterations):
            forces = {eid: 0.0 for eid in self.entities}

            for id_a, entity_a in self.entities.items():
                for id_b, entity_b in self.entities.items():
                    if id_a == id_b:
                        continue

                    dist = self.semantic_distance(entity_a, entity_b)
                    if dist < 0.8:  # Anlamsal olarak yakınlarsa çek
                        for pos_a in entity_a.positions:
                            for pos_b in entity_b.positions:
                                dx = pos_b["x"] - pos_a["x"]
                                force = self.gravity_factor * (1.0 - dist)
                                forces[id_a] += force * dx

                    # Itme kuvveti (çok yakınsa birbirini it)
                    avg_x_a = sum(p["x"] for p in entity_a.positions) / len(entity_a.positions)
                    avg_x_b = sum(p["x"] for p in entity_b.positions) / len(entity_b.positions)
                    if abs(avg_x_a - avg_x_b) < 5:
                        forces[id_a] -= self.repulsion_factor

            # Pozisyonları güncelle
            for eid, force in forces.items():
                entity = self.entities[eid]
                for pos in entity.positions:
                    pos["x"] += force
                    # Sınır kontrolü
                    pos["x"] = max(0, min(self.width, pos["x"]))

    def get_aligned_entities(self, x: float, radius: float = 50.0) -> List[EntityRow]:
        """X pozisyonuna yakın hizalanan entity’leri getir"""
        aligned = []
        for entity in self.entities.values():
            for pos in entity.positions:
                if abs(pos["x"] - x) <= radius:
                    aligned.append(entity)
                    break
        return aligned
