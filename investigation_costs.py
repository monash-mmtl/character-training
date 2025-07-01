"""
Cost mapping for medical investigations commonly used in headache cases.
Costs are in AUD and represent Medicare Benefits Schedule (MBS) benefits as of 2024.
Item numbers are included for reference.

Source: Medicare Benefits Schedule (MBS) Online
http://www9.health.gov.au/mbs/search.cfm

Note: Many pathology tests are grouped under the same item numbers.
For example, Item 66500 covers multiple biochemical tests that can be performed on the same sample.
"""

INVESTIGATION_COSTS = {
    # Blood Tests
    "Full Blood Count": {
        "cost": 16.95,
        "item_number": "65070",
        "description": "Erythrocyte count, haematocrit, haemoglobin, calculation or measurement of red cell index or indices, platelet count, leucocyte count and manual or instrument generated differential count, from a single sample"
    },
    "Complete Blood Count": {
        "cost": 16.95,
        "item_number": "65070",
        "description": "Erythrocyte count, haematocrit, haemoglobin, calculation or measurement of red cell index or indices, platelet count, leucocyte count and manual or instrument generated differential count, from a single sample"
    },
    "Basic Metabolic Panel": {
        "cost": 17.70,
        "item_number": "66512",
        "description": "Quantitation of 5 or more common chemical analytes in serum, plasma, urine, or other body fluid (e.g., glucose, creatinine, electrolytes, urea)"
    },
    "comprehensive metabolic panel": {
        "cost": 17.70,
        "item_number": "66512",
        "description": "Quantitation of 5 or more common chemical analytes in serum, plasma, urine, or other body fluid (e.g., glucose, creatinine, electrolytes, urea)"
    },
    "Blood Glucose": {
        "cost": 9.70,
        "item_number": "66500",
        "description": "Quantitation of glucose in serum, plasma, urine or other body fluid"
    },
    "serum creatinine": {
        "cost": 9.70,
        "item_number": "66500",
        "description": "Quantitation in serum, plasma, urine or other body fluid (except amniotic fluid), by any method except reagent tablet or reagent strip (with or without reflectance meter) of: creatinine - 1 test"
    },
    "serum urea": {
        "cost": 9.70,
        "item_number": "66500",
        "description": "Quantitation in serum, plasma, urine or other body fluid (except amniotic fluid), by any method except reagent tablet or reagent strip (with or without reflectance meter) of: urea - 1 test"
    },
    "U&E": {
        "cost": 11.65,
        "item_number": "66503",
        "description": "Quantitation in serum, plasma, urine or other body fluid (except amniotic fluid), by any method except reagent tablet or reagent strip (with or without reflectance meter) of: urea and creatinine - 2 tests"
    },
    "Urea and Electrolytes": {
        "cost": 11.65,
        "item_number": "66503",
        "description": "Quantitation in serum, plasma, urine or other body fluid (except amniotic fluid), by any method except reagent tablet or reagent strip (with or without reflectance meter) of: urea and creatinine - 2 tests"
    },
    "Lipid Panel (Lipid Studies)": {
        "cost": 11.65,
        "item_number": "66503",
        "description": "Quantitation of 2 tests described in item 66500, which includes total cholesterol and triglycerides, performed in serum, plasma, urine or other body fluid by any method except reagent tablet or reagent strip. This is a recognized group of tests abbreviated as 'FATS'."
    },
    "FATS": {
        "cost": 11.65,
        "item_number": "66503",
        "description": "Quantitation of 2 tests described in item 66500, which includes total cholesterol and triglycerides, performed in serum, plasma, urine or other body fluid by any method except reagent tablet or reagent strip. This is a recognized group of tests abbreviated as 'FATS'."
    },
    "HbA1c (Glycated Haemoglobin)": {
        "cost": 16.80,
        "item_number": "66551",
        "description": "Quantitation of glycated haemoglobin performed in the management of established diabetes. This test can also be performed for the diagnosis of diabetes in asymptomatic patients at high risk (item 66841, $16.80)."
    },
    "HbA1c": {
        "cost": 16.80,
        "item_number": "66551",
        "description": "Quantitation of glycated haemoglobin performed in the management of established diabetes. This test can also be performed for the diagnosis of diabetes in asymptomatic patients at high risk (item 66841, $16.80)."
    },
    "Electrolytes": {
        "cost": 15.65,
        "item_number": "66509",
        "description": "Quantitation of 4 chemical analytes (Sodium, Potassium, Chloride, and Bicarbonate) in serum, plasma, urine, or other body fluid"
    },
    "Blood Culture": {
        "cost": 92.20,
        "item_number": "69360",
        "description": "Blood culture for pathogenic micro-organisms (other than viruses), including sub-cultures and identification of any cultured pathogen and necessary antibiotic susceptibility testing, for 3 sets of cultures"
    },
    "erythrocyte sedimentation rate (ESR)": {
        "cost": 7.85,
        "item_number": "65060",
        "description": "Haemoglobin, erythrocyte sedimentation rate, blood viscosity - 1 or more tests"
    },
    "C-reactive protein (CRP)": {
        "cost": 9.70,
        "item_number": "66500",
        "description": "Quantitation in serum, plasma, urine or other body fluid (except amniotic fluid), by any method except reagent tablet or reagent strip (with or without reflectance meter) of: C-reactive protein"
    },
    "serum osmolality": {
        "cost": 24.70,
        "item_number": "66563",
        "description": "Osmolality, estimation by osmometer, in serum or in urine - 1 or more tests"
    },
    
    # Hormone Tests (all use item 66695, $30.50 each)
    "thyroid function tests": {
        "cost": 34.80,
        "item_number": "66719",
        "description": "Thyroid function tests, comprising the service described in item 66716 (TSH quantitation) and either or both of a test for free thyroxine (FT4) and a test for free T3 (FT3)"
    },
    "TSH quantitation": {
        "cost": 25.05,
        "item_number": "66716",
        "description": "TSH quantitation"
    },
    "serum aldosterone": {
        "cost": 30.50,
        "item_number": "66695",
        "description": "Quantitation in blood or urine of hormones and hormone binding proteins - ACTH, aldosterone, androstenedione, C-peptide, calcitonin, cortisol, DHEAS, 11-deoxycortisol, dihydrotestosterone, FSH, gastrin, glucagon, growth hormone, hydroxyprogesterone, insulin, LH, oestradiol, oestrone, progesterone, prolactin, PTH, renin, sex hormone binding globulin, somatomedin C(IGF-1), free or total testosterone, urine steroid fraction or fractions, vasoactive intestinal peptide - 1 test"
    },
    "ACTH Quantitation": {
        "cost": 30.50,
        "item_number": "66695",
        "description": "Quantitation in blood or urine of hormones and hormone binding proteins - ACTH, aldosterone, androstenedione, C-peptide, calcitonin, cortisol, DHEAS, 11-deoxycortisol, dihydrotestosterone, FSH, gastrin, glucagon, growth hormone, hydroxyprogesterone, insulin, LH, oestradiol, oestrone, progesterone, prolactin, PTH, renin, sex hormone binding globulin, somatomedin C(IGF-1), free or total testosterone, urine steroid fraction or fractions, vasoactive intestinal peptide - 1 test"
    },
    "IGF-1 (Somatomedin C)": {
        "cost": 30.50,
        "item_number": "66695",
        "description": "Quantitation in blood or urine of hormones and hormone binding proteins - ACTH, aldosterone, androstenedione, C-peptide, calcitonin, cortisol, DHEAS, 11-deoxycortisol, dihydrotestosterone, FSH, gastrin, glucagon, growth hormone, hydroxyprogesterone, insulin, LH, oestradiol, oestrone, progesterone, prolactin, PTH, renin, sex hormone binding globulin, somatomedin C(IGF-1), free or total testosterone, urine steroid fraction or fractions, vasoactive intestinal peptide - 1 test"
    },
    "Prolactin": {
        "cost": 30.50,
        "item_number": "66695",
        "description": "Quantitation in blood or urine of hormones and hormone binding proteins - ACTH, aldosterone, androstenedione, C-peptide, calcitonin, cortisol, DHEAS, 11-deoxycortisol, dihydrotestosterone, FSH, gastrin, glucagon, growth hormone, hydroxyprogesterone, insulin, LH, oestradiol, oestrone, progesterone, prolactin, PTH, renin, sex hormone binding globulin, somatomedin C(IGF-1), free or total testosterone, urine steroid fraction or fractions, vasoactive intestinal peptide - 1 test"
    },
    "plasma renin activity": {
        "cost": 30.50,
        "item_number": "66695",
        "description": "Quantitation in blood or urine of hormones and hormone binding proteins - ACTH, aldosterone, androstenedione, C-peptide, calcitonin, cortisol, DHEAS, 11-deoxycortisol, dihydrotestosterone, FSH, gastrin, glucagon, growth hormone, hydroxyprogesterone, insulin, LH, oestradiol, oestrone, progesterone, prolactin, PTH, renin, sex hormone binding globulin, somatomedin C(IGF-1), free or total testosterone, urine steroid fraction or fractions, vasoactive intestinal peptide - 1 test"
    },
    "serum/morning cortisol levels": {
        "cost": 30.50,
        "item_number": "66695",
        "description": "Quantitation in blood or urine of hormones and hormone binding proteins - ACTH, aldosterone, androstenedione, C-peptide, calcitonin, cortisol, DHEAS, 11-deoxycortisol, dihydrotestosterone, FSH, gastrin, glucagon, growth hormone, hydroxyprogesterone, insulin, LH, oestradiol, oestrone, progesterone, prolactin, PTH, renin, sex hormone binding globulin, somatomedin C(IGF-1), free or total testosterone, urine steroid fraction or fractions, vasoactive intestinal peptide - 1 test"
    },
    "24 hours urinary free cortisol": {
        "cost": 30.50,
        "item_number": "66695",
        "description": "Quantitation in blood or urine of hormones and hormone binding proteins - ACTH, aldosterone, androstenedione, C-peptide, calcitonin, cortisol, DHEAS, 11-deoxycortisol, dihydrotestosterone, FSH, gastrin, glucagon, growth hormone, hydroxyprogesterone, insulin, LH, oestradiol, oestrone, progesterone, prolactin, PTH, renin, sex hormone binding globulin, somatomedin C(IGF-1), free or total testosterone, urine steroid fraction or fractions, vasoactive intestinal peptide - 1 test"
    },
    
    # Imaging Tests
    "CT Head": {
        "cost": 211.35,
        "item_number": "56001",
        "description": "Computed tomography—scan of brain without intravenous contrast medium, not being a service to which item 57001 applies."
    },
    "CT Head with contrast": {
        "cost": 270.85,
        "item_number": "56007",
        "description": "Computed tomography—scan of brain with intravenous contrast medium and with any scans of the brain before intravenous contrast injection, when performed, not being a service to which item 57007 applies."
    },
    "MRI Brain": {
        "cost": 426.50,
        "item_number": "63001",
        "description": "MRI—scan of head (including MRA, if performed) for tumour of the brain or meninges. Many other MRI scans of the head for specified conditions share this same fee and can include MRA if performed, as indicated by '(Contrast)' in their description [1-12]."
    },
    "MRV (Magnetic Resonance Venography) of the Brain": {
        "cost": 426.50,
        "item_number": "63055",
        "description": "MRI—scan of head (including MRA, if performed) for venous sinus thrombosis."
    },
    "CT Angiography of the Head": {
        "cost": 552.50,
        "item_number": "57352",
        "description": "Computed tomography—angiography with intravenous contrast medium of any or all, or any part, of: (a) the arch of the aorta; or (b) the carotid arteries; or (c) the vertebral arteries and their branches (head and neck); including any scans performed before intravenous contrast injection—one or more data acquisitions, including image editing, and maximum intensity projections or 3 dimensional surface shaded display, with hardcopy or digital recording of multiple projections, if requested by a specialist or consultant physician, or with specific discussion/indication if requested by a medical practitioner."
    },
    "Chest X-ray": {
        "cost": 47.05,
        "item_number": "58500",
        "description": "Radiographic examination of the chest, 1 or 2 projections"
    },
    "CT Chest": {
        "cost": 433.35,
        "item_number": "56307",
        "description": "Computed tomography scan of chest, including lungs, mediastinum, chest wall and pleura, with or without scans of the upper abdomen, with intravenous contrast medium and any scans before contrast injection, when undertaken"
    },
    "cervical spine X-ray": {
        "cost": 72.70,
        "item_number": "58100",
        "description": "Radiographic examination of the spine—cervical region"
    },
    "sinus X-ray": {
        "cost": 69.85,
        "item_number": "57907",
        "description": "Radiographic examination of the sinuses or facial bones – orbit, maxilla or malar, any or all"
    },
    "CT scan of sinuses": {
        "cost": 243.75,
        "item_number": "56022",
        "description": "Computed tomography—scan of facial bones, para nasal sinuses or both without intravenous contrast medium (R) (Anaes.)"
    },
    "CT scan of sinuses with contrast": {
        "cost": 364.85,
        "item_number": "56028",
        "description": "Computed tomography—scan of facial bones, para nasal sinuses or both with intravenous contrast medium and with any scans of the facial bones, para nasal sinuses or both before intravenous contrast injection, when performed (R) (Anaes.)"
    },
    "Adrenal CT Scan": {
        "cost": 270.85,
        "item_number": "56401",
        "description": "Computed tomography—scan of upper abdomen only (diaphragm to iliac crest) without intravenous contrast medium, not being a service to which item 56301, 56501, 56801 or 57001 applies. (Adrenal glands are located within the upper abdomen)."
    },
    "Adrenal CT Scan with contrast": {
        "cost": 390.05,
        "item_number": "56407",
        "description": "Computed tomography—scan of upper abdomen only (diaphragm to iliac crest), with intravenous contrast medium, and with any scans of upper abdomen (diaphragm to iliac crest) before intravenous contrast injection, when undertaken, not being a service to which item 56307, 56507, 56807 or 57007 applies. (Adrenal glands are located within the upper abdomen)."
    },
    
    # Procedures
    "Lumbar Puncture": {
        "cost": 175.45,
        "item_number": "144",
        "description": "Lumbar cerebrospinal fluid drain, insertion of"
    },
    "Lumbar Puncture with CSF Analysis": {
        "cost": "Sum of component services",
        "item_number": "Multiple Items",
        "description": "This service is represented by multiple individual MBS items. The components and their respective costs are: Lumbar Puncture (e.g., 144: $175.45 for drain insertion, or 56219: $353.40 for CT scan of spine with intrathecal contrast medium which includes preparation for injection), CSF Culture (69321: $48.15), CSF Protein (66500: $9.70), CSF Glucose (66500: $9.70), and CSF Cell Count (69300: $12.50)."
    },
    
    # CSF Tests
    "CSF Culture": {
        "cost": 48.15,
        "item_number": "69321",
        "description": "Microscopy and culture of CSF specimens for the presence of pathogenic micro-organisms, involving aerobic and anaerobic cultures and different culture media"
    },
    "CSF Protein": {
        "cost": 9.70,
        "item_number": "66500",
        "description": "Quantitation of total protein in other body fluid"
    },
    "CSF Glucose": {
        "cost": 9.70,
        "item_number": "66500",
        "description": "Quantitation of glucose in other body fluid"
    },
    "CSF Cell Count": {
        "cost": 12.50,
        "item_number": "69300",
        "description": "Microscopy of wet film material (other than blood), obtained directly from a patient, including differential cell count if performed"
    },
    
    # Urine Tests
    "Urinalysis": {
        "cost": 20.55,
        "item_number": "69333",
        "description": "Urine examination (including serial examinations) by any means other than simple culture by dip slide, covering cell count, culture, colony count, and other tests as performed"
    },
    "Urine Culture": {
        "cost": 20.55,
        "item_number": "69333",
        "description": "Urine examination including culture, colony count, and identification of cultured pathogens (This item covers a comprehensive urine examination including culture, no specific standalone urine culture item is listed)"
    },
    "urine osmolality": {
        "cost": 24.70,
        "item_number": "66563",
        "description": "Osmolality, estimation by osmometer, in serum or in urine - 1 or more tests"
    },
    
    # Infectious Disease Tests
    "HIV Test": {
        "cost": 180.25,
        "item_number": "69378",
        "description": "Quantitation of HIV viral RNA load in plasma or serum in the monitoring of a HIV sero-positive patient not on antiretroviral therapy"
    },
    "Syphilis Test": {
        "cost": 69.10,
        "item_number": "69387",
        "description": "Syphilis serology including Rapid plasma regain test (RPR) or Venereal disease research laboratory test (VDRL), and Treponema pallidum haemagglutination test (TPHA) or Fluorescent treponemal antibody-absorption test (FTA)"
    },
    
    # Specialized Tests
    "visual field testing (perimetry)": {
        "cost": 70.10,
        "item_number": "10940",
        "description": "COMPUTERISED PERIMETRY Full quantitative computerised perimetry (automated absolute static threshold) with unilateral or bilateral assessment and report, where indicated by the presence of relevant ocular disease or suspected pathology of the visual pathways or brain"
    },
    "measure blood pressure and check for orthostatic hypotension": {
        "cost": 169.80,
        "item_number": "11724",
        "description": "Up-right tilt table test, for a patient with recurrent unexplained syncope where a diagnosis has not been achieved through all other available cardiac investigations and a neurogenic cause is not suspected. Routine blood pressure measurement is typically part of a general medical examination or consultation, not a separately billable test item."
    },
    "refraction test to assess for any refractive errors": {
        "cost": 135.95,
        "item_number": "10803",
        "description": "Attendance for the investigation and evaluation of a patient for the fitting of contact lenses, with keratometry and testing with trial lenses and the issue of a prescription—one service in any period of 36 months—patient with manifest hyperopia of 5.0 dioptres or greater (spherical equivalent) in one eye. A direct standalone 'refraction test' item is not explicitly listed, but the assessment of refractive errors would be integral to a comprehensive optometric consultation or a service like this one where trial lenses are used to issue a prescription."
    },
    "12-lead electrocardiography": {
        "cost": 20.25,
        "item_number": "11707",
        "description": "Twelve-lead electrocardiography, trace only, by a medical practitioner, if the trace is required to inform clinical decision making and is reviewed in a clinically appropriate timeframe to identify potentially serious or life threatening abnormalities."
    },
    "sleep study (polysomnography)": {
        "cost": 695.95,
        "item_number": "12203",
        "description": "Overnight diagnostic assessment of sleep, for at least 8 hours, for a patient aged 18 years or more, to confirm diagnosis of obstructive sleep apnoea, if certain clinical criteria and monitoring requirements are met."
    },
    
    # Contrast and Modifiers
    "Contrast (for CT/MRI)": {
        "cost": "Included in imaging service fee",
        "item_number": "N/A",
        "description": "The cost of contrast medium for imaging procedures (CT/MRI) is typically incorporated into the fee of the primary service item when a contrast-enhanced study is performed. There is no separate MBS item for the contrast medium itself."
    },
    "MRI/MRA Contrast Agent (Modifier)": {
        "cost": 47.40,
        "item_number": "63491",
        "description": "MRI or MRA service to which an item in this Group (other than an item in this Subgroup) applies if: (a) the service is performed on a person in accordance with clause 2.5.1; and (b) the item for the service includes in its description '(Contrast)'; and (c) the service is performed using a contrast agent. This item is claimed in addition to the primary MRI/MRA service when a contrast agent is administered [13, 14]."
    }
}

