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
- **Carnevalli** – módulo específico para extrusoras e coextrusoras  
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
            if st.button("🔸 Carnevalli ", use_container_width=True):
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
        if st.button("Carnevalli", key="btn_carnevalli"):
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
        # =========================================================
    # PAINEL DE DIFERENCIAIS — "Onde a In.Pack se destaca"
    # Só mostra métricas onde In.Pack tem vantagem real
    # =========================================================
    st.markdown("---")
    st.markdown("## 🏆 Onde a In.Pack se Destaca")
    st.caption(
        "Exibe apenas os indicadores onde a In.Pack tem vantagem significativa. "
        "Métricas onde a diferença é pequena são automaticamente ocultadas."
    )

    # --- Limiares mínimos de relevância (editáveis pelo usuário) ---
    with st.expander("⚙️ Ajustar sensibilidade dos filtros"):
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            lim_lucro = st.number_input(
                "Δ Lucro/ano mínimo (€)",
                value=5000.0, step=1000.0, key="lim_lucro"
            )
        with col_f2:
            lim_prod = st.number_input(
                "Δ Produção/mês mínima (kg)",
                value=500.0, step=100.0, key="lim_prod"
            )
        with col_f3:
            lim_conv = st.number_input(
                "Δ Custo conversão/kg mínimo (€)",
                value=0.005, step=0.001, format="%.3f", key="lim_conv"
            )
        with col_f4:
            lim_ee = st.number_input(
                "Δ Custo energia/mês mínimo (€)",
                value=100.0, step=50.0, key="lim_ee"
            )

    # --- Referência: In.Pack vs cada cenário ---
    # Para cada métrica, calcula o delta In.Pack - concorrente
    # Só mostra se o delta superar o limiar

    comparacoes = {
        "Cliente": {"label": "vs Máq. do Cliente", "cor": "#ef4444"},
        "Equip":   {"label": "vs Equiparação",     "cor": "#22c55e"},
    }

    for comp_key, comp_info in comparacoes.items():
        if comp_key not in keys_vis or "InPack" not in keys_vis:
            continue

        r_ip   = r["InPack"]
        r_comp = r[comp_key]
        cor_comp = comp_info["cor"]

        # Calcula deltas
        delta_lucro = r_ip["lucro_liq"]  - r_comp["lucro_liq"]
        delta_prod  = r_ip["kg_mes"]     - r_comp["kg_mes"]
        delta_conv  = r_comp["conv_kg"]  - r_ip["conv_kg"]   # positivo = InPack é mais barato
        delta_ee    = r_comp["ee_mes"]   - r_ip["ee_mes"]    # positivo = InPack consome menos

        # Filtra só os que passam no limiar
        destaques = []

        if delta_lucro > lim_lucro:
            destaques.append({
                "label": "Ganho adicional de lucro/ano",
                "valor": delta_lucro,
                "formato": "€{:,.0f}",
                "cor": "#22c55e",
                "icon": "💰",
                "descricao": f"In.Pack gera € {delta_lucro:,.0f} a mais por ano"
            })

        if delta_prod > lim_prod:
            destaques.append({
                "label": "Aumento de produção/mês",
                "valor": delta_prod,
                "formato": "{:,.0f} kg",
                "cor": "#3b82f6",
                "icon": "🏭",
                "descricao": f"In.Pack produz {delta_prod:,.0f} kg a mais por mês"
            })

        if delta_conv > lim_conv:
            destaques.append({
                "label": "Redução de custo de conversão/kg",
                "valor": delta_conv,
                "formato": "€{:.4f}",
                "cor": "#f59e0b",
                "icon": "⚡",
                "descricao": f"In.Pack custa € {delta_conv:.4f} a menos por kg produzido"
            })

        if delta_ee > lim_ee:
            destaques.append({
                "label": "Economia de energia/mês",
                "valor": delta_ee,
                "formato": "€{:,.0f}",
                "cor": "#8b5cf6",
                "icon": "🔌",
                "descricao": f"In.Pack economiza € {delta_ee:,.0f} em energia por mês"
            })

        # --- Exibe os resultados ---
        st.markdown(f"### In.Pack {comp_info['label']}")

        if not destaques:
            st.info(
                f"Neste cenário a diferença entre In.Pack e {comp_info['label'].replace('vs ', '')} "
                "é pequena nos indicadores configurados. Ajuste os parâmetros ou a sensibilidade dos filtros."
            )
            continue

        # Cards de destaque
        ncols = min(len(destaques), 4)
        dest_cols = st.columns(ncols)
        for col, d in zip(dest_cols, destaques):
            with col:
                valor_fmt = d["formato"].format(d["valor"])
                st.markdown(f"""
<div style="background:linear-gradient(135deg,#1e293b,#020617);
            border-radius:12px; padding:16px 14px;
            border-left:5px solid {d['cor']};
            box-shadow:0 4px 15px rgba(0,0,0,0.3);
            margin-bottom:8px;">
  <div style="font-size:22px; margin-bottom:4px;">{d['icon']}</div>
  <div style="color:#94a3b8; font-size:12px; margin-bottom:4px;">{d['label']}</div>
  <div style="color:{d['cor']}; font-weight:700; font-size:20px; margin-bottom:6px;">{valor_fmt}</div>
  <div style="color:#e5e7eb; font-size:11px;">{d['descricao']}</div>
</div>
""", unsafe_allow_html=True)

        # Gráfico de barras dos diferenciais — só os que passaram no filtro
        if len(destaques) > 0:
            labels_graf  = [d["icon"] + " " + d["label"] for d in destaques]
            valores_graf = [d["valor"] for d in destaques]
            cores_graf   = [d["cor"] for d in destaques]

            # Normaliza para % do maior valor (facilita comparação visual)
            max_val = max(valores_graf) if max(valores_graf) > 0 else 1
            pct_graf = [v / max_val * 100 for v in valores_graf]

            fig_dest = go.Figure()
            fig_dest.add_trace(go.Bar(
                x=labels_graf,
                y=pct_graf,
                marker_color=cores_graf,
                text=[
                    d["formato"].format(d["valor"]) for d in destaques
                ],
                textposition="outside",
                textfont=dict(color="white", size=13),
            ))
            fig_dest.update_layout(
                paper_bgcolor="#0e1117", plot_bgcolor="#1e2130",
                font_color="white", height=380,
                title=dict(
                    text=f"Vantagens reais da In.Pack {comp_info['label']}",
                    font=dict(color="white", size=14)
                ),
                yaxis=dict(
                    title="Intensidade do diferencial (%)",
                    gridcolor="#334155",
                    range=[0, 130],
                ),
                xaxis=dict(gridcolor="#334155"),
                showlegend=False,
            )
            st.plotly_chart(fig_dest, use_container_width=True)

        st.markdown("---")

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
# MÓDULO 2 - CARNEVALLI COMPARADOR MÁQUINAS
# =====================================================================
def show_carnevalli():
    show_top_menu()

    st.markdown("""
<div style="margin-bottom: 15px;">
    <h1 style="margin-bottom: 0;">⚙️ Carnevalli – Extrusoras</h1>
</div>
<p style="font-size: 1.05rem; color: #94a3b8;">
    Comparativo financeiro entre <b>Mono Camada</b>, <b>Coex 3 Camadas</b> e <b>Coex 5 Camadas</b>.
    Fórmulas fiéis à planilha original. Todos os parâmetros são editáveis.
</p>
""", unsafe_allow_html=True)

    st.markdown("### 👁️ Selecione as máquinas para comparar")
    col_cb1, col_cb2, col_cb3 = st.columns(3)
    with col_cb1:
        mostrar_mono = st.checkbox("Mono Camada",    value=True, key="cb_mono")
    with col_cb2:
        mostrar_c3   = st.checkbox("Coex 3 Camadas", value=True, key="cb_c3")
    with col_cb3:
        mostrar_c5   = st.checkbox("Coex 5 Camadas", value=True, key="cb_c5")

    keys_vis = []
    if mostrar_mono: keys_vis.append("mono")
    if mostrar_c3:   keys_vis.append("c3")
    if mostrar_c5:   keys_vis.append("c5")

    if not keys_vis:
        st.warning("Selecione ao menos uma máquina para exibir.")
        return

    cores_maq = {"mono": "#3b82f6", "c3": "#22c55e", "c5": "#f59e0b"}
    nomes_maq = {"mono": "Mono Camada", "c3": "Coex 3 Camadas", "c5": "Coex 5 Camadas"}

    # =========================================================
    # PARÂMETROS GERAIS
    # =========================================================
    st.markdown("### 🌐 Parâmetros Gerais")
    cg1, cg2, cg3 = st.columns(3)
    with cg1:
        preco_venda_kg = st.number_input(
            "Preço de venda (USD/kg)", value=2.0, step=0.05,
            format="%.4f", key="pv_kg"
        )
    with cg2:
        pct_lucro_payback = st.number_input(
            "% do lucro para pagar a máquina", value=30.0, step=5.0,
            format="%.1f", key="pct_pb"
        )
    with cg3:
        espessura_total = st.number_input(
            "Espessura total do filme (µ)", value=100.0, step=5.0,
            format="%.1f", key="esp_total"
        )

    # =========================================================
    # PREÇOS DAS MATÉRIAS-PRIMAS
    # =========================================================
    st.markdown("### 🧪 Preços das Matérias-Primas (USD/kg)")
    mp_nomes = ["LDPE","LLDPE","HDPE","ADITIVO 1","ADITIVO 2","RECICLADO","OFF GRADE","CARBONATO","OTHER"]
    mp_defaults = {
        "LDPE": 1.00, "LLDPE": 0.95, "HDPE": 1.10,
        "ADITIVO 1": 2.30, "ADITIVO 2": 3.00,
        "RECICLADO": 0.75, "OFF GRADE": 0.50,
        "CARBONATO": 0.50, "OTHER": 0.90,
    }
    cols_mp = st.columns(len(mp_nomes))
    precos_mp = {}
    for col, nome in zip(cols_mp, mp_nomes):
        with col:
            precos_mp[nome] = st.number_input(
                nome, value=mp_defaults[nome], step=0.05,
                format="%.2f", key=f"preco_{nome}"
            )

    # =========================================================
    # ESTRUTURA DE CAMADAS
    # =========================================================
    estrutura_defaults = {
        "mono": [
            {"label": "Camada A (única)", "dist": 1.0,
             "comp": {"LDPE":0.36,"LLDPE":0.40,"HDPE":0.03,"ADITIVO 1":0.03,"ADITIVO 2":0.03,
                      "RECICLADO":0.00,"OFF GRADE":0.00,"CARBONATO":0.00,"OTHER":0.15}},
        ],
        "c3": [
            {"label": "Camada A (skin ext)", "dist": 0.2,
             "comp": {"LDPE":0.40,"LLDPE":0.44,"HDPE":0.03,"ADITIVO 1":0.03,"ADITIVO 2":0.03,
                      "RECICLADO":0.00,"OFF GRADE":0.00,"CARBONATO":0.00,"OTHER":0.07}},
            {"label": "Camada B (core)", "dist": 0.6,
             "comp": {"LDPE":0.00,"LLDPE":0.00,"HDPE":0.00,"ADITIVO 1":0.00,"ADITIVO 2":0.00,
                      "RECICLADO":0.40,"OFF GRADE":0.60,"CARBONATO":0.00,"OTHER":0.00}},
            {"label": "Camada A (skin int)", "dist": 0.2,
             "comp": {"LDPE":0.40,"LLDPE":0.44,"HDPE":0.03,"ADITIVO 1":0.03,"ADITIVO 2":0.03,
                      "RECICLADO":0.00,"OFF GRADE":0.00,"CARBONATO":0.00,"OTHER":0.07}},
        ],
        "c5": [
            {"label": "Camada A ext (0.1)", "dist": 0.1,
             "comp": {"LDPE":0.30,"LLDPE":0.54,"HDPE":0.03,"ADITIVO 1":0.03,"ADITIVO 2":0.03,
                      "RECICLADO":0.00,"OFF GRADE":0.00,"CARBONATO":0.00,"OTHER":0.07}},
            {"label": "Camada B ext (0.2)", "dist": 0.2,
             "comp": {"LDPE":0.00,"LLDPE":0.00,"HDPE":0.00,"ADITIVO 1":0.00,"ADITIVO 2":0.00,
                      "RECICLADO":0.25,"OFF GRADE":0.75,"CARBONATO":0.00,"OTHER":0.00}},
            {"label": "Camada C core (0.4)", "dist": 0.4,
             "comp": {"LDPE":0.00,"LLDPE":0.00,"HDPE":0.00,"ADITIVO 1":0.00,"ADITIVO 2":0.00,
                      "RECICLADO":0.25,"OFF GRADE":0.75,"CARBONATO":0.00,"OTHER":0.00}},
            {"label": "Camada B int (0.2)", "dist": 0.2,
             "comp": {"LDPE":0.00,"LLDPE":0.00,"HDPE":0.00,"ADITIVO 1":0.00,"ADITIVO 2":0.00,
                      "RECICLADO":0.25,"OFF GRADE":0.75,"CARBONATO":0.00,"OTHER":0.00}},
            {"label": "Camada A int (0.1)", "dist": 0.1,
             "comp": {"LDPE":0.30,"LLDPE":0.54,"HDPE":0.03,"ADITIVO 1":0.03,"ADITIVO 2":0.03,
                      "RECICLADO":0.00,"OFF GRADE":0.00,"CARBONATO":0.00,"OTHER":0.07}},
        ],
    }

    op_defaults = {
        "mono": {
            "prod_kg_h":400.0,"horas_dia":21.0,"dias_mes":30.0,
            "valor_exw":760000.0,"valor_cif":950000.0,"dep_meses":120.0,
            "n_operarios":1.0,"custo_op_mes":1000.0,"n_turnos":3.0,
            "potencia_kw":250.0,"consumo_pct":45.0,"custo_kwh":0.20,
            "outros_mes":6000.0,
        },
        "c3": {
            "prod_kg_h":500.0,"horas_dia":21.0,"dias_mes":30.0,
            "valor_exw":1200000.0,"valor_cif":1500000.0,"dep_meses":120.0,
            "n_operarios":1.0,"custo_op_mes":1000.0,"n_turnos":3.0,
            "potencia_kw":450.0,"consumo_pct":37.0,"custo_kwh":0.20,
            "outros_mes":6000.0,
        },
        "c5": {
            "prod_kg_h":800.0,"horas_dia":21.0,"dias_mes":30.0,
            "valor_exw":2000000.0,"valor_cif":2500000.0,"dep_meses":120.0,
            "n_operarios":1.0,"custo_op_mes":1000.0,"n_turnos":3.0,
            "potencia_kw":750.0,"consumo_pct":35.0,"custo_kwh":0.20,
            "outros_mes":6000.0,
        },
    }

    # =========================================================
    # ABAS DE EDIÇÃO
    # =========================================================
    st.markdown("### ⚙️ Parâmetros por Máquina")
    tabs = st.tabs([nomes_maq[k] for k in ["mono","c3","c5"]])

    params_op   = {}
    estrut_edit = {}

    for tab, key in zip(tabs, ["mono","c3","c5"]):
        base_op = op_defaults[key]
        with tab:
            st.markdown(f"#### 🏭 {nomes_maq[key]}")
            st.markdown("**Produção e Operação**")
            oc1, oc2, oc3, oc4 = st.columns(4)
            with oc1:
                prod_kg_h  = st.number_input("Produção (kg/h)",            value=base_op["prod_kg_h"],  step=10.0,    key=f"prod_{key}")
                horas_dia  = st.number_input("Horas produtivas/dia",        value=base_op["horas_dia"],  step=1.0,     key=f"hd_{key}")
                dias_mes   = st.number_input("Dias operativos/mês",         value=base_op["dias_mes"],   step=1.0,     key=f"dm_{key}")
            with oc2:
                valor_exw  = st.number_input("Valor EXW (USD)",             value=base_op["valor_exw"],  step=50000.0, key=f"exw_{key}")
                valor_cif  = st.number_input("Valor CIF (USD)",             value=base_op["valor_cif"],  step=50000.0, key=f"cif_{key}")
                dep_meses  = st.number_input("Depreciação (meses)",         value=base_op["dep_meses"],  step=12.0,    key=f"dep_{key}")
            with oc3:
                n_operarios = st.number_input("Nº operários/máquina",      value=base_op["n_operarios"], step=1.0,    key=f"nop_{key}")
                custo_op    = st.number_input("Custo 1 operário/mês (USD)", value=base_op["custo_op_mes"],step=100.0,  key=f"cop_{key}")
                n_turnos    = st.number_input("Nº de turnos",               value=base_op["n_turnos"],   step=1.0,     key=f"ntu_{key}")
            with oc4:
                potencia_kw = st.number_input("Potência instalada (kW)",    value=base_op["potencia_kw"],step=50.0,    key=f"kw_{key}")
                consumo_pct = st.number_input("Consumo elétrico real (%)",  value=base_op["consumo_pct"],step=1.0,     key=f"cee_{key}")
                custo_kwh   = st.number_input("Custo energia (USD/kWh)",    value=base_op["custo_kwh"],  step=0.01,    format="%.3f", key=f"kwh_{key}")
                outros_mes  = st.number_input("Outros indiretos/mês (USD)", value=base_op["outros_mes"], step=500.0,   key=f"ind_{key}")

            params_op[key] = {
                "prod_kg_h": prod_kg_h, "horas_dia": horas_dia, "dias_mes": dias_mes,
                "valor_exw": valor_exw, "valor_cif": valor_cif, "dep_meses": dep_meses,
                "n_operarios": n_operarios, "custo_op_mes": custo_op, "n_turnos": n_turnos,
                "potencia_kw": potencia_kw, "consumo_pct": consumo_pct, "custo_kwh": custo_kwh,
                "outros_mes": outros_mes,
            }

            st.markdown("**Distribuição de Matérias-Primas por Camada**")
            st.caption("Frações decimais (ex: 0.36 = 36%). A soma de cada camada deve ser 1.00.")

            estrut_edit[key] = []
            for i, cam in enumerate(estrutura_defaults[key]):
                with st.expander(f"{cam['label']}  —  participação: {cam['dist']*100:.0f}%"):
                    dist_val = st.number_input(
                        "Participação desta camada (0.0 a 1.0)",
                        value=cam["dist"], step=0.05, format="%.2f",
                        key=f"dist_{key}_{i}_total"
                    )
                    mp_cols = st.columns(len(mp_nomes))
                    comp_edit = {}
                    for mc, mp in zip(mp_cols, mp_nomes):
                        with mc:
                            comp_edit[mp] = st.number_input(
                                mp, value=cam["comp"][mp],
                                step=0.01, format="%.2f",
                                key=f"dist_{key}_{i}_{mp}"
                            )
                    estrut_edit[key].append({"dist": dist_val, "comp": comp_edit})

    # =========================================================
    # CÁLCULOS FIÉIS À PLANILHA
    # =========================================================
    def calc_custo_mp(key):
        total = 0.0
        for cam in estrut_edit[key]:
            custo_cam = sum(cam["comp"][mp] * precos_mp[mp] for mp in mp_nomes)
            total += cam["dist"] * custo_cam
        return total

    def calc_maquina(key):
        p = params_op[key]

        custo_mp_kg = calc_custo_mp(key)

        prod_kg_dia = p["prod_kg_h"] * p["horas_dia"]
        prod_kg_mes = prod_kg_dia * p["dias_mes"]
        prod_kg_ano = prod_kg_mes * 12.0

        dep_mes = p["valor_cif"] / p["dep_meses"] if p["dep_meses"] > 0 else 0.0

        custo_mo_mes = p["n_operarios"] * p["custo_op_mes"] * p["n_turnos"]

        consumo_ef_kw = p["potencia_kw"] * (p["consumo_pct"] / 100.0)
        custo_ee_kg   = (consumo_ef_kw * p["custo_kwh"]) / p["prod_kg_h"] if p["prod_kg_h"] > 0 else 0.0
        custo_ee_mes  = custo_ee_kg * prod_kg_mes

        outros = p["outros_mes"]

        custo_outros_mes = dep_mes + custo_mo_mes + custo_ee_mes + outros
        custo_outros_kg  = custo_outros_mes / prod_kg_mes if prod_kg_mes > 0 else 0.0

        custo_total_kg  = custo_mp_kg + custo_outros_kg
        custo_total_ton = custo_total_kg * 1000.0

        ganho_kg  = preco_venda_kg - custo_total_kg
        ganho_ano = ganho_kg * prod_kg_ano

        ingressos_ano   = preco_venda_kg * prod_kg_ano
        custo_total_ano = custo_total_kg  * prod_kg_ano

        payback_anos = p["valor_cif"] / ganho_ano if ganho_ano > 0 else float("inf")
        frac         = pct_lucro_payback / 100.0
        payback_pct  = p["valor_cif"] / (ganho_ano * frac) if (ganho_ano * frac) > 0 else float("inf")

        return {
            "custo_mp_kg":      custo_mp_kg,
            "prod_kg_dia":      prod_kg_dia,
            "prod_kg_mes":      prod_kg_mes,
            "prod_kg_ano":      prod_kg_ano,
            "dep_mes":          dep_mes,
            "custo_mo_mes":     custo_mo_mes,
            "consumo_ef_kw":    consumo_ef_kw,
            "custo_ee_kg":      custo_ee_kg,
            "custo_ee_mes":     custo_ee_mes,
            "outros_mes":       outros,
            "custo_outros_mes": custo_outros_mes,
            "custo_outros_kg":  custo_outros_kg,
            "custo_total_kg":   custo_total_kg,
            "custo_total_ton":  custo_total_ton,
            "ganho_kg":         ganho_kg,
            "ganho_ano":        ganho_ano,
            "ingressos_ano":    ingressos_ano,
            "custo_total_ano":  custo_total_ano,
            "payback_anos":     payback_anos,
            "payback_pct":      payback_pct,
        }

    resultados = {k: calc_maquina(k) for k in ["mono","c3","c5"]}

      # =========================================================
    # CARDS DE RESUMO – estilo card, mas usando só markdown
    # =========================================================
    st.markdown("---")
    st.markdown("### 📊 Resumo Comparativo")

    card_cols = st.columns(len(keys_vis))
    for col, key in zip(card_cols, keys_vis):
        r   = resultados[key]
        cor = cores_maq[key]
        cor_ganho = "#22c55e" if r["ganho_kg"] > 0 else "#ef4444"

        with col:
            st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #1e293b 0%, #020617 100%);
    border-radius: 12px;
    padding: 16px 18px;
    border-left: 5px solid {cor};
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
    font-size: 13px;">
  <div style="font-weight: 700; font-size: 16px; color: {cor}; margin-bottom: 8px;">
    {nomes_maq[key]}
  </div>

  <div style="color:#94a3b8;">Custo MP/kg</div>
  <div style="color:#e5e7eb; font-weight:600; margin-bottom:4px;">USD {r['custo_mp_kg']:.5f}</div>

  <div style="color:#94a3b8;">Outros custos/kg</div>
  <div style="color:#e5e7eb; font-weight:600; margin-bottom:4px;">USD {r['custo_outros_kg']:.5f}</div>

  <div style="color:#94a3b8;">Custo Total/kg</div>
  <div style="color:{cor}; font-weight:700; font-size:18px; margin-bottom:6px;">USD {r['custo_total_kg']:.5f}</div>

  <div style="color:#94a3b8;">Produção mensal</div>
  <div style="color:#e5e7eb; font-weight:600; margin-bottom:4px;">{r['prod_kg_mes']:,.0f} kg/mês</div>

  <div style="color:#94a3b8;">Ganho/kg</div>
  <div style="color:{cor_ganho}; font-weight:600; margin-bottom:4px;">USD {r['ganho_kg']:.5f}</div>

  <div style="color:#94a3b8;">Ganho/ano</div>
  <div style="color:{cor_ganho}; font-weight:600; margin-bottom:4px;">USD {r['ganho_ano']:,.0f}</div>

  <div style="color:#94a3b8;">Payback (100% lucro)</div>
  <div style="color:#e5e7eb; font-weight:600; margin-bottom:4px;">{r['payback_anos']:.3f} anos</div>

  <div style="color:#94a3b8;">Payback ({pct_lucro_payback:.0f}% lucro)</div>
  <div style="color:{cor}; font-weight:600;">{r['payback_pct']:.3f} anos</div>
