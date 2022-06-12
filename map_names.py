map_name_dict_config = {
    "br": {
        "Olympus": "奥林匹斯",
        "World's Edge": "世界尽头",
        "Storm Point": "风暴点",
        "Kings Canyon": "诸王峡谷"
    },
    "arena": {
        "Phase Runner": "相位穿梭器",
        "Party Crasher": "派对破坏者",
        "Overflow": "溢出",
        "Encore": "再来一次",
        "Habitat 4": "栖息地4",
        "Habitat": "栖息地4",
        "Drop-Off": "原料厂"
    }
}

# 全部转为小写方便比较
map_name_dict = {}
for mode in map_name_dict_config:
    map_name_dict[mode] = {}
    for i, j in map_name_dict_config[mode].items():
        map_name_dict[mode][i.lower()] = j
