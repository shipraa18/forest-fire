import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score
from sklearn.svm import SVC
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
from plotly.offline import iplot
import plotly as py
import plotly.tools as tls
import cufflinks as cf
import plotly.figure_factory as ff
import plotly.express as px
import streamlit.components.v1 as components

py.offline.init_notebook_mode(connected = True)
cf.go_offline()
cf.set_config_file(theme='white')

# Load SVM model from pickle file
with open("svm_model_new.pkl", "rb") as model_file:
    svc_model = pickle.load(model_file)

df = pd.read_csv("forestfires.csv")

def welcome():

    return "Welcome All"








def main_prediction():
    html_temp = """
    <div style="background-color:#00b3ff;padding:10px">
    <h2 style="color:white;text-align:center;">Forest Fire Prediction</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    st.markdown("""<br>""", unsafe_allow_html=True)
    ffmc = st.text_input("FFMC", "91.7")
    dmc = st.text_input("DMC", "26.2")
    dc = st.text_input("DC", "77.5")
    isi = st.text_input("ISI", "12.3")
    temp = st.text_input("Temp", "14.6")
    rh = st.text_input("RH", "30")
    wind = st.text_input("Wind", "5.4")
    rain = st.text_input("Rain", "0.8")

    result = ""
    if st.button("Predict"):
        try:
            result = predict_forest_fire(ffmc, dmc, dc, isi, temp, rh, wind, rain)
            st.success('{}'.format(result))
            if result == "Your forest is Safe":
                st.balloons()

        except:
            st.error("Please fill up all the inputs and make sure all are in numeric form")

def predict_forest_fire(ffmc, dmc, dc, isi, temp, rh, wind, rain):
    try:
        # Use the loaded SVM model to make predictions
        prediction = svc_model.predict([[ffmc, dmc, dc, isi, temp, rh, wind, rain]])
        
        if prediction[0] == 0:
            return "Your forest is Safe"
        elif prediction[0] == 1:
            return "Your forest is in danger"
        else:
            return "Invalid prediction value"

    except Exception as e:
        return f"An error occurred: {str(e)}"







def corr_plot():
    # st.write("You selected",len(location),"locations")
    
    # st.text("see plots")
    # df = pd.read_csv("forestfires.csv")
    # st.dataframe(df)
    
    corr = df.corr()

    mask = np.triu(np.ones_like(corr, dtype=np.bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(5, 5))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.title('Correlation Plot',size=15)

    st.pyplot(f)

@st.cache(suppress_st_warning=True)
def pair_plot():
    # df = pd.read_csv("forestfires.csv")

    # fig = plt.figure(figsize=(3,4))
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # fig = plt.figure()
    # sns.set_style('whitegrid')
    sns.pairplot(df)
    plt.title("Pair Plot")
    # plt.show()
    st.pyplot()


def V_corr_plot():
    # df = pd.read_csv("forestfires.csv")
    corr_new_train=df.corr()
    fig = plt.figure(figsize=(3,4))
    sns.heatmap(corr_new_train[['area']].sort_values(by=['area'],ascending=False).head(60),vmin=-1, cmap='seismic', annot=True)
    plt.title("Vertical Correlation plot")
    st.pyplot(fig)   

def threeD_Plot():
    # df = pd.read_csv("forestfires.csv")
    dmc = list(df['DMC'])
    temp = list(df['temp'])
    area = list(df['area'])
    train_f1 = pd.DataFrame(dmc,columns=['Dmc'])
    train_f2 = pd.DataFrame(temp,columns=['Temp'])
    train_target = pd.DataFrame(area,columns=['Target'])
    train_data = pd.concat([train_f1,train_f2,train_target],axis = 1)
    # train_data.head(5)
    sns.set_style("whitegrid", {'axes.grid' : False})

    fig = plt.figure(figsize=(3,3))

    ax = Axes3D(fig) # Method 1
    # ax = fig.add_subplot(111, projection='3d') # Method 2

    x = np.random.uniform(1,20,size=20)
    y = np.random.uniform(1,100,size=20)
    z = np.random.uniform(1,100,size=20)


    ax.scatter(train_data['Dmc'], train_data['Temp'], train_data['Target'], c=train_data['Dmc'],marker='o')
    ax.set_xlabel('Dmc')
    ax.set_ylabel('Temp')
    ax.set_zlabel('Target')
    ax.set_title("3D Scatter plot of DMC,temp and area")

    # plt.show()
    st.pyplot(fig)

def get_pie_plot(feature):
  df['area'] = df['area'].apply(lambda x : np.log(x+1))
  df1 = df.groupby(feature).sum()  
  df1 = df1[df1.area >0 ]

  theme = plt.get_cmap('hsv')
  cs = theme(np.arange(len(df1.area))/len(df1.area))
  fig, ax = plt.subplots(figsize = (3, 3))
  plt.pie(df1.area,labels = df1.index, colors = cs)
  plt.title("Relative amount of area affected per "+feature, fontsize = 14)
  # plt.show()
  st.pyplot(fig)

def load_img(img_name):
    img = Image.open(img_name)
    st.image(img,width=800)


# html_img = """<center><img src="logo_jnu.png"></center>"""
# st.sidebar.markdown(html_img,unsafe_allow_html=True)

st.sidebar.markdown("""## Navigation Bar: <br> """,unsafe_allow_html=True)
st.markdown("""<br><br>""",unsafe_allow_html=True)
red = st.sidebar.radio(" ",["Prediction","Exploratory Data Analysis","Collaborators of the Project"])
# st.markdown("""<br></br> <br>""",unsafe_allow_html=True)
st.sidebar.markdown("""<br><br><br><br><br> Thank you for visiting the site🤗""",unsafe_allow_html=True)
st.sidebar.markdown(""" [  My Github Repository](https://github.com/sarthak98765)""",unsafe_allow_html=True)



