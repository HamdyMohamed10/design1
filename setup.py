from bokeh.layouts import row,column
from bokeh.models.layouts import Row
from bokeh.models.widgets.buttons import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, output_file, show, Column,curdoc
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource,CDSView, IndexFilter,Dropdown,Select
from math import *
from scipy.signal import freqz
import numpy as np
from scipy.signal import zpk2ss, ss2zpk, tf2zpk, zpk2tf
from cmath import *
from bokeh.models.widgets import RadioButtonGroup
from bokeh.events import DoubleTap, Tap,Press,PanEnd,Pan,SelectionGeometry

""" To Run the file ( python -m bokeh serve --show testt.py) in the terminal   """
x_co = [-3.14,3.14]
y_co = [0,0]
x_co_1=[0,0]
y_co_1=[-10,10]
s1 = figure(plot_width=300, plot_height=300,x_range=(-3, 2), y_range=(-2, 2),toolbar_location="below",title="zPolar")
s1.circle(x=[0], y=[0], color="grey",
              radius=1,alpha=0.3 )
s2 = figure(plot_width=300, plot_height=300,x_range=(-3, 2), y_range=(-2, 2),toolbar_location="below",title="zPolar of filter")
s2.circle(x=[0], y=[0], color="grey",
              radius=1,alpha=0.3 )
##################################################################
MagGraph=figure(x_range=(-3.14,3.14), y_range=(-10,10), tools=["pan,wheel_zoom"],
title='Magnitude',plot_width=370, plot_height=385)
MagGraph.line(x_co,y_co, color='black', line_width=2)
MagGraph.line(x_co_1,y_co_1,color='black', line_width=2)
##################################################################
MagGraph_2=figure(x_range=(-3.14,3.14), y_range=(-10,10), tools=["pan,wheel_zoom"],
title='Magnitude of filter',plot_width=370, plot_height=385)
MagGraph_2.line(x_co,y_co,color='black', line_width=2)
MagGraph_2.line(x_co_1,y_co_1,color='black', line_width=2)
###################################################################
phaseGraph=figure(x_range=(-3.14,3.14), y_range=(-10,10), tools=["pan,wheel_zoom"],
title='Phase',plot_width=370, plot_height=385)
phaseGraph.line(x_co,y_co,color='black', line_width=2)
phaseGraph.line(x_co_1,y_co_1,color='black', line_width=2)
####################################################################
phaseGraph_2=figure(x_range=(-3.14,3.14), y_range=(-10,10), tools=["pan,wheel_zoom"],
title='Phase of filter',plot_width=370, plot_height=385)
phaseGraph_2.line(x_co,y_co,color='black', line_width=2)
phaseGraph_2.line(x_co_1,y_co_1,color='black', line_width=2)
######################################################################
source4= ColumnDataSource({
    'w':[], 'p':[]
})
source6= ColumnDataSource({
    'w2':[], 'p2':[]
})

#########################poles##########################################
source = ColumnDataSource(data=dict(x_of_poles=[], y_of_poles=[]))

renderer = s1.circle(x="x_of_poles", y="y_of_poles", source=source, color='red', size=10)
columns_1 = [TableColumn(field="x_of_poles", title="x_of_poles"),
           TableColumn(field="y_of_poles", title="y_of_poles")
           ]
table = DataTable(source=source, columns=columns_1, editable=True, height=200)

#source poles ,source 2 zeors
#################################FILTER####################################

source5 = ColumnDataSource(data=dict(x_of_poles_2=[], y_of_poles_2=[]))

renderer_5 = s2.circle(x='x_of_poles_2', y='y_of_poles_2', source=source5, color='blue', size=10)
columns_5 = [TableColumn(field="x_of_poles_2", title="x_of_poles_2"),
           TableColumn(field="y_of_poles_2", title="y_of_poles_2")
           ]
table_5 = DataTable(source=source5, columns=columns_5, editable=True, height=200)

