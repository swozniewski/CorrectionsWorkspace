#!/usr/bin/env python
import ROOT
import imp
import json
from array import array
wsptools = imp.load_source('wsptools', 'workspaceTools.py')


def GetFromTFile(str):
    print str
    f = ROOT.TFile(str.split(':')[0])
    obj = f.Get(str.split(':')[1]).Clone()
    f.Close()
    return obj

# Boilerplate
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.RooWorkspace.imp = getattr(ROOT.RooWorkspace, 'import')
ROOT.TH1.AddDirectory(0)
ROOT.gROOT.LoadMacro("CrystalBallEfficiency.cxx+")

w = ROOT.RooWorkspace('w')


### KIT electron/muon tag and probe results
loc = 'inputs/KIT/embedded'

SF_histsToWrap = [
    (loc+'/ZmmTP_Data_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',                    'm_id_data'),
    (loc+'/ZmmTP_Embedding_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',              'm_id_mc'),
    (loc+'/ZmmTP_Data_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',                    'm_iso_data'),
    (loc+'/ZmmTP_Embedding_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',              'm_iso_mc'),
    (loc+'/ZmmTP_Data_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',                    'm_aiso1_data'),
    (loc+'/ZmmTP_Embedding_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',              'm_aiso1_mc'),
    (loc+'/ZmmTP_Data_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',                    'm_aiso2_data'),
    (loc+'/ZmmTP_Embedding_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',              'm_aiso2_mc'),
    (loc+'/ZmmTP_Data_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',                    'm_trg_data'),
    (loc+'/ZmmTP_Embedding_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',              'm_trg_mc')]



for task in SF_histsToWrap:
 wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_iso_binned_data', ['m_iso_data', 'm_aiso1_data', 'm_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_iso_binned_mc', ['m_iso_mc', 'm_aiso1_mc', 'm_aiso2_mc'])


for t in ['id', 'iso', 'trg', 'trg_binned', 'iso_binned']:
    w.factory('expr::m_%s_ratio("@0/@1", m_%s_data, m_%s_mc)' % (t, t, t))


### KIT electron/muon tag and probe results
loc = 'inputs/KIT/embedded'

SF_histsToWrap = [
    (loc+'/ZeeTP_Data_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',                    'e_id_data'),
    (loc+'/ZeeTP_Embedding_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',              'e_id_mc'),
    (loc+'/ZeeTP_Data_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',                    'e_iso_data'),
    (loc+'/ZeeTP_Embedding_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',              'e_iso_mc'),
    (loc+'/ZeeTP_Data_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',                    'e_aiso1_data'),
    (loc+'/ZeeTP_Embedding_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',              'e_aiso1_mc'),
    (loc+'/ZeeTP_Data_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',                    'e_aiso2_data'),
    (loc+'/ZeeTP_Embedding_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',              'e_aiso2_mc'),
    (loc+'/ZeeTP_Data_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',                    'e_trg_data'),
    (loc+'/ZeeTP_Embedding_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',              'e_trg_mc'),
    (loc+'/ZeeTP_Data_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',                    'e_trg_aiso1_data'),
    (loc+'/ZeeTP_Embedding_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',              'e_trg_aiso1_mc'),
    (loc+'/ZeeTP_Embedding_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',                    'e_trg_aiso2_data'),
    (loc+'/ZeeTP_Embedding_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',              'e_trg_aiso2_mc')
]

for task in SF_histsToWrap:
 wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])
                          
                          
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_iso_binned_data', ['e_iso_data', 'e_aiso1_data', 'e_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_iso_binned_mc', ['e_iso_mc', 'e_aiso1_mc', 'e_aiso2_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg_binned_data', ['e_trg_data', 'e_trg_aiso1_data', 'e_trg_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg_binned_mc', ['e_trg_mc', 'e_trg_aiso1_mc', 'e_trg_aiso2_mc'])
                                   

for t in ['id', 'iso', 'trg', 'trg_binned', 'iso_binned']:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))

### KIT electron/muon tag and probe results
loc = 'inputs/KIT/embedded'

for task in Sel_histsToWrap:
    wsptools.SafeWrapHist(w, ['expr::t_abs_eta("TMath::Abs(@0)",t_eta[0])','t_pt'],
                          GetFromTFile(task[0]), name=task[1])
for t in ['sel_id', 'sel_iso','sel_trg']:
    w.factory('expr::t_%s_ratio("(1.0)/@0", t_%s_data)' % (t, t))


### Hadronic tau trigger efficiencies
with open('fitresults_tt_moriond2017.json') as jsonfile:
    pars = json.load(jsonfile)
    for tautype in ['genuine', 'fake']:
        for iso in ['VLooseIso','LooseIso','MediumIso','TightIso','VTightIso','VVTightIso']:
            for dm in ['dm0', 'dm1', 'dm10']:
                label = '%s_%s_%s' % (tautype, iso, dm)
                x = pars['data_%s' % (label)]
                w.factory('CrystalBallEfficiency::t_%s_tt_data(t_pt[0],%g,%g,%g,%g,%g)' % (
                    label, x['m_{0}'], x['sigma'], x['alpha'], x['n'], x['norm']
                ))

                x = pars['mc_%s' % (label)]
                w.factory('CrystalBallEfficiency::t_%s_tt_mc(t_pt[0],%g,%g,%g,%g,%g)' % (
                    label, x['m_{0}'], x['sigma'], x['alpha'], x['n'], x['norm']
                ))
            label = '%s_%s' % (tautype, iso)
            wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                               't_%s_tt_data' % label, ['t_%s_dm0_tt_data' % label, 't_%s_dm1_tt_data' % label, 't_%s_dm10_tt_data' % label])
            wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                               't_%s_tt_mc' % label, ['t_%s_dm0_tt_mc' % label, 't_%s_dm1_tt_mc' % label, 't_%s_dm10_tt_mc' % label])
            w.factory('expr::t_%s_tt_ratio("@0/@1", t_%s_tt_data, t_%s_tt_mc)' % (label, label, label))

w.importClassCode('CrystalBallEfficiency')

w.Print()
w.writeToFile('htt_scalefactors_v16_5_embedded.root')
w.Delete()
