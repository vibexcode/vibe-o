# main.py
"""
VIBE-O: Dinamik Ontolojik Matris
İlk çalışma simülasyonu
"""

from src.ontology import EntityRow
from src.matrix import VibeOMatrix

# 1. Matrise bağlan
matrix = VibeOMatrix(width=500.0)

# 2. Entity'leri tanımla
bee = EntityRow("1.0.0.15", "Bee", namespace="universal")
bee.add_function("fly")
bee.add_function("produce_honey")
bee.add_position(x=120, context="aerial_bio", weight=0.95)

drone = EntityRow("1.1.0.5", "Drone", namespace="universal")
drone.add_function("fly")
drone.add_function("record_video")
drone.add_position(x=300, context="aerial_mech", weight=0.92)

penguin = EntityRow("1.0.0.27", "Penguin", namespace="universal")
penguin.add_function("swim")
penguin.add_function("walk")
penguin.add_position(x=400, context="aquatic", weight=0.98)

# 3. Matrise ekle
matrix.add_entity(bee)
matrix.add_entity(drone)
matrix.add_entity(penguin)

# 4. Başlangıç pozisyonlarını yazdır
print("🚀 Başlangıç pozisyonları:")
for e in [bee, drone, penguin]:
    avg_x = sum(p["x"] for p in e.positions) / len(e.positions)
    print(f"  {e.name}: X ≈ {avg_x:.1f}")

# 5. Dinamik güncelleme → hizalama
print("\n🔄 Hizalama işlemi başlıyor...")
matrix.update_positions(iterations=100)

# 6. Son pozisyonları yazdır
print("\n🎯 Sonuç: Hizalanmış pozisyonlar")
for e in [bee, drone, penguin]:
    avg_x = sum(p["x"] for p in e.positions) / len(e.positions)
    print(f"  {e.name}: X ≈ {avg_x:.1f}")

# 7. Kontrol: Arı ve Drone yakın mı oldu?
bee_x = sum(p["x"] for p in bee.positions) / len(bee.positions)
drone_x = sum(p["x"] for p in drone.positions) / len(drone.positions)

distance = abs(bee_x - drone_x)
print(f"\n🐝 Arı ↔ 🛰️ Drone mesafesi: {distance:.1f} birim")
if distance < 50:
    print("✅ Uçuş işlevi nedeniyle birbirine yaklaştılar!")
else:
    print("⚠️  Yeterince yaklaşmadılar → parametreleri kontrol et.")
