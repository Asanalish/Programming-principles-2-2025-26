import json

# 1. Открываем и читаем JSON-файл
with open(r"/Users/asanali/Desktop/PythonLearning/pp2/python/Practice4/sample-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. В JSON есть ключ "imdata" — это список
imdata = data["imdata"]

# 3. Печатаем заголовок
print("Interface Status")
print("=" * 90)

print(f"{'DN':<55} {'Descrition':<20} {'Speed':<8} {'MTU':<6}")

# 4. Перебираем каждый интерфейс
for item in imdata:
    attrs = item["l1PhysIf"]["attributes"]

    dn = attrs["dn"]
    descr = attrs["descr"]
    speed = attrs["speed"]
    mtu = attrs["mtu"]

# 5. Печатаем строку таблицы
    print(f"{dn:<55} {descr:<20} {speed:<8} {mtu:<6}")
