import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px


def plot_temperature_comparison(data):
    sns.set_theme(style="whitegrid")
    palette = sns.color_palette("viridis", len(data['City'].unique()))  # Create a color palette
    sns.lineplot(x='Date', y='Temperature', hue='City', data=data, marker='o', palette=palette)
    plt.title('Temperature Comparison Among Cities')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=-55)  # Rotate the x-axis labels for better readability
    plt.tight_layout()  # Adjusts plot to make sure everything fits without overlap
    plt.legend(title='City')
    plt.show()

def plot_interactive_temperature_comparison(data):
    fig = px.line(data, x='Date', y='Temperature', color='City', title='Temperature Comparison Among Cities',
                  markers=True)
    fig.update_yaxes(title='Temperature (°C)', tickformat=".1f° C")
    fig.update_xaxes(tickangle=45)
    fig.show()
