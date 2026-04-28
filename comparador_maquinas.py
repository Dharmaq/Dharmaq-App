import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# =====================================================================
# CONFIGURAÇÃO GERAL
# =====================================================================
st.set_page_config(page_title="Dharmaq - Simuladores", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; }
    h1 { color: #00d4ff; }
    h2 { color: #ffffff; border-bottom: 2px solid #00d4ff; padding-bottom: 8px; }
    h3 { color: #00d4ff; }
    .menu-button {
        display: inline-block;
        padding: 12px 18px;
        margin: 8px 6px 8px 0;
        border-radius: 8px;
        border: 1px solid #3b82f6;
        color: #ffffff;
        background-color: #111827;
        text-decoration: none;
        cursor: pointer;
        font-size: 14px;
    }
    .menu-button-active {
        background-color: #3b82f6;
        border-color: #60a5fa;
        color: #ffffff;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# CONTROLE DE NAVEGAÇÃO (HOME / INPACK / CARNEVALLI / IMPORTAÇÃO)
# =====================================================================
if "page" not in st.session_state:
    st.session_state.page = "home"  # home, inpack, carnevalli, importacao

def go_to(page_name: str):
    st.session_state.page = page_name

# =====================================================================
# TELA INICIAL (HOME)
# =====================================================================
def show_home():
    home_img_path = Path(__file__).parent / "home_dharmaq.png"

    col_left, col_right = st.columns([2, 3])
    with col_left:
        if home_img_path.exists():
            st.image(str(home_img_path), use_column_width=True)
        else:
            st.markdown("### Dharmaq")
            st.markdown("Bem-vindo ao painel de simulação.")

    with col_right:
        st.markdown("## Bem-vindo ao simulador Dharmaq")
        st.markdown("""
Use este painel para comparar cenários reais de produção e investimento:

- **In.Pack** – simulação completa de máquina multivias vs máquina atual vs cenário de equiparação  
- **Carnevalli** – módulo específico para extrusoras e filmes (em breve)  
- **Contas para Importação** – cálculo do custo final da máquina no Brasil, com câmbio e impostos

Escolha abaixo qual módulo deseja abrir.
""")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔹 Simulador In.Pack", use_container_width=True):
                go_to("inpack")
        with c2:
            if st.button("🔹 Contas para Importação", use_container_width=True):
                go_to("importacao")

        c3, c4 = st.columns(2)
        with c3:
            if st.button("🔸 Carnevalli (em breve)", use_container_width=True):
                go_to("carnevalli")
        with c4:
            st.info("Outros módulos podem ser adicionados aqui futuramente.")

# =====================================================================
# BARRA DE MENU (APARECE EM TODAS AS TELAS, EXCETO HOME SE QUISER)
# =====================================================================
def show_top_menu():
    st.markdown("### Navegação")

    cols = st.columns(4)
    with cols[0]:
        if st.button("🏠 Home", key="btn_home"):
            go_to("home")
    with cols[1]:
        if st.button("In.Pack", key="btn_inpack"):
            go_to("inpack")
    with cols[2]:
        if st.button("Carnevalli (em breve)", key="btn_carnevalli"):
            go_to("carnevalli")
    with cols[3]:
        if st.button("Contas para Importação", key="btn_import"):
            go_to("importacao")

    st.markdown("---")

# =====================================================================
# MÓDULO 1 - SIMULADOR IN.PACK  (CÓDIGO QUE VOCÊ JÁ TINHA)
# =====================================================================
def show_inpack():
    show_top_menu()

    st.title("Simulador Dharmaq - In.Pack")
    st.markdown("### Comparativo: Máquina do Cliente x In.Pack x Equiparação")

    # ----------------- DADOS BASE -----------------
    dados_base = {
        "Cliente": {
            "nome": "Máquina do Cliente (Atual)",
            "largura_total": 300.0,
            "comprimento": 400.0,
            "espessura": 6.0,
            "densidade": 0.949,
            "qtde_maq": 1.0,
            "pistas": 1.0,
            "gpm": 600.0,
            "bolsas_rolo": 560.0,
            "horas_dia": 18.0,
            "minutos_hora": 54.0,
            "dias_mes": 22.0,
            "exw": 50000.0,
            "cif_pct": 10.0,
            "dep_meses": 96.0,
            "mo_qtde": 1.0,
            "mo_valor": 800.0,
            "potencia": 8.0,
            "consumo_pct": 60.0,
            "custo_kwh": 0.15,
            "outros": 800.0,
            "conv_moeda": 6.0,
            "bobina_local": 20.0,
            "venda_local": 23.0,
        },
        "InPack": {
            "nome": "In.Pack",
            "largura_total": 300.0,
            "comprimento": 400.0,
            "espessura": 6.0,
            "densidade": 0.949,
            "qtde_maq": 1.0,
            "pistas": 4.0,
            "gpm": 600.0,
            "bolsas_rolo": 560.0,
            "horas_dia": 18.0,
            "minutos_hora": 54.0,
            "dias_mes": 22.0,
            "exw": 350000.0,
            "cif_pct": 10.0,
            "dep_meses": 96.0,
            "mo_qtde": 2.0,
            "mo_valor": 800.0,
            "potencia": 14.0,
            "consumo_pct": 60.0,
            "custo_kwh": 0.15,
            "outros": 1600.0,
            "conv_moeda": 6.0,
            "bobina_local": 20.0,
            "venda_local": 23.0,
        },
        "Equip": {
            "nome": "Equiparação (várias máquinas simples)",
            "largura_total": 300.0,
            "comprimento": 400.0,
            "espessura": 6.0,
            "densidade": 0.949,
            "qtde_maq": 4.0,
            "pistas": 4.0,
            "gpm": 600.0,
            "bolsas_rolo": 560.0,
            "horas_dia": 18.0,
            "minutos_hora": 54.0,
            "dias_mes": 22.0,
            "exw": 200000.0,
            "cif_pct": 10.0,
            "dep_meses": 96.0,
            "mo_qtde": 4.0,
            "mo_valor": 800.0,
            "potencia": 32.0,
            "consumo_pct": 60.0,
            "custo_kwh": 0.15,
            "outros": 3200.0,
            "conv_moeda": 6.0,
            "bobina_local": 20.0,
            "venda_local": 23.0,
        },
    }

    def calcular(m):
        bobina_euro = m["bobina_local"] / m["conv_moeda"]
        venda_euro  = m["venda_local"]  / m["conv_moeda"]

        area_mm2  = m["largura_total"] * m["comprimento"] * 2.0
        area_m2   = area_mm2 / 1_000_000.0
        esp_m     = m["espessura"] * 1e-6
        dens_kgm3 = m["densidade"] * 1000.0
        peso_kg   = area_m2 * esp_m * dens_kgm3
        peso_gr   = peso_kg * 1000.0

        bolsas_min = m["gpm"] * m["pistas"]
        trocas_min = bolsas_min / m["bolsas_rolo"]
        rolos_hora = bolsas_min * m["minutos_hora"] / m["bolsas_rolo"]
        bolsas_dia = bolsas_min * m["minutos_hora"] * m["horas_dia"]
        rolos_dia  = bolsas_dia / m["bolsas_rolo"]

        kg_hora = bolsas_min * m["minutos_hora"] * peso_kg
        kg_dia  = kg_hora * m["horas_dia"]
        kg_mes  = kg_dia * m["dias_mes"]
        kg_ano  = kg_mes * 12.0

        valor_cif = m["exw"] * (1.0 + m["cif_pct"] / 100.0)
        dep_mes   = valor_cif / m["dep_meses"]

        mo_mes = m["mo_qtde"] * m["mo_valor"]

        consumo_kw = m["potencia"] * (m["consumo_pct"] / 100.0)
        horas_mes  = m["horas_dia"] * m["dias_mes"]
        ee_mes     = consumo_kw * horas_mes * m["custo_kwh"]

        custo_mes = dep_mes + mo_mes + ee_mes + m["outros"]
        conv_kg   = custo_mes / kg_mes
        conv_ton  = conv_kg * 1000.0
        conv_ano  = custo_mes * 12.0

        fatur_anual        = venda_euro * kg_ano
        custo_material_ano = bobina_euro * kg_ano
        lucro_liq          = fatur_anual - custo_material_ano - conv_ano

        return {
            "bobina_euro": bobina_euro, "venda_euro": venda_euro,
            "area_mm2": area_mm2, "peso_gr": peso_gr, "peso_kg": peso_kg,
            "bolsas_min": bolsas_min, "trocas_min": trocas_min,
            "rolos_hora": rolos_hora, "bolsas_dia": bolsas_dia,
            "rolos_dia": rolos_dia, "kg_hora": kg_hora,
            "kg_dia": kg_dia, "kg_mes": kg_mes, "kg_ano": kg_ano,
            "valor_cif": valor_cif, "dep_mes": dep_mes,
            "mo_mes": mo_mes, "consumo_kw": consumo_kw,
            "ee_mes": ee_mes, "custo_mes": custo_mes,
            "conv_kg": conv_kg, "conv_ton": conv_ton, "conv_ano": conv_ano,
            "fatur_anual": fatur_anual,
            "custo_material_ano": custo_material_ano,
            "lucro_liq": lucro_liq,
        }

    cores_map = {
        "Cliente": "#ef4444",
        "InPack":  "#3b82f6",
        "Equip":   "#22c55e",
    }
    fillcolors_map = {
        "Cliente": "rgba(239, 68, 68, 0.08)",
        "InPack":  "rgba(59, 130, 246, 0.08)",
        "Equip":   "rgba(34, 197, 94, 0.08)",
    }
    keys = ["Cliente", "InPack", "Equip"]

    st.sidebar.title("Parâmetros das Máquinas - In.Pack")
    st.sidebar.markdown("Edite os valores. Os gráficos atualizam automaticamente.")

    maquinas = {}
    for key in keys:
        base  = dados_base[key]
        cor   = cores_map[key]
        st.sidebar.markdown(f"<h3 style='color:{cor}'>{base['nome']}</h3>", unsafe_allow_html=True)

        nome = st.sidebar.text_input("Nome / cenário", value=base["nome"], key=f"nome_{key}")

        with st.sidebar.expander("Bolsa / Material"):
            largura_total = st.number_input("Largura Total (mm)", value=base["largura_total"], step=1.0, key=f"lt_{key}")
            comprimento   = st.number_input("Comprimento (mm)", value=base["comprimento"], step=1.0, key=f"comp_{key}")
            espessura     = st.number_input("Espessura (micra)", value=base["espessura"], step=0.5, key=f"esp_{key}")
            densidade     = st.number_input("Densidade (g/cm³)", value=base["densidade"], step=0.001, format="%.3f", key=f"dens_{key}")

        with st.sidebar.expander("Produção"):
            qtde_maq     = st.number_input("Qtd máquinas", value=base["qtde_maq"], step=1.0, key=f"qtde_{key}")
            pistas       = st.number_input("Linhas / Pistas", value=base["pistas"], step=1.0, key=f"pistas_{key}")
            gpm          = st.number_input("GPM (bolsas/min/pista)", value=base["gpm"], step=10.0, key=f"gpm_{key}")
            bolsas_rolo  = st.number_input("Bolsas por rolo", value=base["bolsas_rolo"], step=10.0, key=f"br_{key}")
            horas_dia    = st.number_input("Horas/dia", value=base["horas_dia"], step=1.0, key=f"hd_{key}")
            minutos_hora = st.number_input("Minutos produtivos/hora", value=base["minutos_hora"], step=1.0, key=f"mh_{key}")
            dias_mes     = st.number_input("Dias/mês", value=base["dias_mes"], step=1.0, key=f"dm_{key}")

        with st.sidebar.expander("Investimento / Custos"):
            exw         = st.number_input("EXW (Euro)", value=base["exw"], step=1000.0, key=f"exw_{key}")
            cif_pct     = st.number_input("CIF (%)", value=base["cif_pct"], step=0.5, key=f"cif_{key}")
            dep_meses   = st.number_input("Depreciação (meses)", value=base["dep_meses"], step=1.0, key=f"dep_{key}")
            mo_qtde     = st.number_input("Operadores x Turnos", value=base["mo_qtde"], step=1.0, key=f"moq_{key}")
            mo_valor    = st.number_input("Valor MO/mês (Euro)", value=base["mo_valor"], step=50.0, key=f"mov_{key}")
            potencia    = st.number_input("Potência (kW)", value=base["potencia"], step=1.0, key=f"pot_{key}")
            consumo_pct = st.number_input("Consumo EE (%)", value=base["consumo_pct"], step=1.0, key=f"cee_{key}")
            custo_kwh   = st.number_input("Valor EE (Euro/kWh)", value=base["custo_kwh"], step=0.01, key=f"kwh_{key}")
            outros      = st.number_input("Outros custos (Euro/mês)", value=base["outros"], step=100.0, key=f"outros_{key}")

        with st.sidebar.expander("Preços / Moeda"):
            conv_moeda   = st.number_input("Conversão moeda/Euro", value=base["conv_moeda"], step=0.1, key=f"conv_{key}")
            bobina_local = st.number_input("Bobina/kg (moeda local)", value=base["bobina_local"], step=0.5, key=f"bobloc_{key}")
            venda_local  = st.number_input("Venda/kg (moeda local)", value=base["venda_local"], step=0.5, key=f"vendloc_{key}")

        maquinas[key] = {
            "nome": nome,
            "largura_total": largura_total, "comprimento": comprimento,
            "espessura": espessura, "densidade": densidade,
            "qtde_maq": qtde_maq, "pistas": pistas, "gpm": gpm,
            "bolsas_rolo": bolsas_rolo, "horas_dia": horas_dia,
            "minutos_hora": minutos_hora, "dias_mes": dias_mes,
            "exw": exw, "cif_pct": cif_pct, "dep_meses": dep_meses,
            "mo_qtde": mo_qtde, "mo_valor": mo_valor,
            "potencia": potencia, "consumo_pct": consumo_pct,
            "custo_kwh": custo_kwh, "outros": outros,
            "conv_moeda": conv_moeda, "bobina_local": bobina_local,
            "venda_local": venda_local,
        }

    r    = {k: calcular(v) for k, v in maquinas.items()}
    keys_all = ["Cliente", "InPack", "Equip"]

    st.markdown("## Selecione os cenários a exibir")
    col_cb1, col_cb2, col_cb3 = st.columns(3)
    mostrar = {
        "Cliente": col_cb1.checkbox("Máquina do Cliente", value=True),
        "InPack":  col_cb2.checkbox("In.Pack", value=True),
        "Equip":   col_cb3.checkbox("Equiparação (várias máquinas simples)", value=True),
    }
    keys_vis = [k for k in keys_all if mostrar[k]]
    if not keys_vis:
        st.warning("Selecione ao menos um cenário para exibir.")
        return

    # ---- CARDS ----
    st.markdown("## Resumo Executivo")
    card_cols = st.columns(len(keys_vis))
    for col, k in zip(card_cols, keys_vis):
        cor    = cores_map[k]
        lucro  = r[k]["lucro_liq"]
        kg_mes = r[k]["kg_mes"]
        conv_k = r[k]["conv_kg"]
        ganho_vs_atual = lucro - r["Cliente"]["lucro_liq"]
        sinal = "+" if lucro >= 0 else ""
        sinal_g = "+" if ganho_vs_atual >= 0 else ""

        with col:
            st.markdown(f"""
            <div style='background-color:#1e2130; padding:20px; border-radius:12px;
                        border-left: 5px solid {cor}; margin-bottom:10px;'>
                <h3 style='color:{cor}; margin:0'>{maquinas[k]['nome']}</h3>
                <p style='color:#aaa; margin:8px 0 2px'>Produção mensal</p>
                <h2 style='color:white; margin:0'>{kg_mes:,.0f} kg/mês</h2>
                <p style='color:#aaa; margin:8px 0 2px'>Lucro líquido / ano</p>
                <h2 style='color:{cor}; margin:0'>{sinal}€ {lucro:,.0f}</h2>
                <p style='color:#aaa; margin:8px 0 2px'>Ganho adicional vs atual / ano</p>
                <h3 style='color:{"#22c55e" if ganho_vs_atual >= 0 else "#ef4444"}; margin:0'>
                    {sinal_g}€ {ganho_vs_atual:,.0f}
                </h3>
                <p style='color:#aaa; margin:8px 0 2px'>Custo conversão / kg</p>
                <h3 style='color:white; margin:0'>€ {conv_k:.4f}</h3>
            </div>
            """, unsafe_allow_html=True)

    # ---- GAUGE PRODUÇÃO ----
    st.markdown("## Capacidade de Produção (kg/mês)")
    st.caption("Quanto cada cenário produz por mês — quanto maior, melhor")

    max_prod = max(r[k]["kg_mes"] for k in keys_vis) * 1.2
    gauge_cols = st.columns(len(keys_vis))
    for col, k in zip(gauge_cols, keys_vis):
        val = r[k]["kg_mes"]
        cor = cores_map[k]
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=val,
            delta={"reference": r["Cliente"]["kg_mes"], "valueformat": ",.0f"},
            title={"text": maquinas[k]["nome"], "font": {"color": "white", "size": 13}},
            number={"suffix": " kg", "valueformat": ",.0f", "font": {"color": cor, "size": 20}},
            gauge={
                "axis": {"range": [0, max_prod], "tickcolor": "white"},
                "bar": {"color": cor},
                "bgcolor": "#1e2130",
                "bordercolor": "#333",
                "steps": [
                    {"range": [0, max_prod * 0.33], "color": "#1a1a2e"},
                    {"range": [max_prod * 0.33, max_prod * 0.66], "color": "#16213e"},
                    {"range": [max_prod * 0.66, max_prod], "color": "#0f3460"},
                ],
                "threshold": {
                    "line": {"color": "white", "width": 2},
                    "thickness": 0.75,
                    "value": r["Cliente"]["kg_mes"],
                },
            },
        ))
        fig.update_layout(
            paper_bgcolor="#0e1117", font_color="white",
            height=260, margin=dict(t=60, b=20, l=30, r=30)
        )
        col.plotly_chart(fig, use_container_width=True)

    # ---- COMPARATIVO GERAL (3 subplots) ----
    st.markdown("## Comparativo Geral")
    fig_bar = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Produção kg/mês", "Custo Conversão €/kg", "Lucro Líquido Anual (€)"),
    )
    for i, k in enumerate(keys_vis):
        nome = maquinas[k]["nome"]
        cor  = cores_map[k]
        fig_bar.add_trace(go.Bar(
            name=nome, x=[nome], y=[r[k]["kg_mes"]],
            marker_color=cor,
            text=[f"{r[k]['kg_mes']:,.0f}"], textposition="auto",
            showlegend=(i == 0),
        ), row=1, col=1)
        fig_bar.add_trace(go.Bar(
            name=nome, x=[nome], y=[r[k]["conv_kg"]],
            marker_color=cor,
            text=[f"€{r[k]['conv_kg']:.4f}"], textposition="auto",
            showlegend=False,
        ), row=1, col=2)
        fig_bar.add_trace(go.Bar(
            name=nome, x=[nome], y=[r[k]["lucro_liq"]],
            marker_color=cor,
            text=[f"€{r[k]['lucro_liq']:,.0f}"], textposition="auto",
            showlegend=False,
        ), row=1, col=3)

    fig_bar.update_layout(
        paper_bgcolor="#0e1117", plot_bgcolor="#1e2130",
        font_color="white", height=400,
        showlegend=True,
    )
    fig_bar.update_xaxes(showgrid=False)
    fig_bar.update_yaxes(gridcolor="#333")
    st.plotly_chart(fig_bar, use_container_width=True)

    # ---- FLUXO DE CAIXA ACUMULADO ----
    st.markdown("## Fluxo de Caixa Acumulado — 0 a 10 anos")
    st.caption("Inclui o investimento inicial no Ano 0. Mostra quando cada cenário se paga e quanto acumula.")

    anos = list(range(0, 11))
    fig_fc = go.Figure()
    for k in keys_vis:
        cor  = cores_map[k]
        fill = fillcolors_map[k]
        investimento = maquinas[k]["exw"] * (1 + maquinas[k]["cif_pct"] / 100)
        lucro_anual  = r[k]["lucro_liq"]

        fluxo = [-investimento]
        for _ in range(1, 11):
            fluxo.append(fluxo[-1] + lucro_anual)

        fig_fc.add_trace(go.Scatter(
            x=anos, y=fluxo,
            mode="lines+markers",
            name=maquinas[k]["nome"],
            line=dict(color=cor, width=3),
            marker=dict(size=8, color=cor),
            fill="tozeroy",
            fillcolor=fill,
            hovertemplate=(
                f"<b>{maquinas[k]['nome']}</b><br>"
                "Ano %{x}<br>"
                "Fluxo acumulado: €%{y:,.0f}<extra></extra>"
            ),
        ))

    fig_fc.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.4,
                     annotation_text="Ponto de equilíbrio", annotation_position="bottom right")

    fig_fc.update_layout(
        paper_bgcolor="#0e1117", plot_bgcolor="#1e2130",
        font_color="white", height=500,
        xaxis=dict(title="Anos", gridcolor="#333", tickvals=list(range(0, 11))),
        yaxis=dict(title="Fluxo de Caixa Acumulado (€)", gridcolor="#333"),
        legend=dict(bgcolor="#1e2130", bordercolor="#333"),
        hovermode="x unified",
    )
    st.plotly_chart(fig_fc, use_container_width=True)

    # ---- PIZZA CUSTOS MENSAIS ----
    st.markdown("## Composição dos Custos Mensais")
    st.caption("Como cada cenário distribui seus custos fixos mensais")

    pizza_cols = st.columns(len(keys_vis))
    for col, k in zip(pizza_cols, keys_vis):
        cor = cores_map[k]
        labels = ["Depreciação", "Mão de Obra", "Energia", "Outros"]
        values = [
            r[k]["dep_mes"],
            r[k]["mo_mes"],
            r[k]["ee_mes"],
            maquinas[k]["outros"],
        ]
        fig_p = go.Figure(go.Pie(
            labels=labels, values=values,
            hole=0.45,
            marker=dict(colors=["#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6"]),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>€%{value:,.2f}<br>%{percent}<extra></extra>",
        ))
        fig_p.update_layout(
            title=dict(text=maquinas[k]["nome"], font=dict(color=cor, size=13)),
            paper_bgcolor="#0e1117", font_color="white",
            height=350, margin=dict(t=60, b=20, l=20, r=20),
            annotations=[dict(
                text=f"€{r[k]['custo_mes']:,.0f}", x=0.5, y=0.5,
                font_size=14, font_color="white", showarrow=False,
            )],
            showlegend=False,
        )
        col.plotly_chart(fig_p, use_container_width=True)

    # ---- TABELA COMPLETA ----
    with st.expander("Ver tabela completa (conferência com Pasta10.xlsx)"):
        linhas = [
            ("Bolsa Largura Total (mm)",               lambda m, rv: m["largura_total"]),
            ("Bolsa Comprimento (mm)",                 lambda m, rv: m["comprimento"]),
            ("Bolsa Área Total (mm²)",                 lambda m, rv: rv["area_mm2"]),
            ("Espessura (micra)",                      lambda m, rv: m["espessura"]),
            ("Densidade do Material (g/cm³)",          lambda m, rv: m["densidade"]),
            ("Bolsa Peso Gr",                          lambda m, rv: rv["peso_gr"]),
            ("Quantidade de máquina",                  lambda m, rv: m["qtde_maq"]),
            ("Linhas ou pistas",                       lambda m, rv: m["pistas"]),
            ("GPM-Estimado",                           lambda m, rv: m["gpm"]),
            ("Bolsas x rolo ou pacote",                lambda m, rv: m["bolsas_rolo"]),
            ("Quantidade de trocas/min",               lambda m, rv: rv["trocas_min"]),
            ("Bolsas/minuto",                          lambda m, rv: rv["bolsas_min"]),
            ("Rolos ou pacotes/hora",                  lambda m, rv: rv["rolos_hora"]),
            ("Horas trabalhadas/dia",                  lambda m, rv: m["horas_dia"]),
            ("Minutos/hora",                           lambda m, rv: m["minutos_hora"]),
            ("Dias trabalhados/mês",                   lambda m, rv: m["dias_mes"]),
            ("Bolsas/dia",                             lambda m, rv: rv["bolsas_dia"]),
            ("Rolos ou pacotes/dia",                   lambda m, rv: rv["rolos_dia"]),
            ("Produção em Kg/hora",                    lambda m, rv: rv["kg_hora"]),
            ("Produção em Kgs/dia",                    lambda m, rv: rv["kg_dia"]),
            ("Produção em Kgs/mês",                    lambda m, rv: rv["kg_mes"]),
            ("Valor máquina - EXW Euro",               lambda m, rv: m["exw"]),
            ("CIF Euro",                               lambda m, rv: rv["valor_cif"]),
            ("Depreciação em meses (€/mês)",           lambda m, rv: rv["dep_mes"]),
            ("Mão de Obra Neces/maq (X qtde turnos)",  lambda m, rv: m["mo_qtde"]),
            ("Valor MO/Mês(Eu)",                       lambda m, rv: m["mo_valor"]),
            ("MO/mês (Eu)",                            lambda m, rv: rv["mo_mes"]),
            ("Potência Instalada (kW)",                lambda m, rv: m["potencia"]),
            ("Consumo de EE (60%) kW",                 lambda m, rv: rv["consumo_kw"]),
            ("Valor EE (kWh) Eu",                      lambda m, rv: m["custo_kwh"]),
            ("Custo de EE (Eu/mês)",                   lambda m, rv: rv["ee_mes"]),
            ("Outros Custos Fixos (Eu/mês)",           lambda m, rv: m["outros"]),
            ("Custo conversão/kilo (Euro)",            lambda m, rv: rv["conv_kg"]),
            ("Custo conversão/tonelada (Euro)",        lambda m, rv: rv["conv_ton"]),
            ("Faturamento anual em Euros",             lambda m, rv: rv["fatur_anual"]),
            ("Custo conversão/ano",                    lambda m, rv: rv["conv_ano"]),
            ("Custo com material (Bobinas/ano)",       lambda m, rv: rv["custo_material_ano"]),
            ("Lucro líquido ano",                      lambda m, rv: rv["lucro_liq"]),
        ]

        tabela = {"Item": []}
        for k in keys_vis:
            tabela[maquinas[k]["nome"]] = []

        for label, fn in linhas:
            tabela["Item"].append(label)
            for k in keys_vis:
                tabela[maquinas[k]["nome"]].append(fn(maquinas[k], r[k]))

        df_tab = pd.DataFrame(tabela)
        st.dataframe(df_tab, use_container_width=True)

