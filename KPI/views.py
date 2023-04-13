import os
import subprocess as sp
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from KPI.main import kpis
from djangoProject.settings import MEDIA_ROOT

# Create your views here.


def simple_upload(request):
    if request.method == 'POST' and request.FILES['wrike_file']:
        myfile = request.FILES['wrike_file']
        budget = request.POST['budget']
        mandays = request.POST['mandays']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        if uploaded_file_url:
            print(MEDIA_ROOT)
            try:
                output, l1, inc_tot, inc_time_tot, t1, inc_time_ind, inc_cost_tot, t2, inc_cost_ind, t3, cc_time_tot,\
                    t4, cc_time_ind, cc_cost_tot, t5, cc_cost_ind, t6, bcws_costo, ev_costo, acwp_costo, pr_costo, \
                    pf_costo, cv_costo, t7, bcws_time, ev_time, acwp_time, pr_time, pf_time, sv_time, mandays_tiempo, \
                    ev_mandays_time, pr_mandays_tiempo, pf_mandays_time, sv_mandays_time = kpis(myfile, budget, mandays)
                os.remove((os.path.join(MEDIA_ROOT + '/' + filename)))
            except sp.CalledProcessError as e:
                print(e)
        return render(request, 'KPI/index.html', locals())
    return render(request, 'KPI/index.html')
