import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

# 讀取數據
df = pd.read_csv('/Users/linyanfu/Desktop/Pokemon.csv')

# 生成 Type 1 的唯一類型列表
type_1_unique = df['Type 1'].unique()

# Pokémon 类型的代表颜色
type_colors = {
    'Bug': 'green', 'Dark': 'black', 'Dragon': 'blue', 'Electric': 'yellow', 
    'Fairy': 'pink', 'Fighting': 'red', 'Fire': 'orange', 'Flying': 'lightblue', 
    'Ghost': 'purple', 'Grass': 'forestgreen', 'Ground': 'brown', 'Ice': 'lightcyan',
    'Normal': 'gray', 'Poison': 'purple', 'Psychic': 'fuchsia', 'Rock': 'gold', 
    'Steel': 'silver', 'Water': 'dodgerblue'
}

# 初始化 Dash 應用程式
app = dash.Dash(__name__)

# 設置 Dash 布局
app.layout = html.Div([
    html.H1("Interactive Pokémon Visualization with Filters"),

    # Dropdown 用來選擇屬性 (基於 Type 1 的資料)
    dcc.Dropdown(
        id='attribute-dropdown',
        options=[
            {'label': type_1, 'value': type_1} for type_1 in type_1_unique
        ],
        value=type_1_unique[0],  # 默認選擇第一個 Type 1
        placeholder="Select Pokémon Type"
    ),

    # RangeSlider 用來設置 Total 範圍
    dcc.RangeSlider(
        id='sales-range-slider',
        min=df['Total'].min(),
        max=df['Total'].max(),
        step=100,  # 設置步長
        marks={i: str(i) for i in range(df['Total'].min(), df['Total'].max(), 5000)},
        value=[df['Total'].min(), df['Total'].max()],  # 默認為完整範圍
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    
    # 顯示圖表
    dcc.Graph(id='pokemon-graph-1'),  # 用來顯示 Type 1 計數的子圖
    dcc.Graph(id='pokemon-graph-2')   # 用來顯示所有符合篩選條件的 Pokémon 的 Total 的子圖
])

# 回調函數，根據選擇的屬性來更新第一個子圖
@app.callback(
    Output('pokemon-graph-1', 'figure'),
    Input('attribute-dropdown', 'value')
)
def update_graph_1(selected_type):
    # 根據選擇的 Type 1 屬性篩選數據
    filtered_df = df[df['Type 1'] == selected_type]
    
    # 顯示 Type 1 類別下的 Pokémon 計數
    type_count_filtered = filtered_df['Type 1'].value_counts().reset_index()
    type_count_filtered.columns = ['Type', 'Count']
    
    # 取得對應的顏色
    color = type_colors.get(selected_type, 'gray')
    
    fig = go.Figure(go.Bar(x=type_count_filtered['Type'], y=type_count_filtered['Count'], 
                           name="Type Count", marker=dict(color=color)))
    
    fig.update_layout(
        title=f"Count of Pokémon for Type {selected_type}",
        height=400,
        showlegend=True
    )
    
    return fig

# 回調函數，根據選擇的屬性和 Total 範圍來更新第二個子圖
@app.callback(
    Output('pokemon-graph-2', 'figure'),
    [Input('attribute-dropdown', 'value'),
     Input('sales-range-slider', 'value')]
)
def update_graph_2(selected_type, sales_range):
    # 根據選擇的 Type 1 屬性篩選數據
    filtered_df = df[df['Type 1'] == selected_type]
    
    # 進一步根據選擇的 Total 範圍過濾數據
    filtered_df = filtered_df[
        (filtered_df['Total'] >= sales_range[0]) &
        (filtered_df['Total'] <= sales_range[1])
    ]
    
    # 取得對應的顏色
    color = type_colors.get(selected_type, 'gray')
    
    # 顯示選定 Type 1 下所有 Pokémon 的 Total 數值
    fig = go.Figure(go.Bar(x=filtered_df['Name'], y=filtered_df['Total'],
                           name="Total Pokémon",
                           text=filtered_df['Name'], textposition='outside',
                           marker=dict(color=color)))
    
    fig.update_layout(
        title=f"Pokémon by Total for Type {selected_type}",
        height=600,
        showlegend=True,
        xaxis_title="Pokémon",
        yaxis_title="Total"
    )
    
    return fig

# 運行 Dash 應用程式
if __name__ == '__main__':
    app.run_server(debug=True)

