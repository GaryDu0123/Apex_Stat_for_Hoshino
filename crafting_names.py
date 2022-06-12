#!/usr/bin/env python
# -*-coding:utf-8 -*-

# 因为开发者没有提供所有物品的名字, 所以不明的暂时空着, 上了复制器在加, 最近可能还会再更新一些名字
crafting_config_dict = {
    # 武器
    "辅助手枪": [],
    "P2020": [],
    "RE-45": [],
    "VK-47平行步枪": [],
    "赫姆洛克步枪": [],
    "R-301卡宾枪": ["r301"],
    "哈沃克步枪": [],
    "转换者冲锋枪": [],
    "猎兽冲锋枪": [],
    "R-99冲锋枪": [],
    "电能冲锋枪": [],
    "C.A.R冲锋枪": [],
    "专注轻机枪": [],
    "喷火轻机枪": [],
    "L-star轻机枪": [],
    "暴走轻机枪": ["rampage"],
    "G7侦查枪": [],
    "30-30": [],
    "三重式狙击枪": [],
    "波塞克复合弓": [],
    "长弓狙击步枪": [],
    "充能步枪": [],
    "哨兵狙击步枪": [],
    "克雷贝尔狙击枪": [],
    "EVA-8": [],
    "獒犬霰弹枪": [],
    "莫桑比克": [],
    "和平捍卫者": [],

    # 弹药
    "子弹": ['ammo'],
    "轻型弹药": [],
    "重型弹药": [],
    "霰弹弹药": ["shotgun"],
    "狙击弹药": ["sniper"],
    "能量弹药": [],
    "弓箭": ['arrows'],

    # 投掷物
    "碎片手雷": [],
    "铝热剂手雷": [],
    "电弧星": [],

    # 瞄准镜
    "单倍幻影": [],
    "单倍全息衍射式瞄准镜“经典”": [],
    "单倍至2倍可调节式幻影瞄准镜": [],
    "2倍全息衍射式瞄准镜“格斗家”": ['optic_hcog_bruiser'],
    "6倍光学瞄准镜": [],
    "3倍全息衍射式瞄准镜“游侠”": ["optic_hcog_ranger"],
    "2倍至4倍可调节式高级光学瞄准镜": ['optic_variable_aog'],
    "4倍至8倍可调节式光学瞄准镜": ['optic_variable_sniper'],
    "单倍数字化威胁": ['optic_digital_threat'],
    "4倍至10倍数字化狙击威胁": [],

    # 消耗品
    "小型护盾电池": [],
    "护盾电池": ['large_shield_cell'],
    "注射器": [],
    "医疗箱": ['med_kit'],
    "凤凰治疗包": [],
    "移动重生信标": ["mobile_respawn_beacon"],
    "绝招加速剂": [],
    "隔热板": [],

    # 配件
    "枪管稳定器": ['barrel_stabilizer'],
    "标准枪托": ['standard_stock'],
    "狙击枪托": ['sniper_stock'],
    "霰弹枪枪栓": ['shotgun_bolt'],

    # 弹匣
    "加长式轻型弹匣": ['extended_light_mag'],
    "加长式重型弹匣": ['extended_heavy_mag'],
    "加长式狙击弹匣": ['extended_sniper_mag'],
    "加长式能量弹匣": ['extended_energy_mag'],

    # 即用配件
    "涡轮增压器": ['turbocharger'],
    "神射手速度节拍": [],
    "粉碎帽": ["shatter_caps"],
    "加速装填器": ['boosted_loader'],
    "动能供弹器": ['kinetic_loader'],
    "锤击点": ['hammerpoint_rounds'],
    "双发装填器": [],
    "干扰子弹": [],
    "双发扳机": [],
    "快捷枪套": [],
    "穿颅器": [],
    "铁砧接收器": [],
    "精准收束器": [],
    "射击模式选择器": [],
    "涂鸦改装": [],

    # 物品
    "背包": ['backpack'],
    "击倒护盾": ["knockdown_shield"],
    "防护罩": [],
    "进化护盾": ['evo_armor'],
    "头盔": ['helmet']
}

rarity_dict = {
    'Legendary': "传说",
    'Epic': "史诗",
    'Rare': "稀有",
    'Common': "普通",
}

crafting_dict = {}
for i, j in crafting_config_dict.items():
    for name in j:
        crafting_dict[name] = i
