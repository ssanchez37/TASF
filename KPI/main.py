import KPI.funciones as fnc
import numpy as np
import pandas as pd
import warnings as wn

wn.simplefilter("ignore")


# noinspection PyGlobalUndefined
def kpis(file, budget, mandays):
    global t1, inc_time_tot, inc_tot, inc_time_ind, t2, inc_cost_ind, inc_cost_tot, cc_time_tot, t4, cc_time_ind, \
        cc_cost_tot, t5, cc_cost_ind
    t = pd.read_excel(file)
    tc = pd.read_excel('media/CostoRecurso.xlsx')
    project = t['Nombre'][0]
    project = str(project)
    print(project)
    l1 = str('------------------------ Retrabajo por incidencias ------------------------')
    print(l1)
    col_tiempo_empleado = t["Tiempo empleado"]
    n = len(col_tiempo_empleado)
    col_tiempo_empleado_datetime = np.zeros(n)
    for x in range(n):
        col_tiempo_empleado_datetime[x] = fnc.excel_date(col_tiempo_empleado[x])

    col_incidencias = t["Incidencia / Error"]
    col_incidencias_id = t["Id Incidencia"]
    tiempo_total = col_tiempo_empleado_datetime[0]
    tiempo_total_mins = tiempo_total * 60
    incidencias_index = []
    for i in range(n):
        if col_incidencias.values.item(i) == 1:
            incidencias_index.append(i)

    n = len(incidencias_index)
    incidencias_tiempos = np.zeros(n)
    incidencias_id = np.zeros(n)
    if n > 0:
        for i in range(n):
            m = incidencias_index[i]
            incidencias_tiempos[i] = col_tiempo_empleado_datetime[m]
            incidencias_id[i] = col_incidencias_id[m]
        incidencias_tiempos_mins = incidencias_tiempos * 60
        tiempo_total_incidencias = sum(incidencias_tiempos_mins)
        r_inc = tiempo_total_incidencias/tiempo_total_mins
        r_inc_porc = r_inc * 100
        num = len(np.unique(incidencias_id))

        inc_tot = str("En el proyecto existen " + str(num) + " incidencias en total.")
        print(inc_tot)
        inc_time_tot = str("El porcentaje del tiempo de retrabajo por el total de incidencias es: %.2f" % r_inc_porc +
                           "%.")
        print(inc_time_tot)
        asignados_inc = t["Asignado"][incidencias_index]
        incidencias_id_series = pd.Series(incidencias_id, name="ID")
        incidencias_id_series.index = incidencias_index
        incidencias_tiempos_series = pd.Series(incidencias_tiempos, name="Tiempo")
        incidencias_tiempos_series.index = incidencias_index
        asignados_inc = pd.concat([asignados_inc, incidencias_id_series, incidencias_tiempos_series], axis=1)
        asignados_inc = asignados_inc.join(tc.set_index('Asignado'), on='Asignado')
        asignados_inc = asignados_inc.sort_values('ID')
        asignados_inc.index = range(n)
        asignados = asignados_inc["Asignado"]
        costos = asignados_inc["CostoHora"]
        incidencias_tiempos_hour = asignados_inc["Tiempo"]
        incidencias_id = asignados_inc["ID"]
        costos_inc = incidencias_tiempos_hour * costos
        costos_inc_total = sum(costos_inc)
        incidencias_tiempos_mins = incidencias_tiempos_hour * 60
        tiempo_incidencias_ind = incidencias_tiempos_mins/tiempo_total_mins
        t1 = str("El porcentaje del tiempo total de retrabajo por cada incidencia es:")
        print(t1)
        inc_time_ind = []
        for i in range(n):
            if tiempo_incidencias_ind[i] != 0:
                texto = "Responsable: %s" % str(asignados[i])
                inc_time_ind.append("Incidencia #%d = %.2f" % (incidencias_id[i], tiempo_incidencias_ind[i]*100) +
                                    "% - " + texto)
                print("Incidencia #%d = %.2f" % (incidencias_id[i], tiempo_incidencias_ind[i]*100) + "% - " + texto)
        inc_cost_tot = ("El costo total del retrabajo por incidencias es: $ %.2f" % costos_inc_total + ".")
        print(inc_cost_tot)
        t2 = str("El costo de retrabajo por cada incidencia es:")
        print(t2)
        inc_cost_ind = []
        for i in range(n):
            if costos_inc[i] != 0:
                texto = "Responsable: %s" % str(asignados[i])
                inc_cost_ind.append('Incidencia #%d = $%.2f' % (incidencias_id[i], costos_inc[i]) + " - " + texto)
                print('Incidencia #%d = $%.2f' % (incidencias_id[i], costos_inc[i]) + " - " + texto)
    else:
        print("No se detectaron incidencias")

    t3 = str("----------------- Retrabajo por Controles de Cambios ------------------")
    print(t3)

    col_id_cc = t["Id Control de Cambio"]
    n = len(col_tiempo_empleado)
    cc_index = []
    for i in range(n):
        if type(col_id_cc.values.item(i)) != float:
            cc_index.append(i)

    n = len(cc_index)
    cc_tiempos = np.zeros(n)

    if n > 0:
        for i in range(n):
            m = cc_index[i]
            cc_tiempos[i] = col_tiempo_empleado_datetime[m]

        cc_tiempos_mins = cc_tiempos * 60
        cc_tiempos_ind = cc_tiempos_mins / tiempo_total_mins
        tiempo_total_cc = sum(cc_tiempos_mins)
        r_cc = tiempo_total_cc/tiempo_total_mins
        r_cc_porc = r_cc * 100

        cc_time_tot = str("El porcentaje del tiempo de retrabajo por control de cambios es de: %.2f" % r_cc_porc + "%")
        print(cc_time_tot)
        t4 = str("El porcentaje del tiempo total de retrabajo por cada control de cambios es:")
        print(t4)
        cc_time_ind = []
        j = 1
        for i in range(n):
            if cc_tiempos_ind[i] != 0:
                cc_time_ind.append('CC_%d = %.2f' % (j, cc_tiempos_ind[i]*100) + "%")
                print('CC_%d = %.2f' % (j, cc_tiempos_ind[i] * 100) + "%")
                j += 1

        asignados_cc = t["Asignado"][cc_index]
        cc_tiempos_series = pd.Series(cc_tiempos, name="Tiempo")
        cc_tiempos_series.index = cc_index
        asignados_cc = pd.concat([asignados_cc, cc_tiempos_series], axis=1)
        asignados_cc = asignados_cc.join(tc.set_index('Asignado'), on='Asignado')
        costos = asignados_cc["CostoHora"]
        cc_tiempos_hours = asignados_cc["Tiempo"]
        costos_cc = cc_tiempos_hours * costos
        costos_cc_total = sum(costos_cc)
        cc_cost_tot = str("El costo total del retrabajo por Control de Cambios es: $%.2f" % costos_cc_total)
        print(cc_cost_tot)

        t5 = str("El costo del retrabajo por cada control de cambios es: ")
        print(t5)

        cc_cost_ind = []
        j = 1
        for i in range(n):
            m = cc_index[i]
            if costos_cc[m] != 0:
                cc_cost_ind.append("CC_%d = $%.2f" % (j, costos_cc[m]))
                print("CC_%d = $%.2f" % (j, costos_cc[m]))
                j += 1

    else:
        print("No se detectaron controles de cambios")

    t6 = str("----------------- Métrica del valor ganado de costos --------------------")
    print(t6)
    progreso = t['Progreso'][0]
    progreso_mat = progreso / 100

    # bcws = 74983.04
    bcws = float(budget)
    ev = progreso_mat * bcws
    bcws_costo = str("BCWS (Costo Presupuestado del Trabajo Planificado) = $%.2f" % bcws)
    print(bcws_costo)
    ev_costo = str("El valor ganado (EV) es de $%.2f con un progreso de %.2f" % (ev, progreso) + "%")
    print(ev_costo)

    tiempo_empleado = col_tiempo_empleado_datetime
    tiempo_empleado = np.delete(tiempo_empleado, 0)
    tiempo_empleado = np.delete(tiempo_empleado, -1)
    tiempo_empleado_nonzero = tiempo_empleado.nonzero()
    tiempo_empleado_nonzero = np.asarray(tiempo_empleado_nonzero)
    tiempo_empleado_nonzero = tiempo_empleado_nonzero.flatten()
    t_aux = t
    t_aux = t_aux.drop(index=t_aux.index[0])
    t_aux = t_aux.drop(index=t_aux.index[-1])
    t_aux.reset_index(drop=True, inplace=True)
    t_asignado = t_aux['Asignado'][tiempo_empleado_nonzero]
    t_asignado.reset_index(drop=True, inplace=True)
    t_tiempo_empleado = t_aux['Tiempo empleado'][tiempo_empleado_nonzero]
    t_tiempo_empleado.reset_index(drop=True, inplace=True)
    k = len(t_tiempo_empleado)
    t_tiempo_empleado_datetime = np.zeros(k)
    for i in range(k):
        t_tiempo_empleado_datetime[i] = fnc.excel_date(t_tiempo_empleado[i])

    t_asignado_index = t_asignado.notnull()
    t_asignado_true_index = []
    for i in range(k):
        if t_asignado_index[i]:
            t_asignado_true_index.append(i)

    t_tiempo_empleado_datetime = pd.Series(t_tiempo_empleado_datetime, name="Tiempo empleado")
    t_joined = pd.concat([t_asignado, t_tiempo_empleado_datetime], axis=1)
    t_asignado_true_index = np.array(t_asignado_true_index)
    t_joined = t_joined.loc[t_asignado_true_index, :]
    t_joined.reset_index(drop=True, inplace=True)
    t_joined = t_joined.join(tc.set_index('Asignado'), on='Asignado')
    t_joined_tiempo_hours = t_joined["Tiempo empleado"]
    t_joined_costo = t_joined["CostoHora"]
    costo_individual = t_joined_tiempo_hours * t_joined_costo
    acwp = sum(costo_individual)
    acwp_costo = str("ACWP (Costo Actual del Trabajo Realizado): $%.2f" % acwp)
    print(acwp_costo)
    pr = (ev/acwp)
    if pr > 1:
        status = 'SUPERIOR'
    elif pr < 1:
        status = 'INFERIOR'
    else:
        status = 'IGUAL'

    pr_costo = str('La relación de rendimiento (PR) es: %.2f, es decir que el rendimiento del proyecto es ' % pr +
                   status + ' al esperado')
    print(pr_costo)
    pf = bcws/pr

    pf_costo = str('El pronóstico previsto (PF) es que el proyecto tenga un costo de: $%.2f' % pf)
    print(pf_costo)
    cv = ev - acwp

    if cv > 0:
        status = 'POR DEBAJO'
    elif cv < 0:
        status = 'POR ENCIMA'
    else:
        status = 'IGUAL'

    cv_costo = str('La variación de costo (CV) es: $%.2f e indica que el proyecto se encuentra ' % cv + status +
                   ' del presupuesto')
    print(cv_costo)

    t7 = str('-------------- Métrica del valor ganado (EV) de tiempos ----------------')
    print(t7)

    mandays = float(mandays)
    mandays_hours = mandays * 8
    t = t.drop(index=t_aux.index[0])
    t_ev_asignado = t['Asignado']
    t_ev_asignado.reset_index(drop=True, inplace=True)
    t_ev_index = t_ev_asignado.notnull()
    t_ev_true_index = []
    k = len(t_ev_index)
    for i in range(k):
        if t_ev_index[i]:
            t_ev_true_index.append(i)
    bcws_time = t['Trabajo']
    bcws_time = bcws_time[bcws_time.index[-1]]
    bcws_time = fnc.excel_date(bcws_time)
    mandays_tiempo = ("BCWS (Tiempo Presupuestado del Trabajo Planificado - original) = %.fhrs" % mandays_hours)
    print(mandays_tiempo)
    ev_mandays = progreso_mat * mandays_hours
    ev_mandays_mins = ev_mandays * 60
    ev_mandays_h, ev_mandays_m = fnc.min2hour(ev_mandays_mins)
    ev_mandays_time = str("El valor ganado (EV) con respecto al BCWS original es: %d:%2dhrs. Con un progreso de %d" %
                          (ev_mandays_h, ev_mandays_m, progreso) + "%")
    print(ev_mandays_time)

    ev_hours = progreso_mat * bcws_time

    bcws_tiempo = ("BCWS (Tiempo Presupuestado del Trabajo Planificado) = %.fhrs" % bcws_time)
    print(bcws_tiempo)
    ev_mins = ev_hours * 60
    ev_h, ev_m = fnc.min2hour(ev_mins)
    ev_time = str("El valor ganado (EV) en horas es: %d:%2dhrs. Con un progreso de %d" % (ev_h, ev_m, progreso) + "%")
    print(ev_time)
    acwp_hours = tiempo_total
    acwp_mins = acwp_hours * 60
    acwp_h, acwp_m = fnc.min2hour(acwp_mins)

    acwp_time = str("ACWP (Tiempo Actual del Trabajo Realizado): %d:%2dhrs" % (acwp_h, acwp_m))
    print(acwp_time)
    pr_mandays_time = ev_mandays/acwp_hours
    if pr_mandays_time > 1:
        status = 'SUPERIOR'
    elif pr_mandays_time < 1:
        status = 'INFERIOR'
    else:
        status = 'IGUAL'

    pr_mandays_tiempo = str("La relación de rendimiento (PR) es: %.2f, es decir que el rendimiento del proyecto es "
                            % pr_mandays_time + status + ' al esperado.')
    print(pr_mandays_tiempo)

    pf_mandays_time = mandays_hours / pr_mandays_time
    pf_mandays_time_mins = pf_mandays_time * 60
    pf_mandays_h, pf_mandays_m = fnc.min2hour(pf_mandays_time_mins)

    pf_mandays_time = str("El pronóstico previsto (PF) es que el tiempo de finalización del proyecto sea de: %d:%2dhrs."
                          % (pf_mandays_h, pf_mandays_m))
    print(pf_mandays_time)

    sv_mandays = ev_mandays - acwp_hours

    if sv_mandays > 0:
        status = 'POR DEBAJO'
    elif sv_mandays < 0:
        status = 'POR ENCIMA'
    else:
        status = 'IGUAL'

    sv_mandays_mins = sv_mandays * 60
    sv_mandays_h, sv_mandays_m = fnc.min2hour(sv_mandays_mins)

    sv_mandays_time = str("La variación de tiempo (SV) es: %d:%2dhrs. e indica que el proyecto se encuentra " %
                          (sv_mandays_h, sv_mandays_m) + status + " del tiempo planificado.")
    print(sv_mandays_time)

    pr_time = ev_hours/acwp_hours
    if pr_time > 1:
        status = 'SUPERIOR'
    elif pr_time < 1:
        status = 'INFERIOR'
    else:
        status = 'IGUAL'

    pr_tiempo = str("La relación de rendimiento (PR) es: %.2f, es decir que el rendimiento del proyecto es " % pr_time +
                    status + ' al esperado.')
    print(pr_tiempo)

    pf_time = bcws_time/pr_time
    pf_time_mins = pf_time * 60
    pf_h, pf_m = fnc.min2hour(pf_time_mins)

    pf_time = str("El pronóstico previsto (PF) es que el tiempo de finalización del proyecto sea de: %d:%2dhrs." %
                  (pf_h, pf_m))
    print(pf_time)

    sv = ev_hours - acwp_hours

    if sv > 0:
        status = 'POR DEBAJO'
    elif sv < 0:
        status = 'POR ENCIMA'
    else:
        status = 'IGUAL'

    sv_mins = sv * 60
    sv_h, sv_m = fnc.min2hour(sv_mins)

    sv_time = str("La variación de tiempo (SV) es: %d:%2dhrs. e indica que el proyecto se encuentra " % (sv_h, sv_m) +
                  status + " del tiempo planificado.")
    print(sv_time)

    return project, l1, inc_tot, inc_time_tot, t1, inc_time_ind, inc_cost_tot, t2, inc_cost_ind, t3, cc_time_tot, t4, \
        cc_time_ind, cc_cost_tot, t5, cc_cost_ind, t6, bcws_costo, ev_costo, acwp_costo, pr_costo, pf_costo, cv_costo, \
        t7, bcws_tiempo, ev_time, acwp_time, pr_tiempo, pf_time, sv_time, mandays_tiempo, ev_mandays_time, \
        pr_mandays_tiempo, pf_mandays_time, sv_mandays_time
