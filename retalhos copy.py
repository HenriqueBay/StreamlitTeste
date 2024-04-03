# Definindo a visibilidade e desabilitação dos elementos
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

container = st.container()


# Incluindo  o CSS
with open("main.css") as f:
    st.write(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Seleção dentro do container


@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i: i + rows - 1, :]
          for i in range(0, len(input_df), rows)]
    return df


dataset = pd.read_csv(os.path.join('customer.csv'))
# extract unique list for below
Customer = dataset['year'].to_list()
Customer = list(set(Customer))
Product = dataset['discipline'].to_list()
Product = list(set(Product))
top_menu = st.columns(2)
with top_menu[0]:
    Category = st.selectbox('Select Category', ["year", "discipline"])
    with top_menu[1]:
        if Category == "year":
            Subcategory = st.selectbox('Select year', Customer)
        elif Category == "discipline":
            Subcategory = st.selectbox('Select discipline', Product)
        result = dataset[dataset[Category] == Subcategory]
        dataset = result.sort_values(
            by=Category, ignore_index=True
        )
pagination = st.container()
bottom_menu = st.columns((4, 1, 1))
with bottom_menu[2]:
    batch_size = st.selectbox("Page Size", options=[25, 50, 100])
with bottom_menu[1]:
    total_pages = (
        int(len(result) / batch_size) if int(len(result) / batch_size) > 0 else 1
    )
    current_page = st.number_input(
        "Page", min_value=1, max_value=total_pages, step=1
    )
with bottom_menu[0]:
    st.markdown(f"Page **{current_page}** of **{total_pages}** ")

pages = split_frame(result, batch_size)
pagination.dataframe(data=pages[current_page - 1], use_container_width=True)

# Fechando a tag div do container
container.markdown("</div>", unsafe_allow_html=True)
container.markdown("<hr>", unsafe_allow_html=True)


def my_function():
    st.write("")


button = st.button("Salvar", on_click=my_function)

if button:
    st.write("Os dados foram salvos")
st.page_link("pages\info.py", label="Informações")


# Create a dictionary of data
data = {'Name': ['A', 'A', 'B', 'B', 'C', 'C', 'C', 'D', 'D', 'D'],
        'Color': ['Cerrados Oeste', 'blue', 'black', 'blue', 'green', 'black', 'blue', 'green', 'yellow', 'white']}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Create an empty DataFrame to store filtered data
df_filtered = pd.DataFrame()

# Initialize the name_select variable
name_select = None

# Get a list of unique color options from the original DataFrame
color_options = df['Color'].unique()

# Create a multi-select widget to select colors
color_select = st.multiselect("Select Color", color_options, key="color")

# Create a flag to track if the color select has been changed
color_select_changed = False

# If the user selects one or more colors:
if color_select:
    # Set the flag to indicate the color select has been changed
    color_select_changed = True

    # Filter the original DataFrame to only include rows with the selected colors
    df_filtered = df[df['Color'].isin(color_select)]

    # Get a list of unique name options from the filtered DataFrame
    name_options = df_filtered['Name'].unique()

    # Create a multi-select widget to select names
    name_select = st.multiselect("Select Name", name_options, key="name")

# If the user selects one or more names, but the color select has not been changed:
if name_select and not color_select_changed:
    # Filter the original DataFrame to only include rows with the selected names
    df_filtered = df[df['Name'].isin(name_select)]

    # Get a list of unique color options from the filtered DataFrame
    color_options = df_filtered['Color'].unique()

    # Create a multi-select widget to select colors
    color_select = st.multiselect("Select Color", color_options, key="color")

# If the filtered DataFrame is not empty, display it
if not df_filtered.empty:
    st.write(df_filtered)

