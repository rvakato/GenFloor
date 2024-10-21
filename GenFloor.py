import streamlit as st
import json
import base64

st.title('Floor Height JSON Generator')

initial_height = st.number_input('Initial Floor Height', value=3010.0, step=0.1)

if 'number_of_rows' not in st.session_state:
    st.session_state.number_of_rows = 3

floor_data = []

for i in range(st.session_state.number_of_rows):
    col1, col2, col3 = st.columns(3)
    with col1:
        floor_range = st.text_input(f'Floor Range #{i + 1}', key=f'floor_range_{i}', placeholder='e.g., 0-3 or 6')
    with col2:
        floor_height = st.text_input(f'Floor Height #{i + 1}', key=f'floor_height_{i}', placeholder='e.g., 330.5')
    with col3:
        floor_type = st.text_input(f'Floor Type #{i + 1}', key=f'floor_type_{i}', placeholder='e.g., A_Floor_3')

    if floor_range and floor_height and floor_type:
        floor_data.append((floor_range, floor_height, floor_type))

col1, col2, _, _, _ = st.columns(5)

with col1:
    if st.button('Add Floors'):
        st.session_state.number_of_rows = min(st.session_state.number_of_rows + 1, 30)
        st.rerun()

with col2:
    if st.button('Remove Floors'):
        st.session_state.number_of_rows = max(st.session_state.number_of_rows - 1, 1)
        st.rerun()

if st.button('Generate JSON', help='Click to generate JSON', type='primary'):
    json_output = []
    current_height = initial_height

    for floor_range, floor_height, floor_type in floor_data:
        try:
            floor_height = float(floor_height)
            if '-' in floor_range:
                start, end = map(int, floor_range.split('-'))
                floor_list = list(range(start, end + 1))
            else:
                floor_list = [int(floor_range)]

            for floor in floor_list:
                json_output.append({
                    'Floor': floor,
                    'Height': current_height,
                    'FloorType': floor_type
                })
                current_height += floor_height
        except ValueError:
            st.error(f'Invalid input for floor range or height: {floor_range}, {floor_height}')

    st.json(json_output)
    json_string = json.dumps({'FloorPlan': json_output}, indent=2)
    b64 = base64.b64encode(json_string.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="floor_plan.json">Download JSON File</a>'
    st.markdown(href, unsafe_allow_html=True)
