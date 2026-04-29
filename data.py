"""
Shared data, constants, and helper functions for the Water Instrument Dashboard.
All item content is drawn from water_instrument_v11_alternate_conceptions_bank.docx.

Color tokens live in theme.py. Import them from there in any new code:
    from theme import CC_COLOR, AC_COLOR, AC_FADED_COLOR, FLAG_COLOR
"""

import os
import pandas as pd
import numpy as np

# Re-export color tokens so older imports (`from data import CC_COLOR`) keep working.
# theme.py is the single source of truth for the palette.
from theme import CC_COLOR, AC_COLOR, AC_FADED_COLOR, FLAG_COLOR  # noqa: F401

# ── Anchoring Concept definitions ────────────────────────────────────────────
# The decorative emoji icons were removed in the dark-theme refactor.
# If you need a visual marker per AC, use a colored dot in the page CSS.
ANCHORING_CONCEPTS = {
    "AC1: Atoms": {
        "items": [1],
        "description": "Atomic structure, isotopes, and subatomic particles",
    },
    "AC2: Bonding": {
        "items": [2, 3, 4, 5, 6],
        "description": "Covalent and ionic bonding, potential energy diagrams",
    },
    "AC3: Structure & Function": {
        "items": [7, 8, 9, 10, 11],
        "description": "Molecular geometry, hybridization, polarity, electron density",
    },
    "AC4: Intermolecular Forces": {
        "items": [12, 13, 14, 15, 16, 17, 18, 19, 21],
        "description": "Hydrogen bonding, London dispersion forces, phase changes",
    },
    "AC5: Reactions": {
        "items": [22, 23],
        "description": "Formation of water, bond energy and reaction energetics",
    },
    "AC6: Energy & Thermodynamics": {
        "items": [20, 24, 25, 26, 31, 32],
        "description": "Kinetic energy distributions, entropy, spontaneity, free energy",
    },
    "AC7: Kinetics": {
        "items": [28, 29, 30],
        "description": "Reaction rate, order, and thermodynamic independence",
    },
    "AC8: Equilibrium": {
        "items": [27, 33, 34, 35, 36, 37, 38],
        "description": "Equilibrium constants, Le Chatelier's principle, acid-base",
    },
}

