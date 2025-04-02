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
from contextlib import redirect_stdout, redirect_stderr

class getdist_analysis:
    def __init__(self, data):
        
        """
        Load samples and parameters
        """
        
        self.folderpath = data['folderpath']
        self.burnin = data['burnin'] 
        self.parameters = data['parameters'] 
        self.legend = data['legend']
        self.color = data['color']
        self.fontsize = data['fontsize']
        self.linewidth = float(data['linewidth'])
        self.alpha = float(data['alpha'])
        self.filled = data['filled']
        
        for file in os.listdir(self.folderpath):
            if file.endswith(".updated.yaml"):
                update_files = file.replace(".updated.yaml", "")
            
        sample_file = self.folderpath + '/' + update_files    
        
        with warnings.catch_warnings(), io.StringIO() as f, io.StringIO() as e:
            warnings.simplefilter("ignore") 
            with redirect_stdout(f), redirect_stderr(e): 
                self.samples = getdist.mcsamples.loadMCSamples(sample_file, settings={'ignore_rows': self.burnin, 'names': self.parameters})


    def generate_image(self):
        
        """
        Generate image using getdist
        """
        
        g = plots.get_subplot_plotter(width_inch=10)
        g.settings.linewidth_contour = self.linewidth
        g.settings.linewidth = self.linewidth
        g.settings.fontsize = self.fontsize
        g.settings.alpha_filled_add = self.alpha

        plt.rcParams.update({'font.size': self.fontsize})

        g.triangle_plot(self.samples, self.parameters, filled=self.filled, legend_labels=[self.legend], contour_colors=[self.color])
        
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        
        return img_base64
    
    def generate_text(self):
        """
        Generate stats text using getdist
        """
        
        marge_stats = str(self.samples.getTable().tableTex())
        
        return marge_stats
        
        
        

if __name__ == "__main__":
    input_data = sys.stdin.read()
    data = json.loads(input_data)
    getdist_anlst = getdist_analysis(data)
    img_data = getdist_anlst.generate_image()
    text_data = getdist_anlst.generate_text()
    print(json.dumps({"image": img_data, "text": text_data}))