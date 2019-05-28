#!/usr/bin/env python
import ROOT
import imp
import json
from array import array
wsptools = imp.load_source('wsptools', 'workspaceTools.py')


def GetFromTFile(str):
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


# ### KIT electron/muon tag and probe results
# TODO measure

# DESY electron/muon tag and probe results
# Muons
loc = 'inputs/LeptonEfficiencies'

desyHistsToWrap = [
    (loc+'/Muon/Run2016_legacy/Muon_Run2016_legacy_IdIso.root',
     'MC',   'm_idiso_desy_mc'),
    (loc+'/Muon/Run2016_legacy/Muon_Run2016_legacy_IdIso.root',
     'Data', 'm_idiso_desy_data'),
    (loc+'/Muon/Run2016_legacy/Muon_Run2016_legacy_IsoMu22.root',
     'MC',   'm_trgIsoMu22_desy_mc'),
    (loc+'/Muon/Run2016_legacy/Muon_Run2016_legacy_IsoMu22.root',
     'Data', 'm_trgIsoMu22_desy_data'),
    (loc+'/Muon/Run2016_legacy/Muon_Run2016_legacy_IsoMu24.root',
     'MC',   'm_trgIsoMu24_desy_mc'),
    (loc+'/Muon/Run2016_legacy/Muon_Run2016_legacy_IsoMu24.root',
     'Data', 'm_trgIsoMu24_desy_data'),
]

for task in desyHistsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          wsptools.ProcessDESYLeptonSFs(task[0], task[1], task[2]), name=task[2])
for t in ['idiso_desy', 'trgIsoMu22_desy', 'trgIsoMu24_desy']:
    w.factory('expr::m_%s_ratio("@0/@1", m_%s_data, m_%s_mc)' % (t, t, t))

# Electrons
desyHistsToWrap = [
    (loc+'/Electron/Run2016_legacy/Electron_Run2016_legacy_IdIso.root',
     'MC',   'e_idiso_desy_mc'),
    (loc+'/Electron/Run2016_legacy/Electron_Run2016_legacy_IdIso.root',
     'Data', 'e_idiso_desy_data'),
    (loc+'/Electron/Run2016_legacy/Electron_Run2016_legacy_Ele25.root',
     'MC',   'e_trgEle25_desy_mc'),
    (loc+'/Electron/Run2016_legacy/Electron_Run2016_legacy_Ele25.root',
     'Data', 'e_trgEle25_desy_data')
]
for task in desyHistsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          wsptools.ProcessDESYLeptonSFs(task[0], task[1], task[2]), name=task[2])

for t in ['idiso_desy', 'trgEle25_desy']:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))


# LO DYJetsToLL Z mass vs pT correction
histsToWrap = [
    ('inputs/DYWeights/zpt_weights_summer2016_v2.root:zptmass_histo', 'zptmass_weight_nom')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['z_gen_mass', 'z_gen_pt'],
                          GetFromTFile(task[0]), name=task[1])

w.importClassCode('CrystalBallEfficiency')

w.Print()
w.writeToFile('output/htt_scalefactors_legacy_v16_1.root')
w.Delete()
