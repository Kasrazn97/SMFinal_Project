import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def get_colors(num_of_colors):
    
    tableau = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), 
             (23, 190, 207), 
             (158, 218, 229)]

    colors = tableau[:num_of_colors]

    for i in range(num_of_colors):   
        r, g, b = tableau[i]   
        colors[i] = (r / 255., g / 255., b / 255.)

    return colors

def plot_immigration_flow(data):
    
    STEPS = data.step.max()

    plt.style.use("seaborn-dark-palette")
    plt.figure(figsize=(12, 14))

    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)    
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()  

    # plt.ylim(0, 350)
    # plt.xlim(979, 2012)
    plt.title("Immigration flow dynamics of highly educated people", fontsize=17, ha="center") 

    colors = get_colors(len(data['country'].unique()))
    for i, country in enumerate(data['country'].unique()):
            plt.plot(np.arange(1, STEPS+1, 1),    
                    data[data['country'] == country]['num_of_immigrants'],
                            lw=2, 
                    color=colors[i]
                    )
            y_pos = data[(data['country']==country)&(data.step == STEPS)]['num_of_immigrants']
            plt.text(x=STEPS, y=y_pos, s = country, fontsize=14, color=colors[i]) 
                
    # for y in range(1, df.step, ):    
    #     plt.plot(range(1980, 2011, 5), np.repeat(y, len(range(1980, 2011, 5))), "--", lw=0.5, color="black", alpha=0.3) 

    plt.xticks(size=14)
    plt.yticks(size=14)