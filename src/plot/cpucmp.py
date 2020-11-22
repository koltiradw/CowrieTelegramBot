import matplotlib.pyplot as plt

PATH_TO_PHOTO = 'images/cpu_usage.jpeg'

def create_plot(common, cowrie, time):
    fig, ax = plt.subplots(1, figsize=(8, 6))

    fig.suptitle('CPU usage compare', fontsize = 15)

    ax.plot(time, common, color = "red", label = "Common cpu usage")
    ax.plot(time, cowrie, color = "blue", label = "Cowrie cpu usage")
    
    ax.set_xlabel("Time, minutes")
    ax.set_ylabel("Usage, %")

    plt.legend(loc="upper left", title="Curves", frameon=False)

    fig.savefig(PATH_TO_PHOTO)



