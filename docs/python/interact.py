try:
    from ipywidgets import widgets
    from ipywidgets.widgets import *
except:
    try:
        from IPython.html import widgets
        from IPython.html.widgets import *
    except:
        print ('do: pip install --user ipywidgets')
        
    
from IPython.display import clear_output, display, HTML
import pylab as plt
import numpy as np

def show_args(**kwargs):
    w = int(kwargs['a'])
    sd = float(kwargs['sd'])
    filt = {}
    filt['Low Pass'] = np.array([1./w]*w).astype(float)
    filt['1st Order High Pass'] = np.array([0]*w).astype(float)
    filt['1st Order High Pass'][0] = 1
    filt['1st Order High Pass'][-1] = -1
    filt['2nd Order High Pass'] = np.array([0]*w).astype(float)
    filt['2nd Order High Pass'][0] = 1
    filt['2nd Order High Pass'][-1] = 1
    filt['2nd Order High Pass'][int(w/2)] = -2

    x = np.linspace(0, 100, 500)

    y = {}
    y['Step'] = np.ones_like(x);
    y['Step'][x<=x.max()/2] = 0.

    y['Ramp'] = x.copy()/x.max()
    y['Ramp'][x>x.max()/2] = 1. - y['Ramp'][x>x.max()/2]
    y['Ramp'] *= 2

    y['Flat'] = x*0 + 0.5
    y['Pulse'] = y['Step'].copy()
    half = y['Pulse'][::2]
    other = half[::-1]

    y['Pulse'] = np.append(half,other).flatten()

    xx = x.copy()
    yy = y[kwargs['Signal']].copy()
    ff = filt[kwargs['FilterType']].copy()
    if sd:
      yy = np.random.normal(yy, sd)
    rr = np.convolve(yy,ff,'valid')

    #s = '<h3>Filter:</h3><table>\n'
    #for k,v in kwargs.items():
    #    s += '<tr><td>{0}</td><td>{1}</td></tr>\n'.format(k,v)
    #s += '</table>'
   
    #display(HTML(s))
    fig = plt.figure(1,figsize=(10,7))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(xx,yy,'k-')
    ax.set_ylim(-1.5,1.5)
    l = xx.shape[0] - rr.shape[0]
    xxx = xx[int(l/2):]
    l = rr.shape[0] - xxx.shape[0]
    print(l,rr.shape,xx.shape,xxx.shape)
    ax.plot(xxx[:l],rr,'r')
    _=fig.canvas.draw();
    #plt.plot(xx,rr,'r')



interact(show_args,
         Signal =['Step','Ramp','Flat','Pulse'],
         FilterType =['Low Pass','1st Order High Pass','2nd Order High Pass'],
         a=widgets.FloatSlider(min=2, max=100, step=1, value=3, description="Filter width", continuous_update=False),
         sd=widgets.FloatSlider(min=0.0, max=0.5, step=0.01,value = 0.0, description="noise sd",continuous_update=False)
         )
