import re
import json

# 1) читаем файл
with open("/Users/asanali/Desktop/PythonLearning/pp2/python/Practice5/raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

lines = [line.strip() for line in text.splitlines() if line.strip()]


# 2) регулярки (шаблоны)


# Цена: "154,00" или "1 200,00" или "7 330,00"
price_re = re.compile(r"\d{1,3}(?: \d{3})*,\d{2}")

# Товар начинается с "1." "2." и т.д.
item_start_re = re.compile(r"^(\d+)\.$")

# Дата/время: "Время: 18.04.2019 11:13:58"
dt_re = re.compile(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})")

# ИТОГО:
total_re = re.compile(r"^ИТОГО:\s*$")

# Оплата:
pay_re = re.compile(r"^Банковская карта:\s*$")

# Строка вида "2,000 x 154,00"
qty_price_re = re.compile(r"^(\d+,\d+)\s*x\s*(\d{1,3}(?: \d{3})*,\d{2})$")


# 3) сбор товаров и их сумм


items = []
all_prices = []

i = 0
while i < len(lines):
    line = lines[i]

    # собрать вообще все цены из текста (просто как список)
    for p in price_re.findall(line):
        all_prices.append(p)

    # если нашли начало товара: "12."
    m = item_start_re.match(line)
    if m:
        # следующая строка — название
        if i + 1 < len(lines):
            name = lines[i + 1]
        else:
            name = ""

        qty = None
        unit_price = None
        item_sum = None

        # дальше обычно есть строка "1,000 x 841,00"
        if i + 2 < len(lines):
            m2 = qty_price_re.match(lines[i + 2])
            if m2:
                qty = m2.group(1)         # строкой
                unit_price = m2.group(2)  # строкой

        # потом обычно следующая строка — сумма по позиции
        # например после "2,000 x 154,00" идёт "308,00"
        if i + 3 < len(lines) and price_re.fullmatch(lines[i + 3]):
            item_sum = lines[i + 3]

        items.append({
            "name": name,
            "qty": qty,
            "unit_price": unit_price,
            "sum": item_sum
        })

    i += 1


# 4) ИТОГО

total_amount = None
for idx, line in enumerate(lines):
    if total_re.match(line):
        if idx + 1 < len(lines) and price_re.fullmatch(lines[idx + 1]):
            total_amount = lines[idx + 1]
            break


# 5) Способ оплаты и сумма оплаты

payment_method = None
paid_amount = None
for idx, line in enumerate(lines):
    if pay_re.match(line):
        payment_method = "Банковская карта"
        if idx + 1 < len(lines) and price_re.fullmatch(lines[idx + 1]):
            paid_amount = lines[idx + 1]
        break


# 6) Дата/время

date = None
time = None
m = dt_re.search(text)
if m:
    date = m.group(1)
    time = m.group(2)


# 7) Посчитать сумму по товарам (если есть sum у каждой позиции)
#    Переводим "7 330,00" -> 7330.00

def to_float_kz(s):
    # убрать пробелы тысяч: "7 330,00" -> "7330,00"
    s = s.replace(" ", "")
    # заменить запятую на точку
    s = s.replace(",", ".")
    return float(s)

items_total_calc = 0.0
count_sums = 0
for it in items:
    if it["sum"]:
        items_total_calc += to_float_kz(it["sum"])
        count_sums += 1


# 8) JSON-вывод

result = {
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "paid_amount": paid_amount,
    "total_amount_from_receipt": total_amount,
    "items_total_calculated": round(items_total_calc, 2),
    "items_count_with_sum": count_sums,
    "items": items,
    "all_prices_found": all_prices
}

print(json.dumps(result, ensure_ascii=False, indent=2))