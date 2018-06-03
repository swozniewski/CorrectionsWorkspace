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

loc = 'inputs/ICSF/'

histsToWrap = [
    (loc+'2017/SingleLepton/muon_SFs.root:data_id_eff', 'm_id_data'),
    (loc+'2017/SingleLepton/muon_SFs.root:ZLL_id_eff', 'm_id_mc'),
    (loc+'2017/SingleLepton/muon_SFs.root:data_iso_eff', 'm_iso_data'),
    (loc+'2017/SingleLepton/muon_SFs.root:ZLL_iso_eff', 'm_iso_mc'),
    (loc+'2017/SingleLepton/muon_SFs.root:data_idiso_eff', 'm_idiso_data'),
    (loc+'2017/SingleLepton/muon_SFs.root:ZLL_idiso_eff', 'm_idiso_mc'),
    (loc+'2017/SingleLepton/muon_SFs.root:data_trg_eff', 'm_trg_data'),
    (loc+'2017/SingleLepton/muon_SFs.root:ZLL_trg_eff', 'm_trg_mc')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_trg_binned_data', ['m_trg_data', 'm_trg_data', 'm_trg_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_trg_mc', ['m_trg_mc', 'm_trg_mc', 'm_trg_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_idiso_binned_data', ['m_idiso_data', 'm_idiso_data', 'm_idiso_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'm_idiso_mc', ['m_idiso_mc', 'm_idiso_mc', 'm_idiso_mc'])

for t in ['trg', 'trg_binned', 'id', 'iso', 'idiso', 'idiso_binned' ]:
    w.factory('expr::m_%s_ratio("@0/@1", m_%s_data, m_%s_mc)' % (t, t, t))
        
histsToWrap = [
    (loc+'2017/SingleLepton/electron_SFs.root:data_id_eff', 'e_id_data'),
    (loc+'2017/SingleLepton/electron_SFs.root:ZLL_id_eff', 'e_id_mc'),
    (loc+'2017/SingleLepton/electron_SFs.root:data_iso_eff', 'e_iso_data'),
    (loc+'2017/SingleLepton/electron_SFs.root:ZLL_iso_eff', 'e_iso_mc'),
    (loc+'2017/SingleLepton/electron_SFs.root:data_idiso_eff', 'e_idiso_data'),
    (loc+'2017/SingleLepton/electron_SFs.root:ZLL_idiso_eff', 'e_idiso_mc'),
    (loc+'2017/SingleLepton/electron_SFs.root:data_trg_eff', 'e_trg_data'),
    (loc+'2017/SingleLepton/electron_SFs.root:ZLL_trg_eff', 'e_trg_mc')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.30, 0.50],
                                   'e_trg_binned_data', ['e_trg_data', 'e_trg_data', 'e_trg_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.30, 0.50],
                                   'e_trg_mc', ['e_trg_mc', 'e_trg_mc', 'e_trg_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.30, 0.50],
                                   'e_idiso_binned_data', ['e_idiso_data', 'e_idiso_data', 'e_idiso_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.10, 0.30, 0.50],
                                   'e_idiso_mc', ['e_idiso_mc', 'e_idiso_mc', 'e_idiso_mc'])


for t in ['trg', 'trg_binned', 'id', 'iso', 'idiso', 'idiso_binned' ]:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))


## IC em qcd os/ss weights
wsptools.SafeWrapHist(w, ['expr::m_pt_max100("min(@0,100)",m_pt[0])', 'expr::e_pt_max100("min(@0,100)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_factors_maiso.root:qcd_factors'), 'em_qcd_factors')
wsptools.SafeWrapHist(w, ['expr::m_pt_max100("min(@0,100)",m_pt[0])', 'expr::e_pt_max100("min(@0,100)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_factors_bothaiso.root:qcd_factors'), 'em_qcd_factors_bothaiso')
wsptools.SafeWrapHist(w, ['expr::dR_max4p5("min(@0,4.5)",dR[0])','expr::njets_max1("min(@0,1)",njets[0])'],  GetFromTFile(loc+'/em_qcd/em_aiso_iso_extrap.root:extrap_uncert'), 'em_qcd_extrap_uncert')

w.factory('expr::em_qcd_0jet("(2.162-0.05135*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_1jet("(2.789-0.2712*@0)*@1",dR,em_qcd_factors)')

w.factory('expr::em_qcd_0jet_bothaiso("(3.212-0.2186*@0)*@1",dR,em_qcd_factors_bothaiso)')
w.factory('expr::em_qcd_1jet_bothaiso("(3.425-0.3629*@0)*@1",dR,em_qcd_factors_bothaiso)')

