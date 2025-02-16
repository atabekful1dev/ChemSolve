import streamlit as st

# Если переменная для авторизации отсутствует, инициализируем её
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Если пользователь еще не авторизован – показываем страницу входа
if not st.session_state.authenticated:
    st.title("ChemSolve - химиялық есептерді тез әрі тиімді шешуге арналған онлайн платформа! ")
    st.write("Платформаны қолдану үшін Админге хабарласыңыз және тарифті сатып алыңыз!")
    st.markdown("[Админмен байланысу](https://wa.me/77783819882?text=%D0%A1%D3%99%D0%BB%D0%B5%D0%BC!%20%F0%9F%91%8B%20ChemSolve%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%81%D1%8B%D0%BD%D1%8B%D2%A3%20%D1%82%D0%B0%D1%80%D0%B8%D1%84%D1%96%D0%BD%20%D1%81%D0%B0%D1%82%D1%8B%D0%BF%20%D0%B0%D0%BB%D1%83%20%D0%B1%D0%BE%D0%B9%D1%8B%D0%BD%D1%88%D0%B0%20%D1%85%D0%B0%D0%B1%D0%B0%D1%80%D0%BB%D0%B0%D1%81%D1%8B%D0%BF%20%D1%82%D2%B1%D1%80%D0%BC%D1%8B%D0%BD!)")  # Замените ссылку на реальную, если необходимо.
    st.write("Админнен сатып алған кодты енгізіңіз!")
    
    access_code = st.text_input("Код:")
    
    if st.button("Тіркелу"):
        if access_code == "ChemSolVe123":
            st.session_state.authenticated = True
            st.success("Код дұрыс ✅ Платформаға қош келдіңіз! ")
        else:
            st.error("Кодты қате енгіздіңіз немесе сатып алмадыңыз!")

# Если пользователь авторизован – показываем основное приложение
if st.session_state.authenticated:
    st.title("Химиялық есептерді шешу")
    st.write("Төмендегі батырманы басыңыз 'Тіктөртбұрыштар әдісіне есеп шығару'.")

    if "show_calculator" not in st.session_state:
        st.session_state.show_calculator = False

    if st.button("Тіктөртбұрыштар әдісіне есеп шығару"):
        st.session_state.show_calculator = True

    if st.session_state.show_calculator:
        st.subheader("4 элементті енгізіңіз 1 ұяшық бос болуы міндетті!")
        
        with st.form("calculation_form"):
            m1_str = st.text_input("m₁ (1-ші компонеттің массасы)", key="m1")
            w1_str = st.text_input("ω₁ (1-ші компонеттің қалдығы)", key="w1")
            m2_str = st.text_input("m₂ (2-ші компонеттің массасы)", key="m2")
            w2_str = st.text_input("ω₂ (2-ші компонеттің қалдығы)", key="w2")
            mw_str = st.text_input("mω (Салмақтық орташа үлес)", key="mw")
            
            submitted = st.form_submit_button("Есепті шешу")
            
            if submitted:
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
                    st.error("Өтініш, тек 4 ұяшықты толтырыңыз, 1 ұяшық бос болуы керек")
                else:
                    missing_field = missing[0]
                    
                    try:
                        # Преобразуем введённые значения в float для заполненных полей
                        values = {key: float(value) for key, value in inputs.items() if key != missing_field}
                    except ValueError:
                        st.error("Өтініш, Дұрыс санды енгізіңіз")
                        st.stop()
                    
                    try:
                        # Вычисляем недостающее значение в зависимости от того, какое поле отсутствует
                        if missing_field == "mw":
                            m1 = values["m1"]
                            w1 = values["w1"]
                            m2 = values["m2"]
                            w2 = values["w2"]
                            if m1 + m2 == 0:
                                raise ZeroDivisionError("Массалар суммасы 0 ге тең")
                            result = (m1 * w1 + m2 * w2) / (m1 + m2)
                        elif missing_field == "m1":
                            m2 = values["m2"]
                            w2 = values["w2"]
                            mw = values["mw"]
                            w1 = values["w1"]
                            denominator = mw - w1
                            if denominator == 0:
                                raise ZeroDivisionError("m₁ есептеу барысында 0 ге бөлініп қалды")
                            result = m2 * (w2 - mw) / denominator
                        elif missing_field == "m2":
                            m1 = values["m1"]
                            w1 = values["w1"]
                            mw = values["mw"]
                            w2 = values["w2"]
                            denominator = mw - w2
                            if denominator == 0:
                                raise ZeroDivisionError("m₂ есептеу барысында 0 ге бөлініп қалды")
                            result = m1 * (w1 - mw) / denominator
                        elif missing_field == "w1":
                            m1 = values["m1"]
                            m2 = values["m2"]
                            w2 = values["w2"]
                            mw = values["mw"]
                            if m1 == 0:
                                raise ZeroDivisionError("m₁ 0 ге тең")
                            result = (mw * (m1 + m2) - m2 * w2) / m1
                        elif missing_field == "w2":
                            m2 = values["m2"]
                            m1 = values["m1"]
                            w1 = values["w1"]
                            mw = values["mw"]
                            if m2 == 0:
                                raise ZeroDivisionError("m₂ 0 ге тең")
                            result = (mw * (m1 + m2) - m1 * w1) / m2
                        
                        st.success(f"Есептің жауабы {missing_field}: {result:.2f}")
                    except ZeroDivisionError as e:
                        st.error(f"Қате орын алды: {e}")
                    except Exception as e:
                        st.error(f"Қате орын алды: {e}")
