import streamlit as st
import pandas as pd
import os

# Настройка страницы
st.set_page_config(
    page_title="Иркутская область 3D | CesiumJS", 
    page_icon="🏔️",
    layout="wide"
)

# Координаты центров
REGION_CENTER = {
    "Иркутская область": [56.4977, 104.1794, 1000000],
    "Иркутск": [52.2864, 104.2807, 50000],
    "Братск": [56.1514, 101.6342, 50000],
    "Байкал": [53.5, 107.5, 200000]
}

# Основные города и населенные пункты
settlements = [
    {"name": "Иркутск", "coords": [52.2864, 104.2807], "type": "город", "population": 617000},
    {"name": "Братск", "coords": [56.1514, 101.6342], "type": "город", "population": 224000},
    {"name": "Ангарск", "coords": [52.5362, 103.8865], "type": "город", "population": 222000},
    {"name": "Усть-Илимск", "coords": [58.0006, 102.6619], "type": "город", "population": 80000},
    {"name": "Усолье-Сибирское", "coords": [52.7561, 103.6386], "type": "город", "population": 75000},
    {"name": "Черемхово", "coords": [53.1367, 103.0675], "type": "город", "population": 49000},
    {"name": "Шелехов", "coords": [52.2139, 104.0975], "type": "город", "population": 47000},
    {"name": "Тайшет", "coords": [55.9406, 98.0031], "type": "город", "population": 33000},
    {"name": "Усть-Кут", "coords": [56.8000, 105.8333], "type": "город", "population": 41000},
    {"name": "Нижнеудинск", "coords": [54.8969, 99.0276], "type": "город", "population": 34000},
    {"name": "Тулун", "coords": [54.5614, 100.5794], "type": "город", "population": 39000},
    {"name": "Киренск", "coords": [57.7857, 108.1111], "type": "город", "population": 11000},
    {"name": "Слюдянка", "coords": [51.6594, 103.7061], "type": "город", "population": 18000},
    {"name": "Байкальск", "coords": [51.5233, 104.1475], "type": "город", "population": 13000},
    {"name": "Листвянка", "coords": [51.8675, 104.8564], "type": "поселок", "population": 2000}
]

# Аэропорты
airports = [
    {"name": "Иркутск (Международный)", "coords": [52.2680, 104.3890], "iata": "IKT"},
    {"name": "Братск", "coords": [56.3706, 101.6983], "iata": "BTK"},
    {"name": "Усть-Илимск", "coords": [58.1361, 102.5650], "iata": "UIK"},
    {"name": "Усть-Кут", "coords": [56.8567, 105.7300], "iata": "UKX"}
]

# Речные порты
river_ports = [
    {"name": "Иркутский порт", "coords": [52.2900, 104.3000], "river": "Ангара"},
    {"name": "Братский порт", "coords": [56.1500, 101.6500], "river": "Ангара"},
    {"name": "Порт Осетрово", "coords": [56.8167, 105.9000], "river": "Лена"}
]

# Железнодорожные станции
railway_stations = [
    {"name": "Иркутск-Пассажирский", "coords": [52.2754, 104.2849], "lines": "Транссиб"},
    {"name": "Слюдянка", "coords": [51.6594, 103.7061], "lines": "Транссиб"},
    {"name": "Тайшет", "coords": [55.9406, 98.0031], "lines": "Транссиб, БАМ"},
    {"name": "Усть-Кут", "coords": [56.8000, 105.8333], "lines": "БАМ"},
    {"name": "Братск", "coords": [56.1514, 101.6342], "lines": "БАМ"}
]

# Основные реки
rivers = [
    {
        "name": "Ангара",
        "coords": [
            [51.8675, 104.8564], [52.2864, 104.2807], [52.5362, 103.8865],
            [52.7561, 103.6386], [53.1367, 103.0675], [56.1514, 101.6342],
            [58.0006, 102.6619]
        ]
    },
    {
        "name": "Лена",
        "coords": [
            [53.9683, 107.8803], [56.8000, 105.8333], [57.7857, 108.1111]
        ]
    }
]

# Железнодорожные линии
railway_lines = [
    {
        "name": "Транссибирская магистраль",
        "coords": [
            [55.9406, 98.0031], [54.8969, 99.0276], [54.5614, 100.5794],
            [53.9202, 102.0442], [53.1367, 103.0675], [52.7561, 103.6386],
            [52.5362, 103.8865], [52.2864, 104.2807], [51.6594, 103.7061]
        ]
    },
    {
        "name": "Байкало-Амурская магистраль",
        "coords": [
            [55.9406, 98.0031], [56.1167, 101.1667], [56.1514, 101.6342],
            [56.7000, 104.2500], [56.8000, 105.8333], [56.8167, 105.9000]
        ]
    }
]

