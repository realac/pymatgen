#!/usr/bin/env python

"""
This module provides classes and utilities to plot band structures
"""




__author__="Geoffroy Hautier, Shyue Ping Ong, Michael Kocher"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "1.0"
__maintainer__ = "Geoffroy Hautier"
__email__ = "geoffroy@uclouvain.be"
__status__ = "Development"
__date__ ="March 14, 2012"

class BSPlotter(object):
    
    def __init__(self, bs):
        """
        Arguments:
            bs - a Bandstructure_line object.
        """
        self._bs=bs
        self._nb_bands=bs._nb_bands
    
    @property
    def bs_plot_data(self):   
        energy=[]
        occup=[]
        distance=[self._bs._distance[j] for j in range(len(self._bs._kpoints))]
        ticks=self.get_ticks()
        for i in range(self._nb_bands):
            #pylab.plot([self._distance[j] for j in range(len(self._kpoints))],[self._bands[i]['energy'][j] for j in range(len(self._kpoints))],'b-',linewidth=5)
            energy.append([self._bs._bands[i]['energy'][j] for j in range(len(self._bs._kpoints))])
            occup.append([self._bs._bands[i]['occup'][j] for j in range(len(self._bs._kpoints))])
        
        return {'ticks':ticks,'distances':distance,'energy':energy,'occup':occup}
        
    def showplot(self):
        """
        plot the band structure.
        """
        import pylab
        from matplotlib import rc
        rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],'size':20})
        rc('text', usetex=True)
        pylab.figure
        data=self.bs_plot_data
        energy=[]
        occup=[]
        distance=[self._bs._distance[j] for j in range(len(self._bs._kpoints))]
        ticks=self.get_ticks()
        for i in range(self._nb_bands):
            pylab.plot(data['distances'],data['energy'][i],'b-',linewidth=5)
            
        ticks=self.get_ticks()
        for i in range(len(ticks['label'])):
            if(ticks['label'][i]!=None):
                pylab.axvline(ticks['distance'][i],color='k')
        
        #pylab.axhline(self._efermi, color='r')
            
        pylab.gca().set_xticks(ticks['distance'])
        pylab.gca().set_xticklabels(ticks['label'])
        pylab.xlabel('Kpoints', fontsize = 'large')
        pylab.ylabel('Energy(eV)', fontsize = 'large')
        vbm=self._bs.getVBM()
        cbm=self._bs.getCBM()
        if(cbm['kpoint'].label!=None):
            for i in range(len(self._bs._kpoints)):
                if(self._bs._kpoints[i].label==cbm['kpoint'].label):
                    pylab.scatter(self._bs._distance[i],cbm['energy'],color='r',marker='o',s=100)
        else:
            pylab.scatter(self._bs._distance[cbm['kpoint_index']],cbm['energy'],color='r',marker='o',s=100)
            
        if(vbm['kpoint'].label!=None):
            for i in range(len(self._bs._kpoints)):
                if(self._bs._kpoints[i].label==vbm['kpoint'].label):
                    pylab.scatter(self._bs._distance[i],vbm['energy'],color='G',marker='o',s=100)
        else:
            pylab.scatter(self._bs._distance[vbm['kpoint_index']],vbm['energy'],color='g',marker='o',s=100)


        pylab.ylim(vbm['energy']-4,cbm['energy']+4)
        pylab.legend()
        pylab.show()
        
        
        
        
    def get_ticks(self):
        """
        get all ticks and labels for a band structure plot
        """
        tick_distance=[]
        tick_labels=[]
        previous_label=self._bs._kpoints[0].label
        previous_branch=self._bs.get_branch_name(0)
        for i in range(len(self._bs._kpoints)):
            c=self._bs._kpoints[i]
            if(c.label!=None):
                tick_distance.append(self._bs._distance[i])
                if(c.label!=previous_label and previous_branch!=self._bs.get_branch_name(i)):
                    label1=c.label
                    if(label1.startswith("\\") or label1.find("_")!=-1):
                        label1="$"+label1+"$"
                    label0=previous_label
                    if(label0.startswith("\\") or label0.find("_")!=-1):
                        label0="$"+label0+"$"
                    tick_labels.pop()
                    tick_distance.pop()
                    tick_labels.append(label0+"$|$"+label1)
                    #print label0+","+label1
                else:
                    if(c.label.startswith("\\") or c.label.find("_")!=-1):
                        tick_labels.append("$"+c.label+"$")
                    else:
                        tick_labels.append(c.label)
                previous_label=c.label
                previous_branch=self._bs.get_branch_name(i)
        return {'distance':tick_distance,'label':tick_labels}   