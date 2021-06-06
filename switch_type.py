show_data_widget = None


def switch_type(option):
    global show_data_widget
    if show_data_widget is not None:
        show_data_widget.close()
    if option == 'Просто покажи данные':
        show_data_widget = interactive(
            show_data_default,
            {'manual': True},
            start_date=get_date_widget(text="Дата начала", year=2016, month=5, day=20),
            end_date=get_date_widget(text="Дата окончания", year=2020),
        )
        display(show_data_widget)
    elif option == '[ETH] Закупаем вечно':
        show_data_widget = interactive(
            show_data_slow_buyer_eth,
            {'manual': True},
            year_budget=year_budget_widget,
            comission=get_comission_widget(),
            skip=get_skip_widget(value=0.33),
            start_date=get_date_widget(text="Дата начала", year=2018),
            end_date=get_date_widget(text="Дата окончания", year=2020),
        )
        display(show_data_widget)
    elif option == '[ETH] Закупаем мощность':
        show_data_widget = interactive(
            show_data_miner_eth,
            {'manual': True},
            start_date=get_date_widget(text="Дата начала", year=2018),
            end_date=get_date_widget(text="Дата окончания", year=2020),
            year_budget=year_budget_widget,
            comission=get_comission_widget(),
            sell_part=get_sell_part_widget(max=1.0, value=0.9),
            skip=get_skip_widget(value=0.5),
            price_of_100_power=price_of_100_power_widget,
            el_for_100_power=el_for_100_power_widget,
            el_cost=el_cost_widget,
            years_amort=years_amort_widget,
            amort_part=amort_part_widget,
            exit_price=exit_price_widget,
        )
        display(show_data_widget)
    elif option == '[ETH] Купили мощность разово':
        show_data_widget = interactive(
            show_data_miner_once_eth,
            {'manual': True},
            start_date=get_date_widget(text="Дата начала", year=2018),
            end_date=get_date_widget(text="Дата окончания", year=2020),
            total_budget=total_budget_widget,
            comission=get_comission_widget(),
            sell_part=get_sell_part_widget(max=1.0, value=0.9),
            skip=get_skip_widget(value=0.5),
            price_of_100_power=price_of_100_power_widget,
            el_for_100_power=el_for_100_power_widget,
            el_cost=el_cost_widget,
            years_amort=years_amort_widget,
            amort_part=amort_part_widget,
            exit_price=exit_price_widget,
        )
        display(show_data_widget)
    elif option == '[ETH] Закупаем Асики/Видеокарты':
        show_data_widget = interactive(
            show_data_miner_cards_eth,
            {'manual': True},
            start_date=get_date_widget(text="Дата начала", year=2018),
            end_date=get_date_widget(text="Дата окончания", year=2020),
            year_budget=year_budget_widget,
            comission=get_comission_widget(),
            sell_part=get_sell_part_widget(max=1.0, value=0.9),
            skip=get_skip_widget(value=0.5),
            asic_price=asic_price_widget,
            asic_power=asic_power_widget,
            asic_el=asic_el_widget,
            el_cost=el_cost_widget,
            years_amort=years_amort_widget,
            amort_part=amort_part_widget,
            exit_price=exit_price_widget,
        )
        display(show_data_widget)
    elif option == '[BTC] Закупаем вечно':
        show_data_widget = interactive(
            show_data_slow_buyer_btc,
            {'manual': True},
            start_date=get_date_widget(text="Дата начала", year=2018),
            end_date=get_date_widget(text="Дата окончания", year=2020),
            year_budget=year_budget_widget,
            comission=get_comission_widget(),
            skip=get_skip_widget(value=0.33),
        )
        display(show_data_widget)
    elif option == 'Закупка индексов':
        show_data_widget = interactive(
            show_data_slow_buyer_indexes,
            {'manual': True},
            start_date=get_date_widget(text="Дата начала", year=2010),
            end_date=get_date_widget(text="Дата окончания", year=2020),
            year_budget=year_budget_widget,
            comission=get_comission_widget(value=0.02),
            skip=get_skip_widget(value=0.33),
            tax=get_tax_widget(),
            iis=get_iis_widget(value=False),
        )
        display(show_data_widget)
    elif option == 'Покупаем индекс':
        show_data_widget = interactive(
            show_data_slow_buyer_index,
            {'manual': True},
            ticker=get_switch_index_widget(),
            start_date=get_date_widget(text="Дата начала", year=2010),
            end_date=get_date_widget(text="Дата окончания", year=2020),
            year_budget=year_budget_widget,
            comission=get_comission_widget(value=0.02),
            skip=get_skip_widget(value=0.33),
            tax=get_tax_widget(),
            iis=get_iis_widget(value=False),
        )
        display(show_data_widget)
