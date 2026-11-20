from check_one import *
import streamlit as st

# 1. Настройка страницы
st.set_page_config(page_title="Расчет параметров линии", layout="wide")

# 2. Кастомные стили (CSS)
st.markdown(
    """
<style>
    .result-card {
        background-color: #1f242d;
        border-radius: 12px;
        padding: 24px;
        color: #e0e6ed;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .status-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 14px;
        color: #ffffff;
        margin-bottom: 16px;
    }
    .main-res {
        color: #f1c40f;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 12px;
    }
    .details-text {
        font-size: 16px;
        line-height: 1.5;
        color: #cfd8dc;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Панель управления и расчета")
st.write("---")

col_left, col_right = st.columns([1, 1], gap="large")

# --- ЛЕВАЯ ПОЛОВИНА: Ползунки и кнопка ---
with col_left:
    st.subheader("Параметры системы")

    # Ползунок 1: Длина/высота трубки
    val1 = st.slider(
        "Высота (длина) трубки",
        min_value=1,
        max_value=50,
        value=25,
        format="%d мм",
    )
    st.caption(f"Высота трубки: **{val1} мм**")

    # Ползунок 2: Диаметр трубки
    val2 = st.slider(
        "Диаметр трубки", min_value=1, max_value=50, value=25, format="%d мм"
    )
    st.caption(f"Диаметр трубки: **{val2} мм**")

    # Ползунок 3: Высота колонны
    val3 = st.slider(
        "Высота колонны", min_value=1, max_value=50, value=5, format="%d м"
    )
    st.caption(f"Высота колонны: **{val3} м**")

    # Дополнительный ползунок расхода (нужен для pressure_check)
    flow_ls = st.slider(
        "Расход жидкости",
        min_value=0.05,
        max_value=2.0,
        value=0.2,
        step=0.05,
        format="%.2f л/с",
    )
    st.caption(f"Расход: **{flow_ls:.2f} л/с**")

    st.write("")
    calc_clicked = st.button(
        "Рассчитать", type="primary", use_container_width=True
    )

# --- ПРАВАЯ ПОЛОВИНА: Окно вывода результата ---
with col_right:
    st.subheader("Результат")

    # Перевод единиц измерения для физики (в СИ)
    tube_len_m = val1 / 1000.0  # мм -> м
    diam_m = val2 / 1000.0  # мм -> м
    height_m = float(val3)  # уже в м
    flow_m3s = flow_ls / 1000.0  # л/с -> м³/с

    # Расчет объема первого брака (в литрах)
    # Объем цилиндра = S * L (в м³), умножаем на 1000 для перевода в литры
    brack_volume = round(count_area(diam_m) * (tube_len_m + height_m) * 1000, 3)

    if not calc_clicked:
        badge_color = "#546e7a"
        badge_text = "ОЖИДАНИЕ РАСЧЕТА"
        main_title = "Задайте параметры слева"
        details = "Нажмите кнопку «Рассчитать» для проверки системы и расчета первого брака."
    else:
        # Вызов функции из check_one.py (общая длина L = высота колонны + трубка)
        is_pushable, p_out_bar = pressure_check(
            diam=diam_m,
            height=height_m,
            L=height_m + tube_len_m,
            Q=flow_m3s,
            using=0,
        )

        # Логика светофора по остаточному давлению на выходе
        if is_pushable and p_out_bar >= 0.3:
            badge_color = "#2e7d32"  # Зеленый
            badge_text = "ЗЕЛЕНЫЙ — ПАРАМЕТРЫ В НОРМЕ"
            main_title = "Насыщение газом: 96% — ГОДИТСЯ"
            details = (
                f"Остаточное давление в норме: <b>{p_out_bar} бар</b> (запас достаточный)<br>"
                f"Первый брак: <b>{brack_volume} литра</b> (слить перед пуском)"
            )
        elif is_pushable and p_out_bar > 0:
            badge_color = "#f57f17"  # Желтый
            badge_text = "ЖЕЛТЫЙ — ЕСТЬ РИСК"
            main_title = "Насыщение газом: 78% — ДОПУСТИМО"
            details = (
                f"Низкое остаточное давление: <b>{p_out_bar} бар</b>. Насос работает на пределе.<br>"
                f"Первый брак: <b>{brack_volume} литра</b> (слить в канализацию)."
            )
        else:
            badge_color = "#c62828"  # Красный
            badge_text = "КРАСНЫЙ — СИСТЕМА НЕРАБОТОСПОСОБНА"
            main_title = "Насос не продавит систему"
            details = (
                f"Дефицит давления: <b>{p_out_bar} бар</b>.<br>"
                "Рекомендация: уменьшите высоту колонны или увеличьте диаметр трубки."
            )

    # Отрисовка карточки результата
    st.markdown(
        f"""
    <div class="result-card">
        <div class="status-badge" style="background-color: {badge_color};">
            {badge_text}
        </div>
        <div class="main-res">{main_title}</div>
        <div class="details-text">{details}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

