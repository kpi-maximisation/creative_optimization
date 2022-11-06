import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib.gridspec import GridSpec
from matplotlib import ticker

def plotly_plot_pie(df, column, limit=None, title=None):
    a = pd.DataFrame({'count': df.groupby([column]).size()}).reset_index()
    a = a.sort_values("count", ascending=False)
    if limit:
        a.loc[a['count'] < limit, column] = f'Other {column}s'
    if title == None:
        title=f'Distribution of {column}'
    fig = px.pie(a, values='count', names=column, title=title, width=800, height=500)
    fig.show()

def plotly_plot_hist(df, column, color=['cornflowerblue'], title=None):
    if title == None:
        title=f'Distribution of {column}'
    fig = px.histogram(
            df,
            x=column,
            marginal='box',
            color_discrete_sequence=color,
            title=title)
    fig.update_layout(bargap=0.01)
    fig.show()

def plotly_multi_hist(sr, rows, cols, title_text, subplot_titles):
  fig = make_subplots(rows=rows, cols=cols, subplot_titles=subplot_titles)
  for i in range(rows):
    for j in range(cols):
      x = ["-> " + str(i) for i in sr[i+j].index]
      fig.add_trace(go.Bar(x=x, y=sr[i+j].values ), row=i+1, col=j+1)
  fig.update_layout(showlegend=False, title_text=title_text)
  fig.show()

def plotly_plot_scatter(df, x_col, y_col, marker_size, hover=[]):
    fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            opacity=0.8,
            hover_data=hover,
            title=f'{x_col} vs. {y_col}')
    fig.update_traces(marker_size=marker_size)
    fig.show()

def plot_hist(df:pd.DataFrame, column:str, color:str='cornflowerblue')->None:
    sns.displot(data=df, x=column, color=color, kde=True, height=6, aspect=2)
    plt.title(f'Distribution of {column}', size=20, fontweight='bold')
    plt.show()

def plot_count(df:pd.DataFrame, column:str) -> None:
    plt.figure(figsize=(12, 7))
    sns.countplot(data=df, x=column)
    plt.title(f'Distribution of {column}', size=20, fontweight='bold')
    plt.show()

def plot_bar(df:pd.DataFrame, x_col:str, y_col:str, title:str, xlabel:str, ylabel:str)->None:
    plt.figure(figsize=(12, 7))
    sns.barplot(data = df, x=x_col, y=y_col)
    plt.title(title, size=20)
    plt.xticks(rotation=75, fontsize=14)
    plt.yticks( fontsize=14)
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    plt.show()

def plot_heatmap(df:pd.DataFrame, title:str, cmap='Reds')->None:
    plt.figure(figsize=(12, 7))
    sns.heatmap(df, annot=True, cmap=cmap, vmin=0, vmax=1, fmt='.2f', linewidths=.7, cbar=True )
    plt.title(title, size=18, fontweight='bold')
    plt.show()

def plot_box(df:pd.DataFrame, x_col:str, title:str) -> None:
    plt.figure(figsize=(12, 7))
    sns.boxplot(data = df, x=x_col)
    plt.title(title, size=20)
    plt.xticks(rotation=75, fontsize=14)
    plt.show()

def plot_box_multi(df:pd.DataFrame, x_col:str, y_col:str, title:str) -> None:
    plt.figure(figsize=(12, 7))
    sns.boxplot(data = df, x=x_col, y=y_col)
    plt.title(title, size=20)
    plt.xticks(rotation=75, fontsize=14)
    plt.yticks( fontsize=14)
    plt.show()

def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str) -> None:
    plt.figure(figsize=(12, 7))
    sns.scatterplot(data = df, x=x_col, y=y_col)
    plt.title(f'{x_col} Vs. {y_col}\n', size=20)
    plt.xticks(fontsize=14)
    plt.yticks( fontsize=14)
    plt.show()

def hist(sr):
    x = ["Id: " + str(i) for i in sr.index]
    fig = px.histogram(x=x, y=sr.values)
    fig.show()


def plot_time_series(data, scaled_data):
    """
        A simple function to plot a time series
    """

    fig = plt.figure()
    gs = GridSpec(2, 1, figure=fig)

    fig.set_figheight(20)
    fig.set_figwidth(30)
    fig.tight_layout(pad=15)

    M = 100
    xticks = ticker.MaxNLocator(M)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(data.index, data.Sales, 'b-')
    ax1.xaxis.set_major_locator(xticks)
    ax1.tick_params(labelrotation=90)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Thousands of Units')
    ax1.title.set_text('Time Series Plot of Sales')
    ax1.grid(True)

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(scaled_data.index, scaled_data.Sales, 'g-')
    ax2.xaxis.set_major_locator(xticks)
    ax2.tick_params(labelrotation=90)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Scaled Units')
    ax2.title.set_text(
        'Time Series Plot of Scaled Sales')
    ax2.grid(True)
    plt.show()

def plot_histogram(data, scaled_data):
    """
        a simple function to plot time series histogram
    """
    fig = plt.figure()
    gs = GridSpec(2, 1, figure=fig)

    fig.set_figheight(10)
    fig.set_figwidth(30)
    fig.tight_layout(pad=6)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.hist(data.Sales, density=True, bins=60)
    ax1.title.set_text('Histogram of Sales')
    ax1.grid(True)

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.hist(scaled_data.Sales, density=True, bins=60)
    ax2.title.set_text('Histogram of the of Scaled  Sales')
    ax2.grid(True)
    plt.show()

def plot_correlations(array: np.array, prefix: str):
    plt.figure(figsize=(30, 5))
    plt.title(
        f"{prefix}  Autocorrelations of Scaled Sales")
    plt.bar(range(len(array)), array)
    plt.grid(True)
    plt.savefig(f'../images/{prefix}autocorrelation.png')
    plt.show()
