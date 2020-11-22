import matplotlib.pyplot as plt

PATH_TO_PHOTO = 'images/mem_usage.jpeg'

def create_plot(common, cowrie, time):
    fig = plt.figure()
    common_ax = fig.add_subplot(111)
    cowrie_ax = common_ax.twinx() 

    common_ax.plot(time, common, label = u'Common memory usage', color='red')
    common_ax.set_xlabel(u'Time, minutes')
    common_ax.set_ylabel(u'Usage, %', color='red')
    common_ax.grid(True, color='red')
    common_ax.tick_params(axis='y', which='major', labelcolor='red')

    cowrie_ax.plot(time, cowrie, label = u'Cowrie memory uisage', color='blue')
    cowrie_ax.set_ylabel(u'Usage, %', color='blue')
    cowrie_ax.grid(True, color='blue')
    cowrie_ax.tick_params(axis='y', which='major', labelcolor='blue')

    common_ax.set_title(u'Memory usage compare')

    fig.savefig(PATH_TO_PHOTO)