</div>
""", unsafe_allow_html=True)
    # =========================================================
    # GRÁFICOS
    # =========================================================
    st.markdown("---")
    st.markdown("### 📈 Gráficos Comparativos")

    nomes_vis = [nomes_maq[k] for k in keys_vis]
    cores_vis = [cores_maq[k] for k in keys_vis]

    # 1) Composição custo/kg empilhado
    st.markdown("#### 1) Composição do Custo Total por kg (USD)")
    st.caption("Quanto é matéria-prima e quanto são outros custos operacionais")
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        name="Matéria-Prima",
        x=nomes_vis,
        y=[resultados[k]["custo_mp_kg"] for k in keys_vis],
        marker_color="#3b82f6",
        text=[f"USD {resultados[k]['custo_mp_kg']:.4f}" for k in keys_vis],
        textposition="inside",
    ))
    fig1.add_trace(go.Bar(
        name="Outros Custos (dep+MO+EE+ind)",
        x=nomes_vis,
        y=[resultados[k]["custo_outros_kg"] for k in keys_vis],
        marker_color="#f59e0b",
        text=[f"USD {resultados[k]['custo_outros_kg']:.4f}" for k in keys_vis],
        textposition="inside",
    ))
    fig1.update_layout(
        barmode="stack",
        paper_bgcolor="#0e1117", plot_bgcolor="#1e2130",
        font_color="white", height=420,
        yaxis=dict(title="USD/kg", gridcolor="#334155"),
        xaxis=dict(gridcolor="#334155"),
        legend=dict(bgcolor="#1e2130", bordercolor="#334155"),
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2) Ganho anual
    st.markdown("#### 2) Ganho Anual por Máquina (USD/ano)")
    st.caption("Quanto cada máquina gera de lucro por ano")
    fig2 = go.Figure()
    for k in keys_vis:
        fig2.add_trace(go.Bar(
            name=nomes_maq[k],
            x=[nomes_maq[k]],
            y=[resultados[k]["ganho_ano"]],
            marker_color=cores_maq[k],
            text=[f"USD {resultados[k]['ganho_ano']:,.0f}"],
            textposition="outside",
        ))
    fig2.update_layout(
        paper_bgcolor="#0e1117", plot_bgcolor="#1e2130",
        font_color="white", height=420,
        yaxis=dict(title="USD/ano", gridcolor="#334155"),
        showlegend=False,
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 3) Payback
    st.markdown("#### 3) Payback – Recuperação do Investimento (anos)")
    st.caption("Quanto menor, melhor. Linha branca = 100% do lucro. Barras = percentual configurado.")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        name=f"Payback ({pct_lucro_payback:.0f}% lucro)",
        x=nomes_vis,
        y=[resultados[k]["payback_pct"] for k in keys_vis],
        marker_color=cores_vis,
        text=[f"{resultados[k]['payback_pct']:.3f} anos" for k in keys_vis],
        textposition="outside",
    ))
    fig3.add_trace(go.Scatter(
        name="Payback (100% lucro)",
        x=nomes_vis,
        y=[resultados[k]["payback_anos"] for k in keys_vis],
        mode="lines+markers+text",
        line=dict(color="white", width=2, dash="dash"),
        marker=dict(size=10, color="white"),
        text=[f"{resultados[k]['payback_anos']:.3f}" for k in keys_vis],
        textposition="top center",
        textfont=dict(color="white"),
    ))
    fig3.update_layout(
        paper_bgcolor="#0e1117", plot_bgcolor="#1e2130",
        font_color="white", height=420,
        yaxis=dict(title="Anos", gridcolor="#334155"),
        legend=dict(bgcolor="#1e2130", bordercolor="#334155"),
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 4) Produção anual
    st.markdown("#### 4) Capacidade de Produção Anual (kg/ano)")
    fig4 = go.Figure()
    for k in keys_vis:
        fig4.add_trace(go.Bar(
            name=nomes_maq[k],
            x=[nomes_maq[k]],
            y=[resultados[k]["prod_kg_ano"]],
            marker_color=cores_maq[k],
            text=[f"{resultados[k]['prod_kg_ano']:,.0f} kg"],
            textposition="outside",
        ))
    fig4.update_layout(
        paper_bgcolor="#0e1117", plot_bgcolor="#1e2130",
        font_color="white", height=420,
        yaxis=dict(title="kg/ano", gridcolor="#334155"),
        showlegend=False,
    )
    st.plotly_chart(fig4, use_container_width=True)

    # 5) Scatter custo x ganho
    st.markdown("#### 5) Custo vs Ganho por kg")
    st.caption("Ideal: menor custo e maior ganho")
    fig5 = go.Figure()
    for k in keys_vis:
        fig5.add_trace(go.Scatter(
            x=[resultados[k]["custo_total_kg"]],
            y=[resultados[k]["ganho_kg"]],
            mode="markers+text",
            name=nomes_maq[k],
            marker=dict(size=35, color=cores_maq[k], opacity=0.85),
            text=[nomes_maq[k]],
            textposition="top center",
        ))
    fig5.update_layout(
        paper_bgcolor="#0e1117", plot_bgcolor="#1e2130",
        font_color="white", height=450,
        xaxis=dict(title="Custo Total (USD/kg)", gridcolor="#334155"),
        yaxis=dict(title="Ganho (USD/kg)", gridcolor="#334155"),
        legend=dict(bgcolor="#1e2130", bordercolor="#334155"),
    )
    st.plotly_chart(fig5, use_container_width=True)

    # 6) Fluxo de caixa acumulado
    st.markdown("#### 6) Fluxo de Caixa Acumulado – 0 a 5 anos")
    st.caption("Inclui investimento inicial (CIF) no Ano 0. Mostra quando cada máquina se paga.")
    anos = list(range(0, 6))
    fig6 = go.Figure()
    fills = {
        "mono": "rgba(59,130,246,0.08)",
        "c3":   "rgba(34,197,94,0.08)",
        "c5":   "rgba(245,158,11,0.08)",
    }
    for k in keys_vis:
        r   = resultados[k]
        cor = cores_maq[k]
        inv = params_op[k]["valor_cif"]
        fluxo = [-inv]
        for _ in range(1, 6):
            fluxo.append(fluxo[-1] + r["ganho_ano"])
        fig6.add_trace(go.Scatter(
            x=anos,
            y=fluxo,
            mode="lines+markers",
            name=nomes_maq[k],
            line=dict(color=cor, width=3),
            marker=dict(size=8),
            fill="tozeroy",
            fillcolor=fills[k],
            hovertemplate=f"<b>{nomes_maq[k]}</b><br>Ano %{{x}}<br>USD %{{y:,.0f}}<extra></extra>",
        ))
    fig6.add_hline(
        y=0, line_dash="dash", line_color="white", opacity=0.4,
        annotation_text="Ponto de equilíbrio",
        annotation_position="bottom right"
    )
    fig6.update_layout(
        paper_bgcolor="#0e1117", plot_bgcolor="#1e2130",
        font_color="white", height=450,
        xaxis=dict(title="Anos", gridcolor="#334155", tickvals=list(range(0, 6))),
        yaxis=dict(title="Fluxo Acumulado (USD)", gridcolor="#334155"),
        legend=dict(bgcolor="#1e2130", bordercolor="#334155"),
        hovermode="x unified",
    )
    st.plotly_chart(fig6, use_container_width=True)

    # =========================================================
    # TABELA DETALHADA
    # =========================================================
    st.markdown("---")
    with st.expander("📋 Tabela Detalhada (conferência com a planilha Excel)"):
        linhas = []
        for key in keys_vis:
            r = resultados[key]
            p = params_op[key]
            linhas.append({
                "Máquina":                     nomes_maq[key],
                "Custo MP/kg (USD)":           r["custo_mp_kg"],
                "Outros custos/kg (USD)":      r["custo_outros_kg"],
                "Custo Total/kg (USD)":        r["custo_total_kg"],
                "Custo Total/ton (USD)":       r["custo_total_ton"],
                "Produção kg/dia":             r["prod_kg_dia"],
                "Produção kg/mês":             r["prod_kg_mes"],
                "Produção kg/ano":             r["prod_kg_ano"],
                "Depreciação/mês (USD)":       r["dep_mes"],
                "MO/mês (USD)":                r["custo_mo_mes"],
                "Energia/kg (USD)":            r["custo_ee_kg"],
                "Energia/mês (USD)":           r["custo_ee_mes"],
                "Outros indiretos/mês (USD)":  r["outros_mes"],
                "Ganho/kg (USD)":              r["ganho_kg"],
                "Ganho/ano (USD)":             r["ganho_ano"],
                "Ingressos/ano (USD)":         r["ingressos_ano"],
                "Custo total/ano (USD)":       r["custo_total_ano"],
                "Payback 100% lucro (anos)":   r["payback_anos"],
                f"Payback {pct_lucro_payback:.0f}% lucro (anos)": r["payback_pct"],
            })
        df_tab = pd.DataFrame(linhas)
        st.dataframe(
            df_tab.style.format({
                "Custo MP/kg (USD)":          "{:.5f}",
                "Outros custos/kg (USD)":     "{:.5f}",
                "Custo Total/kg (USD)":       "{:.5f}",
                "Custo Total/ton (USD)":      "{:.3f}",
                "Produção kg/dia":            "{:,.0f}",
                "Produção kg/mês":            "{:,.0f}",
                "Produção kg/ano":            "{:,.0f}",
                "Depreciação/mês (USD)":      "{:,.3f}",
                "MO/mês (USD)":               "{:,.2f}",
                "Energia/kg (USD)":           "{:.6f}",
                "Energia/mês (USD)":          "{:,.2f}",
                "Outros indiretos/mês (USD)": "{:,.2f}",
                "Ganho/kg (USD)":             "{:.5f}",
                "Ganho/ano (USD)":            "{:,.0f}",
                "Ingressos/ano (USD)":        "{:,.0f}",
                "Custo total/ano (USD)":      "{:,.0f}",
                "Payback 100% lucro (anos)":  "{:.6f}",
            }),
            use_container_width=True,
        )# =====================================================================
# MÓDULO 3 - CONTAS PARA IMPORTAÇÃO (VERSÃO INICIAL)
# =====================================================================
def show_importacao():
    show_top_menu()
    st.title("Contas para Importação de Máquinas")

    st.markdown("""
