from folder1.kis_rank import get_top_volume_stocks

stocks = get_top_volume_stocks()

print("최종 종목 수:", len(stocks))

for code, name in stocks.items():
    print(code, name)