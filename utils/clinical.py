import random
import string
from datetime import datetime


DR_CLASSES = [
    "No DR",
    "Mild DR",
    "Moderate DR",
    "Severe DR",
    "Proliferative DR"
]

DR_SEVERITY_MAP = {
    "No DR": {
        "severity": "None",
        "risk": "Low",
        "follow_up": "Annual screening recommended.",
        "color": "#10B981",
        "icon": "✅",
        "title": "No Diabetic Retinopathy Detected"
    },
    "Mild DR": {
        "severity": "Mild Non-Proliferative DR",
        "risk": "Low-Moderate",
        "follow_up": "Follow-up within 12 months. Optimize glycemic control.",
        "color": "#F59E0B",
        "icon": "⚠️",
        "title": "Mild Non-Proliferative DR"
    },
    "Moderate DR": {
        "severity": "Moderate Non-Proliferative DR",
        "risk": "Moderate",
        "follow_up": "Ophthalmology consultation within 3-6 months.",
        "color": "#F97316",
        "icon": "🔶",
        "title": "Moderate Non-Proliferative DR"
    },
    "Severe DR": {
        "severity": "Severe Non-Proliferative DR",
        "risk": "High",
        "follow_up": "Urgent specialist evaluation within 1-3 months.",
        "color": "#EF4444",
        "icon": "🚨",
        "title": "Severe Non-Proliferative DR"
    },
    "Proliferative DR": {
        "severity": "Proliferative DR — Vision Threatening",
        "risk": "Critical",
        "follow_up": "Immediate referral required. Anti-VEGF or PRP evaluation.",
        "color": "#A855F7",
        "icon": "🆘",
        "title": "Proliferative DR"
    }
}

CLINICAL_NOTES = {
    "No DR": [
        "Retinal examination reveals no microaneurysms, hemorrhages, or exudates. Macula and optic disc appear normal. No signs of diabetic retinopathy detected.",
        "Fundus examination unremarkable. Normal cup-to-disc ratio. Retinal vasculature within normal limits. No evidence of diabetic retinopathy.",
        "No pathological findings on funduscopy. Normal foveal reflex and intact retinal architecture. Continue routine diabetes management."
    ],
    "Mild DR": [
        "Presence of a few microaneurysms and dot-blot hemorrhages in the posterior pole, consistent with mild non-proliferative diabetic retinopathy. Macular edema not observed.",
        "Scattered microaneurysms noted in the temporal vascular arcades. Mild NPDR findings without clinically significant macular edema.",
        "Early NPDR changes with occasional retinal hemorrhages. No venous beading or IRMA observed. Recommend optimizing systemic control."
    ],
    "Moderate DR": [
        "Multiple microaneurysms, dot-blot hemorrhages, and hard exudates observed across all quadrants. Mild intraretinal microvascular abnormalities (IRMA) present. No neovascularization.",
        "Moderate NPDR with cotton-wool spots, venous caliber changes, and deep hemorrhages. Macular thickening noted on optical coherence tomography correlation.",
        "Widespread retinal hemorrhages and exudates extending beyond the posterior pole. IRMA and venous beading present. Clinically significant macular edema suspected."
    ],
    "Severe DR": [
        "Severe NPDR with extensive hemorrhages and microaneurysms in all four quadrants. Venous beading in two or more quadrants. Prominent IRMA. High risk of progression to PDR.",
        "Advanced NPDR findings: significant intraretinal hemorrhages, venous dilatation and beading, and numerous cotton-wool spots. Urgent ophthalmology referral indicated.",
        "Severe NPDR with the 4-2-1 rule positive: hemorrhages in 4 quadrants, venous beading in 2 quadrants, IRMA in 1 quadrant. High-risk characteristics present."
    ],
    "Proliferative DR": [
        "Neovascularization of the optic disc (NVD) and elsewhere (NVE) observed. Vitreous hemorrhage present. High-risk PDR requiring immediate pan-retinal photocoagulation.",
        "Active proliferative disease with neovascular fronds extending into the vitreous cavity. Pre-retinal hemorrhage noted. Urgent anti-VEGF therapy and PRP indicated.",
        "Advanced PDR with tractional retinal detachment suspected. Neovascular glaucoma risk. Immediate vitreoretinal consultation required for possible surgical intervention."
    ]
}

RECOMMENDATIONS = {
    "No DR": {
        "patient": "Continue annual dilated eye examinations. Maintain optimal glycemic control (HbA1c < 7%), blood pressure < 140/90 mmHg, and lipid management.",
        "clinical": "No retinopathy detected. Standard diabetes management with annual retinal screening. Patient education on symptom awareness.",
        "urgency": "Routine"
    },
    "Mild DR": {
        "patient": "Schedule follow-up dilated eye examination within 12 months. Optimize glycemic, blood pressure, and lipid control. Report any visual changes immediately.",
        "clinical": "Mild NPDR. Annual follow-up recommended. Enhanced systemic risk factor management. Patient education on progression warning signs.",
        "urgency": "Routine"
    },
    "Moderate DR": {
        "patient": "Ophthalmology referral recommended within 3-6 months. Consider OCT for macular edema evaluation. Strict glycemic and BP control essential.",
        "clinical": "Moderate NPDR. Refer to ophthalmology for comprehensive evaluation. Consider fluorescein angiography. Monitor for CSME development.",
        "urgency": "Within 3-6 months"
    },
    "Severe DR": {
        "patient": "Urgent ophthalmology referral required within 1-3 months. High risk of progression to proliferative stage. Pan-retinal photocoagulation may be indicated.",
        "clinical": "Severe NPDR. Prompt specialist evaluation. PRP consideration. Close monitoring for neovascularization. OCT and FA recommended.",
        "urgency": "Within 1-3 months"
    },
    "Proliferative DR": {
        "patient": "IMMEDIATE ophthalmology referral. Vision-threatening condition. Treatment options: anti-VEGF injections, pan-retinal photocoagulation, or vitrectomy.",
        "clinical": "PDR with high-risk characteristics. Emergency vitreoretinal consultation. Anti-VEGF therapy initiation. PRP scheduling. Monitor for vitreous hemorrhage and retinal detachment.",
        "urgency": "Immediate"
    }
}


def generate_patient_id():
    year = datetime.now().year
    num = random.randint(10000, 99999)
    return f"RG-{year}-{num}"


def generate_exam_number():
    num = random.randint(1000, 9999)
    return f"EXM-{num}"


def generate_patient_data():
    ages = list(range(22, 88))
    weights = [1] * 5 + [3] * 15 + [5] * 20 + [4] * 15 + [2] * 6 + [1] * 5
    age = random.choices(ages, weights=weights, k=1)[0]
    gender = random.choice(["Male", "Female", "Male", "Female", "Male"])
    return {
        "patient_id": generate_patient_id(),
        "age": age,
        "gender": gender,
        "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "exam_number": generate_exam_number(),
    }


def get_clinical_note(predicted_class):
    notes = CLINICAL_NOTES.get(predicted_class, CLINICAL_NOTES["No DR"])
    return random.choice(notes)


def get_recommendation(predicted_class):
    return RECOMMENDATIONS.get(predicted_class, RECOMMENDATIONS["No DR"])


def get_severity_info(predicted_class):
    return DR_SEVERITY_MAP.get(predicted_class, DR_SEVERITY_MAP["No DR"])