# =====================================================================
# MÓDULO 2 - CARNEVALLI (EM BREVE)
# =====================================================================
def show_carnevalli():
    show_top_menu()
    st.title("Carnevalli - Extrusoras")
    st.info("Módulo em desenvolvimento. Em breve, iremos conectar este painel a uma planilha de extrusoras (Carnevalli) para simular produção, consumo e retorno de investimento.")

# =====================================================================
# MÓDULO 3 - CONTAS PARA IMPORTAÇÃO (VERSÃO INICIAL)
# =====================================================================
def show_importacao():
    show_top_menu()
    st.title("Contas para Importação de Máquinas")

    st.markdown("""
Preencha os campos abaixo para estimar o **custo total da máquina importada no Brasil**, considerando:

- Preço da máquina em Euro (EXW)
- Frete + seguro internacional
- Alíquota de impostos
- Taxa de câmbio Euro → Real

Essa é uma **versão inicial**. Depois, quando você enviar a planilha específica, refinamos as fórmulas.
""")

    col1, col2 = st.columns(2)

    with col1:
        exw_eur = st.number_input("Preço EXW da máquina (Euro)", value=350000.0, step=5000.0)
        frete_seguro_eur = st.number_input("Frete + Seguro internacional (Euro)", value=15000.0, step=1000.0)
        outros_eur = st.number_input("Outros custos em Euro (despesas no exterior)", value=0.0, step=1000.0)

        cambio = st.number_input("Câmbio Euro → Real (R$/€)", value=6.0, step=0.1)

    with col2:
        st.markdown("### Impostos (% sobre valor aduaneiro em R$)")
        ii = st.number_input("Imposto de Importação (II) %", value=14.0, step=0.5)
        ipi = st.number_input("IPI %", value=5.0, step=0.5)
        pis = st.number_input("PIS %", value=2.0, step=0.1)
        cofins = st.number_input("COFINS %", value=9.0, step=0.1)
        icms = st.number_input("ICMS %", value=18.0, step=0.5)

    # Cálculos básicos
    valor_mercadoria_eur = exw_eur + frete_seguro_eur + outros_eur
    valor_mercadoria_brl = valor_mercadoria_eur * cambio

    base_ii = valor_mercadoria_brl
    valor_ii = base_ii * (ii / 100.0)

    base_ipi = valor_mercadoria_brl + valor_ii
    valor_ipi = base_ipi * (ipi / 100.0)

    base_pis_cofins = valor_mercadoria_brl + valor_ii + valor_ipi
    valor_pis = base_pis_cofins * (pis / 100.0)
    valor_cofins = base_pis_cofins * (cofins / 100.0)

    # ICMS (simplificado: base = tudo + ICMS, mas aqui vamos usar base sem gross-up,
    # depois ajustamos com a planilha real)
    base_icms = valor_mercadoria_brl + valor_ii + valor_ipi + valor_pis + valor_cofins
    valor_icms = base_icms * (icms / 100.0)

    custo_total_brl = valor_mercadoria_brl + valor_ii + valor_ipi + valor_pis + valor_cofins + valor_icms

    st.markdown("## Resultado")

    colr1, colr2 = st.columns(2)
    with colr1:
        st.markdown("### Valores em Euro")
        st.write(f"- EXW máquina: **€ {exw_eur:,.2f}**")
        st.write(f"- Frete + seguro: **€ {frete_seguro_eur:,.2f}**")
        st.write(f"- Outros custos no exterior: **€ {outros_eur:,.2f}**")
        st.write(f"- Total mercadoria + frete + outros: **€ {valor_mercadoria_eur:,.2f}**")

    with colr2:
        st.markdown("### Valores em Reais (R$)")
        st.write(f"- Valor mercadoria (CIF) em R$: **R$ {valor_mercadoria_brl:,.2f}**")
        st.write(f"- II: **R$ {valor_ii:,.2f}**")
        st.write(f"- IPI: **R$ {valor_ipi:,.2f}**")
        st.write(f"- PIS: **R$ {valor_pis:,.2f}**")
        st.write(f"- COFINS: **R$ {valor_cofins:,.2f}**")
        st.write(f"- ICMS (aprox.): **R$ {valor_icms:,.2f}**")
        st.markdown(f"### **Custo total estimado Brasil (R$): `R$ {custo_total_brl:,.2f}`**")

    with st.expander("Ver detalhes da base de cálculo (para conferir com a planilha depois)"):
        st.write(f"Base II: R$ {base_ii:,.2f}")
        st.write(f"Base IPI: R$ {base_ipi:,.2f}")
        st.write(f"Base PIS/COFINS: R$ {base_pis_cofins:,.2f}")
        st.write(f"Base ICMS (simplificada): R$ {base_icms:,.2f}")
        st.info("Quando você enviar a planilha 'contas para importação', ajustamos as fórmulas para ficar idêntico ao seu modelo.")

# =====================================================================
# ROTEAMENTO ENTRE PÁGINAS
# =====================================================================
page = st.session_state.page

if page == "home":
    show_home()
elif page == "inpack":
    show_inpack()
elif page == "carnevalli":
    show_carnevalli()
elif page == "importacao":
    show_importacao()
else:
    show_home()