# ── Item bank: question text, correct conception, alternate conceptions ────────
# Drawn directly from the alternate conceptions bank document
ITEMS = {
    1: {
        "text": "D₂O is comprised of one of hydrogen's isotopes deuterium (²H) and oxygen. How do D₂O and H₂O compare?",
        "correct_choice": "D₂O has a higher mass than H₂O.",
        "correct_conception": "Isotopes of the same element have different masses; deuterium has a greater mass than hydrogen",
        "alternate_conceptions": [
            "D₂O contains more electrons than H₂O",
            "D₂O takes up more physical space than H₂O",
            "D₂O contains more protons than H₂O",
        ],
        "vocab_note": "Students may confuse 'isotope' with 'ion'. Emphasizing that isotopes differ only in neutron count (not proton or electron count) can help.",
    },
    2: {
        "text": "Which of the following best describes the electrons in a bond formed between H and O in a water molecule?",
        "correct_choice": "Core electrons do not participate, and valence electrons are shared in a polar covalent bond.",
        "correct_conception": "Valence electrons are shared in covalent bonding and core electrons do not participate",
        "alternate_conceptions": [
            "Core and valence electrons are shared in the polar covalent bond",
            "Core electrons do not participate, and valence electrons are shared in a nonpolar covalent bond",
        ],
        "vocab_note": "The terms 'core' vs. 'valence' electrons are critical here. Students sometimes use these interchangeably.",
    },
    3: {
        "text": "How does ionic bonding (e.g. NaCl) differ from the bond formed between H and O in a water molecule?",
        "correct_choice": "Ionic bonding occurs when positive and negative ions are held together by electrostatic forces.",
        "correct_conception": "Positive and negative ions are held together by electrostatic forces in an ionic bond",
        "alternate_conceptions": [
            "Ionic bonding involves the uneven sharing of electrons",
            "Ionic bonds form molecules by transferring electrons between two atoms",
            "Ionic bonding occurs between a metal and a nonmetal atom",
        ],
        "vocab_note": "Students sometimes confuse 'transfer' with 'sharing'. Distinguishing ionic vs. covalent at the electron level is key.",
    },
    4: {
        "text": "What causes the attraction in a bond between H and O in a single water molecule?",
        "correct_choice": "The valence electrons of each atom are attracted to the nucleus of the other atom.",
        "correct_conception": "Valence electrons of each are attracted to the nucleus of the other atom",
        "alternate_conceptions": [
            "H is positively charged, and O is negatively charged",
            "Oxygen needs to fill its valence shell",
            "Oxygen is more electronegative and attracts hydrogen's electron to itself",
        ],
        "vocab_note": "Electronegativity language like 'attracts the electron to itself' can reinforce a misconception that the electron fully transfers.",
    },
    5: {
        "text": "Which location on the potential energy diagram represents the highest likelihood of two O atoms existing as a molecule?",
        "correct_choice": "B, the energy minimum on the potential energy diagram",
        "correct_conception": "Bond formation corresponds to the energy minimum on a potential energy diagram",
        "alternate_conceptions": [
            "A: a bond is associated with the highest potential energy",
            "C: a bond is associated with 0 potential energy",
        ],
        "vocab_note": "Students often conflate 'stability' with 'low energy' in a general sense but misread PE diagrams.",
    },
    6: {
        "text": "How would you compare the attractive and repulsive forces of the two O atoms in an O₂ molecule at the lowest potential energy (B)?",
        "correct_choice": "There are net repulsive forces at A, net attractive forces at B, and zero net forces at C.",
        "correct_conception": "Net repulsive forces at A, net attractive forces at B, zero net forces at C",
        "alternate_conceptions": [
            "Zero net forces at A, net attractive forces at B, net repulsive forces at C",
            "Net attractive forces at A, zero net forces at B, net repulsive forces at C",
            "Net attractive forces at A, net repulsive forces at B, zero net forces at C",
        ],
        "vocab_note": None,
    },
    7: {
        "text": "What factors in the Lewis Structure help determine the molecular shape of a water molecule?",
        "correct_choice": "Both the bonds and lone pairs, since they exert repulsive forces.",
        "correct_conception": "Molecular shape of H₂O is determined by both bonds and lone pairs",
        "alternate_conceptions": [
            "Primarily the lone pairs, since they take up more space than bonds",
            "Primarily the bonds, since they exist between two atoms",
        ],
        "vocab_note": "Students using VSEPR rules sometimes over-index on lone pairs as 'dominant.'",
    },
    8: {
        "text": "Which bonding model most accurately explains the shape of H₂O?",
        "correct_choice": "The sp³ hybridized bonding model",
        "correct_conception": "sp³ hybridized bonding model",
        "alternate_conceptions": [
            "Simplistic unhybridized structure (molecular geometry model only)",
            "Fully unhybridized bonding model",
            "Fully unhybridized, incorrect bonding structure",
        ],
        "vocab_note": "Instructors who de-emphasize hybridization in GC (saving it for organic) may see high rates of the 'molecular geometry' alternate conception. This is pedagogically intentional for some courses.",
    },
    9: {
        "text": "Which representation best depicts a water molecule's electron density distribution (high electron density shaded in red)?",
        "correct_choice": "High electron density around the O atom in H₂O due to electronegativity",
        "correct_conception": "High electron density around the O atom in H₂O due to electronegativity",
        "alternate_conceptions": [
            "Understanding of polarization, but incorrect direction",
            "Equally high electron density across the whole H₂O molecule",
        ],
        "vocab_note": None,
    },
    10: {
        "text": "What determines the distribution of electron density in a water molecule?",
        "correct_choice": "All of the electrons (core and valence) will be more localized around the oxygen atom because the nucleus of oxygen has a strong pull on the electrons.",
        "correct_conception": "High electron density around the O atom in H₂O due to electronegativity",
        "alternate_conceptions": [
            "Electron density of H₂O is determined by charges on O and H",
            "Only valence electrons are evenly distributed in covalently bonded molecules",
            "Misapplication of Heisenberg uncertainty principle to electron cloud",
        ],
        "vocab_note": "Distinguishing 'charge' from 'electronegativity' is critical; students often conflate these.",
    },
    11: {
        "text": "What is the relationship between the partial charges, shape, and the polarity of H₂O?",
        "correct_choice": "Shape and partial charges determine polarity of the molecule.",
        "correct_conception": "Both shape and partial charges determine polarity of the molecule",
        "alternate_conceptions": [
            "Polarity is determined only by partial charges; shape has no role",
            "Partial charges determine shape and polarity of a molecule",
            "Partial charges are determined by polarity and shape",
        ],
        "vocab_note": None,
    },
    12: {
        "text": "Which best describes intermolecular forces in an aqueous solution?",
        "correct_choice": "They are a result of uneven distributions of electrons in a molecule.",
        "correct_conception": "IMFs occur when there is an uneven distribution of electrons",
        "alternate_conceptions": [
            "IMFs are only present between polar molecules",
            "IMFs are not dependent on polarity of molecules (temporary or permanent)",
            "IMFs only occur between two different types of molecules",
        ],
        "vocab_note": "Students often frame IMFs as exclusively between 'different' molecules and may forget self-interactions (e.g., water-water hydrogen bonding).",
    },
    13: {
        "text": "Identify which atoms are involved in intermolecular forces with the two water molecules and describe their interaction.",
        "correct_choice": "There are hydrogen bonds between atoms 2 and 4.",
        "correct_conception": "Hydrogen bonding occurs between a hydrogen and an intermolecular electrophilic heteroatom",
        "alternate_conceptions": [
            "Hydrogen bonding occurs between two intermolecular electrophilic heteroatoms without hydrogen present",
            "Hydrogen bonding occurs within a single H₂O molecule",
            "Hydrogen bonding occurs between two hydrogens",
        ],
        "vocab_note": "Numbering ambiguity in diagrams can contribute to errors here; clarity in atom labeling helps.",
    },
    14: {
        "text": "How do London Dispersion Forces occur in water?",
        "correct_choice": "An instantaneous uneven distribution of electrons induces instantaneous dipoles in neighboring molecules.",
        "correct_conception": "LDFs are instantaneous dipoles that induce other instantaneous dipoles",
        "alternate_conceptions": [
            "LDFs are an inducement of permanent dipoles",
            "LDFs are an attraction to a permanent dipole",
            "LDFs are permanent dipole-dipole interactions",
        ],
        "vocab_note": "The word 'induces' is key and often glossed over; students may substitute 'attracts' or 'causes.'",
    },
    15: {
        "text": "Why do London Dispersion Forces occur in water?",
        "correct_choice": "Fluctuation of one electron cloud can cause fluctuations in a nearby electron cloud, so that they attract to each other.",
        "correct_conception": "LDFs are due to sequential fluctuations in electron clouds",
        "alternate_conceptions": [
            "LDFs are due to charges (not electron cloud fluctuation)",
            "LDFs are due to simultaneous fluctuations in electron clouds",
            "LDFs require repulsion to be overcome before IMF can form",
        ],
        "vocab_note": "The sequential vs. simultaneous distinction is subtle. The language like 'cause' vs. 'happen at the same time' matters here.",
    },
    16: {
        "text": "What is inside the bubbles in a pot of boiling water?",
        "correct_choice": "The bubbles contain water (water vapor).",
        "correct_conception": "Bubbles from boiling water contain water; no bonds are broken when water boils",
        "alternate_conceptions": [
            "Bubbles from boiling contain trapped air",
            "Oxygen is released when water boils; bonds are broken when water boils",
            "Hydrogen is released when water boils; bonds are broken when water boils",
        ],
        "vocab_note": "This item probes a well-documented alternate conception. The word 'boiling' triggers the idea of decomposition for many students.",
    },
    17: {
        "text": "Which of the following best describes the phase change of water boiling at 100°C?",
        "correct_choice": "H₂O molecules gain energy resulting in a phase change to gas, and temperature remains constant.",
        "correct_conception": "Temperature remains constant during a phase change",
        "alternate_conceptions": [
            "At boiling point, temperature continues to increase prior to phase change",
            "Temperature increases beyond the boiling point during process of evaporation",
        ],
        "vocab_note": "Heating curve diagrams are frequently used but students may misread the plateau as 'nothing happening.'",
    },
    18: {
        "text": "Which molecular-level properties can explain why less energy is required to melt H₂O(s) than vaporize H₂O(l)?",
        "correct_choice": "Liquid water has a dynamic molecular network whereas solid water has a rigid crystal structure.",
        "correct_conception": "Correct understanding of hydrogen bonding differences in solid vs. liquid water",
        "alternate_conceptions": [
            "Misapplication of bulk kinetic properties of water to individual water molecules",
            "Misapplication of bulk temperature differences between solid and liquid water",
            "More energy is required to overcome vapor pressure for liquid water",
        ],
        "vocab_note": None,
    },
    19: {
        "text": "If you could compare two individual water molecules, what would be different between an individual molecule of H₂O in the gas phase and an individual molecule in the solid phase?",
        "correct_choice": "The gas phase H₂O molecule is the same as the solid phase H₂O molecule.",
        "correct_conception": "Correct understanding of immutability of molecular-level water properties",
        "alternate_conceptions": [
            "Bulk density properties apply to individual molecules",
            "Bulk temperature properties apply to individual molecules",
            "Bond length is dependent on state of matter",
        ],
        "vocab_note": "This item targets the macro-micro distinction. Students frequently apply bulk properties to the molecular scale.",
    },
    20: {
        "text": "What do you expect to happen to a kinetic energy distribution curve with an increase in temperature?",
        "correct_choice": "The maximum would shift right, and the curve will get wider because there is a larger variance in the speed of the molecules.",
        "correct_conception": "At higher temperatures there is a larger variance in molecular speed",
        "alternate_conceptions": [
            "The number of molecules decreases as they move at higher speeds",
            "The area under the curve increases with increasing temperature",
            "At higher temperatures there is no change in variance, only an increase in average kinetic energy",
        ],
        "vocab_note": "Students often focus on the shift of the peak without recognizing the broadening of the curve.",
    },
    21: {
        "text": "Why is energy input required for phase changes A and B on a heating curve for water?",
        "correct_choice": "The energy input in A and B overcomes intermolecular forces to change phases.",
        "correct_conception": "Phase change occurs due to energy input overcoming intermolecular forces",
        "alternate_conceptions": [
            "Phase change requires energy input to increase kinetic energy",
            "Phase changes are time dependent",
            "Phase change requires energy input to break bonds within molecules",
        ],
        "vocab_note": "Students frequently confuse breaking IMFs with breaking intramolecular bonds. Vocabulary around 'bonds' is ambiguous in common usage.",
    },
    22: {
        "text": "Select the diagram that best describes the formation of water from its constituent elements.",
        "correct_choice": "Water molecules form from the reaction of diatomic elemental oxygen and hydrogen molecules (H₂ + O₂ → H₂O)",
        "correct_conception": "Water molecules form from the reaction of diatomic elemental oxygen and hydrogen molecules",
        "alternate_conceptions": [
            "Oxygen and hydrogen exist naturally as monatomic elements",
            "Water forms from monatomic hydrogen atoms and OH molecules",
            "Oxygen exists naturally as a monatomic element (literal interpretation of molecular formula)",
        ],
        "vocab_note": "Students may not recognize that elemental O and H exist as diatomic molecules.",
    },
    23: {
        "text": "Why does the formation of water release energy?",
        "correct_choice": "Because the energy required to break bonds in reactants is less than the energy released by forming bonds in water.",
        "correct_conception": "Energy is required to break bonds and released when bonds are formed",
        "alternate_conceptions": [
            "Energy is released by breaking bonds in reactants",
            "Energy is required to both break and form bonds",
            "Energy is released both when bonds break and form",
        ],
        "vocab_note": "The directionality of energy in bond breaking vs. forming is a foundational and persistent alternate conception.",
    },
    24: {
        "text": "Which option best describes the entropy change of the reaction shown?",
        "correct_choice": "The change in entropy is negative because entropy is determined by the number of ways to distribute energy in the system.",
        "correct_conception": "Entropy is determined by the number of ways to distribute energy",
        "alternate_conceptions": [
            "Entropy is determined by randomness versus microstates; positive sign",
            "Entropy is determined by randomness versus microstates; negative sign",
            "Change in entropy is positive when there are fewer ways to distribute energy",
        ],
        "vocab_note": "Instructors who introduce entropy as 'disorder' or 'randomness' may see elevated alternate conceptions here. The microstate/energy distribution framing aligns better with the correct answer.",
    },
    25: {
        "text": "Given that the reaction below is exothermic, and the change in entropy is negative, which best describes the spontaneity of the reaction?",
        "correct_choice": "It will be spontaneous at low temperatures.",
        "correct_conception": "When entropy is negative and a reaction is exothermic, the reaction will be spontaneous only at low temperatures",
        "alternate_conceptions": [
            "It will be spontaneous at all temperatures",
            "It will be spontaneous at high temperatures",
            "It will be nonspontaneous at all temperatures",
        ],
        "vocab_note": "Students may know the Gibbs equation but struggle to apply it to sign analysis across temperature ranges.",
    },
    26: {
        "text": "Select the free energy curve that best describes the formation of water: 2H₂(g) + O₂(g) ⇌ 2H₂O(l), Keq = 2.4 × 10⁴⁷ @ 500 K",
        "correct_choice": "Formation of water is spontaneous (ΔG < 0); correct application of free energy curve",
        "correct_conception": "Formation of water is spontaneous (ΔG < 0 for formation of water); correct application of free energy curve",
        "alternate_conceptions": [
            "The net change in Gibbs free energy for the formation of water is zero",
            "Formation of water is non-spontaneous; incorrect application of free energy curve",
        ],
        "vocab_note": None,
    },
    27: {
        "text": "What does an equilibrium constant (Keq) with a value of 2.4 × 10⁴⁷ at 500 K tell you about the reaction: 2H₂(g) + O₂(g) ⇌ 2H₂O(l)?",
        "correct_choice": "There will be primarily water at equilibrium.",
        "correct_conception": "Higher Keq values correspond to primarily products at equilibrium",
        "alternate_conceptions": [
            "Higher Keq values mean reaction will reach equilibrium quickly",
            "Higher Keq values correspond to primarily reactants at equilibrium",
            "At equilibrium, there are equivalent amounts of reactants and products",
        ],
        "vocab_note": "Students often confuse the magnitude of Keq with the rate of reaching equilibrium.",
    },
    28: {
        "text": "Which best describes the rate of an exothermic and endothermic reaction occurring at the same temperature?",
        "correct_choice": "The rate of reaction cannot be determined from the provided information.",
        "correct_conception": "Reaction rates cannot be determined based on enthalpy",
        "alternate_conceptions": [
            "Exothermic reactions are faster than endothermic reactions",
            "Endothermic reactions are faster than exothermic reactions",
            "The reactions occur at the same rate",
        ],
        "vocab_note": "The conflation of thermodynamics with kinetics is a foundational and widespread alternate conception.",
    },
    29: {
        "text": "Which of the following is directly related to the reaction rate and why? 2H₂(g) + O₂(g) ⇌ 2H₂O(l)",
        "correct_choice": "Thermodynamic quantities do not provide information about reaction times.",
        "correct_conception": "Reaction rate is independent of thermodynamic properties",
        "alternate_conceptions": [
            "Exothermic reactions proceed faster (enthalpy → rate)",
            "More spontaneous reactions proceed faster (entropy → rate)",
            "More favorable reactions proceed faster (Gibbs free energy → rate)",
        ],
        "vocab_note": "This item directly probes the thermo-kinetics conflation; all three alternate conceptions are common.",
    },
    30: {
        "text": "The reaction 2H₂(g) + O₂(g) → 2H₂O(l) is a 2nd order reaction with respect to O₂(g). What does the reaction order tell you?",
        "correct_choice": "The extent to which the concentration of O₂ affects the reaction rate.",
        "correct_conception": "Reaction order describes effects of concentration on rate",
        "alternate_conceptions": [
            "Reaction order conflated with direct change in concentration over time",
            "Reaction order describes the proportional relationship between concentration and rate",
            "Reaction order is determined by stoichiometry",
        ],
        "vocab_note": None,
    },
    31: {
        "text": "Based on the first law of thermodynamics (ΔU = q + w), what do you expect to happen when the valve between H₂(g) and O₂(g) bulbs is opened?",
        "correct_choice": "What will happen cannot be determined based on the first law of thermodynamics.",
        "correct_conception": "Understanding of when and how to use the first law of thermodynamics",
        "alternate_conceptions": [
            "Mixing of gases requires heat; misconceptions about physical vs. chemical change",
            "First law of thermodynamics is dependent on the temperature of a system (misapplication)",
            "Gases will mix and react to form water because this reaction is exothermic (misapplication)",
        ],
        "vocab_note": "Students may try to apply ΔH or ΔG reasoning rather than recognizing the limits of the first law.",
    },
    32: {
        "text": "How is the mixing of H₂(g) and O₂(g) related to the 2nd law of thermodynamics?",
        "correct_choice": "The gases will mix and increase the number of ways energy can be distributed, so entropy will increase.",
        "correct_conception": "Correct application of the second law of thermodynamics (Entropy increases when gases mix)",
        "alternate_conceptions": [
            "Increase in volume corresponds to increase in entropy (volume-entropy conflation)",
            "Gases will mix and react to form water, so entropy will increase (incorrect application)",
            "Total pressure will remain constant, so entropy will stay the same",
        ],
        "vocab_note": "Volume and entropy are often equated by students; distinguishing microstates from volume is important.",
    },
    33: {
        "text": "When the reaction quotient (Q) is equivalent to the equilibrium constant (Keq) for: 2H₂(g) + O₂(g) ⇌ 2H₂O(l), what conclusions can you draw?",
        "correct_choice": "The reaction is at equilibrium.",
        "correct_conception": "Q = Keq at equilibrium",
        "alternate_conceptions": [
            "When Q = Keq there are primarily reactants present",
            "When Q = Keq there are primarily products present",
            "When Q = Keq there are equal concentrations of all reactants and products",
        ],
        "vocab_note": None,
    },
    34: {
        "text": "Based on Kw, what must always be true about an acid-base solution in equilibrium?",
        "correct_choice": "At 25°C, [H₃O⁺] and [OH⁻] must always equal 1.0 × 10⁻¹⁴, regardless of whether an acid or base is present.",
        "correct_conception": "Kw = 1.0 × 10⁻¹⁴ at 25°C regardless of the presence of acid or base",
        "alternate_conceptions": [
            "pH of solution with strong acid must be above 1; pH of solution with strong base must be below 14",
            "The extent of auto-ionization is dependent on the presence of acid or base",
            "Kw = 1.0 × 10⁻¹⁴ only in the presence of a strong acid or base",
        ],
        "vocab_note": None,
    },
    35: {
        "text": "Which best describes the equilibrium of: H₂O(l) + HF(aq) ⇌ H₃O⁺(aq) + F⁻(aq), ΔH = 102 kJ/mol, Keq = 6.6 × 10⁻⁴?",
        "correct_choice": "There will be reactions in both directions, with mostly the reactants existing at equilibrium.",
        "correct_conception": "At equilibrium, reactions occur in both directions and the small Keq means that there will be mostly reactants at equilibrium",
        "alternate_conceptions": [
            "At equilibrium, the reaction is complete and the reverse reaction will not occur",
            "At equilibrium, equal amounts of products and reactants are present",
            "Small Keq means mostly products at equilibrium (sign confusion)",
        ],
        "vocab_note": "Students often misinterpret small Keq as meaning mostly products; the magnitude-direction relationship needs explicit attention.",
    },
    36: {
        "text": "If you were to heat the HF(aq) + H₂O reaction (ΔH = 102 kJ/mol, Keq = 6.6 × 10⁻⁴), how would you expect the system to respond?",
        "correct_choice": "The rate of the forward reaction will increase more than the rate of the reverse reaction.",
        "correct_conception": "Positive ΔH value means that the rate of the forward reaction will increase more than rate of the reverse when reaction is heated",
        "alternate_conceptions": [
            "Rate of the forward and reverse reaction will stay the same",
            "Rate of the forward and reverse reactions will both increase by the same magnitude",
            "Rate of the reverse reaction will increase more than the rate of the forward reaction",
        ],
        "vocab_note": None,
    },
    37: {
        "text": "Classify water in the following Bronsted-Lowry reaction: H₂CO₃(aq) + 2H₂O(l) ⇌ 2H₃O⁺(aq) + CO₃²⁻(aq)",
        "correct_choice": "H₂O is a weak base.",
        "correct_conception": "In the presence of H₂CO₃, water will act as a weak base",
        "alternate_conceptions": [
            "In the presence of H₂CO₃, water will act as a strong base",
            "Water does not behave as an acid or a base",
            "In the presence of H₂CO₃, water will act as either an acid or a base",
        ],
        "vocab_note": "Water's amphoteric nature is nuanced; students may default to 'water is neutral' thinking.",
    },
    38: {
        "text": "Why does HCl dissociate completely in water whereas H₂CO₃ does not?",
        "correct_choice": "HCl has larger electronegativity differences between atoms than H₂CO₃.",
        "correct_conception": "The relative electronegativity differences determine the extent of dissociation",
        "alternate_conceptions": [
            "Strong acids dissociate completely due to having weaker bonds than weak acids",
            "Monoprotic acids dissociate completely while diprotic acids do not",
            "HCl dissociates completely because it has fewer valence electrons than H₂CO₃",
        ],
        "vocab_note": "The 'weak bond = strong acid' alternate conception is pervasive; connecting bond polarity (from electronegativity) to acid strength helps.",
    },
}

