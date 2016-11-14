from definitions import *

# kinematical cuts
xB_cut          = "(Xb > 1.05)"
# ---------------------------------------------
p_miss_cut      = "(0.3 < Pmiss.P() && Pmiss.P() < 1.0)"
p_miss_t_cut    = "(Pmiss.Pt() < 0.4)"
theta_pq_cut    = "(theta_pq < 25)"
p_over_q_cut    = "(0.62 < p_over_q && p_over_q < 0.96)"
m_miss2_cut     = "(Mmiss < 1.1)"


# detector cuts
pEdep_cut = []
for i in range(3): pEdep_cut.append( dm.pEdepCut(i) )

pppEdep_cut      = pEdep_cut[0].GetName() + "&&" + pEdep_cut[1].GetName() + "&&" + pEdep_cut[2].GetName()
pp_ctof_cut     = "(pCTOFCut[0] && pCTOFCut[1] )"
ppp_ctof_cut    = "(pCTOFCut[0] && pCTOFCut[1] && pCTOFCut[2])"

p0_fiducial_cut = "(pFiducCut[0]==1)"
p1_fiducial_cut = "(pFiducCut[1]==1)"
p2_fiducial_cut = "(pFiducCut[2]==1)"

# vertex
def p_vertex_cut( i , zmin , zmax ):
    return "(%.2f < pVertex[%d].Z() && pVertex[%d].Z() < %.2f)"%(zmin , i , i , zmax)

# 2p-SRC
p_lead_cut      = p_vertex_cut( 0 , -24.5 , -20 )
p_recoil_cut    = "(0.35 < Prec.P())" + "&&" + p_vertex_cut( 1 , -24.5 , -20 )

# 3p-SRC
p1_cut          = p_vertex_cut( 0 , -27 , -20 )
p2_cut          = "(0.3 < protons[1].P())" + "&&" + p_vertex_cut( 1 , -27 , -20 )
p3_cut          = "(0.3 < protons[2].P())" + "&&" + p_vertex_cut( 2 , -27 , -20 )
p1p2p3_cut      = p1_cut + "&&" + p2_cut + "&&" + p3_cut
m_miss3_cut     = "(Pcm.Mag() < 3*0.938)"
    
#ppNothing_alpha12_vs_XbCut = dm.alpha12_vs_XbCut()
#alpha12_vs_XbCutDIS = ppNothing_alpha12_vs_XbCut.GetName()
#alpha12_vs_XbCutCorrelation = "(!%s)",ppNothing_alpha12_vs_XbCut.GetName()

# final cuts
src_cut         = xB_cut + "&&" + theta_pq_cut + "&&" + p_over_q_cut + "&&" + p_miss_cut
# 1p-SRC
p_src_cut       = src_cut + "&&" + p_miss_t_cut + "&&" + "(1 <= Np)"
# 2p-SRC
pp_src_cut      = src_cut + "&&" + "(1.2 <= Xb)" + "&&" + m_miss2_cut + "&&" + "(2 <= Np)" + "&&" + p_lead_cut + "&&" + p_recoil_cut + "&&" + pp_ctof_cut
evtgen_pp_src_cut = p_lead_cut + "&&" + p_recoil_cut
# 3p-SRC
ppp_src_cut     = src_cut + "&&" + "(3 <= Np)" + "&&" + p1p2p3_cut + "&&" + pppEdep_cut + "&&" + ppp_ctof_cut + "&&" + p_miss_t_cut + "&&" + m_miss3_cut
