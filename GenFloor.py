import json

def create_floor_plan():
    floor_plan = []
    current_floor = 0
    current_height = int(input("請輸入初始樓層高度："))
    initial_height = current_height

    while True:
        floor_input = input("請輸入樓層類型和高度差（例如：F0-4, 600），或輸入 'ok' 完成：")
        if floor_input.lower() == 'ok':
            break

        floor_type, height_diff = floor_input.split(', ')
        height_diff = int(height_diff)

        start_floor, end_floor = floor_type[1:].split('-') if '-' in floor_type else (floor_type[1:], floor_type[1:])
        start_floor, end_floor = int(start_floor), int(end_floor)

        for floor in range(start_floor, end_floor + 1):
            floor_plan.append({
                "Floor": current_floor,
                "Height": current_height,
                "FloorType": floor_type
            })
            current_floor += 1
            if floor < end_floor:
                current_height += height_diff
            else:
                current_height = initial_height + (current_floor * height_diff)

    return floor_plan

def save_json(data, filename):
    with open(f"{filename}.json", 'w', encoding='utf-8') as f:
        json.dump({"FloorPlan": data}, f, ensure_ascii=False, indent=2)

def main():
    floor_plan = create_floor_plan()
    filename = input("請輸入 JSON 檔案名稱（不需要加副檔名）：")
    save_json(floor_plan, filename)
    print(f"JSON 檔案 '{filename}.json' 已成功創建。")

if __name__ == "__main__":
    main()