# ── Tailored resources: mapped to prominent ACs ───────────────────────────────
# Format: item_id → list of {ac, title, type, url, description, asset_note}
RESOURCES = {
    1: [
        {
            "ac": "Isotopes of the same element have a different number of electrons",
            "title": "Conceptions of first-year university students of the constituents of matter and the notions of acids and bases",
            "type": "Research Article",
            "url": "https://www.tandfonline.com/doi/abs/10.1080/0140528860080307",
            "description": "Documents how students conflate atomic number, mass, and electron count when reasoning about elements and isotopes.",
            "asset_note": "Students correctly understand that isotopes are related atoms. Build on this to clarify which subatomic particle count changes and which stays the same.",
        },
        {
            "ac": "Deuterium takes up more space than hydrogen",
            "title": "Generating construct maps from a systematic review of atomic models",
            "type": "Research Article",
            "url": "https://onlinelibrary.wiley.com/doi/full/10.1002/tea.22016",
            "description": "Reviews how students develop atomic models and where spatial/size reasoning goes wrong when comparing isotopes.",
            "asset_note": "Students are drawing on a sensible intuition that more mass means more space. Redirect toward the nuclear model where atomic radius is determined by electron shells, not nuclear mass.",
        },
    ],
    2: [
        {
            "ac": "Core and valence electrons are shared in a covalent bond",
            "title": "Development of the Bonding Representations Inventory to Identify Student Misconceptions about Covalent and Ionic Bonding Representations",
            "type": "Research Article",
            "url": "https://pubs.acs.org/doi/full/10.1021/ed400700q",
            "description": "Identifies and categorizes student misconceptions about which electrons participate in bonding, including the core/valence confusion.",
            "asset_note": "Build on students' understanding that electrons do interact in bonding. Redirect to which electrons participate and why core electrons are shielded.",
        },
        {
            "ac": "Core electrons do not participate, and valence electrons are shared in a nonpolar covalent bond",
            "title": "The Trouble with Chemical Energy: Why Understanding Bond Energies Requires an Interdisciplinary Systems Approach",
            "type": "Research Article",
            "url": "https://www.lifescied.org/doi/10.1187/cbe.12-10-0170",
            "description": "Explores how students reason about bond polarity and energy, including why electronegativity framing matters for identifying bond type.",
            "asset_note": "Students who identify the correct electron participation but miss polarity are close. Scaffold toward electronegativity difference as the key for determining polarity.",
        },
    ],
    3: [
        {
            "ac": "Ionic bonding involves the uneven sharing of electrons",
            "title": "Development of the Bonding Representations Inventory to Identify Student Misconceptions about Covalent and Ionic Bonding Representations",
            "type": "Research Article",
            "url": "https://pubs.acs.org/doi/full/10.1021/ed400700q",
            "description": "Systematically documents the transfer vs. sharing confusion in ionic bonding, with instructional implications.",
            "asset_note": "Students recognize that electrons behave differently in ionic vs. covalent bonds. Build on this by distinguishing the degree of electron movement: sharing vs. complete transfer.",
        },
    ],
    4: [
        {
            "ac": "O is more electronegative and attracts the H electron to itself",
            "title": "A Common Core to Chemical Conceptions: Learners' Conceptions of Chemical Stability, Change and Bonding",
            "type": "Research Chapter",
            "url": "https://link.springer.com/chapter/10.1007/978-94-007-5914-5_19",
            "description": "Reviews learner conceptions of bonding attractions, including the conflation of electronegativity with full electron transfer.",
            "asset_note": "Students correctly identify oxygen as the more electronegative atom. Build on this to clarify that electronegativity creates a partial pull, not a complete transfer of the electron.",
        },
    ],
    5: [
        {
            "ac": "A bond is associated with the highest potential energy",
            "title": "Developing a new teaching approach for the chemical bonding concept aligned with current scientific and pedagogical knowledge",
            "type": "Research Article",
            "url": "https://onlinelibrary.wiley.com/doi/epdf/10.1002/sce.20201",
            "description": "Proposes evidence-based instructional approaches for bonding including potential energy diagrams, addressing where students misread stability.",
            "asset_note": "Students understand that energy and bonding are connected. Scaffold toward the specific relationship: bond formation releases energy, and the energy minimum corresponds to the stable bond.",
        },
    ],
    6: [
        {
            "ac": "Net attractive forces at A, zero net forces at B, net repulsive forces at C",
            "title": "Developing a new teaching approach for the chemical bonding concept aligned with current scientific and pedagogical knowledge",
            "type": "Research Article",
            "url": "https://onlinelibrary.wiley.com/doi/epdf/10.1002/sce.20201",
            "description": "Addresses force reasoning on potential energy diagrams, including where students misassign attractive and repulsive regions.",
            "asset_note": "Students correctly identify that forces change across the diagram. Build on their spatial reasoning by anchoring each region to what is physically happening between the atoms at that distance.",
        },
    ],
    7: [
        {
            "ac": "Molecular shape of H2O is primarily determined by the lone pairs",
            "title": "Development and Application of a Diagnostic Instrument to Evaluate Grade-11 and -12 Students' Concepts of Covalent Bonding and Structure Following a Course of Instruction",
            "type": "Research Article",
            "url": "https://onlinelibrary.wiley.com/doi/pdf/10.1002/tea.3660260404",
            "description": "Documents student reasoning about molecular geometry, including overemphasis on lone pairs relative to bonding pairs.",
            "asset_note": "Students who focus on lone pairs are applying VSEPR reasoning. Redirect toward the full picture: both bonding and lone pairs exert repulsive forces that together determine shape.",
        },
    ],
    8: [
        {
            "ac": "Simplistic unhybridized structure (molecular geometry model only)",
            "title": "From Abstract to Manipulatable: The Hybridization Explorer, A Digital Interactive for Studying Orbitals",
            "type": "Simulation",
            "url": "https://pubs.acs.org/doi/full/10.1021/acs.jchemed.0c00847",
            "description": "Interactive digital tool for visualizing orbital hybridization, designed to bridge between abstract orbital theory and molecular geometry.",
            "asset_note": "Students who select the molecular geometry model have the shape correct. Build on this foundation to introduce why hybridization is the more complete explanation for that geometry.",
        },
    ],
    9: [
        {
            "ac": "Understanding of polarization but incorrect direction",
            "title": "Teaching Chemistry with Electron Density Models. 2. Can Atomic Charges Adequately Explain Electrostatic Potential Maps?",
            "type": "Research Article",
            "url": "https://online.ucpress.edu/tce/article-abstract/6/1/36/216061/Teaching-Chemistry-with-Electron-Density-Models-2?redirectedFrom=fulltext",
            "description": "Examines how electrostatic potential maps can be used instructionally to help students reason about electron density distribution and directionality.",
            "asset_note": "Students who recognize polarization but reverse the direction have the core idea right. Use EPM visualizations to anchor the direction of electron density toward the more electronegative atom.",
        },
    ],
    10: [
        {
            "ac": "Electron density of H2O is determined by charges on O and H",
            "title": "Development and Application of a Diagnostic Instrument to Evaluate Grade-11 and -12 Students' Concepts of Covalent Bonding and Structure Following a Course of Instruction",
            "type": "Research Article",
            "url": "https://onlinelibrary.wiley.com/doi/pdf/10.1002/tea.3660260404",
            "description": "Identifies the common conflation of formal charge with electronegativity when students explain electron density distribution.",
            "asset_note": "Students who invoke charge are reasoning about something real. Scaffold toward the distinction between formal charge and electronegativity as the driver of electron density distribution.",
        },
    ],
    11: [
        {
            "ac": "Polarity is determined only by partial charges; shape has no role",
            "title": "Development and Application of a Diagnostic Instrument to Evaluate Grade-11 and -12 Students' Concepts of Covalent Bonding and Structure Following a Course of Instruction",
            "type": "Research Article",
            "url": "https://onlinelibrary.wiley.com/doi/pdf/10.1002/tea.3660260404",
            "description": "Documents how students reason about molecular polarity and the underweighting of molecular geometry in their explanations.",
            "asset_note": "Students who focus on partial charges are identifying a real contributor to polarity. Build toward the vector addition logic that shows why geometry is also required.",
        },
    ],
    12: [
        {
            "ac": "IMFs are only present between polar molecules",
            "title": "Student Understanding of Intermolecular Forces: A Multimodal Study",
            "type": "Research Article",
            "url": "https://pubs.acs.org/doi/full/10.1021/acs.jchemed.5b00169",
            "description": "Examines how students represent and reason about intermolecular forces across multiple modes, including misconceptions about which molecules can experience IMFs.",
            "asset_note": "Students who limit IMFs to polar molecules understand that polarity matters. Extend this to show that all molecules have electrons that can fluctuate, making LDFs universal.",
        },
    ],
    13: [
        {
            "ac": "Hydrogen bonding occurs between two intermolecular electrophilic heteroatoms without hydrogen present",
            "title": "Intermolecular Forces Dominoes! A Game for Aiding Students in Their Review of Intermolecular Forces",
            "type": "Classroom Activity",
            "url": "https://pubs.acs.org/doi/full/10.1021/acs.jchemed.3c00024",
            "description": "Game-based activity for reviewing IMF types including hydrogen bonding, requiring students to identify correct donor-acceptor pairs.",
            "asset_note": "Students who identify two heteroatoms understand that electronegative atoms are involved. Build toward the specific requirement that hydrogen must be the bridge between donor and acceptor.",
        },
        {
            "ac": "Hydrogen bonding occurs within a single H2O molecule",
            "title": "Analysis of students' diagrams of water molecules in snowflakes to reveal their conceptual understanding of hydrogen bonds",
            "type": "Research Article",
            "url": "https://pubs.rsc.org/en/content/articlelanding/2023/rp/d2rp00175f",
            "description": "Uses student-drawn diagrams to reveal how students locate hydrogen bonds, including within-molecule errors.",
            "asset_note": "Students who place hydrogen bonds within a molecule understand that O and H interact strongly. Redirect toward the intermolecular nature of hydrogen bonding using diagrams of multiple water molecules.",
        },
    ],
    17: [
        {
            "ac": "At boiling point, temperature continues to increase prior to phase change",
            "title": "Roles of Terminology, Experience, and Energy Concepts in Student Conceptions of Freezing and Boiling",
            "type": "Research Article",
            "url": "https://pubs.acs.org/doi/10.1021/ed2007668",
            "description": "Investigates how students reason about the temperature-energy relationship during phase changes, including the plateau misconception.",
            "asset_note": "Students understand that heating a substance changes something. Scaffold toward distinguishing temperature (average kinetic energy) from energy input, which goes into breaking IMFs during a phase change.",
        },
    ],
    20: [
        {
            "ac": "The number of molecules decreases as they move at higher speeds",
            "title": "Investigating first-year undergraduate chemistry students' reasoning with reaction coordinate diagrams when choosing among particulate-level reaction mechanisms",
            "type": "Research Article",
            "url": "https://pubs.rsc.org/en/content/articlehtml/2021/rp/d0rp00193g",
            "description": "Examines how students read and interpret distribution curves in chemistry, including misreadings of axes and curve shape changes.",
            "asset_note": "Students reading the y-axis as a count that decreases are reasoning about the graph. Redirect toward what the curve shape change means: the same molecules are redistributed across a broader speed range.",
        },
        {
            "ac": "At higher temperatures there is no change in variance, only an increase in average kinetic energy",
            "title": "PhET: Gas Properties Simulation",
            "type": "Simulation",
            "url": "https://phet.colorado.edu/sims/html/gas-properties/latest/gas-properties_all.html",
            "description": "Interactive simulation allowing students to observe how temperature changes affect the speed distribution of gas molecules in real time.",
            "asset_note": "Students who recognize the rightward shift are partially correct. Use the simulation to show the widening of the distribution alongside the shift.",
        },
    ],
    21: [
        {
            "ac": "Phase change requires energy input to break bonds within molecules",
            "title": "Student Understanding of a Simple Heating Curve: Scientific Interpretations and Consistency of Responses",
            "type": "Research Article",
            "url": "https://dergipark.org.tr/en/download/article-file/486976",
            "description": "Documents the persistent confusion between breaking intermolecular forces and breaking intramolecular bonds during phase changes.",
            "asset_note": "Students correctly understand that energy is required and that something breaks. Redirect toward what breaks: intermolecular forces between molecules, not the covalent bonds within them.",
        },
    ],
    22: [
        {
            "ac": "Oxygen and hydrogen exist naturally as monatomic elements",
            "title": "What you see is what you learn? The role of visual model comprehension for academic success in chemistry",
            "type": "Research Article",
            "url": "https://pubs.rsc.org/en/content/articlehtml/2019/rp/c9rp00016j",
            "description": "Examines how students interpret particulate diagrams, including where monatomic vs. diatomic representations cause confusion.",
            "asset_note": "Students reading H2O as H + H + O are interpreting a real representation. Build toward the distinction between elemental symbols in a formula vs. the natural diatomic form of H and O.",
        },
    ],
    23: [
        {
            "ac": "Energy is released by breaking bonds in reactants",
            "title": "The Trouble with Chemical Energy: Why Understanding Bond Energies Requires an Interdisciplinary Systems Approach",
            "type": "Research Article",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3671656/",
            "description": "Addresses the deeply rooted misconception that breaking bonds releases energy, with discussion of instructional strategies.",
            "asset_note": "Students understand that energy and bonds are connected. Redirect the directionality: breaking requires energy input, while forming releases it. The net sign depends on which is larger.",
        },
    ],
    24: [
        {
            "ac": "Entropy is determined by randomness versus microstates; positive sign",
            "title": "Exploiting language in the teaching of entropy",
            "type": "Research Article",
            "url": "https://www.scientiasocialis.lt/jbse/files/pdf/vol10/27-35.Jeppsson_Vol.10_No.1.pdf",
            "description": "Analyzes how entropy language and metaphors shape student reasoning, and how to leverage everyday language productively.",
            "asset_note": "Students using 'randomness' are drawing on a real metaphor. Redirect toward microstates as a more precise framing that supports correct sign determination.",
        },
        {
            "ac": "Entropy is determined by randomness versus microstates; negative sign",
            "title": "Language aspects of engineering students' view of entropy",
            "type": "Research Article",
            "url": "https://pubs.rsc.org/en/content/pdf/article/2016/rp/c5rp00227c",
            "description": "Explores how different framings of entropy affect students' ability to reason about sign and direction of entropy change.",
            "asset_note": "Students who get the sign right but use randomness framing have arrived at the correct answer through an imprecise route. Build toward the microstate explanation for why fewer ways to distribute energy means negative delta S.",
        },
    ],
    25: [
        {
            "ac": "It will be spontaneous at all temperatures",
            "title": "Creating and testing an activity with interdisciplinary connections: entropy to osmosis",
            "type": "Research Article",
            "url": "https://pubs.rsc.org/en/content/pdf/article/2021/rp/d0rp00353k",
            "description": "Uses osmosis as an accessible context for reasoning about spontaneity and entropy, supporting temperature-dependent Gibbs analysis.",
            "asset_note": "Students who predict spontaneous at all temperatures are correctly reading the exothermic sign. Build toward why the negative entropy term eventually dominates at high temperatures.",
        },
        {
            "ac": "It will be spontaneous at high temperatures",
            "title": "Capturing student conceptions of thermodynamics and kinetics using writing",
            "type": "Research Article",
            "url": "https://pubs.rsc.org/en/content/pdf/article/2020/rp/c9rp00292h",
            "description": "Uses student writing to reveal reasoning about spontaneity, including temperature-dependent errors in Gibbs free energy application.",
            "asset_note": "Students who predict high temperature spontaneity may be overgeneralizing from entropy-driven reactions. Use sign analysis tables to help students work through each case systematically.",
        },
    ],
    26: [
        {
            "ac": "The net change in Gibbs free energy for the formation of water is zero",
            "title": "Determining Students' Conceptual Understanding Level of Thermodynamics",
            "type": "Research Article",
            "url": "https://files.eric.ed.gov/fulltext/EJ1094600.pdf",
            "description": "Assesses conceptual understanding of thermodynamic constructs including free energy curves and spontaneity.",
            "asset_note": "Students who choose delta G = 0 may be thinking of equilibrium. Build on this by distinguishing the equilibrium state from the reaction pathway: the large Keq tells us the curve is strongly downhill.",
        },
        {
            "ac": "Formation of water is non-spontaneous; incorrect application of free energy curve",
            "title": "An extension of the Thermodynamics Conceptual Reasoning Inventory (TCRI): measuring undergraduate students' understanding of introductory thermodynamics concepts",
            "type": "Research Article",
            "url": "https://www.tandfonline.com/doi/full/10.1080/09500693.2021.1975847",
            "description": "Documents patterns in student reasoning about free energy diagrams and spontaneity, including reversal errors.",
            "asset_note": "Students who select the non-spontaneous curve are applying the logic of free energy correctly. Redirect toward the connection between a very large Keq and a strongly negative delta G.",
        },
    ],
    27: [
        {
            "ac": "Large Keq values mean reaction will reach equilibrium quickly",
            "title": "Understanding Chemical Reaction Kinetics and Equilibrium with Interlocking Building Blocks",
            "type": "Classroom Activity",
            "url": "https://pubs.acs.org/doi/full/10.1021/ed1010773",
            "description": "Hands-on activity using building blocks to represent equilibrium position and kinetics separately, addressing the conflation of Keq magnitude with rate.",
            "asset_note": "Students who connect large Keq to fast equilibration are conflating thermodynamics with kinetics. Build on their understanding that large Keq means product-favored, then establish that rate is a separate question.",
        },
    ],
    28: [
        {
            "ac": "Exothermic reactions are faster than endothermic reactions",
            "title": "Capturing student conceptions of thermodynamics and kinetics using writing",
            "type": "Research Article",
            "url": "https://pubs.rsc.org/en/content/articlehtml/2020/rp/c9rp00292h",
            "description": "Uses student writing to surface the thermodynamics-kinetics conflation, providing a window into how students reason about rate and energy.",
            "asset_note": "Students who link exothermicity to rate are reasoning that energy release should speed things up. Help them map enthalpy to thermodynamic domain and activation energy to kinetic domain as separate concepts.",
        },
    ],
    29: [
        {
            "ac": "Exothermic reactions proceed faster (enthalpy to rate)",
            "title": "Prospective Chemistry Teachers' Conceptions of Chemical Thermodynamics and Kinetics",
            "type": "Research Article",
            "url": "https://www.ejmste.com/article/prospective-chemistry-teachersconceptions-of-chemicalthermodynamics-and-kinetics-4181",
            "description": "Documents how learners and even teachers conflate thermodynamic and kinetic reasoning, with implications for instruction.",
            "asset_note": "Students invoking enthalpy to explain rate are applying a real property of reactions to the wrong domain. Scaffold toward the distinction between whether a reaction is favorable and how fast it proceeds.",
        },
    ],
    30: [
        {
            "ac": "Reaction order is determined by stoichiometry",
            "title": "Charting an Alternate Pathway to Reaction Orders and Rate Laws in Introductory Chemistry Courses",
            "type": "Research Article",
            "url": "https://pubs.acs.org/doi/full/10.1021/ed3006743",
            "description": "Proposes an instructional sequence that explicitly separates stoichiometric coefficients from experimentally determined reaction orders.",
            "asset_note": "Students who derive order from stoichiometry are applying a logical but incorrect shortcut. Build toward the idea that reaction order must be determined experimentally and reflects mechanism, not balanced equation coefficients.",
        },
    ],
    31: [
        {
            "ac": "Mixing of gases requires heat; misconceptions about physical vs. chemical change",
            "title": "Student Interpretations of Equations Related to the First Law of Thermodynamics",
            "type": "Research Article",
            "url": "https://pubs.acs.org/doi/full/10.1021/ed1001625",
            "description": "Documents how students misapply the first law equation to physical and chemical processes, including gas mixing scenarios.",
            "asset_note": "Students who invoke heat requirements are applying thermodynamic reasoning. Redirect toward what the first law actually constrains and what it cannot tell us about this process.",
        },
    ],
    32: [
        {
            "ac": "Increase in volume corresponds to increase in entropy",
            "title": "The Second Law and Entropy Misconceptions Demystified",
            "type": "Research Article",
            "url": "https://doi.org/10.3390/e22060648",
            "description": "Directly addresses common entropy misconceptions including the volume-entropy conflation, with accessible explanations.",
            "asset_note": "Students who connect volume to entropy are drawing on a real relationship that holds in some contexts. Redirect toward the microstate definition to explain why mixing increases entropy even when volume changes are minimal.",
        },
        {
            "ac": "Gases will mix and react to form water, so entropy will increase",
            "title": "Entropy, Microstates, and Probability: Interactive Lecture Demonstration Guide",
            "type": "Simulation",
            "url": "https://phet.colorado.edu/en/activities/3948",
            "description": "PhET-based lecture demonstration connecting microstates to probability and entropy change, applicable to gas mixing.",
            "asset_note": "Students who predict reaction are reasoning about the well-known reactivity of H2 and O2. Scaffold toward distinguishing the physical process of mixing from the chemical process of reacting, and what the second law addresses.",
        },
    ],
    33: [
        {
            "ac": "When Q = Keq there are primarily reactants present",
            "title": "The Reaction Quotient Is Unnecessary To Solve Equilibrium Problems / The Reaction Quotient (Q) IS Useful After All",
            "type": "Research Article",
            "url": "https://pubs.acs.org/doi/pdf/10.1021/ed082p1149.1",
            "description": "Debates the pedagogical role of Q and clarifies what Q = Keq actually tells us about the state of the system.",
            "asset_note": "Students who predict primarily reactants when Q = Keq may be confusing direction of shift with position. Build toward the definition: Q = Keq means the system is at equilibrium, not shifted in either direction.",
        },
    ],
    34: [
        {
            "ac": "The extent of auto-ionization is dependent on the presence of acid or base",
            "title": "Student Conceptions of pH Buffers Using a Resource Framework: Layered Resource Graphs and Levels of Resource Activation",
            "type": "Research Article",
            "url": "https://pubs-acs-org.echo.louisville.edu/doi/full/10.1021/acs.jchemed.1c01078",
            "description": "Examines student reasoning about acid-base equilibria including Kw, auto-ionization, and the constancy of the ion product.",
            "asset_note": "Students who think auto-ionization depends on added acid or base are reasoning about Le Chatelier's principle. Build toward Kw as a temperature-dependent constant that holds regardless of what else is in solution at 25C.",
        },
    ],
    35: [
        {
            "ac": "Small Keq means mostly products at equilibrium",
            "title": "A Simple System for Observing Dynamic Phase Equilibrium via an Inquiry-Based Laboratory or Demonstration",
            "type": "Classroom Activity",
            "url": "https://pubs.acs.org/doi/full/10.1021/ed100846k",
            "description": "Inquiry-based lab that builds intuition for equilibrium position through observable phase equilibrium, supporting Keq interpretation.",
            "asset_note": "Students who reverse the Keq interpretation are applying magnitude reasoning but in the wrong direction. Use a number line or ratio framing to build the connection between small Keq and reactant-favored equilibrium.",
        },
    ],
    36: [
        {
            "ac": "Rate of the forward and reverse reactions will both increase by the same magnitude",
            "title": "A Simple System for Observing Dynamic Phase Equilibrium via an Inquiry-Based Laboratory or Demonstration",
            "type": "Classroom Activity",
            "url": "https://pubs.acs.org/doi/full/10.1021/ed100846k",
            "description": "Supports reasoning about how temperature perturbations affect equilibrium systems, building toward Le Chatelier reasoning.",
            "asset_note": "Students who predict equal increases are applying a symmetric logic. Build toward why an endothermic forward reaction is preferentially accelerated by heat, using the connection between temperature and activation energy.",
        },
    ],
    37: [
        {
            "ac": "Water does not behave as an acid or a base",
            "title": "The impact of coupling assessments on conceptual understanding and connection-making in chemical equilibrium and acid-base chemistry",
            "type": "Research Article",
            "url": "https://pubs-rsc-org.echo.louisville.edu/en/content/articlehtml/2020/rp/d0rp00038h",
            "description": "Examines how students develop understanding of amphoteric behavior and acid-base roles in equilibrium contexts.",
            "asset_note": "Students who say water is neutral are drawing on a real everyday observation. Scaffold toward the Bronsted-Lowry framework where acid-base identity is context-dependent, not fixed.",
        },
    ],
    38: [
        {
            "ac": "Strong acids dissociate completely due to having weaker bonds than weak acids",
            "title": "Development and Assessment of a Diagnostic Tool to Identify Organic Chemistry Students' Alternative Conceptions Related to Acid Strength",
            "type": "Research Article",
            "url": "https://www.tandfonline.com/doi/epdf/10.1080/09500693.2012.684433",
            "description": "Documents the weak bond misconception and relates it to instructional language around acid strength and dissociation.",
            "asset_note": "Students recognize that something about the bond determines acid strength. Redirect from bond strength to bond polarity: the electronegativity difference drives dissociation, not whether the bond is weak or strong in absolute terms.",
        },
    ],
}


