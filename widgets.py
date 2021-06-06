import datetime

from ipywidgets import widgets, Layout

from base.DataStorage import DataStorage

style = {'description_width': '150px'}
layout=Layout(width='50%')


def get_date_widget(text="Выбор даты", year=2018, month=10, day=10):
    return widgets.DatePicker(
        description=text,
        disabled=False,
        value=datetime.date(year, month, day)
)
year_budget_widget=widgets.IntSlider(
    min=1000,
    max=50000,
    step=500,
    value=10000,
    description="Годовой бюджет")
total_budget_widget=widgets.IntSlider(
    min=1000,
    max=50000,
    step=500,
    value=10000,
    description="Бюджет закупок",
    )
    
def get_comission_widget(value=0.05):
    return widgets.FloatSlider(
        min=0.0,
        max=1.0,
        step=0.01,
        value=value,
        readout_format='.2f',
        description="Комиссия общая",
        )
        
def get_sell_part_widget(max=0.99, value=0.0):
    return widgets.FloatSlider(
        min=0.0,
        max=max,
        step=0.001,
        value=value,
        readout_format='.3f',
        description="Скидываем от полученого",
        )
        
def get_skip_widget(value=0.33):
    return widgets.FloatSlider(
        min=0.0,
        max=0.99,
        step=0.01,
        value=value,
        readout_format='.2f',
        description="Не выходим времени",
        )
        
price_of_100_power_widget = widgets.FloatSlider(
    min=100,
    max=5000,
    step=0.1,
    value=1004.6,
    readout_format='.1f',
    description="Цена 100 мощности",
    )
    
el_for_100_power_widget = widgets.FloatSlider(
    min=0.0,
    max=10,
    step=0.01,
    value=0.59,
    readout_format='.2f',
    description="Квт на 100 мощности",
    )
    
el_cost_widget = widgets.FloatSlider(
    min=0.0,
    max=0.4,
    step=0.001,
    value=0.038,
    readout_format='.3f',
    description="Цена КвтЧас",
    )
    
years_amort_widget = widgets.FloatSlider(
    min=0.5,
    max=20,
    step=0.1,
    value=3,
    readout_format='.1f',
    description="Срок амортизации оборудования (лет)",
    )
    
amort_part_widget = widgets.FloatSlider(
    min=0.0,
    max=1.0,
    step=0.1,
    value=0.7,
    readout_format='.1f',
    description="Доля амортизации оборудования",
    )
    
exit_price_widget = widgets.FloatSlider(
    min=0.0,
    max=1.0,
    step=0.1,
    value=0.5,
    readout_format='.1f',
    description="Цена сброса оборудования",
    )
    
asic_price_widget = widgets.IntSlider(
    min=1,
    max=10000,
    step=5,
    value=310,
    description="Цена оборудования",
    )
    
asic_power_widget = widgets.FloatSlider(
    min=0.5,
    max=1000.0,
    step=0.5,
    value=30.5,
    readout_format='.1f',
    description="Мощность майнинга оборудования",
    )
    
asic_el_widget = widgets.FloatSlider(
    min=0.05,
    max=5,
    step=0.01,
    value=0.14,
    readout_format='.2f',
    description="Потребление оборудования",
    )
    
def get_tax_widget(value=0.13):
    return widgets.FloatSlider(
        min=0.00,
        max=0.99,
        step=0.01,
        value=value,
        readout_format='.2f',
        description="Налог на прибыль",
        )
        
def get_iis_widget(value=True):
    return widgets.Checkbox(
        value=value,
        description='Наличие ИИС типа А',
        disabled=False,
        indent=True
    )
def get_switch_index_widget():
    data = DataStorage()
    data.read_files()
    return widgets.Dropdown(
        options=data.tickers,
        value=data.tickers[0],
        description='Индекс',
        disabled=False)