Preencha os campos abaixo para estimar o **custo total da máquina importada no Brasil**, considerando:
- Preço da máquina em Euro (FOB / EXW)
- Frete + seguro internacional (como % do FOB)
- Alíquota de impostos
- Taxa de câmbio Euro → Real
""")

    st.markdown("### Parâmetros Gerais")

    col1, col2, col3 = st.columns(3)

    with col1:
        fob_eur = st.number_input("Valor da máquina (FOB/EXW) em Euro", value=150_000.0, step=10_000.0, format="%.2f")
        cambio = st.number_input("Câmbio Euro → Real (R$/€)", value=6.0, step=0.1, format="%.3f")

    with col2:
        frete_pct = st.number_input("Frete + seguro (% sobre FOB em R$)", value=5.0, step=0.5, format="%.2f")
        usar_frete_manual = st.checkbox("Informar frete/seguro em R$ manualmente?")
        frete_brl_manual = st.number_input("Frete + seguro (R$)", value=0.0, step=1_000.0, format="%.2f", disabled=not usar_frete_manual)

    with col3:
        st.markdown("#### Alíquotas de Impostos (%)")
        ii_sem_ex = st.number_input("II (Sem Ex-tarifário)", value=14.0, step=0.5, format="%.2f")
        ii_com_ex = st.number_input("II (Com Ex-tarifário)", value=0.0, step=0.5, format="%.2f")
        ipi = st.number_input("IPI", value=0.0, step=0.5, format="%.2f")
        pis = st.number_input("PIS-Importação", value=2.10, step=0.1, format="%.2f")
        cofins = st.number_input("COFINS-Importação", value=10.65, step=0.1, format="%.2f")
        icms = st.number_input("ICMS (por dentro)", value=18.0, step=0.5, format="%.2f")

    # ---------------- Cálculos ----------------
    fob_brl = fob_eur * cambio

    if usar_frete_manual and frete_brl_manual > 0:
        frete_brl = frete_brl_manual
    else:
        frete_brl = fob_brl * (frete_pct / 100.0)

    valor_aduaneiro = fob_brl + frete_brl

    def calcula_cenario(ii_aliquota):
        valor_ii = valor_aduaneiro * (ii_aliquota / 100.0)
        base_ipi = valor_aduaneiro + valor_ii
        valor_ipi = base_ipi * (ipi / 100.0)
        base_pis_cofins = valor_aduaneiro + valor_ii + valor_ipi
        valor_pis = base_pis_cofins * (pis / 100.0)
        valor_cofins = base_pis_cofins * (cofins / 100.0)
        base_icms = valor_aduaneiro + valor_ii + valor_ipi + valor_pis + valor_cofins
        aliquota_icms_frac = icms / 100.0
        valor_icms = base_icms * (aliquota_icms_frac / (1.0 - aliquota_icms_frac))
        custo_com_icms = base_icms + valor_icms
        custo_sem_icms = base_icms
        return {
            "VA": valor_aduaneiro,
            "II": valor_ii,
            "IPI": valor_ipi,
            "PIS": valor_pis,
            "COFINS": valor_cofins,
            "BASE_ICMS": base_icms,
            "ICMS": valor_icms,
            "CUSTO_COM_ICMS": custo_com_icms,
            "CUSTO_SEM_ICMS": custo_sem_icms,
        }

    cen_a = calcula_cenario(ii_sem_ex)
    cen_b = calcula_cenario(ii_com_ex)

    # ---------------- Tabela A ----------------
    st.markdown("---")
    st.markdown("## A) Sem Ex-tarifário (II > 0)")

    col_a1, col_a2 = st.columns([1, 2])
    with col_a1:
        st.markdown("### Dados básicos")
        st.write(f"- FOB (Euro): **€ {fob_eur:,.2f}**")
        st.write(f"- Câmbio: **R$ {cambio:,.3f} / €**")
        st.write(f"- FOB em R$: **R$ {fob_brl:,.2f}**")
        st.write(f"- Frete + seguro (R$): **R$ {frete_brl:,.2f}**")
        st.write(f"- Valor Aduaneiro (VA): **R$ {cen_a['VA']:,.2f}**")

    with col_a2:
        st.markdown("### Impostos")
        st.write(f"- II ({ii_sem_ex:.2f}% sobre VA): **R$ {cen_a['II']:,.2f}**")
        st.write(f"- IPI ({ipi:.2f}%): **R$ {cen_a['IPI']:,.2f}**")
        st.write(f"- PIS ({pis:.2f}%): **R$ {cen_a['PIS']:,.2f}**")
        st.write(f"- COFINS ({cofins:.2f}%): **R$ {cen_a['COFINS']:,.2f}**")
        st.write(f"- Base ICMS (simplificada): **R$ {cen_a['BASE_ICMS']:,.2f}**")
        st.write(f"- ICMS ({icms:.2f}% por dentro): **R$ {cen_a['ICMS']:,.2f}**")
        st.markdown("#### Visões de custo")
        st.write(f"- **Custo total (ICMS como custo):** R$ {cen_a['CUSTO_COM_ICMS']:,.2f}")
        st.write(f"- **Custo efetivo (ICMS recuperável):** R$ {cen_a['CUSTO_SEM_ICMS']:,.2f}")

    # ---------------- Tabela B ----------------
    st.markdown("---")
    st.markdown("## B) Com Ex-tarifário (II = 0%)")

    col_b1, col_b2 = st.columns([1, 2])
    with col_b1:
        st.markdown("### Dados básicos")
        st.write(f"- FOB (Euro): **€ {fob_eur:,.2f}**")
        st.write(f"- Câmbio: **R$ {cambio:,.3f} / €**")
        st.write(f"- FOB em R$: **R$ {fob_brl:,.2f}**")
        st.write(f"- Frete + seguro (R$): **R$ {frete_brl:,.2f}**")
        st.write(f"- Valor Aduaneiro (VA): **R$ {cen_b['VA']:,.2f}**")

    with col_b2:
        st.markdown("### Impostos")
        st.write(f"- II ({ii_com_ex:.2f}% sobre VA): **R$ {cen_b['II']:,.2f}**")
        st.write(f"- IPI ({ipi:.2f}%): **R$ {cen_b['IPI']:,.2f}**")
        st.write(f"- PIS ({pis:.2f}%): **R$ {cen_b['PIS']:,.2f}**")
        st.write(f"- COFINS ({cofins:.2f}%): **R$ {cen_b['COFINS']:,.2f}**")
        st.write(f"- Base ICMS (simplificada): **R$ {cen_b['BASE_ICMS']:,.2f}**")
        st.write(f"- ICMS ({icms:.2f}% por dentro): **R$ {cen_b['ICMS']:,.2f}**")
        st.markdown("#### Visões de custo")
        st.write(f"- **Custo total (ICMS como custo):** R$ {cen_b['CUSTO_COM_ICMS']:,.2f}")
        st.write(f"- **Custo efetivo (ICMS recuperável):** R$ {cen_b['CUSTO_SEM_ICMS']:,.2f}")

    # ---------------- Resumo C ----------------
    st.markdown("---")
    st.markdown("## C) Resumo e Economia com Ex-tarifário")

    resumo = {
        "Cenário": [
            "Sem Ex / ICMS como custo",
            "Sem Ex / ICMS recuperável",
            "Com Ex / ICMS como custo",
            "Com Ex / ICMS recuperável",
        ],
        "Custo (R$)": [
            cen_a["CUSTO_COM_ICMS"],
            cen_a["CUSTO_SEM_ICMS"],
            cen_b["CUSTO_COM_ICMS"],
            cen_b["CUSTO_SEM_ICMS"],
        ],
    }
    df_resumo = pd.DataFrame(resumo)
    st.dataframe(df_resumo.style.format({"Custo (R$)": "R$ {:,.2f}"}), use_container_width=True)

    economia_icms_custo = cen_a["CUSTO_COM_ICMS"] - cen_b["CUSTO_COM_ICMS"]
    economia_icms_rec   = cen_a["CUSTO_SEM_ICMS"] - cen_b["CUSTO_SEM_ICMS"]

    st.markdown("### Economia com Ex-tarifário")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown(f"Se **ICMS é custo**: economia ≈ **R$ {economia_icms_custo:,.2f}**")
    with col_e2:
        st.markdown(f"Se **ICMS é recuperável**: economia ≈ **R$ {economia_icms_rec:,.2f}**")

    st.caption("Obs.: A economia em 'ICMS recuperável' tende a ser igual ao próprio II que deixou de ser pago.")
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