# ── Correct answer key ────────────────────────────────────────────────────────
CORRECT_ANSWERS = {
    1: 3, 2: 2, 3: 3, 4: 3, 5: 2, 6: 2, 7: 3, 8: 2, 9: 1, 10: 2,
    11: 3, 12: 2, 13: 1, 14: 3, 15: 3, 16: 4, 17: 3, 18: 2, 19: 4, 20: 1,
    21: 1, 22: 1, 23: 4, 24: 4, 25: 2, 26: 2, 27: 2, 28: 4, 29: 4, 30: 3,
    31: 4, 32: 2, 33: 3, 34: 3, 35: 4, 36: 3, 37: 1, 38: 1,
}


# ── Real data loader ──────────────────────────────────────────────────────────
def load_real_data(filepath):
    """
    Load student response data from the Water Instrument Excel file.
    Columns: Q1-Q38 (answer choice, 1-indexed), QA1-QA38 (confidence, 1-5).

    Each row in the returned DataFrame has, in addition to the legacy fields:
        choice_counts: dict like {1: 11, 2: 7, 3: 28, 4: 0}  raw count per choice A..D
        prominent_choice: int (1..4) or None  the choice number of the prominent AC
    """
    raw = pd.read_excel(filepath)
    rows = []
    for item_id, item in ITEMS.items():
        col = f"Q{item_id}"
        conf_col = f"QA{item_id}"
        if col not in raw.columns:
            continue
        responses = raw[col].dropna()
        n = len(responses)
        if n == 0:
            continue
        correct_choice = CORRECT_ANSWERS[item_id]
        cc_pct = round((responses == correct_choice).mean() * 100)

        # NEW: per-choice raw counts (always slots for A..D, missing → 0)
        choice_counts = {c: int((responses == c).sum()) for c in range(1, 5)}

        all_choices = sorted(responses.unique())
        wrong_choices = [c for c in all_choices if c != correct_choice]
        ac_pcts = []
        for choice in wrong_choices:
            pct = round((responses == choice).mean() * 100)
            ac_pcts.append(pct)

        n_acs = len(item["alternate_conceptions"])
        while len(ac_pcts) < n_acs:
            ac_pcts.append(0)
        ac_pcts = ac_pcts[:n_acs]

        ac_pcts_sorted = sorted(ac_pcts, reverse=True)

        # Per-choice prominence: any wrong choice within 15 points of the
        # correct choice's percentage is flagged as prominent. An item can
        # have zero, one, or several prominent ACs.
        prominent_choices = []
        if cc_pct < 85 and n > 0:
            for c in range(1, 5):
                if c == correct_choice:
                    continue
                c_pct = round(choice_counts.get(c, 0) / n * 100)
                if c_pct >= cc_pct - 15:
                    prominent_choices.append(c)

        prominent = len(prominent_choices) > 0

        # Backwards-compatible single field: the most-chosen prominent choice.
        wrong_counts = {c: choice_counts.get(c, 0) for c in prominent_choices}
        prominent_choice = (
            max(wrong_counts, key=wrong_counts.get) if wrong_counts else None
        )

        conf_mean = None
        if conf_col in raw.columns:
            conf_vals = raw[conf_col].dropna()
            if len(conf_vals) > 0:
                conf_mean = round(conf_vals.mean(), 2)

        row = {
            "item_id": item_id,
            "cc_pct": cc_pct,
            "n_students": n,
            "prominent_ac": prominent,
            "prominent_ac_label": item["alternate_conceptions"][0] if prominent else None,
            "conf_mean": conf_mean,
            "choice_counts": choice_counts,
            "prominent_choice": prominent_choice,
            "prominent_choices": prominent_choices,
        }
        for i, p in enumerate(ac_pcts_sorted):
            row[f"ac{i+1}_pct"] = p
        rows.append(row)

    return pd.DataFrame(rows)