w.factory('expr::em_qcd_0jet_shapeup("(2.162-(0.05135-0.0583)*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_0jet_shapedown("(2.162-(0.05135+0.0583)*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_1jet_shapeup("(2.789-(0.2712-0.0390)*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_1jet_shapedown("(2.789-(0.2712+0.0390)*@0)*@1",dR,em_qcd_factors)')

w.factory('expr::em_qcd_0jet_rateup("(2.162+0.192-0.05135*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_0jet_ratedown("(2.162-0.192-0.05135*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_1jet_rateup("(2.789+0.0105-0.2712*@0)*@1",dR,em_qcd_factors)')
w.factory('expr::em_qcd_1jet_ratedown("(2.789-0.0105-0.2712*@0)*@1",dR,em_qcd_factors)')

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_binned', ['em_qcd_0jet','em_qcd_1jet'])

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_binned_bothaiso', ['em_qcd_0jet_bothaiso','em_qcd_1jet_bothaiso'])


wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_shapeup_binned', ['em_qcd_0jet_shapeup','em_qcd_1jet_shapeup'])

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_shapedown_binned', ['em_qcd_0jet_shapedown','em_qcd_1jet_shapedown'])

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_rateup_binned', ['em_qcd_0jet_rateup','em_qcd_1jet_rateup'])

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_ratedown_binned', ['em_qcd_0jet_ratedown','em_qcd_1jet_ratedown'])


wsptools.SafeWrapHist(w, ['expr::m_pt_max100("min(@0,100)",m_pt[0])', 'expr::e_pt_max100("min(@0,100)",e_pt[0])'],  GetFromTFile(loc+'/em_qcd/em_qcd_factors_2.root:qcd_factors'), 'em_qcd_factors_bothaiso')

w.factory('expr::em_qcd_0jet_bothaiso("(3.208-0.217*@0)*@1",dR,em_qcd_factors_bothaiso)')
w.factory('expr::em_qcd_1jet_bothaiso("(3.426-0.3628*@0)*@1",dR,em_qcd_factors_bothaiso)')

wsptools.MakeBinnedCategoryFuncMap(w, 'njets', [0,1,10000],
                                   'em_qcd_osss_binned_bothaiso', ['em_qcd_0jet_bothaiso','em_qcd_1jet_bothaiso'])

w.factory('expr::em_qcd_extrap_up("@0*@1",em_qcd_osss_binned,em_qcd_extrap_uncert)')
w.factory('expr::em_qcd_extrap_down("@0*(2-@1)",em_qcd_osss_binned,em_qcd_extrap_uncert)')

w.factory('expr::em_qcd_bothaiso_extrap_up("@0*@1",em_qcd_osss_binned_bothaiso,em_qcd_extrap_uncert)')
w.factory('expr::em_qcd_bothaiso_extrap_down("@0*(2-@1)",em_qcd_osss_binned_bothaiso,em_qcd_extrap_uncert)')

### Electron tracking efficiency scale factor from the egamma POG
loc = 'inputs/EGammaPOG'

electron_trk_eff_hist = GetFromTFile(loc+'/egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root:EGamma_SF2D')
wsptools.SafeWrapHist(w, ['e_sceta','e_pt'], electron_trk_eff_hist, name='e_trk_ratio')


### LO DYJetsToLL Z mass vs pT correction
histsToWrap = [
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo'                 , 'zpt_weight_nom'         ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_ESUp'            , 'zpt_weight_esup'        ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_ESDown'          , 'zpt_weight_esdown'      ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_TTUp'            , 'zpt_weight_ttup'        ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_TTDown'          , 'zpt_weight_ttdown'      ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_StatM400pT0Up'   , 'zpt_weight_statpt0up'   ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_StatM400pT0Down' , 'zpt_weight_statpt0down' ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_StatM400pT40Up'  , 'zpt_weight_statpt40up'  ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_StatM400pT40Down', 'zpt_weight_statpt40down'),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_StatM400pT80Up'  , 'zpt_weight_statpt80up'  ),
    ('inputs/DYWeights/zpt_weights_summer2016_v5.root:zptmass_histo_StatM400pT80Down', 'zpt_weight_statpt80down')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['z_gen_mass', 'z_gen_pt'],
                          GetFromTFile(task[0]), name=task[1])

w.importClassCode('CrystalBallEfficiency')

w.Print()
w.writeToFile('htt_scalefactors_2017_v1.root')
w.Delete()
