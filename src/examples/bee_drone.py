# examples/bee_drone.py
"""
VIBE-O Demo: Bee ve Drone'nun anlamsal hizalanması
Bu örnek, iki farklı ontolojik kökene sahip (biyolojik vs mekanik)
varlığın, ortak işlevler üzerinden aynı semantik alanda hizalanmasını gösterir.
"""

from src.ontology import EntityRow

# 1. Evrensel varlıklar: Arı (biyolojik)
bee = EntityRow("1.0.0.15", "Bee", namespace="universal")
bee.add_function("fly")
bee.add_function("produce_honey")
bee.add_function("pollinate")
bee.add_position(x=120, context="aerial_bio", weight=0.95)

# 2. Evrensel varlık: Drone (teknolojik)
drone = EntityRow("1.1.0.5", "Drone", namespace="universal")
drone.add_function("fly")
drone.add_function("record_video")
drone.add_function("autonomous_navigation")
drone.add_position(x=125, context="aerial_mech", weight=0.92)

# 3. Karşılaştırma
print("🐝 Arı:", bee)
print("🛸 Drone:", drone)
print()

# Anlamsal yakınlık kontrolü
distance = abs(bee.positions[0]["x"] - drone.positions[0]["x"])
print(f"Anlamsal mesafe: {distance:.1f} birim")
if distance < 10:
    print("✅ Çok yakın! → 'Uçuş' bağlamında hizalanmışlar.")
    print("💡 Açıklanabilirlik: LLM, 'Arı ile Drone benzer çünkü ikisi de uçar' demeli.")