if red == "Prediction":
    with open("svm_model_new.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    main_prediction()

if red == "Exploratory Data Analysis":
    
    html_header = """
    <div style="background-color:#00ff2a;padding:10px">
    <h2 style="color:white;text-align:center;">Exploratory Data Analysis</h2>
    </div>
    """
    st.markdown(html_header,unsafe_allow_html=True)
    st.markdown("""<br>""",unsafe_allow_html=True)
    tab = st.checkbox("Check out Data")
    if tab:
        st.dataframe(df)
        
    st.subheader("Select an Analysis Type")
    red2 = st.radio(" ",["Uni-variate Analysis","Bi-variate Analysis","Multi-variate Analysis"])
    
    if red2 == "Multi-variate Analysis":
    

        # MultiSelect
        plot_type = st.selectbox("Choose a plot type",["Correlational plot","Pair Plot","Vertical Correlation Plot","3D Plot"])
        
        if plot_type=="Correlational plot":
            corr_plot()
        
        
        if plot_type == "Pair Plot":
            pair_plot()
            
        if plot_type == "Vertical Correlation Plot":
            V_corr_plot()
            
        if plot_type == "3D Plot":
            threeD_Plot()
                
    if red2 == "Bi-variate Analysis":
        
        plot_type1 = st.selectbox("Choose a plot type",["Pie plot of amount of area affected per month","Pie Plot of amount of area affected per day","Box Plot for affected forest area per month","Box Plot for affected forest area per day","Plot for impact of FFMC on Forest Fire","Plot for impact of DMC on Forest Fire","Plot for impact of DC on Forest Fire","Plot for impact of ISI on Forest Fire","Plot for impact of Temperature on Forest Fire","Plot for impact of RH on Forest Fire","Plot for impact of Wind on Forest Fire","Plot for impact of Rain on Forest Fire"])
        if plot_type1=="Pie plot of amount of area affected per month":
            get_pie_plot("month")
        
        if plot_type1=="Pie Plot of amount of area affected per day":
            get_pie_plot("day")
            
        if plot_type1 == "Box Plot for affected forest area per month":
            html_temp = """<center><img src="https://i.imgur.com/Gd26hjy.png" width="700px"></center>"""
            st.markdown(html_temp,unsafe_allow_html=True)
            
        if plot_type1=="Box Plot for affected forest area per day":
            html_temp = """<center><img src="https://i.imgur.com/Uf2avSv.png" width="700px"></center>"""
            st.markdown(html_temp,unsafe_allow_html=True)
            
        if plot_type1=="Plot for impact of FFMC on Forest Fire":
            # load_img("impact1.png")
            html_temp = """<center><img src="https://i.imgur.com/v1mEJxr.png" width="850px"></center>"""
            st.markdown(html_temp,unsafe_allow_html=True)
            
        if plot_type1=="Plot for impact of DMC on Forest Fire":
            # load_img("impact2.png")
            html_temp = """<center><img src="https://i.imgur.com/rQS688N.png" width="850px"></center>"""
            st.markdown(html_temp,unsafe_allow_html=True)
            
        if plot_type1=="Plot for impact of DC on Forest Fire":
            # load_img("impact3.png")
            html_temp = """<center><img src="https://i.imgur.com/D7iLsh9.png" width="850px"></center>"""
            st.markdown(html_temp,unsafe_allow_html=True)
            
        if plot_type1=="Plot for impact of ISI on Forest Fire":
            # load_img("impact4.png")
            html_temp = """<center><img src="https://i.imgur.com/9elPIJQ.png" width="850px"></center>"""
            st.markdown(html_temp,unsafe_allow_html=True)
            
        if plot_type1=="Plot for impact of Temperature on Forest Fire":
            # load_img("impact5.png")
            html_temp = """<center><img src="https://i.imgur.com/Y32p4bE.png" width="850px"></center>"""
            st.markdown(html_temp,unsafe_allow_html=True)
        
        if plot_type1=="Plot for impact of RH on Forest Fire":
            # load_img("impact6.png")
            html_temp = """<center><img src="https://i.imgur.com/nKXQT3z.png" width="850px"></center>"""
            st.markdown(html_temp,unsafe_allow_html=True)
        if plot_type1=="Plot for impact of Wind on Forest Fire":
            # load_img("impact7.png")
            html_temp = """<center><img src="https://i.imgur.com/Uzl040u.png" width="850px"></center>"""
            st.markdown(html_temp,unsafe_allow_html=True)
            
            
        if plot_type1=="Plot for impact of Rain on Forest Fire":
            # load_img("impact7.png")
            html_temp = """<center><img src="https://i.imgur.com/QPOBOVU.png" width="850px"></center>"""
            st.markdown(html_temp,unsafe_allow_html=True)
            
    if red2 == "Uni-variate Analysis":
        
        plot_type2 = st.selectbox("Choose a plot type",["Scatter Plot of Area",
                                    "Line plot of Area",
                                    "Density(PDF) Plot of Area",
                                    "Histogram of Area",
                                    "Violin Plot of Area"])

        if plot_type2=="Scatter Plot of Area":
            fig = df['area'].iplot(kind = 'scatter' , mode = 'markers',title="Scatter plot of area",
                            yTitle='area',xTitle = 'id',asFigure=True)

            st.plotly_chart(fig)
            
        if plot_type2=="Line plot of Area":
            fig = df['area'].iplot(title="Line plot of area",
                            yTitle='area',xTitle = 'id',asFigure=True)
                            
            st.plotly_chart(fig)
            
        if plot_type2=="Density(PDF) Plot of Area":
            np.random.seed(1)


            x = np.array(df['area'])
            hist_data = [x]
            group_labels = ['area'] 

            fig = ff.create_distplot(hist_data, group_labels)
            st.plotly_chart(fig)
            
            
        if plot_type2=="Histogram of Area":
            fig = pd.DataFrame(df["area"]).iplot(kind="histogram", 
                bins=40, 
                theme="white",
                title="Histogram of area",
                xTitle='area', 
                yTitle='Count',
                asFigure=True)
            
            st.plotly_chart(fig)
            
        if plot_type2=="Violin Plot of Area":
            fig = px.violin(df, y="area", box=True, 
                points='all'
               )
               
            st.plotly_chart(fig)
            
            
if red == "Collaborators of the Project":
    components.html(
        """
        <div style="background-color:#ffe100;padding:10px">
        <h1 style="color:white;text-align:center;">Collaborators:</h1>
        </div>
        <br>
        <br>
        """
    )

    components.html(
        """
        <html>
            <head>

            </head>

            <body>
                <a>
                    <strong style="font-size:20px">
                        <pre class="tab">Sarthak Aggarwal <a style="font-size:14px">X commits </a><a style="color: #2bff00;font-size:10px">X++ </a><a style="color: #FF0000;font-size:10px">X--</a></pre>
                        <div class="github-card" data-github="sarthak98765" data-width="350" data-height="150" data-theme="default"></div>
                        <script src="//cdn.jsdelivr.net/github-cards/latest/widget.js"></script>
                    </strong> 
                    <br>
                    <strong style="font-size:20px">
                        <pre class="tab">Khushi <a style="font-size:14px">Y commits </a><a style="color: #2bff00;font-size:10px">Y++ </a><a style="color: #FF0000;font-size:10px">Y--</a></pre>
                        <div class="github-card" data-github="Khushi-star773" data-width="350" data-height="" data-theme="default"></div>
                        <script src="//cdn.jsdelivr.net/github-cards/latest/widget.js"></script>
                    </strong>
                </a>
            </body>
        </html>
        """,
        height=700, scrolling=True, width=800
    )
    