# Функция для генерации CesiumJS HTML
def generate_cesium_html(cesium_token):
    # Создаем JavaScript код для добавления сущностей
    entities_js = ""
    
    # Добавление городов
    for city in settlements:
        color = "#FF4444" if city["type"] == "город" else "#FFA500"
        pixel_size = 10 if city["population"] > 100000 else 8
        
        entities_js += f"""
            viewer.entities.add({{
                name: '{city['name']}',
                position: Cesium.Cartesian3.fromDegrees({city['coords'][1]}, {city['coords'][0]}, 100),
                point: {{
                    pixelSize: {pixel_size},
                    color: Cesium.Color.fromCssColorString('{color}'),
                    outlineColor: Cesium.Color.WHITE,
                    outlineWidth: 1,
                    heightReference: Cesium.HeightReference.CLAMP_TO_GROUND
                }},
                label: {{
                    text: '{city['name']}',
                    font: '14px sans-serif',
                    fillColor: Cesium.Color.WHITE,
                    style: Cesium.LabelStyle.FILL_AND_OUTLINE,
                    outlineWidth: 2,
                    verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                    pixelOffset: new Cesium.Cartesian2(0, -10),
                    heightReference: Cesium.HeightReference.CLAMP_TO_GROUND
                }},
                description: '{city['name']}<br>Население: {city['population']:,} чел.<br>Тип: {city['type']}'
            }});
        """
    
    # Добавление аэропортов
    for airport in airports:
        entities_js += f"""
            viewer.entities.add({{
                name: '{airport['name']}',
                position: Cesium.Cartesian3.fromDegrees({airport['coords'][1]}, {airport['coords'][0]}, 200),
                billboard: {{
                    image: 'data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'24\\' height=\\'24\\' viewBox=\\'0 0 24 24\\'%3E%3Cpath fill=\\'%23000000\\' d=\\'M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z\\'/%3E%3C/svg%3E',
                    scale: 0.8,
                    verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                    heightReference: Cesium.HeightReference.CLAMP_TO_GROUND
                }},
                description: '{airport['name']}<br>IATA: {airport['iata']}'
            }});
        """
    
    # Добавление речных портов
    for port in river_ports:
        entities_js += f"""
            viewer.entities.add({{
                name: '{port['name']}',
                position: Cesium.Cartesian3.fromDegrees({port['coords'][1]}, {port['coords'][0]}, 50),
                billboard: {{
                    image: 'data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'24\\' height=\\'24\\' viewBox=\\'0 0 24 24\\'%3E%3Cpath fill=\\'%230000FF\\' d=\\'M6 18c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm12 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-6-5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM7.5 7.5L12 3l4.5 4.5H14v7h-4v-7H7.5z\\'/%3E%3C/svg%3E',
                    scale: 0.8,
                    verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                    heightReference: Cesium.HeightReference.CLAMP_TO_GROUND
                }},
                description: '{port['name']}<br>Река: {port['river']}'
            }});
        """
    
    # Добавление железнодорожных станций
    for station in railway_stations:
        entities_js += f"""
            viewer.entities.add({{
                name: '{station['name']}',
                position: Cesium.Cartesian3.fromDegrees({station['coords'][1]}, {station['coords'][0]}, 50),
                billboard: {{
                    image: 'data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'24\\' height=\\'24\\' viewBox=\\'0 0 24 24\\'%3E%3Cpath fill=\\'%238B0000\\' d=\\'M12 2c-4 0-8 .5-8 4v9.5C4 17.43 5.57 19 7.5 19L6 20.5v.5h2l2-2h4l2 2h2v-.5L16.5 19c1.93 0 3.5-1.57 3.5-3.5V6c0-3.5-4-4-8-4zm0 2c3.5 0 6 .5 6 1.5V7H6V5.5C6 4.5 8.5 4 12 4zM6 9h12v3H6V9zm10.5 7c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm-9 0c-.83 0-1.5-.67-1.5-1.5S6.67 13 7.5 13s1.5.67 1.5 1.5S8.33 16 7.5 16z\\'/%3E%3C/svg%3E',
                    scale: 0.8,
                    verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                    heightReference: Cesium.HeightReference.CLAMP_TO_GROUND
                }},
                description: 'Станция {station['name']}<br>Линии: {station['lines']}'
            }});
        """
    
    # Добавление рек
    for river in rivers:
        positions = ", ".join([f"{{lon: {coord[1]}, lat: {coord[0]}}}" for coord in river["coords"]])
        entities_js += f"""
            var riverPositions_{river['name']} = [{positions}];
            var riverPoints_{river['name']} = [];
            for (var i = 0; i < riverPositions_{river['name']}.length; i++) {{
                riverPoints_{river['name']}.push(Cesium.Cartesian3.fromDegrees(
                    riverPositions_{river['name']}[i].lon,
                    riverPositions_{river['name']}[i].lat,
                    0
                ));
            }}
            viewer.entities.add({{
                name: '{river['name']}',
                polyline: {{
                    positions: riverPoints_{river['name']},
                    width: 3,
                    material: Cesium.Color.fromCssColorString('#1E90FF'),
                    clampToGround: true
                }}
            }});
        """
    
    # Добавление железных дорог
    for line in railway_lines:
        positions = ", ".join([f"{{lon: {coord[1]}, lat: {coord[0]}}}" for coord in line["coords"]])
        entities_js += f"""
            var railPositions_{line['name']} = [{positions}];
            var railPoints_{line['name']} = [];
            for (var i = 0; i < railPositions_{line['name']}.length; i++) {{
                railPoints_{line['name']}.push(Cesium.Cartesian3.fromDegrees(
                    railPositions_{line['name']}[i].lon,
                    railPositions_{line['name']}[i].lat,
                    50
                ));
            }}
            viewer.entities.add({{
                name: '{line['name']}',
                polyline: {{
                    positions: railPoints_{line['name']},
                    width: 4,
                    material: Cesium.Color.fromCssString('#8B0000'),
                    clampToGround: false
                }}
            }});
        """
    
    # Добавление озера Байкал
    baikal_coords = [
        [51.5, 104.0], [52.5, 106.5], [54.5, 109.5],
        [55.5, 109.5], [55.5, 108.0], [51.5, 104.0]
    ]
    baikal_positions = ", ".join([f"{{lon: {coord[1]}, lat: {coord[0]}}}" for coord in baikal_coords])
    
    entities_js += f"""
        var baikalPositions = [{baikal_positions}];
        var baikalPoints = [];
        for (var i = 0; i < baikalPositions.length; i++) {{
            baikalPoints.push(Cesium.Cartesian3.fromDegrees(
                baikalPositions[i].lon,
                baikalPositions[i].lat,
                0
            ));
        }}
        viewer.entities.add({{
            name: 'Озеро Байкал',
            polygon: {{
                hierarchy: new Cesium.PolygonHierarchy(baikalPoints),
                material: Cesium.Color.fromCssColorString('#1E90FF').withAlpha(0.3),
                outline: true,
                outlineColor: Cesium.Color.fromCssColorString('#1E90FF'),
                outlineWidth: 2,
                perPositionHeight: true
            }},
            description: 'Озеро Байкал - самое глубокое озеро в мире'
        }});
    """
    
    # Полный HTML с CesiumJS
    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="utf-8">
        <style>
            body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; }}
            #cesiumContainer {{ width: 100%; height: 100vh; position: absolute; top: 0; left: 0; }}
            .cesium-infoBox {{ max-width: 300px; }}
        </style>
        <link href="https://cesium.com/downloads/cesiumjs/releases/1.115/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
        <script src="https://cesium.com/downloads/cesiumjs/releases/1.115/Build/Cesium/Cesium.js"></script>
    </head>
    <body>
        <div id="cesiumContainer"></div>
        <script>
            Cesium.Ion.defaultAccessToken = '{cesium_token}';
            
            (async function() {{
                const viewer = new Cesium.Viewer('cesiumContainer', {{
                    animation: false,
                    baseLayerPicker: true,
                    fullscreenButton: true,
                    vrButton: false,
                    geocoder: true,
                    homeButton: true,
                    infoBox: true,
                    sceneModePicker: true,
                    selectionIndicator: true,
                    timeline: false,
                    navigationHelpButton: true,
                    skyBox: true,
                    skyAtmosphere: true,
                    targetFrameRate: 60,
                    terrainProvider: await Cesium.createWorldTerrainAsync({{
                        requestVertexNormals: true,
                        requestWaterMask: true
                    }})
                }});
                
                // Добавление Bing Maps с подписями
                viewer.imageryLayers.addImageryProvider(
                    new Cesium.BingMapsImageryProvider({{
                        url: 'https://dev.virtualearth.net',
                        key: 'AqC6Q7Gx6x9KjF8kL3pR2sT5vX8yZ4wN7bM1dQ9fH2jS5kL8pR3sT6vX9yZ4wN',
                        mapStyle: Cesium.BingMapsStyle.AERIAL_WITH_LABELS_ON_DEMAND
                    }})
                );
                
                // Установка начальной камеры на Иркутскую область
                viewer.camera.flyTo({{
                    destination: Cesium.Cartesian3.fromDegrees(104.1794, 56.4977, 1500000),
                    duration: 2
                }});
                
                // Добавление всех объектов
                {entities_js}
            }})();
        </script>
    </body>
    </html>
    """
    
    return html

# Основной интерфейс Streamlit
def main():
    st.title("🏔️ Иркутская область в 3D (CesiumJS)")
    
    # Создание боковой панели
    with st.sidebar:
        st.header("ℹ️ Информация")
        st.markdown("""
        ### Иркутская область
        **Административный центр:** Иркутск  
        **Площадь:** 774 846 км²  
        **Население:** ≈ 2.3 млн человек  
        
        ### 🌍 CesiumJS возможности
        - 3D-глобус с рельефом
        - Реалистичная вода
        - Спутниковые снимки
        """)
        
        st.divider()
        
        st.subheader("🔑 Настройки Cesium")
        
        # Поле для ввода токена
        cesium_token = st.text_input(
            "Cesium Ion Token:", 
            type="password",
            help="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJiM2E4YjhiZS01N2EwLTQ1OTQtYjZhYy0yNjg3NzUyOWE1YjkiLCJpZCI6MzkzMTgxLCJpYXQiOjE3NzE4MTUxNDF9.z9_lDEdqdI1btaciZ8esNF-HsKgpOJKJY3rwBxNDBwo"
        )
        
        if cesium_token:
            st.session_state["cesium_token"] = cesium_token
            st.success("✅ Токен установлен!")
        
        st.divider()
        
        st.subheader("🎮 Управление")
        st.markdown("""
        - **Левая кнопка:** Вращение
        - **Правая кнопка:** Панорамирование
        - **Колесо:** Масштаб
        - **Средняя кнопка:** Наклон
        """)
    
    # Основной контент
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if "cesium_token" in st.session_state and st.session_state["cesium_token"]:
            # Генерация HTML с токеном
            html_content = generate_cesium_html(st.session_state["cesium_token"])
            
            # Отображение карты через HTML-компонент
            st.components.v1.html(html_content, height=700, width=None)
        else:
            st.info("👆 Пожалуйста, введите ваш Cesium Ion Token в боковой панели для отображения карты")
            
            st.markdown("""
            ### Как получить токен:
            1. Перейдите на [Cesium Ion](https://cesium.com/ion/signup)
            2. Зарегистрируйтесь (есть бесплатный план)
            3. Скопируйте ваш токен из панели управления
            4. Вставьте его в поле слева
            """)
    
    with col2:
        st.subheader("📊 Статистика")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Городов", len([s for s in settlements if s["type"] == "город"]))
            st.metric("Аэропортов", len(airports))
        with col_b:
            st.metric("ЖД станций", len(railway_stations))
            st.metric("Речных портов", len(river_ports))

if __name__ == "__main__":
    main()
def main():
    st.title("🏔️ Иркутская область в 3D (CesiumJS)")
    
    # Пытаемся получить токен из разных источников
    cesium_token = None
    
    # 1. Из Streamlit secrets (для облачного деплоя)
    try:
        cesium_token = st.secrets.get("cesium_token", "")
    except:
        pass
    
    # 2. Из переменных окружения
    if not cesium_token:
        import os
        cesium_token = os.environ.get("CESIUM_TOKEN", "")
    
    # Создание боковой панели
    with st.sidebar:
        st.header("ℹ️ Информация")
        # ... остальной код ...
        
        st.subheader("🔑 Настройки Cesium")
        
        # 3. Ручной ввод как запасной вариант
        manual_token = st.text_input(
            "Cesium Ion Token:", 
            value=cesium_token,
            type="password",
            help="Вставьте ваш токен от Cesium Ion. Получите на cesium.com/ion"
        )
        
        if manual_token:
            cesium_token = manual_token
            st.session_state["cesium_token"] = manual_token
            st.success("✅ Токен установлен!")