# Helper function to get cost of an investigation
def get_investigation_cost(investigation_name: str) -> float:
    """
    Get the cost of a specific investigation.
    
    Args:
        investigation_name (str): Name of the investigation
        
    Returns:
        float: Medicare benefit for the investigation in AUD, or 0 if not found
    """
    investigation = INVESTIGATION_COSTS.get(investigation_name)
    return investigation["cost"] if investigation else 0

# Helper function to get investigation details
def get_investigation_details(investigation_name: str) -> dict:
    """
    Get full details of a specific investigation including item number and description.
    
    Args:
        investigation_name (str): Name of the investigation
        
    Returns:
        dict: Dictionary containing cost, item number, and description, or None if not found
    """
    return INVESTIGATION_COSTS.get(investigation_name)

# Helper function to get total cost of multiple investigations
def get_total_cost(investigations: list[str]) -> float:
    """
    Calculate total Medicare benefit for a list of investigations.
    
    Args:
        investigations (list[str]): List of investigation names
        
    Returns:
        float: Total Medicare benefit for all investigations in AUD
    """
    return sum(get_investigation_cost(inv) for inv in investigations)

if __name__ == "__main__":
    # Example usage
    test_investigations = ["CT Head", "Full Blood Count", "Lumbar Puncture"]
    total = get_total_cost(test_investigations)
    print(f"Total Medicare benefit for {test_investigations}: ${total:.2f}")
    
    # Print details for each investigation
    for inv in test_investigations:
        details = get_investigation_details(inv)
        if details:
            print(f"\n{inv}:")
            print(f"  Item Number: {details['item_number']}")
            print(f"  Description: {details['description']}")
            print(f"  Medicare Benefit: ${details['cost']:.2f}") 