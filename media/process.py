import warnings
warnings.filterwarnings('ignore')
import sys
import json
import base64
import matplotlib.pyplot as plt
import io
import getdist
import getdist.plots as plots
import os

def generate_image(data):
    
    folderpath = data['folderpath']
    burnin = data['burnin'] 
    parameters = data['parameters'] 
    legend = data['legend']
    color = data['color']
    fontsize = data['fontsize']
    linewidth = float(data['linewidth'])
    alpha = float(data['alpha'])
    filled = data['filled']
    
    g = plots.get_subplot_plotter(width_inch=10)
    g.settings.linewidth_contour = linewidth
    g.settings.linewidth = linewidth
    g.settings.fontsize = fontsize
    g.settings.alpha_filled_add = alpha

    plt.rcParams.update({'font.size': fontsize})
    
    for file in os.listdir(folderpath):
        if file.endswith(".updated.yaml"):
            update_files = file.replace(".updated.yaml", "")
           
    sample_file = folderpath + '/' + update_files        
    samples = getdist.mcsamples.loadMCSamples(sample_file, settings={'ignore_rows': burnin})
    g.triangle_plot(samples, parameters, filled=filled, legend_labels=legend, contour_colors=[color])
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    
    return img_base64

if __name__ == "__main__":
    input_data = sys.stdin.read()
    data = json.loads(input_data)
    img_data = generate_image(data)
    print(json.dumps({"image": img_data}))