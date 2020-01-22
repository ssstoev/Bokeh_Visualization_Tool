from bokeh.models.widgets import Sliderfrom bokeh.layouts import widgetbox, columnfrom bokeh.models import Slider, ColumnDataSourcefrom bokeh.plotting import figure, curdocfrom bokeh.core.properties import valuefrom bokeh.models.ranges import FactorRangefrom bokeh.models import Panel, Tabsimport pandas as pddef stacked_bars(births, deaths):	birth = births	death = deaths 	birth['First Name'] = birth['FirstName']	birth['Last Name'] = birth['Lastname']	merged_data = death.merge(birth, on=['First Name', 'Last Name', 'Place'])	merged_data = merged_data.drop_duplicates(subset=['First Name', 'Last Name'], keep='first', inplace=False)	merged_data['Birth'] = merged_data['Year_y']	merged_data['Death'] = merged_data['Year_x']	merged_data['Gender'] = merged_data['Gender_y']	all_data = merged_data[['Birth', 'Death', 'Gender']]	all_data = all_data.dropna()	all_data = all_data.loc[all_data["Gender"] != "Onbekend"]	birth_data = all_data[['Birth', 'Gender']]	death_data = all_data[['Death', 'Gender']]	birth_data.Birth = birth_data.Birth.astype(int)	death_data.Death = death_data.Death.astype(int)	birth_data = birth_data.sort_values(by=['Birth'])	death_data = death_data.sort_values(by=['Death'])		agg_b_w = birth_data[birth_data['Gender'] == 'Vrouw'].Birth.value_counts().to_frame()	agg_d_w = death_data[death_data['Gender'] == 'Vrouw'].Death.value_counts().to_frame()	agg_b_w = agg_b_w.reset_index()	agg_d_w = agg_d_w.reset_index()	agg_merged_w = agg_b_w.merge(agg_d_w, on='index')	agg_merged_w['Year'] = agg_merged_w['index']	agg_merged_w = agg_merged_w.set_index('Year')	agg_merged_w = agg_merged_w.sort_values(by=['Year'])	new_dict_w = {}	for i in range(len(agg_merged_w)):		new_dict_w[int(agg_merged_w['index'].iloc[i])] = int(agg_merged_w['Birth'].iloc[i]), int(agg_merged_w['Death'].iloc[i])	agg_b_m = birth_data[birth_data['Gender'] == 'Man'].Birth.value_counts().to_frame()	agg_d_m = death_data[death_data['Gender'] == 'Man'].Death.value_counts().to_frame()	agg_b_m = agg_b_m.reset_index()	agg_d_m = agg_d_m.reset_index()	agg_merged_m = agg_b_m.merge(agg_d_m, on='index')	agg_merged_m['Year'] = agg_merged_m['index']	agg_merged_m = agg_merged_m.set_index('Year')	agg_merged_m = agg_merged_m.sort_values(by=['Year'])	new_dict_m = {}	for i in range(len(agg_merged_m)):		new_dict_m[int(agg_merged_m['index'].iloc[i])] = int(agg_merged_m['Birth'].iloc[i]), int(agg_merged_m['Death'].iloc[i])	categories = ['Male', 'Female']	types = ['Born', 'Died']	colors = ["#669acc", "#cc8f66"]	data = {'categories' : categories,			'Born' : new_dict_m[1818],			'Died' : new_dict_w[1818]}	source = ColumnDataSource(data=data)		def make_plot():		p = figure(x_range=categories, plot_height=350, title="Amount of born and dead people per year",		           toolbar_location=None, tools="")				renderers= p.vbar_stack(types, x='categories', width=0.9, color=colors, source=source, \		                         legend=[value(x) for x in types], name=types)		p.y_range.start = 0		p.x_range.range_padding = 0.1		p.xgrid.grid_line_color = None		p.axis.minor_tick_line_color = None		p.outline_line_color = None		p.legend.location = "top_left"		p.legend.orientation = "horizontal"		slider = Slider(start=1818, end=1906, value=1818, step=1, title="Year")		#function to update axis range		def update_axis(attrname, old, new):		    a=slider.value		    new_data = {'categories' : categories,						'Born' : new_dict_m[a],						'Died' : new_dict_w[a]}		    source.data=new_data		#Adding fucntion to on_change		slider.on_change('value', update_axis)		layout = column(p, widgetbox(slider))		return layout	tab = Panel(child=make_plot(), title='Birth and Death')	return tab