############################zeros#########################################
source_2 = ColumnDataSource(data=dict(x_of_zeros=[], y_of_zeros=[]))

renderer_2 = s1.asterisk(x='x_of_zeros', y='y_of_zeros', source=source_2, color='blue', size=10)
columns_2 = [TableColumn(field="x_of_zeros", title="x_of_zeros"),
           TableColumn(field="y_of_zeros", title="y_of_zeros")
           ]
table_2 = DataTable(source=source_2, columns=columns_2, editable=True, height=200)
##########################################################################
def ConjugateBool():
    global conj,Conjugate,s1,draw_tool,Conjugate2
    conj = dropdown2.active
    if conj == 0:
        Conjugate.data = {'x': [], 'y': []}
        Conjugate2.data = {'x': [], 'y': []}
        ZeorsAndPoles(0)
        ZeorsAndPoles_2(0)
    else:
        GenerateConjugate()
source_3= ColumnDataSource({
    'h':[], 'w':[]
})
phaseGraph.line(x='w',y='p',source=source4)

source_7= ColumnDataSource({
    'h2':[], 'w2':[]
})
phaseGraph_2.line(x='w2',y='p2',source=source6)

MagGraph.line(x='h',y='w',source=source_3)
MagGraph_2.line(x='h2',y='w2',source=source_7)
############################################################################
Conjugate = ColumnDataSource({
    'x': [], 'y': []
})
Conjugate2 = ColumnDataSource({
    'x': [], 'y': []
})
renderer3 = s1.circle(x="x", y="y", source=Conjugate, color='red', size=10)
renderer_4 = s1.asterisk(x='x', y='y', source=Conjugate2, color='blue', size=10)

columns_3 = [TableColumn(field="x", title="x_of_poles1"),
           TableColumn(field="y", title="y_of_poles1")
           ]
table3 = DataTable(source=Conjugate, columns=columns_3, editable=True, height=200)

columns_4 = [TableColumn(field="x", title="x_of_zeros1"),
           TableColumn(field="y", title="y_of_zeros1")
           ]
table4 = DataTable(source=Conjugate2, columns=columns_4, editable=True, height=200)
dropdown2 = RadioButtonGroup(labels=['No conjugate', 'Conjugate'], active=0, width=100)




conj = 0

def GenerateConjugate():
    global conj
    x_of_poles1=[]
    y_of_poles1=[]
    x_of_zeros1=[]
    y_of_zeros1=[]
    if conj:
        Conjugate.data = {'x':[],'y':[]}
        Conjugate2.data={'x':[],'y':[]}
        ZeorsAndPoles(-1)
        ZeorsAndPoles_2(-1)
        for i in range(len(source.data['x_of_poles'])):
            x_of_poles1.append(source.data['x_of_poles'][i])
            y_of_poles1.append(source.data['y_of_poles'][i]*-1)
        Conjugate.stream({'x': x_of_poles1,'y':y_of_poles1})
        renderer3 = s1.circle(x="x", y="y", source=Conjugate, color='red', size=10)
        for i in range(len(source_2.data['x_of_zeros'])):
            x_of_zeros1.append(source_2.data['x_of_zeros'][i])
            y_of_zeros1.append(source_2.data['y_of_zeros'][i]*-1)
        Conjugate2.stream({'x': x_of_zeros1,'y':y_of_zeros1})
        renderer_4 = s1.asterisk(x='x', y='y', source=Conjugate2, color='blue', size=10)





        
#######################################################################3
def update(attr, old, new):
    ZeorsAndPoles(0)
    ZeorsAndPoles_2(0)
    GenerateConjugate()

source.on_change('data',update)
source5.on_change('data',update)
source_2.on_change('data',update)