# ── Demo dataset generator (fallback if no data file found) ──────────────────
def generate_demo_data(seed=42, n_students=46):
    rng = np.random.default_rng(seed)
    rows = []
    for item_id, item in ITEMS.items():
        n_acs = len(item["alternate_conceptions"])
        prominent = rng.random() > 0.45
        if prominent:
            cc_pct = rng.integers(20, 50)
            remaining = 100 - cc_pct
            ac_pcts = sorted(rng.dirichlet(np.ones(n_acs)) * remaining, reverse=True)
        else:
            cc_pct = rng.integers(55, 90)
            remaining = 100 - cc_pct
            ac_pcts = sorted(rng.dirichlet(np.ones(n_acs)) * remaining, reverse=True)
        ac_pcts = [round(p) for p in ac_pcts]
        total = cc_pct + sum(ac_pcts)
        ac_pcts[0] += 100 - total

        # Build per-choice raw counts. Items with fewer ACs leave later slots at 0.
        correct_choice = CORRECT_ANSWERS[item_id]
        choice_counts = {c: 0 for c in range(1, 5)}
        choice_counts[correct_choice] = int(round(cc_pct * n_students / 100))

        # Wrong choices come from {1,2,3,4} minus the correct one. We only fill
        # n_acs of them so items with 2 ACs leave one slot at 0 (matches reality).
        wrong_choices = [c for c in range(1, 5) if c != correct_choice]
        # Shuffle so the prominent AC isn't always assigned to the same letter.
        shuffled = list(ac_pcts)
        rng.shuffle(shuffled)
        for choice, pct in zip(wrong_choices, shuffled):
            choice_counts[choice] = int(round(pct * n_students / 100))

        # Per-choice prominence (same threshold as load_real_data so demo and
        # real data behave identically). Multiple wrong choices can be flagged.
        prominent_choices = []
        if cc_pct < 85 and n_students > 0:
            for c in range(1, 5):
                if c == correct_choice:
                    continue
                c_pct = round(choice_counts.get(c, 0) / n_students * 100)
                if c_pct >= cc_pct - 15:
                    prominent_choices.append(c)

        prominent = len(prominent_choices) > 0
        wrong_counts = {c: choice_counts.get(c, 0) for c in prominent_choices}
        prominent_choice = (
            max(wrong_counts, key=wrong_counts.get) if wrong_counts else None
        )

        rows.append({
            "item_id": item_id,
            "cc_pct": cc_pct,
            "n_students": n_students,
            "conf_mean": None,
            **{f"ac{i+1}_pct": p for i, p in enumerate(ac_pcts)},
            "prominent_ac": prominent,
            "prominent_ac_label": item["alternate_conceptions"][0] if prominent else None,
            "choice_counts": choice_counts,
            "prominent_choice": prominent_choice,
            "prominent_choices": prominent_choices,
        })
    return pd.DataFrame(rows)


# ── Primary data loader ───────────────────────────────────────────────────────
# Resolution order for "what file should I read?":
#   1. st.session_state["data_path"]  (set by auth.require_login per logged-in user)
#   2. APP_ROOT/Formatted_IF_Data_for_App.xlsx   (legacy single-file install)
#   3. Demo data (generated)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
LEGACY_DATA_FILE = os.path.join(APP_ROOT, "Formatted_IF_Data_for_App.xlsx")


def _resolve_data_path():
    """Return the path the current session should load, or None for demo."""
    try:
        import streamlit as st  # local import keeps data.py importable outside Streamlit
        path = st.session_state.get("data_path")
        if path and os.path.exists(path):
            return path
    except Exception:
        pass
    if os.path.exists(LEGACY_DATA_FILE):
        return LEGACY_DATA_FILE
    return None


def get_data():
    """Returns (df, is_real). is_real is True when a real data file was loaded."""
    path = _resolve_data_path()
    if path:
        return load_real_data(path), True
    return generate_demo_data(), False


def get_ac_color(is_prominent):
    """Backwards-compatible helper. Prefer importing AC_COLOR / AC_FADED_COLOR directly."""
    return AC_COLOR if is_prominent else AC_FADED_COLOR
