import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px


def plot_temperature_comparison(data):
    sns.set_theme(style="whitegrid")
    sns.color_palette("hls", 8)
    sns.lineplot(x='Data', y='Temperatūra', hue='Miestas', data=data, marker='o', palette='viridis')
    plt.title('Temperatūros palyginimas tarp miestų')
    plt.xlabel('Data')
    plt.ylabel('Temperatūra (°C)')
    plt.xticks(rotation=25)
    plt.legend(title='Miestas')
    plt.show()


def plot_interactive_temperature_comparison(data):
    fig = px.line(data, x='Data', y='Temperatūra', color='Miestas', title='Temperatūros palyginimas tarp miestų',
                  markers=True)
    fig.update_yaxes(title='Temperatūra (°C)', tickformat=".1f° C")
    fig.update_xaxes(tickangle=0)
    fig.show()