def ZeorsAndPoles(a):
    global Zero,Pole
    Zero = []
    Pole = []
    
    for i in range(len(source_2.data['x_of_zeros'])):
        Zero.append(source_2.data['x_of_zeros'][i]+source_2.data['y_of_zeros'][i]*1j)
        Zero.append(source_2.data['x_of_zeros'][i]+source_2.data['y_of_zeros'][i]*1j*a)
    for i in range(len(source.data['x_of_poles'])):
        Pole.append(source.data['x_of_poles'][i]+source.data['y_of_poles'][i]*1j)
        Pole.append(source.data['x_of_poles'][i]+source.data['y_of_poles'][i]*1j*a)
    
    MagAndPhase()

    print(Zero)

#for all pass filter
def ZeorsAndPoles_2(a):
    global Zero_2,Pole_2
    Zero_2 = []
    Pole_2= []
    
    for i in range(len(source5.data['x_of_poles_2'])):
        Pole_2.append(source5.data['x_of_poles_2'][i]+source5.data['y_of_poles_2'][i]*1j)
        Pole_2.append(source5.data['x_of_poles_2'][i]+source5.data['y_of_poles_2'][i]*1j*a)

    for i in range(len(source.data['x_of_poles'])):
        Pole_2.append(source.data['x_of_poles'][i]+source.data['y_of_poles'][i]*1j)
        Pole_2.append(source.data['x_of_poles'][i]+source.data['y_of_poles'][i]*1j*a)

    for i in range(len(source5.data['x_of_poles_2'])):
        Zero_2.append(source5.data['x_of_poles_2'][i]+source5.data['y_of_poles_2'][i]*1j/
        ((source5.data['x_of_poles_2'][i])**2+(source5.data['y_of_poles_2'][i])**2))
        Zero_2.append(source5.data['x_of_poles_2'][i]+source5.data['y_of_poles_2'][i]*1j*a/
        ((source5.data['x_of_poles_2'][i])**2+(source5.data['y_of_poles_2'][i])**2))


    for i in range(len(source_2.data['x_of_zeros'])):
        Zero_2.append(source_2.data['x_of_zeros'][i]+source_2.data['y_of_zeros'][i]*1j)  
        Zero_2.append(source_2.data['x_of_zeros'][i]+source_2.data['y_of_zeros'][i]*1j*a)  
    print(Zero_2)
    print(Zero_2)
    MagAndPhase_2()
    #print(Pole_2)

    
    
    
    
def MagAndPhase():
    source4.data={
    'w':[], 'p':[]
    }

    source_3.data={
    'h': [], 'w': []
    }
   
    num, den=zpk2tf(Zero,Pole,1)
    w,h=freqz(num,den,worN=10000)
    MagAndPhase=np.sqrt(h.real**2+h.imag**2)
    phase=np.arctan(h.imag/h.real)
    if len(Zero)==0 and len(Pole)==0:
        MagAndPhase=[]
        w=[]
        phase=[]
        source_3.data={'w': [], 'h': [] }
    source_3.stream({
    'h': w, 'w': MagAndPhase
    })
    source4.stream({
        'w':w, 'p':phase
    })
def MagAndPhase_2():
    source6.data={
    'w2':[], 'p2':[]
    }

    source_7.data={
    'h2': [], 'w2': []
    }
   
    num, den=zpk2tf(Zero_2,Pole_2,1)
    w,h=freqz(num,den,worN=10000)
    MagAndPhase=np.sqrt(h.real**2+h.imag**2)
    phase=np.arctan(h.imag/h.real)
    if len(source5.data['x_of_poles_2'])==0:
        MagAndPhase=[]
        w=[]
        phase=[]
        source_7.data={'w2': [], 'h2': [] }

    source_7.stream({
    'h2': w, 'w2': MagAndPhase
    })
    source6.stream({
        'w2':w, 'p2':phase
    })
    
    ###########################################################################
