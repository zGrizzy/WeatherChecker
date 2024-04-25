import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px


def plot_temperature_comparison(data):
    sns.set_theme(style="whitegrid")
    sns.color_palette("hls", 8)
    sns.lineplot(x='Date', y='Temperature', hue='City', data=data, marker='o', palette='viridis')
    plt.title('Temperature Comparison Among Cities')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=25)
    plt.legend(title='City')
    plt.show()

def plot_interactive_temperature_comparison(data):
    fig = px.line(data, x='Date', y='Temperature', color='City', title='Temperature Comparison Among Cities',
                  markers=True)
    fig.update_yaxes(title='Temperature (°C)', tickformat=".1f° C")
    fig.update_xaxes(tickangle=0)
    fig.show()