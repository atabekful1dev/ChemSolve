import streamlit as st

st.title("Решение химических задач")
st.write("Нажмите кнопку ниже для расчёта методом 'Тіктөртбұрыштар әдісіне есеп шығару'.")

# Кнопка для отображения формы расчёта
if st.button("Тіктөртбұрыштар әдісіне есеп шығару"):
    st.subheader("Введите 4 значения из 5 (оставьте одно поле пустым)")

    # Поля ввода в виде текстовых полей, чтобы можно было оставить пустым
    m1_str = st.text_input("m1 (масса первого компонента)", key="m1")
    w1_str = st.text_input("w1 (доля первого компонента)", key="w1")
    m2_str = st.text_input("m2 (масса второго компонента)", key="m2")
    w2_str = st.text_input("w2 (доля второго компонента)", key="w2")
    mw_str = st.text_input("mw (средневзвешенная доля)", key="mw")

    if st.button("РЕШИТЬ"):
        # Собираем значения в словарь
        inputs = {
            "m1": m1_str,
            "w1": w1_str,
            "m2": m2_str,
            "w2": w2_str,
            "mw": mw_str
        }

        # Определяем, какое поле осталось пустым
        missing = [key for key, value in inputs.items() if value.strip() == ""]
        if len(missing) != 1:
            st.error("Пожалуйста, заполните ровно четыре поля, оставив одно пустым.")
        else:
            missing_field = missing[0]

            # Преобразуем введённые значения в float для остальных полей
            try:
                values = {key: float(value) for key, value in inputs.items() if key != missing_field}
            except ValueError:
                st.error("Пожалуйста, введите корректные числовые значения.")
                st.stop()

            try:
                # В зависимости от того, какое значение отсутствует, вычисляем его
                if missing_field == "mw":
                    # Формула: mw = (m1*w1 + m2*w2) / (m1 + m2)
                    m1 = values["m1"]
                    w1 = values["w1"]
                    m2 = values["m2"]
                    w2 = values["w2"]
                    if m1 + m2 == 0:
                        raise ZeroDivisionError("Сумма масс равна 0.")
                    result = (m1 * w1 + m2 * w2) / (m1 + m2)
                elif missing_field == "m1":
                    # Вычисление m1:
                    # Исходное уравнение: mw*(m1+m2) = m1*w1 + m2*w2
                    # Выразим m1: m1 = m2*(w2 - mw) / (mw - w1)
                    m2 = values["m2"]
                    w2 = values["w2"]
                    mw = values["mw"]
                    w1 = values["w1"]
                    denominator = mw - w1
                    if denominator == 0:
                        raise ZeroDivisionError("Деление на ноль при вычислении m1.")
                    result = m2 * (w2 - mw) / denominator
                elif missing_field == "m2":
                    # Вычисление m2:
                    # m2 = m1*(w1 - mw) / (mw - w2)
                    m1 = values["m1"]
                    w1 = values["w1"]
                    mw = values["mw"]
                    w2 = values["w2"]
                    denominator = mw - w2
                    if denominator == 0:
                        raise ZeroDivisionError("Деление на ноль при вычислении m2.")
                    result = m1 * (w1 - mw) / denominator
                elif missing_field == "w1":
                    # Вычисление w1:
                    # w1 = (mw*(m1+m2) - m2*w2) / m1
                    m1 = values["m1"]
                    m2 = values["m2"]
                    w2 = values["w2"]
                    mw = values["mw"]
                    if m1 == 0:
                        raise ZeroDivisionError("m1 равна 0.")
                    result = (mw * (m1 + m2) - m2 * w2) / m1
                elif missing_field == "w2":
                    # Вычисление w2:
                    # w2 = (mw*(m1+m2) - m1*w1) / m2
                    m2 = values["m2"]
                    m1 = values["m1"]
                    w1 = values["w1"]
                    mw = values["mw"]
                    if m2 == 0:
                        raise ZeroDivisionError("m2 равна 0.")
                    result = (mw * (m1 + m2) - m1 * w1) / m2

                st.success(f"Вычисленное значение для {missing_field}: {result:.2f}")
            except ZeroDivisionError as e:
                st.error(f"Ошибка вычисления: {e}")
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")