def clear_all():
    source.data['x_of_poles'].clear()
    source.data['y_of_poles'].clear()
    new_data={'x_of_poles':source.data['x_of_poles'],'y_of_poles':source.data['y_of_poles'],}
    source.data=new_data
    ########################################################################
    source_2.data['x_of_zeros'].clear()
    source_2.data['y_of_zeros'].clear()
    new_data_2={'x_of_zeros':source_2.data['x_of_zeros'],'y_of_zeros':source_2.data['y_of_zeros'],}
    source_2.data=new_data_2
    print('deleted')
    ########################################################################
    source5.data['x_of_poles_2'].clear()
    source5.data['y_of_poles_2'].clear()
    new_data_3={'x_of_poles_2':source5.data['x_of_poles_2'],'y_of_poles_2':source5.data['y_of_poles_2'],}
    source5.data=new_data_3
###################################################################################3
menu = Select(options=['None','Filter_1', 'Filter_2', 'Filter_3','Select_All'],value='None' ,title='Filters')
def FilterTypes(attr,old,new):
    #print('entered func')
        if menu.value=="None":
            source5.data['x_of_poles_2'].clear()
            source5.data['y_of_poles_2'].clear()
            new_data_3={'x_of_poles_2':source5.data['x_of_poles_2'],'y_of_poles_2':source5.data['y_of_poles_2'],}
            source5.data=new_data_3
        elif  menu.value== "Filter_1" :
            source5.data=dict(x_of_poles_2=[1,1,-2], y_of_poles_2=[1,1.3,-1])
            new_data_4={'x_of_poles_2':source5.data['x_of_poles_2'],'y_of_poles_2':source5.data['y_of_poles_2'],}
            source5.data=new_data_4
        elif  menu.value== "Filter_2" :
            source5.data=dict(x_of_poles_2=[-1,-1,2], y_of_poles_2=[-1,-1.3,1])
            new_data_5={'x_of_poles_2':source5.data['x_of_poles_2'],'y_of_poles_2':source5.data['y_of_poles_2'],}
            source5.data=new_data_5
        elif  menu.value== "Filter_3" :
            source5.data=dict(x_of_poles_2=[-2,-3,0], y_of_poles_2=[-1.5,2,1.5])
            new_data_6={'x_of_poles_2':source5.data['x_of_poles_2'],'y_of_poles_2':source5.data['y_of_poles_2'],}
            source5.data=new_data_6
        elif  menu.value== "Select_All" :
            source5.data=dict(x_of_poles_2=[1,1,-2,-1,-1,2,-2,-2.5,0], y_of_poles_2=[1,1.3,-1,-1,-1.3,1,-1.5,2,1.5])
            new_data_6={'x_of_poles_2':source5.data['x_of_poles_2'],'y_of_poles_2':source5.data['y_of_poles_2'],}
            source5.data=new_data_6    

menu.on_change('value', FilterTypes) 
#####################################################################################
Clear_button=Button(label="Clear All",button_type="primary",width=100)
Clear_button.on_click(clear_all)
###########################################################################3
draw_tool = PointDrawTool(renderers=[renderer], empty_value='red')
draw_tool_5 = PointDrawTool(renderers=[renderer_5], empty_value='red')
draw_tool_2 = PointDrawTool(renderers=[renderer_2], empty_value='blue')

dropdown2.on_change('active', lambda attr, old, new: ConjugateBool())

s1.add_tools(draw_tool,draw_tool_2)
s1.toolbar.active_tap = draw_tool
s2.add_tools(draw_tool_5)
s2.toolbar.active_tap = draw_tool
plot3=Row(MagGraph,phaseGraph,MagGraph_2,phaseGraph_2)
plot=Row(s1,s2,table,table_5, table_2,table3,table4)
buttonss=Row(Clear_button,menu)
# show(column(dropdown2,plot,buttonss,plot3))
curdoc().theme = 'dark_minimal'
curdoc().add_root(column(dropdown2,plot,buttonss,plot3))
