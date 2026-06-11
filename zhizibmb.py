import folium
import webbrowser
import os

# ==================== 1. 创建基础地图 ====================
m = folium.Map(location=[21.0,30 ], zoom_start=6,
               tiles='OpenStreetMap', control_scale=True)

# ==================== 2. 现代中国版图描边 ====================
china_geojson_url = "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json"
folium.GeoJson(
    china_geojson_url,
    name='中国版图描边',
    style_function=lambda x: {
        'color': '#3186cc', 'weight': 3, 'fillColor': 'none', 'dashArray': '5,5'
    },
    tooltip='中国 (约960万平方公里，含台湾)'
).add_to(m)

# ==================== 3. 领土数据定义（只保留视频） ====================
territories = [
    {
        'name': '外东北地区',
        'area': '约100万平方公里',
        'color': 'red',
        'category': '清朝割让',
        'treaty': '1858年《瑷珲条约》、1860年《北京条约》',
        'now': '俄罗斯',
        'coordinates': [
            [55.0, 120.0], [55.0, 135.0], [48.0, 140.0],
            [45.0, 135.0], [48.0, 130.0], [50.0, 125.0], [53.0, 120.0]
        ],
        'video': 'BV1Db411y7W2'   # ⚠️ 请替换为有效BV号
    },
    {
        'name': '帕米尔地区',
        'area': '约45万平方公里',
        'color': 'red',
        'category': '清朝割让',
        'treaty': '1864年《中俄勘分西北界约记》',
        'now': '塔吉克斯坦、吉尔吉斯斯坦',
        'coordinates': [
            [43.0, 78.0], [45.0, 80.0], [42.0, 82.0],
            [39.0, 75.0], [41.0, 73.0]
        ],
        'video': 'BV1Ff4y1D7XE'   # ⚠️ 请替换为有效BV号
    },
    {
        'name': '外蒙古',
        'area': '约156万平方公里',
        'color': 'orange',
        'category': '民国脱离',
        'treaty': '1946年中华民国政府承认独立',
        'now': '蒙古国',
        'coordinates': [
            [50.0, 87.0], [52.0, 100.0], [50.0, 110.0],
            [48.0, 115.0], [45.0, 115.0], [42.0, 105.0],
            [43.0, 95.0], [46.0, 88.0]
        ],
        'video': 'BV1Mt411H7iC'   # ⚠️ 请替换为有效BV号
    },
    {
        'name': '唐努乌梁海',
        'area': '约17万平方公里',
        'color': 'orange',
        'category': '民国脱离',
        'treaty': '1944年加入苏联',
        'now': '俄罗斯联邦图瓦共和国',
        'coordinates': [
            [53.0, 88.0], [53.0, 98.0], [50.0, 98.0], [50.0, 88.0]
        ],
        'video': 'BV1zW411u7zA'   # ⚠️ 请替换为有效BV号
    },
    {
        'name': '江心坡、南坎地区',
        'area': '约3万平方公里',
        'color': 'orange',
        'category': '历史脱离',
        'treaty': '原属清朝云南省',
        'now': '缅甸',
        'coordinates': [
            [27.5, 97.0], [27.5, 98.5], [25.0, 98.5],
            [24.0, 97.5], [25.5, 96.5]
        ],
        'video': 'BV1sW411v7sp'   # ⚠️ 请替换为有效BV号
    }
]

# ==================== 4. 循环添加失去领土（带B站视频） ====================
for t in territories:
    popup_html = f"""
    <div style="width:380px; padding:5px;">
        <h4 style="margin-top:0;">{t['name']}</h4>
        <p><b>面积:</b>{t['area']}<br>
        <b>性质:</b>{t['category']}<br>
        <b>条约/脱离:</b>{t['treaty']}<br>
        <b>现属:</b>{t['now']}</p>
    """

    if t.get('video'):
        # 使用完整的 HTTPS 链接，确保在 file:// 协议下也能加载
        bilibili_url = f"https://player.bilibili.com/player.html?bvid={t['video']}&page=1&danmaku=0&high_quality=1&autoplay=0"
        popup_html += f'''
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-top:10px;">
            <iframe src="{bilibili_url}" 
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
                    frameborder="no" scrolling="no" allowfullscreen="true">
            </iframe>
        </div>
        <p style="font-size:12px; color:gray;">如果视频无法播放，可能是BV号无效或网络问题，请检查BV号。</p>
        '''
    else:
        popup_html += "<p>暂无相关视频</p>"

    popup_html += "</div>"

    folium.Polygon(
        locations=t['coordinates'],
        color=t['color'],
        fill=True,
        fill_color=t['color'],
        fill_opacity=0.3,
        weight=2,
        popup=folium.Popup(popup_html, max_width=400),
        tooltip=t['name']
    ).add_to(m)

# ==================== 5. 图例说明 ====================
legend_html = '''
<div style="position: fixed; bottom: 50px; left: 50px; width: 280px;
background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
padding: 10px; border-radius: 5px; opacity: 0.9;">
    <b>历史领土变迁图例</b><hr style="margin:5px 0;">
    <p><span style="background-color: #3186cc; width: 20px; height: 3px; display: inline-block; border:2px dashed #3186cc;"></span> 现代中国版图（描边）</p>
    <p><span style="background-color: red; width: 20px; height: 10px; display: inline-block;"></span> 清朝条约割让领土</p>
    <p><span style="background-color: orange; width: 20px; height: 10px; display: inline-block;"></span> 民国时期脱离领土</p>
    <hr style="margin:5px 0;">
    <p><b>总面积统计:</b><br>
    - 清朝割让:约145万平方公里<br>
    - 民国脱离:约176万平方公里<br>
    - 合计:约321万平方公里<br>
    <small>（与1316万-960万=356万接近）</small>
    </p>
    <p><b>📺 点击领土可观看相关B站视频</b></p>
    <p><small>视频默认关闭弹幕、最高清晰度。如果无法播放，请检查BV号。</small></p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# ==================== 6. 标题 ====================
title_html = '''
<div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
background-color: white; border:2px solid grey; z-index:9999; font-size:16px;
padding: 8px 20px; border-radius: 5px; opacity: 0.9; font-weight: bold;">
    清朝/民国时期失去的主要领土（点击可观看B站视频）
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# ==================== 7. 图层控制 ====================
folium.LayerControl(collapsed=False).add_to(m)

# ==================== 8. 保存并打开 ====================
output_file = 'china_historical_territories_video_only.html'
m.save(output_file)
webbrowser.open('file://' + os.path.realpath(output_file))

print(f"🎉 地图已生成:{output_file}")
print("📌 使用说明:")
print("  1. 双击该HTML文件即可在浏览器中打开")
print("  2. 点击红色/橙色区域可观看B站视频")
print("  3. 如果视频无法播放，请检查 territories 列表中的 BV 号是否正确")
print("  4. 视频默认关闭弹幕、最高清晰度")